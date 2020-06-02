from cloud_kernel.trigger.trigger_base import CloudKernelTriggerBase


class GetVsphereHosts(object):
    __metaclass__ = CloudKernelTriggerBase

    def __init__(self):
        self.name = 'vsphere_host.1'
        print(self.name)
