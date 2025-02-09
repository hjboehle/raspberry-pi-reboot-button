"""module main"""

from reboot_button.config import LOG_DIR, LOG_FILE, BUTTON_PIN
from reboot_button.log_file import initialize_log_file
from reboot_button.logger_config import setup_logger
from reboot_button.button_handler import monitor_button


def main():
    """
    Main entry point for the application.
    """
    if not initialize_log_file(LOG_DIR, LOG_FILE):
        raise OSError("Failed to initialize log file")
    logger = setup_logger(LOG_FILE)
    logger.info("Logger initialized successfully.")
    monitor_button(logger, BUTTON_PIN)


if __name__ == "__main__":
    if not initialize_log_file(LOG_DIR, LOG_FILE):
        raise OSError("Failed to initialize log file")
    main_guard_logger = setup_logger(LOG_FILE)
    main_guard_logger.info("Logger initialized successfully.")
    monitor_button(main_guard_logger, BUTTON_PIN)
