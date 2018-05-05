from xword.models.xwords import Xwords


class TestXwords(object):
    def test_create_xword(self):
        """Test that we can create new user."""

        attrs = dict(
            clue='fake clue',
            answer='ANSWER',
            debut=False,
            orientation='across',
        )

        xword_entry = Xwords(**attrs)
        xword_entry.save()
        res = Xwords.get(xword_entry.id)
        for attr in attrs:
            assert getattr(res, attr) == attrs[attr]
