from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import ARRAY

from models import (
    BaseModel,
    db
)
from utilities.exceptions import InvalidRequestData


class Superhero(BaseModel):
    __tablename__ = 'superhero'

    name = db.Column(db.String(400))
    height = db.Column(db.String())
    weight = db.Column(db.String())
    special_power = db.Column(db.String())
    fathers_name = db.Column(db.String(300))
    mothers_name = db.Column(db.String(300))
    main_powers = db.Column(ARRAY(db.String()))
    alive = db.Column(db.Boolean())
    race = db.Column(db.String(200))

    def __init__(self, payload):

        try:

            for key, value in payload.items():
                if key == 'main_powers':
                    continue
                if key == 'alive':
                    if value.lower() == 'yes':
                        setattr(self, key, True)
                    else:
                        setattr(self, key, False)
                setattr(self, key, value)

            if 'main_powers' in payload:
                self.main_powers = payload['main_powers'].strip().split(',')

        except IntegrityError:

            raise InvalidRequestData(errors=[{
                'error': 'Superhero already exists',
                'field': None,
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
        payload['height'] = self.height,
        payload['weight'] = self.weight,
        payload['special_power'] = self.special_power
        payload['fathers_name'] = self.fathers_name
        payload['mothers_name'] = self.mothers_name
        payload['alive'] = self.alive
        payload['race'] = self.race
        payload['main_powers'] = self.main_powers

        return {**self.base_details, **payload}

    @staticmethod
    def get_all_details():
        """
        This function gets the details of all the users in the database
        whose status is active

        :return list(dict): Details of all the users
        """

        superheroes_details = []
        for superhero in Superhero.get_all():
            superheroes_details.append(superhero.get_details())

        return superheroes_details

    def update(self, payload):
        """
        This function updates an user with the given data in the payload.

        :return list(dict): Details of all the users
        """

        try:

            for key, value in payload.items():
                if key == 'main_powers':
                    continue
                if key == 'alive':
                    if value.lower() == 'yes':
                        setattr(self, key, True)
                    else:
                        setattr(self, key, False)
                setattr(self, key, value)

            if 'main_powers' in payload:
                self.main_powers = payload['main_powers'].strip().split(',')

        except IntegrityError:

            raise InvalidRequestData(errors=[{
                'error': 'Superhero already exists',
                'field': None,
            }])

        db.session.commit()

    @staticmethod
    def delete_details(id_):
        """
        This function soft deletes an user from the database.

        :param id_: ID of the superhero to be deleted.

        :return None:
        """
        superhero = Superhero.get_one(id_)
        if superhero:
            superhero.soft_delete()
            db.session.commit()

        return None