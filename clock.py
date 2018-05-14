from rq import Queue
from worker import conn

from xword.lib.database import sched
from xword.lib.xword_etl import etl


# TODO: add logging

q = Queue(connection=conn)


@sched.scheduled_job('cron', hour=16, minute=00, second=0)
def xword_etl():
    q.enqueue(etl)


sched.start()
