"""module log_file"""

import os
from logger_config import setup_file_logger


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
        print(f"Creating directory '{log_dir_name}' for log file if it does not exist.")
        os.makedirs(log_dir_name, exist_ok=True)
        print(f"Directory '{log_dir_name}' for log file created or already exists.")
        print(f"Appending to or creating log file '{log_file_path}'.")
        with open(log_file_path, "a", encoding='utf-8'):
            pass
        print(f"Log file '{log_file_path}' created or opened for appending.")
        return True
    except (IOError, OSError) as err:
        print(f"Failed to create or append to log file '{log_file_path}': {err}")
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
        print(
            f"System-wide log file '{os.path.join(log_dir_root, log_file_name)}' successfully set up."
        )
        setup_file_logger(os.path.join(log_dir_root, log_file_name))
        print("System-wide logger set up.")
        return {"success": True, "log_file_path": os.path.join(log_dir_root, log_file_name)}
    if append_or_create_log_file(log_dir_home, log_file_name):
        print(
            f"User-specific log file '{os.path.join(log_dir_home, log_file_name)}' successfully set up."
        )
        setup_file_logger(os.path.join(log_dir_home, log_file_name))
        print("User-specific logger set up.")
        return {"success": True, "log_file_path": os.path.join(log_dir_home, log_file_name)}
    print("Failed to set up any log file.")
    return {"success": False, "log_file_path": ""}

