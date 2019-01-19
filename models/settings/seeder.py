import logging

import click
from flask.cli import with_appcontext

from models import db
from models.superheroes import Superhero
from models.users import User

logger = logging.getLogger('Seed Logger')


def seed_users():
    """
    This function will seed the superheroes table with a few users
    """

    column_index = {
        'name': 1,
        'username': 2,
        'password': 3,
        'favourite_superhero': 4,
        'profile_picture': 5
    }
    User.load_from_csv(
        'models/seed_data/users.csv',
        column_index,
    )
    db.session.commit()


def seed_superheroes():
    """
    This function will seed the superheroes table with a few superheroes
    """

    column_index = {
        'name': 1,
        'height': 2,
        'weight': 3,
        'special_power': 4,
        'fathers_name': 5,
        'mothers_name': 5,
        'martial_status': 6,
        'main_powers': 7,
        'alive': 8,
        'race': 9
    }
    Superhero.load_from_csv(
        'models/seed_data/superheroes.csv',
        column_index,
    )
    db.session.commit()


def drop_tables():
    db.drop_all()


def create_tables():
    db.create_all()


def seed():
    logger.info('Tables are being seeded...')

    seed_superheroes()
    seed_users()

    logger.info('Seeding was successful!')


@click.command('rebuild')
@with_appcontext
def rebuild():
    drop_tables()
    create_tables()
    seed()
