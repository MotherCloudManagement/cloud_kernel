from sqlalchemy import Table, MetaData, join
from sqlalchemy import schema, sql, util
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, mapper, \
                            class_mapper, relationship, session,\
                            object_session, attributes, Session
from sqlalchemy.orm.interfaces import MapperExtension, EXT_CONTINUE
from sqlalchemy.sql import expression
from sqlalchemy.exc import NoForeignKeysError, ArgumentError

MAX_SQL_VARIABLES = 900
INTERNAL_SESSION_ATTR = '_cloudkernel_sync'
CLOUD_KERNEL_ENGINE_STRING = 'postgresql://localhost:5432'


class AutoAdd(MapperExtension):
    def __init__(self, scoped_session):
        self.scoped_session = scoped_session

    def instrument_class(self, mapper, class_):
        class_.__init__ = self._default__init__(mapper)

    def _default__init__(ext, mapper):
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
        return __init__

    def init_instance(self, mapper, class_, oldinit, instance, args, kwargs):
        session = self.scoped_session()
        state = attributes.instance_state(instance)
        session._save_impl(state)
        return EXT_CONTINUE

    def init_failed(self, mapper, class_, oldinit, instance, args, kwargs):
        sess = object_session(instance)
        if sess:
            sess.expunge(instance)
        return EXT_CONTINUE


class SelectableClassType(type):

    def insert(cls, **kwargs):
        raise TypeError(
            'SQL can only modify mapped Tables (found: %s)' \
            % cls._table.__class__.__name__
        )

    def __clause_element__(cls):
        return cls._table

    def __getattr__(cls, attr):
        if attr == '_query':
            # called during mapper init
            raise AttributeError()
        return getattr(cls._query, attr)


def _selectable_name(selectable):
    if isinstance(selectable, sql.Alias):
        return _selectable_name(selectable.element)
    elif isinstance(selectable, sql.Select):
        return ''.join(_selectable_name(s) for s in selectable.froms)
    elif isinstance(selectable, schema.Table):
        return selectable.name
    else:
        x = selectable.__class__.__name__
        if x[0] == '_':
            x = x[1:]
        return x


class TableClassType(SelectableClassType):

    def insert(cls, **kwargs):
        o = cls()
        o.__dict__.update(kwargs)
        return o

    def relate(cls, propname, *args, **kwargs):

        class_mapper(cls)._configure_property(propname, relationship(*args, **kwargs))

    def __getitem__(cls, key):
        return cls._query[key]


class SelectableClassType(type):

    def insert(cls, **kwargs):
        raise TypeError(
            'SQL can only modify mapped Tables (found: %s)' \
            % cls._table.__class__.__name__
        )

    def __clause_element__(cls):
        return cls._table

    def __getattr__(cls, attr):
        if attr == '_query':
            # called during mapper init
            raise AttributeError()
        return getattr(cls._query, attr)


def class_for_table(session, engine, selectable, base_cls, mapper_kwargs):
    selectable = expression._clause_element_as_expr(selectable)
    mapname = _selectable_name(selectable)
    # Py2K
    if isinstance(mapname, str):
        engine_encoding = engine.dialect.encoding
        mapname = mapname.encode(engine_encoding)

    if isinstance(selectable, Table):
        klass = TableClassType(mapname, (base_cls,), {})
    else:
        klass = SelectableClassType(mapname, (base_cls,), {})

    def _compare(self, o):
        L = list(self.__class__.c.keys())
        L.sort()
        t1 = [getattr(self, k) for k in L]
        try:
            t2 = [getattr(o, k) for k in L]
        except AttributeError:
            raise TypeError('unable to compare with %s' % o.__class__)
        return t1, t2

    def __lt__(self, o):
        t1, t2 = _compare(self, o)
        return t1 < t2

    def __eq__(self, o):
        t1, t2 = _compare(self, o)
        return t1 == t2

    def __repr__(self):
        L = ["%s=%r" % (key, getattr(self, key, ''))
             for key in self.__class__.c.keys()]
        return '%s(%s)' % (self.__class__.__name__, ','.join(L))

    def __getitem__(self, key):
        return self._query[key]

    for m in ['__eq__', '__repr__', '__lt__', '__getitem__']:
        setattr(klass, m, eval(m))
    klass._table = selectable
    klass.c = expression.ColumnCollection()
    mappr = mapper(klass,
                   selectable,
                   extension=AutoAdd(session),
                   **mapper_kwargs)

    for k in mappr.iterate_properties:
        klass.c[k.key] = k.columns[0]

    klass._query = session.query_property()
    return klass


class DatabaseSession(object):

    """
    This is the Base Database session class that will be inherited by all
    other database classes for operation.  The other Database classes such
    as the classes for synchronization and keeping the most up to date data
    will inherited this class giving access to the session and all other attributes
    necessary for basic Database management.

    TODO: I haven't decided if I will use a singleton to register sessions and limit
    the number of new ones created.  This could be useful because SQLAlchemy sessions
    provide access to all associated objects known to that session.  This data could
    allow for efficient synchronization; checking to make sure data is updated.

    """

    def __init__(self, engine=CLOUD_KERNEL_ENGINE_STRING, base=object, session=None):

        if isinstance(engine, MetaData):
            self.metadata = engine
        elif isinstance(engine, (str, Engine)):
            self.metadata = MetaData(engine)
        else:
            raise ValueError('Invalid Argument Type for engine: {}'.format(
                engine
            ))

        self.engine = create_engine(engine)
        self.globalsession = sessionmaker(
            autoflush=False, expire_on_commit=False, bind=self.engine
        )
        self.sess = self.globalsession()

        self._cache = {}
        self.schema = None

    @property
    def bind(self):
        ''' The :class:`sqlalchemy.engine.base.Engine` associated with this :class: `DatabaseSession` '''

        return self.metadata.bind

    def session_delete(self, session_instance):
        ''' Mark a session instance as deleted '''

        self.sess.delete(session_instance)

    def session_execute(self, stmt, **params):
        '''
        Execute an SQL Statement as part of the session

        '''

        return self.sess.execute(sql.text(stmt, bind=self.bind), **params)

    def flush(self):
        ''' Flush Pending changes to the Database '''

        self.sess.flush()

    def rollback(self):
        ''' Rollback the current transaction '''
        self.sess.rollback()

    def commit(self):
        ''' Commit the current transaction '''
        self.sess.commit()

    def expunge(self, instance):
        ''' Clear a specific object from the session '''

        self.sess.expunge(instance)

    def expunge_all(self):
        ''' Clear all object from the session '''

        self.sess.expunge_all()

    def map_to(self, attrname, tablename=None, selectable=None,
               schema=None, base=None, mapper_args=util.immutabledict()):

        if attrname in self._cache:
            raise AttributeError('Attibute {} is already mapped to {}'.format(
                attrname, class_mapper(self._cache[attrname]).mapped_table
            ))

        if tablename is not None:
            if not isinstance(tablename, str):
                raise ArgumentError('Tablename must be a string, type found: {}'.format(
                    type(tablename)
                ))

            if selectable is not None:
                raise ArgumentError('`tablename` and `selectable` are mutually exclusive')

            selectable = Table(tablename,
                               self.metadata,
                               autoload=True,
                               autoload_with=self.bind,
                               schema=schema or self.schema)
        elif schema:
            raise ArgumentError('`tablename` argument is required when using schema.')

        elif selectable is not None:
            if not isinstance(selectable, expression.FromClause):
                raise ArgumentError('`selectable` argument must be a table,'
                                'select, joing, or other construct.')

        else:
            raise ArgumentError('`tablename` or `selectable` argument is required.')

        if not selectable.primary_key.columns and not \
            'primary_key' in mapper_args:

            if tablename:
                raise NoForeignKeysError('table {} does not have a primary key defined'.format(
                    tablename
                ))
            else:
                raise NoForeignKeysError('Selectable {} does not have a primary key defined.'.format(
                    selectable
                ))

        mapped_cls = class_for_table(
            self.sess,
            self.engine,
            selectable,
            base or self.base,
            mapper_args
        )

        self._cache[attrname] = mapped_cls
        return mapped_cls


def invokeglobalsession():
    invoke_session = DatabaseSession()

    return invoke_session.sess


CLOUD_KERNEL_SESSION = invokeglobalsession()
