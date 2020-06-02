from cloud_kernel.db.db_core import *
from cloud_kernel.trigger.trigger_base import CloudKernelTriggerBase


class GetData(metaclass=CloudKernelTriggerBase):
    __triggerattributes__ = ['__bases__']

    def __init__(self):
        self.name = 'aws_data.1'
        print(self.name)

    def __iskerneltrigger__(cls, name, bases):
        return cls.__name__

    def UpdateDataStores(self):
        '''
        Save to Database
        '''
        pass


class GetHosts(metaclass=CloudKernelTriggerBase):
    __triggerattributes__ = ['__bases__']

    def __init__(self):
        self.name = 'aws_host.1'
        print(self.name)

    def __iskerneltrigger__(cls, name, bases):
        return cls.__name__


class GetUsers(metaclass=CloudKernelTriggerBase):
    __triggerattributes__ = ['__bases__']

    def __init__(self):
        self.name = 'aws_user.1'
        print(self.name)

    def __iskerneltrigger__(cls, name, bases):
        return cls.__name__
