from cloud_kernel.trigger.trigger_base import CloudKernelTriggerBase


class GetRackSpaceHosts(object):
    __metaclass__ = CloudKernelTriggerBase

    def __init__(self):
        self.name = 'rackspace.1'
        print(self.name)
