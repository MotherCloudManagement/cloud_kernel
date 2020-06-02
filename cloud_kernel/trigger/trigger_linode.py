from cloud_kernel.trigger.trigger_base import CloudKernelTriggerBase


class GetLinodeHosts(object):
    __metaclass__ = CloudKernelTriggerBase

    def __init__(self):
        self.name = 'linode_host.1'
        print(self.name)
