import typing
from sqlalchemy_utils import database_exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import os
import sys
import logging
from database.db_funds import Fund
from database.db_accounts import Account
from database.db_portfolios import Portfolio
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

    # def insert(self, model, **kwargs):

    #     instance = self.session.query(model).filter_by(**kwargs).one_or_none()

    #     if instance:
    #         logger.debug(
    #             f'This record: Device ID: {instance.isin} - Hostname: {instance.name} already exist.')
    #         return instance, False

    #     else:

    #         instance = model(**kwargs)

    #         try:
    #             self.session.add(instance)
    #             self.session.commit()
    #             logger.debug(f'The record {instance} was created succesfully.')
    #             return instance, True

    #         except Exception as e:  # The actual exception depends on the specific database so we catch all exceptions. This is similar to the official documentation: https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html
    #             self.session.rollback()
    #             instance = self.session.query(model).filter_by(**kwargs).one()
    #             return instance, False
    #             print(str(e))

        # else:
        #     return instance, True

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

        # instance = self.session.query(
        # model).filter_by(isin=isin).one_or_none()

        instance = self.session.query(
            model).filter_by(**filter).one_or_none()

        for k, v in data.items():
            setattr(instance, k, v)

        self.session.commit()

        logger.debug(f'The record {instance} has been updated succesfully.')
        return instance

    # def delete(self, data):
    #     self.session.delete(data)
    #     self.session.commit()

    def session_close(self):
        self.session.close()
