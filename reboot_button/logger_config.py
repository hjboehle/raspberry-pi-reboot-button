"""module logger_config"""

import logging


def setup_file_logger(log_file_path, name="reboot_button"):
    """
    Sets up and returns a logger instance with file logging.

    Args:
        log_file (str): The path to the log file.
        name (str): The name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
