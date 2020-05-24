from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

MAX_SQL_VARIABLES = 900
INTERNAL_SESSION_ATTR = '_cloudkernel_sync'
CLOUD_KERNEL_ENGINE_STRING = 'postgresql://localhost:5432'

if __name__ == "__main__":

    class DatabaseSession(object):

        def __init__(self):
            self.engine = create_engine(CLOUD_KERNEL_ENGINE_STRING)
            self.globalsession = sessionmaker(
                autoflush=False, expire_on_commit=False
            )

            self.globalsession.configure(bind=self.engine)

    def InvokeGlobalSession():
        sess = DatabaseSession()

        return sess.globalsession

    CLOUD_KERNEL_SESSION = InvokeGlobalSession()
