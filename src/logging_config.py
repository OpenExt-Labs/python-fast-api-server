import logging
from logging.handlers import TimedRotatingFileHandler
import os

# Ensure the logs directory exists
os.makedirs("src/logs", exist_ok=True)

# Project name
project_name = "tts_api"

# Create a logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)  # Set the lowest level to capture all log messages

# Helper function to create a timed rotating file handler
def create_timed_rotating_handler(log_dir, project_name, log_level_name, level):
    filename = f"{log_dir}/{project_name}-{log_level_name}.log"
    handler = TimedRotatingFileHandler(
        filename, when="midnight", interval=1, backupCount=5
    )
    handler.setLevel(level)
    handler.suffix = "%Y-%m-%d"
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    return handler

# Log directory
log_dir = "src/logs"

# Create handlers for different log levels
info_handler = create_timed_rotating_handler(log_dir, project_name, "info", logging.INFO)
debug_handler = create_timed_rotating_handler(log_dir, project_name, "debug", logging.DEBUG)
error_handler = create_timed_rotating_handler(log_dir, project_name, "error", logging.ERROR)


# Add handlers to the logger
logger.addHandler(info_handler)
logger.addHandler(debug_handler)
logger.addHandler(error_handler)
