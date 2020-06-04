from cloud_kernel.db import DatabaseSession, CLOUD_KERNEL_ENGINE_STRING
from sqlalchemy import Table, MetaData, join
from sqlalchemy import schema, sql, util
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, mapper, \
    class_mapper, relationship, \
    object_session, attributes, Session
from sqlalchemy.orm.interfaces import MapperExtension, EXT_CONTINUE
from sqlalchemy.sql import expression
from sqlalchemy.exc import NoForeignKeysError, ArgumentError


class DatabaseSessionNormalizer(Session):

    def __init__(self):
        super(DatabaseSessionNormalizer, self).__init__()

    def __getattribute__(self, item):
        DatabaseSessionManager.__getattr__(item)


class DatabaseSessionManager(object):

    def __init__(self, engine, session=None):
        self.engine = create_engine(engine)

        if session is None:
            self._session = sessionmaker(
                autoflush=False,
                expire_on_commit=False,
                bind=self.engine
            )

        self.session = self._session()

    def __getattr__(self, attribute):
        print(self.session.__dict__.keys())
        if not getattr(self.session, attribute):
            setattr(self.session, attribute, 'Owner and CEO')
        return getattr(self.session, attribute)


if __name__ == "__main__":
    db = DatabaseSessionManager(CLOUD_KERNEL_ENGINE_STRING)
    print(db.session.execute('SELECT * FROM aws_data').fetchall())
    print(db.session.maurice)
