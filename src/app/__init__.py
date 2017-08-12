''' Main application '''
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask
from flask_socketio import SocketIO
from mongoengine import register_connection
from .auth import authenticate, identity
from flask_jwt import JWT

SOCKETIO = SocketIO()

def create_app(app_mode='DEVEL'):
    ''' Create flask app and configure it '''
    if app_mode == '':
        app_mode = os.environ.get('APP_MODE', 'DEVEL')
    # create an application
    application = Flask(__name__)
    # set logging
    configure_logging(app_mode, application)
    # configure application
    configure(application)
    # register blueprints
    from .main import main as main_blueprint
    application.register_blueprint(main_blueprint)
    # init socketio
    SOCKETIO.init_app(application)
    # init mongo
    register_connection(
        alias="default",
        name=application.config["MONGO_DBNAME"],
        host=application.config["MONGO_HOST"],
        port=application.config["MONGO_PORT"])
    return application


def configure_logging(app_mode, application):
    ''' Configure logging '''
    log_handler = None
    if app_mode == 'DEVEL':
        # create console handler
        log_handler = logging.StreamHandler()
    elif app_mode == 'PROD':
        # create file time rotating handler
        log_handler = TimedRotatingFileHandler(
            filename=os.environ.get('APP_LOG_FILENAME', 'app.log'),
            when='D',
            backupCount=5,
            encoding='UTF-8'
        )
    if log_handler is None:
        return
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(logging.Formatter(
        fmt='%(asctime)s %(name)-10s %(levelname)-7s %(message)s',
        datefmt='%H:%M:%S'))
    # get root logger
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.DEBUG)
    application.logger.addHandler(log_handler)
    application.logger.setLevel(logging.DEBUG)
    return


def configure(application):
    """
    Configure from env
    """
    logger = logging.getLogger()
    filename = os.environ.get("APP_CONFIG_FILENAME","")
    if filename == "":
        filename = os.path.join(os.getcwd(), "config", "development.py")
    logger.info("Configuring from: " + filename)
    application.config.from_pyfile(filename)
    application.debug = True
    return
