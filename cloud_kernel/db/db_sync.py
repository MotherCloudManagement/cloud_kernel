from cloud_kernel.db import DatabaseSession, CLOUD_KERNEL_ENGINE_STRING
from cloud_kernel.db.db_core import LoadTables
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
from collections import Mapping


class DatabasePush(object):
    """
    The Database push, pushes data from the read/write database
    to the read-only database.
    """
    _table_imports = LoadTables.LoadTableNames()

    def __init__(self, engine, session=None):
        self.engine = create_engine(engine)

        if session is None:
            self._session = sessionmaker(
                autoflush=False,
                expire_on_commit=False,
                bind=self.engine
            )

        self.session = self._session()

    def synchronizedata(self, timeout=None, rollback_condition=None,
                        dataset=None):

        if not isinstance(dataset, Mapping):
            raise TypeError('Dataset type not \'Mapping,\' received: '.format(
                type(dataset)
            ))

        _dataset = dataset
