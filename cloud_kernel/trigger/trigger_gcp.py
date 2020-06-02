from cloud_kernel.trigger.trigger_base import CloudKernelTriggerBase


class GetGCPHosts(object):
    __metaclass__ = CloudKernelTriggerBase

    def __init__(self):
        self.name = 'gcp_host.1'
        print(self.name)
