"""module main"""

import os
from reboot_button.config import (
    LOG_DIR_NAME_ROOT,
    LOG_DIR_NAME_HOME,
    LOG_FILE_NAME,
    BUTTON_PIN)
from reboot_button.log_file import initialize_log_file
from reboot_button.logger_config import setup_logger
#from reboot_button.button_handler import monitor_button


def main():
    """
    Main entry point for the application.
    """
    result_initialize_log_file = initialize_log_file(
        LOG_DIR_NAME_ROOT,
        LOG_DIR_NAME_HOME,
        LOG_FILE_NAME
    )
    if not result_initialize_log_file["success"]:
        os._exit(1)
    os._exit(0)
    logger = setup_logger(result_initialize_log_file["log_file_path"])
    logger.info("Logger initialized successfully.")
    monitor_button(logger, BUTTON_PIN)


if __name__ == "__main__":
    main()
