<img align="left" width="200" height="200" src="/images/cloud_drip.png">




# Cloud Drip
Cloud Drip is a Multi-Tenant Cloud Orchestration and Management Web Application.  Functioning seamlessly with leading cloud providers such as AWS, GCP, Azure, DigitalOcean, and Rackspace.






cloud_kernel is a major component of cloud drip; it's used for the management of Scheduling, Job Storage, Triggering, and DB Synchronization for Cloud Drip, A dynamic cloud management web application for cloud orchestration and data sharing.

# APScheduler
This kernel uses the following components for APScheduler
- Scheduler:
  - BackgroundScheduler
- JobStore:
  - MemoryJobStore
- Executer:
  - ThreadPoolExecuter
- Trigger:
  - Interval
