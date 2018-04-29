Vault
Data Collection system under project olympus.

Deployment procedure
Rabbit:
$ gssh rabbit
if fails, $ gcloud init first with an authorized account
Switch to deployment user: $ sudo su mznco
Navigate to the right folder: $ cd ~/olympus
Kill celery processes: $ pkill -9 -f celery
(Optional) Purge rabbit queues
$ source env/bin/activate
$ git pull
if this fails, $ git reset --hard HEAD, re-pull
Install packages (if necessary): $ fab bootstrap
Migrations (if exist): $ fab production bootstrap.migrate:'upgrade head'
(Optional) Remove the old output file $ rm nohup.out
Restart flower: $ sudo systemctl restart celery_flower
Restart worker:
see workers section below
Restart beat: $ sudo systemctl restart celery_beat
There should only be one celery_beat running
If the previous command was run multiple times, kill all but one
Check flower with celery_flower_prod credential
(Optional) $ ps aux | grep celery make sure things work as intended
Workers:
make sure running from latest master on a machine with olympus_deployment private key
make sure all the servers are listed in the production.yaml --> worker_instances
if we want to change min & max concurrency, visit olympus/constants/celery_queues.py
$ fab production:true deploy:true
Celery Flower and Rabbitmq Management Portal
celery flower
!!! Indications of the scraper working properly:
appropriate workers online (although flower might mislabel online workers to be offline, in which case, double check)
queue_extract_airbnb_calendars task did not fail
this task is queued at 00:00 UTC daily
if failed, to recover:
$ fab production shell
$ from olympus.celery_tasks.vault.airbnb.pricing_extract import queue_extract_airbnb_calendars
$ queue_extract_airbnb_calendars.apply_async()
queue_homeaway_pricing_tasks did not fail
this task is queued at 02:00 UTC daily
if failed, to recover:
$ fab production shell
$ from olympus.celery_tasks.vault.homeaway.pricing_extract import queue_homeaway_pricing_tasks
$ queue_homeaway_pricing_tasks.apply_async()
similarly for the other queueing tasks
only reasonable amount of failed tasks
rabbitmq management portal
Logging
kibana
Google BigQuery
main url
scraped_airbnb table
Click on 'Refresh' to see the latest status (it does not auto refresh upon load)
!!! Indications of the scraper working properly:
If you can see a streaming buffer table on the bottom
If 'Last Modified' is some time today
A handy legacy SQL query to check data completeness:
SELECT partition_id FROM [domio-prod:olympus.scraped_airbnb$__PARTITIONS_SUMMARY__] order by partition_id
Table schema and creation script:
olympus.scripts.create_olympus_dataset_and_tables.py
more columns have been added to the table since creation
It is very hard and costly to modify existing columns on a table
manually changing schemas
Google Cloud Storage
main_url
Bucket structure: domio-vault
airbnb
bookings
date (e.g. 2018-01-05)
JSON blob from date
listings
date (e.g. 2018-01-05)
JSON blob from date
pricing
date (e.g. 2018-01-05)
JSON blob from date
listing_details
date (e.g. 2018-01-05)
JSON blob from date
homeaway
listings
date (e.g. 2018-01-05)
HTML blob from date
pricing
date (e.g. 2018-01-05)
HTML blob from date
!!! Indications of the scraper working properly:
there should be a new folder with present date for airbnb listing details every Tuesday
there should be a new folder with present date for airbnb bookings every Wednesday
there should be a new folder with present date for airbnb pricing everyday
there should be a new folder with present date for homeaway pricing everyday
the latest folder for airbnb listings is within 7 days
the latest folder for homeaway listings is within 7 days
Sample GCS Console Commands:
gsutil help mv
gsutil mv -m gs://[SOURCE_BUCKET_NAME]/[SOURCE_OBJECT_NAME] gs://[DESTINATION_BUCKET_NAME]/[DESTINATION_OBJECT_NAME]
Google Compute Engine
main_url
relavant servers:
rabbit:
server holding celery task queues using rabbitmq
domio-swarm-01
main swarm server to run the etl tasks
Add a new server (pre-Richard Era):
Go to GCP cloud console compute engine, click on create instance
Edit:
Name(domio-xxxx)
Zone(us-east1-b)
Machine Type(beware of quotas)
Boot disk(Ubuntu 16.04 LTS)
Identity and API access (Allow full access to all Cloud APIs if needed, e.g. Bigquery access)
Go to GCP cloud console VPC network --> Enternal IP addresses, reserve static addresss if necessary
Go to Cloudflare with admin account, set up dns
Edit production config and deploy_spinup function accordingly