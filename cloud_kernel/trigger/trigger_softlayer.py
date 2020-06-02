from cloud_kernel.trigger.trigger_base import CloudKernelTriggerBase


class GetSoftLayerHosts(object):
    __metaclass__ = CloudKernelTriggerBase

    def __init__(self):
        self.name = 'softlayer.1'
        print(self.name)
