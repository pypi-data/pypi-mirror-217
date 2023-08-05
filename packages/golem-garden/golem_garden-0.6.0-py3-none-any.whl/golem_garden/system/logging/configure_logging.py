import logging
import logging.handlers
import sys
from logging.config import dictConfig

from golem_garden.system.filenames_and_paths import get_log_file_path

DEFAULT_LOGGING = {"version": 1, "disable_existing_loggers": False}

LOG_FILE_PATH = None

format_string = "[%(asctime)s.%(msecs)04d] [%(levelname)8s] [%(name)s] [%(funcName)s():%(lineno)s] [PID:%(process)d TID:%(thread)d] %(message)s"

default_logging_formatter = logging.Formatter(fmt=format_string, datefmt="%Y-%m-%dT%H:%M:%S")


def get_logging_handlers(entry_point: str = None):

    dictConfig(DEFAULT_LOGGING)

    handlers = []

    if entry_point is not None:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(default_logging_formatter)
        handlers.append(console_handler)


    file_handler = logging.FileHandler(get_log_file_path())
    file_handler.setFormatter(default_logging_formatter)
    file_handler.setLevel(logging.DEBUG)
    handlers.append(file_handler)

    return handlers

def configure_logging():
    print(f"Setting up logging  {__file__}")

    if len(logging.getLogger().handlers) == 0:
        handlers = get_logging_handlers()
        for handler in handlers:
            if not handler in logging.getLogger("").handlers:
                logging.getLogger("").handlers.append(handler)

        logging.root.setLevel(logging.DEBUG)
    else:
        logger = logging.getLogger(__name__)
        logger.info("Logging already configured")
