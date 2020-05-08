'''
The components of the cloud_kernel apscheduler are fairly straightforward:
    - Trigger: Each job has its own trigger which determines when the job should
      be run next. Beyond their initial configuration, triggers are completely
      stateless. (interval)

    - Job Store: houses the scheduled jobs. The default job store simply keeps
      the jobs in memory, but others store them in various kinds of databases.
      Non default stores serialize and deserialize data when when loading and
      unloading.  In this case, the store acts as a middleman for saving, loading,
      updating, and searching jobs. (MemoryJobStore)

    - Scheduler: Is what binds the rest together; providing the developer with an
      interface that handles all interaction between other components.
      (BackgroundScheduler is what cloud_kernel uses.)

    - Executer: Handles the running of the Job.  They submit the callable (job)
      to a thread or process pool.  After execution, the executer notifies the
      scheduler. (ThreadPoolExecutor and/or ProcessPoolExecutor)


Cloud_Kernel Logic:

Callables will be a tuple of 'classes' derived from the SDK level code.  This
will be an immutable collection of classes that will be continually executed to
refresh data.

(Tuple of Classes) --> (job) <---> (Trigger)
                         |
                         |
                         |
                  (Memory or DB)
                         |
                         |
                         | -----------> (Executer) ------> (Thread or Pool)


** You can also instantiate the scheduler first, add jobs and configure the **
   scheduler afterwards. This way you get maximum flexibility for any
   environment.


'''
