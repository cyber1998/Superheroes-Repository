import logging

import click
from flask.cli import with_appcontext
from utilities.helpers import get_rows_from_csv
from models import db
from models.superheroes import Superhero
from models.users import User

logger = logging.getLogger('Seed Logger')


def seed_users():
    """
    This function will seed the superheroes table with a few users
    """

    rows = get_rows_from_csv('models/seed_data/users.csv')
    for row in rows:
        data = {
            'name': row[1],
            'username': row[2],
            'password': row[3],
            'favourite_superhero': row[4],
            'profile_picture': row[5]
        }
        db.session.add(User(data))
    db.session.commit()


def seed_superheroes():
    """
    This function will seed the superheroes table with a few superheroes
    """
    rows = get_rows_from_csv('models/seed_data/superheroes.csv', header=True, quoting=True)
    for row in rows:
        data = {
            'name': row[1],
            'height': row[2],
            'weight': row[3],
            'special_power': row[4],
            'fathers_name': row[5],
            'mothers_name': row[6],
            'martial_status': row[7],
            'main_powers': row[8].strip().split(','),
            'alive': row[9],
            'race': row[10]
        }
        db.session.add(Superhero(data))
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
