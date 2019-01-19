import json
import logging

from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

from models import (
    BaseModel,
    db
)
from utilities.exceptions import InvalidRequestData

secret = Bcrypt()

log = logging.getLogger('User Log')


class User(BaseModel):
    __tablename__ = 'user'

    name = db.Column(db.String(300))
    username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    favourite = db.Column(db.Integer, db.ForeignKey('superhero.id'))
    profile_picture = db.Column(db.String())

    def __init__(self, payload):
        """
        This function initialises an user an adds him to the database.

        :param payload: Payload contains the data of the user needed to
        be added.

        :return: Details of the added user
        """

        try:

            for key, value in payload.items():
                if key == 'password':
                    continue
                setattr(self, key, value)

            self.password = secret.generate_password_hash(
                payload['password']
            ).decode('utf-8')

        except IntegrityError:

            raise InvalidRequestData(errors=[{
                'error': 'Username already exists',
                'field': 'data.username',
            }])

        db.session.add(self)
        db.session.commit()

    def get_details(self):
        """
        This function returns the details of an user in a dictionary
        format.

        :return dict: Details of the user
        """

        payload = dict()
        payload['name'] = self.name
        payload['username'] = self.username,
        payload['favourite'] = self.favourite,
        payload['profile_picture'] = self.profile_picture

        base_details = self.get_base_details()
        return {**base_details, **payload}

    @staticmethod
    def get_all_details():
        """
        This function gets the details of all the users in the database
        whose status is active

        :return list(dict): Details of all the users
        """

        users_details = []
        for user in User.get_all():
            users_details.append(user.get_details())

        return users_details

    def update(self, payload):
        """
        This function updates an user with the given data in the payload.

        :return list(dict): Details of all the users
        """

        try:
            for key, value in payload.items():
                if key == 'password':
                    continue
                setattr(self, key, value)
            self.password = secret.generate_password_hash(
                    payload['password']
                ).decode('utf-8')

        except IntegrityError as e:

            raise InvalidRequestData(errors=[{
                'error': 'Username already exists',
                'field': 'data.username',
            }])

        db.session.commit()
        return self.get_details()

    @staticmethod
    def delete_details(id_):
        """
        This function soft deletes an user from the database.

        :param id_: Username of the user to be deleted.

        :return None:
        """
        user = User.get_one(id_)
        if user:
            data = {
                'username': user.username
            }
            user.deleted_data = json.dumps(data)
            user.soft_delete()
            db.session.commit()

        return None

    def check_password(self, password):
        return secret.check_password_hash(self.password, password)
