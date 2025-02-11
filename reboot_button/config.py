"""module config.py"""

import os


HOME_DIR_NAME = os.environ["HOME"]
LOG_DIR_NAME_ROOT = "/var/log/reboot_button.log"
LOG_DIR_NAME_HOME = f"{HOME_DIR_NAME}/reboot_button/log"
LOG_FILE_NAME = "reboot_button.log"
BUTTON_PIN = 17
