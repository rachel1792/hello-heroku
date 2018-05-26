from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore


# TODO: rename file

db = SQLAlchemy()
sched = BackgroundScheduler(jobstores={'default': RedisJobStore()})
