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


def logfile_exists(logfile) -> bool:
    """
    Check if the specified log file exists.

    Args:
        logfile (str): The path of the log file to check.

    Returns:
        bool: True if the log file exists, False otherwise.
    """
    try:
        path_exists = os.path.exists(logfile)
        logger.info("Log file %s exists", logfile)
        return path_exists
    except OSError:
        logger.error("Failed to check if log file %s exists due to an OS error.", logfile)
        return False
    except TypeError:
        logger.error("Failed to check if log file %s exists due to a type error.", logfile)
        return False
    except ValueError:
        logger.error("Failed to check if log file %s exists due to a value error.", logfile)
        return False


def directory_exists(directory) -> bool:
    """
    Check if the specified directory exists.

    Args:
        directory (str): The path of the directory to check.

    Returns:
        bool: True if the directory exists, False otherwise.
    """
    try:
        path_exists = os.path.exists(directory)
        logger.info("Directory %s exists", directory)
        return path_exists
    except OSError:
        logger.error("Failed to check if directory %s exists due to an OS error.", directory)
        return False
    except TypeError:
        logger.error("Failed to check if directory %s exists due to a type error.", directory)
        return False
    except ValueError:
        logger.error("Failed to check if directory %s exists due to a value error.", directory)
        return False


def create_directory(directory) -> bool:
    """
    Create the specified directory if it does not exist.

    Args:
        directory (str): The path of the directory to create.

    Raises:
        OSError: If the directory cannot be created.
        PermissionError: If the process does not have permission to create the directory.
        FileExistsError: If the path exists and is not a directory.
        FileNotFoundError: If a component of the path does not exist.
        NotADirectoryError: If a component of the path is not a directory.
        ValueError: If the path is an empty string.
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except OSError as err:
        logger.error("Failed to create directory because of an OS error: %s", err)
        return False
    except ValueError as err:
        logger.error(
            "Failed to create directory because the path name is an empty string: %s",
            err
        )
        return False


def initialize_log_file(log_dir, log_file) -> bool:
    """
    Initializes the file logger for the application.

    Args:
        log_dir (str): The directory to store the log file.
        log_file (str): The path of the log file.
    """
    logger.info("Initializing file logger.")
    if not logfile_exists(log_file):
        logger.info("Log file %s does not exist.", log_file)
        if not directory_exists(log_dir):
            logger.info("Directory %s for log file %s does not exist.", log_dir, log_file)
            if not create_directory(log_dir):
                logger.error("Failed to create directory %s for log file %s.", log_dir, log_file)
            else:
                logger.info("Directory %s for logfile %s created.", log_dir, log_file)
                return False
        else:
            logger.info("Directory %s for log file %s exists.", log_dir, log_file)
            return False
        return True
