from apscheduler.schedulers.blocking import BlockingScheduler

from rq import Queue
from worker import conn

from xword.lib.xword_etl import etl


# TODO: add logging


sched = BlockingScheduler()

q = Queue(connection=conn)


@sched.scheduled_job('cron', hour=22, minute=55, second=0)
def xword_etl():
    q.enqueue(etl)


sched.start()
