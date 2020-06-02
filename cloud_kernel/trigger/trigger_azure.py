from cloud_kernel.trigger.trigger_base import CloudKernelTriggerBase


class GetAzureHosts(object):
    __metaclass__ = CloudKernelTriggerBase

    def __init__(self):
        self.name = 'azure_host.1'
        print(self.name)
