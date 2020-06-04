from cloud_kernel.db.db_core import *
from cloud_kernel.trigger.trigger_base import CloudKernelTriggerBase
from cloud_kernel.db import DatabaseSession, CLOUD_KERNEL_ENGINE_STRING


class GetAWSData(metaclass=CloudKernelTriggerBase):
    __triggerattributes__ = ['__bases__']

    def __init__(self):
        self.name = 'aws_data.1'
        print(self.name)
        print(self.updatedatastore())

    def __iskerneltrigger__(cls, name, bases):
        return cls.__name__

    def updatedatastore(self):
        '''
        example use case.  This method could retrieve user data, and then insert into
        the db.  There will also need to be a verification that tables exist using the
        `IF NOT EXIST` statement.
        :return:
        '''
        db = DatabaseSession(CLOUD_KERNEL_ENGINE_STRING)

        return db.sess.execute('SELECT * FROM aws_data').fetchall()


class GetAWSHosts(metaclass=CloudKernelTriggerBase):
    __triggerattributes__ = ['__bases__']

    def __init__(self):
        self.name = 'aws_host.1'
        print(self.name)

    def __iskerneltrigger__(cls, name, bases):
        return cls.__name__


class GetAWSUsers(metaclass=CloudKernelTriggerBase):
    __triggerattributes__ = ['__bases__']

    def __init__(self):
        self.name = 'aws_user.1'
        print(self.name)

    def __iskerneltrigger__(cls, name, bases):
        return cls.__name__
