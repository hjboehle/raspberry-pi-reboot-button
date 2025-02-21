"""module main"""

import sys
from reboot_button.config import (
    LOG_DIR_NAME_ROOT,
    LOG_DIR_NAME_HOME,
    LOG_FILE_NAME,
    BUTTON_PIN
)
from reboot_button.log_file import setup_log_file
from reboot_button.logger_config import setup_file_logger
from reboot_button.button_handler import monitor_button


def main():
    """
    Main entry point for the application.
    """
    result_setup_log_file = setup_log_file(
        LOG_DIR_NAME_ROOT,
        LOG_DIR_NAME_HOME,
        LOG_FILE_NAME
    )
    if not result_setup_log_file["success"]:
        sys.exit(1)
    logger = setup_file_logger(result_setup_log_file["log_file_path"])
    logger.info("File logger initialized successfully.")
    monitor_button(logger, BUTTON_PIN)


if __name__ == "__main__":
    main()
