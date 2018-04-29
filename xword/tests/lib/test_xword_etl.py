import pytest
from freezegun import freeze_time

from xword.lib.xword_etl import extract, transform, load, etl


@pytest.mark.vcr()
@freeze_time('2018-04-29 01:00:00')
def test_extract():
    extract()
