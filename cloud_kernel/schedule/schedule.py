from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.zookeeper import ZooKeeperJobStore
from cloud_kernel.schedule.environment import platform_environment
from cloud_kernel.schedule.callables import FetchStaticTriggers
from cloud_kernel.trigger.trigger_aws import *
from pytz import utc


class CloudKernelSingleton(object):
    """
        - Please read the README.txt (not README.md) before changing

        - instantiate the scheduler, then use logic to determine the best
        combination needed to operate in a given environment.

        - Ex. ThreadPoolExecutor or ProcessPoolExecutor?  ProcessPoolExecutor
        ensures the most efficient use of a multiple core system, which is very
        likely. Things such as this should be taken into account when configuring
        a Scheduler.
    """
    def __init__(self, *args, **kwargs):
        self.ck_scheduler = BackgroundScheduler()
        self.executer = {
            'default': ThreadPoolExecutor(5)
        }
        self.jobstores = {
            'default': MemoryJobStore()
            # 'zookeeper': ZooKeeperJobStore()
        }
        self.job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }

        (cpu, kafka) = platform_environment()
        if kafka:
            # not sure what I want to do with this yet, I'm hoping to use kafka
            # as a storage alternative for memory
            pass
        # if cpu >= 4:
        #     self.executer = ProcessPoolExecutor(5)

        self.ck_scheduler = BackgroundScheduler(
            jobstores=self.jobstores, executors=self.executer, job_defaults=self.job_defaults,
            timezone=utc
        )

    def __call__(self, function):
        def inner_wrapper(*args, **kwargs):

            self.ck_scheduler.start()

            status = function(*args, **kwargs)
            return status
        return inner_wrapper


# @CloudKernelSingleton()
class CloudKernelSchedule(CloudKernelSingleton):
    """
        - ImmutableJobs are the SDK Level Callables that will be loaded
        everytime the program starts.  These will retrieve data from existing
        resources in a cloud Tenant. There will be another feed of Callables
        which will represent jobs for tasks provided by the application user.
        These are tasks to create resources within a cloud Tenant.

        - We will load all of the immutable callables here, and they will be added
        one at a time to the job list.  The FetchCallables method can be used
        to return a normal, unsorted tuple, or a sorted tuple.  The sorted Tuple
        will provide capability for prioritizing the callabe list based on the
        data that it will return, and the associated provider.
    """

    def __init__(self):
        super(CloudKernelSchedule, self).__init__(self)

    # @classmethod
    def ImmutableJobs(self, interval_value=.50, interval_multiplier=1):
        """
        Fetch an immutables list of callables and add them to the scheduler as
        Jobs.  Each pass through in the loop will use the interval and multiplier
        to ensure an adequate offset is provided between execution of scheduled
        jobs.
        """
        interval = interval_value
        multiplier = interval_multiplier
        # ImmutableJobList = FetchCallables()
        ImmutableJobList = FetchStaticTriggers.FetchCallables()

        print("Queing Jobs in Scheduler...")
        for job in ImmutableJobList:
            print("Current Interval Value: {}".format((interval + multiplier/2)))
            self.ck_scheduler.add_job(
                job,
                'interval',
                minutes=interval * multiplier
            )
            interval = interval + multiplier

        print("Jobs Queued for Execution")
        print("{}".format(self.ck_scheduler.print_jobs()))

# TODO: Add event listener, option for kafka, etc.

