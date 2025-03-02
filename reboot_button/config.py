"""module config.py"""

import os


# Directory paths
HOME_DIR_NAME = os.environ["HOME"]
LOG_DIR_NAME_ROOT = "/var/log/reboot_button.log"
LOG_DIR_NAME_HOME = f"{HOME_DIR_NAME}/reboot_button/log"

# Log file name
LOG_FILE_NAME = "reboot_button.log"

# GPIO pin number for the button
BUTTON_PIN = 17

# Exception handling
SUCCESS_KEY = "success"
PROCESS_KEY = "process"
ERROR_TYPE_KEY = "error_type"
ERROR_MESSAGE_KEY = "error_message"
EXCEPTION_KEY = "exception"
