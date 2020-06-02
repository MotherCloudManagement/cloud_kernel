from cloud_kernel.trigger.trigger_base import CloudKernelTriggerBase


class GetVultrHosts(object):
    __metaclass__ = CloudKernelTriggerBase

    def __init__(self):
        self.name = 'vultr_host.1'
        print(self.name)
