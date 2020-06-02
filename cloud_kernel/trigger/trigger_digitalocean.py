from cloud_kernel.trigger.trigger_base import CloudKernelTriggerBase


class GetDOHosts(object):

    __metaclass__ = CloudKernelTriggerBase

    def __init__(self):
        self.name = 'digital_ocean_host.1'
        print(self.name)
