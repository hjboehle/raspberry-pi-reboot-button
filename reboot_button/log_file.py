"""module log_file"""

import logging
import os


def configure_stdout_logger(name="stdout_logger"):
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


def is_log_file_writable(log_file_path) -> bool:
    """
    Check if the file is writable.

    Args:
        log_file_path (str): The path of the file to check.

    Returns:
        bool: True if the log file is writable, False otherwise.
    """
    if not os.path.exists(log_file_path):
        return False
    try:
        with open(log_file_path, 'a', encoding='utf-8'):
            pass
        return True
    except (IOError, OSError):
        return False


def is_log_path_exists(log_path_name) -> bool:
    """
    Check if the log directory exists.

    Args:
        log_dir_name (str): The directory to check.

    Returns:
        bool: True if the log directory exists, False otherwise.
    """
    try:
        return os.path.exists(log_path_name)
    except (IOError, OSError):
        return False


def is_create_directory(log_dir_name) -> bool:
    """
    Create the log directory.

    Args:
        log_dir_name (str): The directory to create.

    Returns:
        bool: True if the log directory is created, False otherwise.
    """
    try:
        os.makedirs(log_dir_name)
        return True
    except (IOError, OSError):
        return False


def check_and_create_log_file(log_dir_name, log_file_name):
    """
    Check if the log file exists and is writable, or create it.
    
    Args:
        log_dir_name (str): The directory to store the log file.
        log_file_name (str): The name of the log file.

    Returns:
        bool: True if the log file exists and is writable, False otherwise.
    """
    log_file_path = os.path.join(log_dir_name, log_file_name)
    if is_log_path_exists(log_file_path):
        logger.info("Log file %s exists.", log_file_path)
        if is_log_file_writable(log_file_path):
            logger.info("Log file %s is writable.", log_file_path)
            return True
        logger.error("Log file %s is not writable.", log_file_path)
        return False
    logger.info("Log file %s does not exist.", log_file_path)
    if not is_log_path_exists(log_dir_name):
        logger.info(
            "Directory %s for log file %s does not exist.",
            log_dir_name,
            log_file_name
        )
        if not is_create_directory(log_dir_name):
            logger.error(
                "Failed to create directory %s for log file %s.",
                log_dir_name,
                log_file_name
            )
            return False
        logger.info("Directory %s for log file %s created.", log_dir_name, log_file_name)
    try:
        with open(log_file_path, 'w', encoding='utf-8'):
            pass
        logger.info("Log file %s created.", log_file_path)
        return True
    except IOError as err:
        logger.error("Failed to create log file %s: %s", log_file_path, err)
        return False


def initialize_log_file(log_dir_root, log_dir_home, log_file_name) -> dict:
    """
    Initializes the file logger for the application.

    Args:
        log_dir_root (str): The root directory for the log file.
        log_dir_home (str): The home directory for the log file.
        log_file_name (str): The name of the log file.
    
    Returns: True if the log file is initialized successfully, False otherwise.
    """
    logger.info("Initializing file logger.")
    if check_and_create_log_file(log_dir_root, log_file_name):
        logger.info(
            "System-wide log file '%s' successfully initialized.",
            os.path.join(log_dir_root, log_file_name)
        )
        return {"success": True, "log_file_path": os.path.join(log_dir_root, log_file_name)}
    if check_and_create_log_file(log_dir_home, log_file_name):
        logger.info(
            "User-specific log file '%s' successfully initialized.",
            os.path.join(log_dir_home, log_file_name)
        )
        return {"success": True, "log_file_path": os.path.join(log_dir_home, log_file_name)}
    logger.error("Failed to initialize log file.")
    return {"success": False, "log_file_path": ""}
