# logging_config.py

import logging

# setup logger
logger = logging.getLogger("signal")

# create a handler that prints log messages to the terminal
handler = logging.StreamHandler()

# add the handler to the logger
logger.addHandler(handler)

# set the logger to print messages at the INFO level
logger.setLevel(logging.INFO)
