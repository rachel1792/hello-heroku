import datetime
import logging
from uuid import uuid4

import factory
from sqlalchemy.exc import InvalidRequestError

from xword.models.sunday_titles import SundayTitles
from xword.models.xwords import Xwords
from xword.lib.database import db
from xword.utils.loggers import get_logger


logger = get_logger(__name__)
logger.setLevel(logging.WARN)


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Base Factory."""

    class Meta:
        abstract = True
        sqlalchemy_session = db.session

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        """Returns a dictionary of a built object."""
        for k in list(kwargs.keys()):
            rel_key = '{}.id'.format(k)
            if rel_key in model_class.relationships():
                # This function is prepared to accept basically anything:
                # a key of the form other_table_id = id (straight id passthrough)
                # a key of the form other_table['id'] = id (dictionary with id)
                # a key of the form other_table.id = id (object with id attribute)
                if '{}_id'.format(k) in kwargs:  # prioritize direct key passthrough if present
                    kwargs['{}_id'.format(k)] = kwargs['{}_id'.format(k)]
                else:
                    try:  # if no direct key exists, look for an attribute
                        # this occurs if you passed in a full object
                        # when factory creating this model
                        kwargs['{}_id'.format(k)] = str(kwargs[k].id)
                    except AttributeError:  # last resort see if this is a dictionary
                        # this occurs if you used a subfactory
                        kwargs['{}_id'.format(k)] = str(kwargs[k]['id'])
        obj = super(BaseFactory, cls)._build(model_class, *args, **kwargs)
        obj_dict = obj.to_dict()
        try:
            db.session.expunge(obj)
        except InvalidRequestError:
            pass
        obj_dict['id'] = uuid4().hex
        return obj_dict

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Overrides create strategy, commits on create
        ACCEPTS ONLY MODEL OBJECTS. NO DICTIONARIES OR DIRECT KEY REFERENCES"""
        for k in list(kwargs.keys()):
            rel_key = '{}.id'.format(k)
            if rel_key in model_class.relationships():
                kwargs['{}_id'.format(k)] = str(kwargs[k].id)
        obj = super(BaseFactory, cls)._create(model_class, *args, **kwargs)
        obj.save()
        return obj


class XwordsFactory(BaseFactory):

    class Meta:
        model = Xwords

    clue = 'fake clue'
    answer = 'ANSWER'
    orientation = 'across'
    debut = False


class SundayTitlesFactory(BaseFactory):

    class Meta:
        model = SundayTitles

    title = 'FAKE TITLE'
    date = datetime.date.today()
