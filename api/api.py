import codecs
import csv
import logging
import os

from datetime import datetime

from flask import (
    abort,
    Blueprint,
    render_template,
    request,
    send_file,
)
from flask_bcrypt import Bcrypt

from models.superheroes import Superhero

from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from utilities.helpers import respond

# from listino.decorators import validate_schema

from utilities.exceptions import (
    InvalidRequestData,
    ResourceNotFound,
)

logger = logging.getLogger(__name__)
bcrypt = Bcrypt()

api_blueprint = Blueprint('api', __name__, static_url_path='static',
                          template_folder='templates')


@api_blueprint.route("/superheroes", methods=['GET', 'POST'])
@api_blueprint.route("/superheroes/<int:id_>", methods=['GET', 'PATCH', 'DELETE'])
def superheroes(id_=None):
    superhero = None
    if id_:
        superhero = Superhero.get_one(id_)

    if request.method == 'GET' :
        if id_:
            return respond(superhero.get_details(), 'Details')

        return respond(Superhero.get_all_details(), 'All superheroes')

    if request.method == 'POST':

        payload = request.get_json()

        try:
            superhero = Superhero(payload['data'])
        except InvalidRequestData as e:
            return respond(e.errors, "Superhero already exists", 400)

        return respond(superhero.get_details(), "Superhero added", 201)

    if request.method == 'PATCH':

        payload = request.get_json()

        try:
            superhero = superhero.update(payload['data'])
        except InvalidRequestData as e:
            return respond(e.errors, "Superhero already exists", 400)

        return respond(superhero, "Superhero updated")

    if request.method == 'DELETE':

        Superhero.delete_details(id_)
        return respond(None, "Superhero deleted")
