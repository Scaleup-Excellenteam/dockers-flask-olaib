import os
import logging
import datetime
from flask import Flask
from flask.cli import load_dotenv
from logging.handlers import TimedRotatingFileHandler

load_dotenv()

CODES_FOLDER = 'codes'
OUTPUT_FOLDER = 'outputs'
FILE = 'file'
EXTENSION_SEPARATOR = '.'
app = Flask(__name__)
LOG_DIR = os.path.join(app.root_path, 'logs')
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
BACKUP_COUNT = 5
app.config['CODES_FOLDER'] = os.path.join(app.root_path, CODES_FOLDER)
app.config['OUTPUT_FOLDER'] = os.path.join(app.root_path, OUTPUT_FOLDER)
MESSAGES = {
    'UNSELECTED_FILE': 'No file selected',
    'FILE_MISSING': 'Bad request: file is missing',
    'FILE_NOT_SUPPORTED': 'file type is not supported',
    'FILE-RECEIVED': 'File received successfully',
    'NOT_FOUND': 'Not found',
    'ERROR_OCCURRED': 'An error occurred while processing the slide: ',
    'NO_CODE_FILES': 'No code files found',
}

CODES_DIR_NAME = 'codes'
EXECUTOR_EXTENSIONS = ['java', 'py', 'dart']
EXECUTOR_PORTS = {'java': 5002, 'py': 5001, 'dart': 5003}
EXECUTOR_URLS = {
    name: f'http://localhost:{port}/execute'
    for name, port in zip(EXECUTOR_EXTENSIONS, EXECUTOR_PORTS.values())
}


def setup_logger(logger_name, log_dir):
    """
    Setup a logger for the application according to the given logger name and log directory
    :param logger_name: dir name
    :param log_dir: log dir path
    :return: logger object that can save last 5 days of logs
    """
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file_name = f"{current_date}.log"
    log_file_path = os.path.join(log_dir, log_file_name)

    # Create the logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Create a timed rotating file handler for the log
    file_handler = TimedRotatingFileHandler(log_file_path, when="midnight", backupCount=BACKUP_COUNT)
    file_handler.setLevel(logging.INFO)

    # Set the log format for the file handler
    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger


os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(app.config['CODES_FOLDER'], exist_ok=True)

log = setup_logger("log", LOG_DIR)
