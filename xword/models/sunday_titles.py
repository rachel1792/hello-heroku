import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from xword.models.base import Base


class SundayTitles(Base):
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
