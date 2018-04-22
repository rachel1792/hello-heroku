import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from app import db


# TODO: Add across/down orientation and clue number.

class Xwords(db.Model):
    __tablename__ = 'xwords'

    id = sa.Column(UUID, default=lambda: uuid4().hex, primary_key=True)
    created_at = sa.Column(
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
        default=sa.func.now(),
        nullable=False
    )
    clue = sa.Column(sa.String(150), nullable=False)
    answer = sa.Column(sa.String(30), nullable=False)
    debut = sa.Column(sa.Boolean(), default=sa.false(), server_default=sa.false())

    def __repr__(self):
        return '<clue: {}, answer: {}>'.format(self.clue, self.answer)


class SundayTitles(db.Model):
    __tablename__ = 'sunday_titles'
    id = sa.Column(UUID, default=lambda: uuid4().hex, primary_key=True)
    created_at = sa.Column(
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
        default=sa.func.now(),
        nullable=False
    )
    title = sa.Column(sa.String(150), nullable=False)
    date = sa.Column(sa.Date(), nullable=False)

    def __repr__(self):
        return '<date: {}, title: {}>'.format(self.date, self.title)
