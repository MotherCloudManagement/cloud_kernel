from cloud_kernel.trigger.trigger_base import CloudKernelTriggerBase


class GetOpenStackHosts(object):
    __metaclass__ = CloudKernelTriggerBase

    def __init__(self):
        self.name = 'openstack_host.1'
        print(self.name)
