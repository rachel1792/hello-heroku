from datetime import datetime, timedelta
import pytz

from xword.lib.database import sched


def test_daily_jobs():
    assert not sched.get_jobs()
    execfile('clock.py')
    # assert len(sched.get_jobs()) == 1
    # for job in sched.get_jobs():
    #     assert job.next_run_time >= pytz.utc.localize(datetime.utcnow())
    #     assert job.next_run_time <= pytz.utc.localize(datetime.utcnow()) + timedelta(days=1)
