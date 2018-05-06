from datetime import date
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

import sqlalchemy as sa
from flask import abort
from pytz import utc
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import ColumnProperty
from sqlalchemy.orm import class_mapper

from xword.lib.database import db


class Base(db.Model):

    __abstract__ = True

    id = sa.Column(UUID, default=lambda: uuid4().hex, primary_key=True)
    created_at = sa.Column(
        sa.TIMESTAMP(timezone=True),
        server_default=db.func.now(),
        default=db.func.now(),
        nullable=False
    )
    deleted_at = sa.Column(sa.TIMESTAMP(timezone=True))
    updated_at = sa.Column(
        sa.TIMESTAMP(timezone=True),
        server_onupdate=db.func.now(),
        onupdate=db.func.now(),
        default=db.func.now(),
        nullable=False
    )

    def __init__(self, **kwargs):
        # Remove invalid keys.
        kwargs = self.remove_extra_keys(**kwargs)
        super(Base, self).__init__(**kwargs)

    def remove_extra_keys(self, **kwargs):
        for k in list(kwargs.keys()):
            if k not in self.columns():
                del kwargs[k]
        return kwargs

    def update_relationship(self, relationship, rel_id):
        """Update a relationship on the model."""
        formatted_rel_name = relationship[:-1]
        if relationship in self.relationships():
            rel_id_name = '{}_id'.format(formatted_rel_name)
            setattr(self, rel_id_name, rel_id)

    @classmethod
    def private_fields(cls):
        """Fields that should be private and never exposed."""
        return 'created_at', 'updated_at', 'deleted_at', 'password'

    @classmethod
    def relationships(cls, key_delim='.'):
        """Get all model foreign keys."""
        return [k.target_fullname.replace('.', key_delim) for k in cls.__table__.foreign_keys]

    @classmethod
    def columns(cls):
        """Get all model columns."""
        return [prop.key for prop in class_mapper(cls).iterate_properties
                if isinstance(prop, ColumnProperty)]

    @classmethod
    def store(cls, resource):
        """Save to the database."""
        cls.add_to_session(resource)
        db.session.commit()

    def to_dict(self):
        """Returns a dict from a record."""
        d = {}
        for col in self.columns():
            if col not in self.private_fields():
                val = getattr(self, col)
                if isinstance(val, Decimal):
                    val = float(val)
                elif isinstance(val, datetime):
                    val = val.astimezone(utc).isoformat()
                elif isinstance(val, date):
                    val = val.isoformat()
                d[col] = val
        return d

    def save(self):
        """Save to the database."""
        self.add_to_session()
        self.commit_session()
        return self

    @classmethod
    def bulk_save(cls, resources):
        """Bulk save many resources."""
        for resource in resources:
            resource.add_to_session()
        cls.commit_session()

        return resources

    @classmethod
    def commit_session(cls):
        """Updates the database records."""
        return db.session.commit()

    def add_to_session(self):
        """Add resource to the session without committing."""
        db.session.add(self)
        return self

    def delete(self, resource, soft_delete=True):
        """Delete a resource."""
        # Soft delete the resource by updating the deleted_at field.
        if soft_delete:
            resource.deleted_at = datetime.now()
            return self.commit_session()
        # Otherwise, permanently delete a resource.
        db.session.delete(resource)
        return db.session.commit()

    @classmethod
    def get_all(cls):
        """Get all records."""
        return cls.query.filter(
            cls.deleted_at.is_(None)
        )

    @classmethod
    def get_all_sorted_asc_by(cls, column):
        """Get all records sorted by certain column."""
        return cls.query.filter(
            cls.deleted_at.is_(None)
        ).order_by(
            getattr(cls, column).asc()
        )

    @classmethod
    def get(cls, record_id):
        """Get a record."""
        return cls.query.filter(
            cls.id == record_id
        ).filter(
            cls.deleted_at.is_(None)
        ).first()

    @classmethod
    def get_only_deleted(cls, record_id):
        """Get a record that has been soft deleted."""
        return cls.query.filter(
            cls.id == record_id
        ).filter(
            cls.deleted_at.isnot(None)
        ).first()

    @classmethod
    def get_by_email(cls, record_email):
        """Get a record."""
        return cls.query.filter(
            cls.email == record_email
        ).filter(
            cls.deleted_at.is_(None)
        ).first()

    @classmethod
    def get_or_initialize_by(cls, **kwargs):
        """Get a record by the arguments or initialize a new record in memory."""
        return cls.query.filter(
            cls.deleted_at.is_(None),
            *(getattr(cls, key) == kwargs[key] for key in kwargs)
        ).first() or cls(**kwargs)

    @classmethod
    def get_or_404(cls, record_id):
        """Get a record or 404."""
        record = cls.query.filter(
            cls.id == record_id
        ).filter(
            cls.deleted_at.is_(None)
        ).first()
        return record or abort(404)

    def update(self, **fields):
        """Update the record with passed in fields. This will commit to the database"""
        fields = self.remove_extra_keys(**fields)
        for col in fields.keys():
            setattr(self, col, fields[col])
        self.save()

    def safe_update(self, **fields):
        """Update the record with passed in fields, ignoring any private fields and 'id'. This
        will not commit to the database."""
        for key in self.private_fields():
            fields.pop(key, None)
        fields.pop('id', None)
        fields = self.remove_extra_keys(**fields)
        for col in fields.keys():
            setattr(self, col, fields[col])

    def clone(self):
        """Return a new model instance with the same contents, except for private fields and
        'id'."""
        previous_contents = self.to_dict()
        for key in self.private_fields():
            previous_contents.pop(key, None)
        previous_contents.pop('id', None)
        return self.__class__(**previous_contents)

    def flush(self):
        """Flush to the database. Does not commit."""
        db.session.flush()
        return self
