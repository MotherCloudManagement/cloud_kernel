from cloud_kernel.schedule.schedule import CloudKernelSchedule
from cloud_kernel.schedule.persistant import CloudKafkaProduce
import time
import os

if __name__ == "__main__":

    test_set = {'Name': 'JohnDoe', 'Task': 'CreateAWSNode',
                'Specification': '{"Hostname": "bordernode", "RAM": "8", "CPU": "4", "Disk": "500"}'}

    print("Testing with the Following Data Sample: "+\
          "Topic: {}, Data: {}".format('test_topic', test_set))

    t = CloudKafkaProduce()
    t.ProduceMessage('test_topic', test_set)

    # in app, sleep and call the ImmutableJobs() again
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        t.ck_scheduler.shutdown()
