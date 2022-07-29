import typing
from sqlalchemy_utils import database_exists
import logging
from database.db_tables import *
from database.base import engine, Base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import MultipleResultsFound


logger = logging.getLogger()


class Connector:

    def __init__(self, session) -> None:

        if not database_exists(engine.url):
            logger.info(f'Creating database at: {engine.url}')
            Base.metadata.create_all(engine)

        self.session = session
        logger.info(f'Connector initialized!')

    def select(self, model, filter: typing.Dict):
        try:
            return self.session.query(model).filter_by(**filter).one_or_none()
        except MultipleResultsFound as e:
            logger.warning(
                f"Multiple result were found for object {model} filter: {filter}:: {e}")
            return None

    def select_all(self, model, filter=None):
        if filter is not None:
            return self.session.query(model).filter_by(**filter).all()
        else:
            return self.session.query(model).all()

    def insert(self, model, data: typing.Dict):

        try:
            instance = model(**data)
            self.session.add(instance)
            self.session.commit()
            return instance

        except IntegrityError as e:
            self.session.rollback()
            logger.warning(
                f"The record: {instance} already exist in the database.:: {e}")
            return None

    def update(self, model, filter: typing.Dict, data: typing.Dict):

        instance = self.session.query(
            model).filter_by(**filter).one_or_none()

        for k, v in data.items():
            setattr(instance, k, v)

        self.session.commit()

        logger.debug(f'The record {instance} has been updated succesfully.')
        return instance

    def delete(self, object):
        self.session.delete(object)
        self.session.commit()
        return True

    def session_close(self):
        self.session.close()
