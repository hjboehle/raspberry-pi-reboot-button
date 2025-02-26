"""module log_file"""

import logging
import os
from reboot_button.logger_config import setup_file_logger


def configure_stdout_logger(name="stdout_logger") -> logging.Logger:
    """
    Configures a logger to write to standard output.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    local_logger = logging.getLogger(name)
    if not local_logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        local_logger.addHandler(handler)
        local_logger.setLevel(logging.INFO)
    return local_logger


logger = configure_stdout_logger()
logger.info("Logging initialized for standard out.")


def append_or_create_log_file(log_dir_name, log_file_name) -> bool:
    """
    Append to the log file or create it and its directory if it does not exist.

    Args:
        log_dir_name (str): The directory to create.
        log_file_name (str): The name of the log file to create.

    Returns:
        bool: True if the log file is created or already exists, False otherwise.
    """
    log_file_path = os.path.join(log_dir_name, log_file_name)
    try:
        logger.info("Creating directory '%s' for log file if it does not exist.", log_dir_name)
        os.makedirs(log_dir_name, exist_ok=True)
        logger.info("Directory '%s' for log file created or already exists.", log_dir_name)
        logger.info("Appending to or creating log file '%s'.", log_file_path)
        with open(log_file_path, "a", encoding='utf-8'):
            pass
        logger.info("Log file '%s' created or opened for appending.", log_file_path)
        return True
    except (IOError, OSError) as err:
        logger.error("Failed to create or append to log file '%s': %s", log_file_path, err)
        return False


def setup_log_file(log_dir_root, log_dir_home, log_file_name) -> dict:
    """
    Sets up the log file for the application, either by binding to an existing one or creating 
    a new one and writes a setup message to the log file.

    Args:
        log_dir_root (str): The root directory for the log file.
        log_dir_home (str): The home directory for the log file.
        log_file_name (str): The name of the log file.
    
    Returns:
        dict: A dictionary containing the success status and the log file path.
    """
    if append_or_create_log_file(log_dir_root, log_file_name):
        logger.info(
            "System-wide log file '%s' successfully set up.",
            os.path.join(log_dir_root, log_file_name)
        )
        setup_file_logger(os.path.join(log_dir_root, log_file_name))
        logger.info("System-wide logger set up.")
        return {"success": True, "log_file_path": os.path.join(log_dir_root, log_file_name)}
    if append_or_create_log_file(log_dir_home, log_file_name):
        logger.info(
            "User-specific log file '%s' successfully set up.",
            os.path.join(log_dir_home, log_file_name)
        )
        setup_file_logger(os.path.join(log_dir_home, log_file_name))
        logger.info("User-specific logger set up.")
        return {"success": True, "log_file_path": os.path.join(log_dir_home, log_file_name)}
    logger.error("Failed to set up log file.")
    return {"success": False, "log_file_path": ""}
