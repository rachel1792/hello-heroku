from datetime import datetime, timedelta
import pytz

from xword.lib.database import sched


def test_daily_jobs():
    from clock import xword_etl
    import pdb
    pdb.set_trace()
    for job in sched.get_jobs():
        assert job.next_run_time >= pytz.utc.localize(datetime.utcnow())
        assert job.next_run_time <= pytz.utc.localize(datetime.utcnow()) + timedelta(days=1)
