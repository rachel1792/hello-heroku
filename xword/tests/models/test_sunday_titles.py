import datetime

from xword.models.sunday_titles import SundayTitles


class TestSundayTitles(object):
    def test_create_sunday_title(self):
        """Test that we can create new sunday title entry."""

        attrs = dict(
            title='fake title',
            date=datetime.date.today(),
        )

        title_entry = SundayTitles(**attrs)
        title_entry.save()
        res = SundayTitles.get(title_entry.id)

        assert res.__repr__() == '<date: {}, title: {}>'.format(attrs['date'], attrs['title'])

        for attr in attrs:
            assert getattr(res, attr) == attrs[attr]
