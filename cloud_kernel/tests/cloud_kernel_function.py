from cloud_kernel.schedule.schedule import CloudKernelSchedule
import time
import os

if __name__ == "__main__":
    t = CloudKernelSchedule()

    t.ImmutableJobs()
    t.ck_scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # in app, sleep and call the ImmutableJobs() again
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        t.ck_scheduler.shutdown()
