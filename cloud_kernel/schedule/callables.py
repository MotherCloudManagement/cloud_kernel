from cloud_kernel.trigger.trigger_aws import *
from cloud_kernel.trigger.trigger_xenserver import *
from cloud_kernel.trigger.trigger_vultr import *
from cloud_kernel.trigger.trigger_vsphere import *
from cloud_kernel.trigger.trigger_softlayer import *
from cloud_kernel.trigger.trigger_rackspace import *
from cloud_kernel.trigger.trigger_OpenStack import *
from cloud_kernel.trigger.trigger_linode import *
from cloud_kernel.trigger.trigger_gcp import *
from cloud_kernel.trigger.trigger_digitalocean import *
from cloud_kernel.trigger.trigger_azure import *


class FetchStaticTriggers(object):
    """
    This class will fetch all static callables and return them so that the Kernel
    can continuously fetch them and add them to the job list.

    Static callables are those which do not change, and will always return the same
    information set, although the data itself will differ.  These are the callables
    that cloud_kernel will monitor for updates because the data is representative
    of something the end-user will always want.

    Ex: GetAWSEC2Hosts(), ListIAMUsers(), GetGCPEnvironments(), etc.
    """

    @classmethod
    def FetchCallables(cls):

        # we want an immutable list
        return (GetData, GetHosts, GetUsers,
                            GetAzureHosts, GetDOHosts, GetGCPHosts,
                            GetLinodeHosts, GetOpenStackHosts, GetOpenStackHosts,
                            GetRackSpaceHosts, GetSoftLayerHosts, GetVsphereHosts,
                            GetVultrHosts, GetXenHosts
                )

