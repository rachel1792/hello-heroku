from rq import Queue
from worker import conn

from xword.lib.database import sched
from xword.lib.xword_etl import etl
from xword.utils.loggers import get_logger

logger = get_logger(__name__)

q = Queue(connection=conn)


@sched.scheduled_job('cron', hour=4, minute=0, second=0)
def xword_etl():
    logger.info('Queueing xword ETL task.')
    q.enqueue(etl)


@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')


logger.info('Running clock.py')
sched.start()
