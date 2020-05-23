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
from cloud_kernel.schedule.persistant import CloudKafkaProduce
from collections.abc import Mapping
import ast
import json


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


class FetchProducedJobs(object):
    """
    This class will use CloudKafkaProduce, to gather user submitted jobs
    from the WebUI, and store them serially into a kafka persistent queue.
    They will remain their until confirmed execution.  The consumer is
    responsible for reading the jobs off of the Queue, and handing the data
    off to a function that will execute them.  The Consumer will destroy the
    Queue once all jobs have been successfully completed.
    """

    @classmethod
    def FetchandProduce(cls, json_data):

        # Lets get the data and verify it before we even both creating a producer.
        if not isinstance(json_data, Mapping):
            try:
                json_data = ast.literal_eval(json_data)
            except ValueError:
                raise TypeError("Did not Receive a valid Mapping and was not able to"+\
                                "Convert it to a valid mapping!")

        producer = CloudKafkaProduce()

        # Provide the parameters topic and data.  Data must be a valid Mapping,
        # verifiable with abc.Mapping()
        producer.ProduceMessage('web_jobs', data=json_data)

        # Here we are not returning a code, at least for now.  I don't wnat the app
        # to stop working if we are not able to get the jobs from the WebUI.  That
        # should simply provide notification.  All that is needed is for the WebUI
        # to somehow call FetchProducedJobs.FetchandProduce()

        return "Producer Execution Completed"
