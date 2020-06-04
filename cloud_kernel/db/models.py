from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta


#: Database Table Prefix for Identifying the proper Table
tablename_prefix = "sync_"


class PrefixTables(DeclarativeMeta):
    def __init__(cls, classname, bases, dict_):
        if '__tablename__' in dict_:
            tn = dict_['__tablename__']
            cls.__tablename__ = dict_['__tablename__'] = tablename_prefix + tn

        return super(PrefixTables, cls).__init__(classname, bases, dict_)


Base = declarative_base(metaclass=PrefixTables)


class Node(Base):

    __tablename__ = ''

    node_id = Column(Integer, primary_key=True)
    node_name = Column(String(128))
    region = Column(String(100))
    provider = Column(String(20))
    network_address = Column(String(15))
    memory_size = Column(Integer)
    storage_size = Column(Integer)
    cpu = Column(Integer)
    application = Column(String(100))

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)

    def __repr__(self):
        return u"<Node node_id: {0}, node_name: {1}, "\
            u"region: {2}, provider: {3}, network_address: {4}, "\
            u"memory_size: {5}, storage_size: {6}, cpu: {7}, "\
            u"application: {8}".\
            format(
                self.node_id, self.node_name,
                self.region, self.provider,
                self.network_address, self.memory_size,
                self.storage_size, self.cpu,
                self.application
            )
