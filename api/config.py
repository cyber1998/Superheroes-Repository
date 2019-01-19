import logging
import os
from models.settings import SQLALCHEMY_DATABASE_URI

logger = logging.getLogger(__name__)

APP_NAME = 'superheroes'
ENV = 'development'
APP_PORT = 5000
DEBUG = True
LOG_DIR = 'logs'
DEBUG_TB_INTERCEPT_REDIRECTS = False

JUNK_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'junk/')


IMAGE_UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'static/images/uploads/')


# If set to True, Flask-SQLAlchemy will track modifications of objects and
# emit signals. The default is None, which enables tracking but issues a
# warning that it will be disabled by default in the future. This requires
# extra memory and should be disabled if not needed.
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuration for the python logging module
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': logging.DEBUG,
        'handlers': ['console', 'file'],
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': logging.DEBUG,
            'formatter': 'detailed',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.DEBUG,
            'formatter': 'detailed',
            'filename':  LOG_DIR + '/' + APP_NAME.lower() + '.log',
            'mode': 'a',
            'maxBytes': 10485760,
            'backupCount': 5,
        }
    },
    'formatters': {
        'detailed': {
            'format': ('%(asctime)s %(name)-17s line:%(lineno)-4d '
                        '%(levelname)-8s %(message)s')
        }
    },
}

# Define the following variables inside the dev_config.py file
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:pass@server/db'

LOG_FILENAME = LOG_DIR + '/' + APP_NAME.lower() + '.log'
if os.path.exists(LOG_FILENAME):
    logger.debug("Log file exists - using {}".format(LOG_FILENAME))
else:
    try:
        os.makedirs(os.path.dirname(LOG_FILENAME), exist_ok=True)
    except OSError as e:
        logger.error("Unable to create log file at {}".format(LOG_FILENAME))
        logger.info("Error: {}".format(e))
    with open(LOG_FILENAME, 'w') as f:
        logger.info("Created new log file... {}".format(LOG_FILENAME))
