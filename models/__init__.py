import datetime
import logging

from flask import abort
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import CheckConstraint
from sqlalchemy.sql import func

from utilities.exceptions import (
    InvalidRequestData,
    ResourceNotFound,
)

db = SQLAlchemy()
logger = logging.getLogger(__name__)

class BaseModel(db.Model):
    __abstract__ = True

    id_ = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(20), nullable=False, default='active')
    deleted_data = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime)  # Manually set while updating row
    deleted_at = db.Column(db.DateTime)  # Manually set while deleted

    # __table_args__ = (CheckConstraint(status.in_(['active', 'deleted'])),)

    def _type(self):
        """
        Get the derived class' name. This method isn't being used
        anywhere currently.
        """

        return self.__class__.__name__

    @classmethod
    def get_one(cls, id_or_token, status='active', error_message=''):
        """
        This function returns the object from the database based on
        whether the filter is the id or the token. Returns None if the
        object is not found. Pass status=None if you do not want the
        status filter to be applied.
        """

        if type(id_or_token) == int:
            # id_or_token contains the id
            obj = cls.query.get(id_or_token)
            if obj is None:
                print(obj)
            if obj is None:
                errors = [{
                    'field': 'data.id',
                    'description': 'id cannot be found',
                }]
                raise InvalidRequestData(errors)
            # Check if the object's status matches the requested status
            if obj.status == status:
                return obj
        elif type(id_or_token) == str:
            # id_or_token contains the token
            if status is None:
                obj = cls.query.filter_by(token=id_or_token).first()
                if obj is None:
                    errors = [{
                        'field': 'data.token',
                        'description': 'token cannot be found',
                    }]
                    raise InvalidRequestData(errors)
                return obj
            obj = cls.query.filter(
                cls.token == id_or_token,
                cls.status == status
            ).first()
            if obj is None:
                errors = [{
                    'field': 'data.token',
                    'description': 'token cannot be found',
                }]
                abort(404)
                raise InvalidRequestData(errors)

            return obj
        else:
            if error_message == '':
                raise ValueError()
            raise ValueError(error_message)

    @classmethod
    def get_all(cls, status='active'):
        """
        This function returns all the objects from the database.
        Pass status=None if you do not want the status filter to be applied.
        """

        if status is None:
            return cls.query.all()
        return cls.query.filter_by(status=status).all()

    @classmethod
    def soft_delete(cls, id_or_token):
        """
        This function sets the status of an object (row) to `deleted` and sets the
        value of the `deleted_at` to the current time. This function does not commit
        the changes to the database, that has to be taken care of in the actions layer.
        Only currently `active` objects can be deleted.
        """

        # Check if the object is existent in the database with the requested type
        if type(id_or_token) == int:
            # id_or_token contains the id
            obj = cls.query.get(id_or_token)

            # Check if object is present
            if obj is None:
                errors = [{
                    'field': 'data.id',
                    'description': 'Resource with id is not found',
                }]
                raise ResourceNotFound(errors)

            # Check if object has the `active` status
            if obj.status != 'active':
                errors = [{
                    'field': 'data.id',
                    'description': 'Active resource with id is not found',
                }]
                raise ResourceNotFound(errors)
        elif type(id_or_token) == str:
            # id_or_token contains the token
            obj = cls.query.filter_by(token=id_or_token).first()

            # Check if object is present
            if obj is None:
                errors = [{
                    'field': 'data.token',
                    'description': 'Resource with token is not found',
                }]
                raise ResourceNotFound(errors)

            # Check if object has the `active` status
            if obj.status != 'active':
                errors = [{
                    'field': 'data.id',
                    'description': 'Active resource with token is not found',
                }]
                raise ResourceNotFound(errors)
        else:
            raise ValueError

        obj.status = 'deleted'
        obj.deleted_at = datetime.datetime.now()

        return obj

    def get_base_details(self):
        """
        Get the base details
        """

        return {
            'id': self.id_,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
        }

