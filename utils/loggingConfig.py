# app/loggerConfig.py

import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')

    # Create file handler
    fileHandler = RotatingFileHandler('app.log', maxBytes=1024*1024, backupCount=5)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    # Create console handler
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

    return logger

# Initialize the logger
logger = setup_logger()
