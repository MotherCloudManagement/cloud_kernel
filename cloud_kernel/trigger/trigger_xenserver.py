from cloud_kernel.trigger.trigger_base import CloudKernelTriggerBase


class GetXenHosts(object):
    __metaclass__ = CloudKernelTriggerBase

    def __init__(self):
        self.name = 'xenhosts_host.1'
        print(self.name)
