from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler


# TODO: rename file

db = SQLAlchemy()
sched = BackgroundScheduler()
