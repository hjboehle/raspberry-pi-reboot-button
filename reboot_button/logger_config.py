"""moduule logger_config"""

import logging
import os


LOG_DIR = ".log/reboot_button"
LOG_FILE = os.path.join(LOG_DIR, "reboot_button.log")


def setup_logger(name="reboot_button"):
    """
    Sets up and returns a logger instance with file logging.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.FileHandler(LOG_FILE)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
