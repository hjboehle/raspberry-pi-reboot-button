"""module button_handler"""

import time
import logging
import os
from RPi import GPIO
from systemd.journal import JournaldLogHandler


logger = logging.getLogger("reboot_button")
logger.addHandler(JournaldLogHandler())
logger.setLevel(logging.INFO)
logger.info("Logging initialized for systemd journal.")


BUTTON_PIN = 17


def button_callback(channel):
    """
    Callback function for the button press event.

    Logs a message and initiates a system reboot when the button is pressed.

    Args:
        channel (int): The GPIO pin number that triggered the callback.
    """
    logger.info("Button pressed on GPIO '%s'. Raspberry Pi will reboot.", channel)
    os.system("sudo reboot")


def monitor_button():
    """
    Monitors the button press and sets up GPIO configurations.

    Initializes GPIO mode, sets up the button pin, and adds event detection 
    for falling edge signals. The function continuously monitors the GPIO 
    pin for changes and logs relevant information or errors.

    Raises:
        GPIO.InvalidChannelException: Raised when an invalid GPIO channel is specified.
        RuntimeError: Raised when there is a runtime issue adding edge detection.
        KeyboardInterrupt: Raised when the program is manually interrupted.
        ValueError: Raised when an invalid GPIO mode or setup parameter is provided.
    """
    try:
        logging.info("Set GPIO mode.")
        GPIO.setmode(GPIO.BCM)
        logging.info("Configuration of the pin as an input pin with pull-up resistor.")
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        logging.info("Add event monitoring.")
        GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

        while True:
            time.sleep(1)
    except ValueError as err:
        logging.error("Invalid GPIO configuration: %s", err)
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
    except RuntimeError as err:
        logging.error("Runtime error occurred: %s", err)
    finally:
        GPIO.cleanup()
        logging.info("GPIO cleanup done.")


if __name__ == "__main__":
    monitor_button()
