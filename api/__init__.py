import logging

from logging.config import dictConfig

from flask_bcrypt import Bcrypt
from flask_cors import CORS

from models import db
from api.api import api_blueprint
from utilities.helpers import ApiFlask
# from views.routes import web_blueprint

bcrypt = Bcrypt()


def create_app(config_module='config'):
    from api.config import APP_NAME

    # Setting up the app object
    app = ApiFlask(APP_NAME)

    # Import app specific configuration
    app.config.from_object(config_module)

    # Initializing the root logger
    dictConfig(app.config['LOGGING'])
    logger = logging.getLogger(__name__)
    logger.debug('Logger initialized')

    # Setting directories

    db.init_app(app)

    from models.settings.seeder import rebuild
    app.cli.add_command(rebuild)

    bcrypt.init_app(app)
    app.bcrypt = bcrypt
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register the blueprints here
    # app.register_blueprint(web_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    return app
