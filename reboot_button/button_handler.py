"""module button_handler"""

import time
import os
import sys
import logging
from RPi import GPIO


def button_callback(logger, channel):
    """
    Callback function for the button press event.

    Logs a message and initiates a system reboot when the button is pressed.

    Args:
        logger (Logger): The logger object to log messages.
        channel (int): The GPIO pin number that triggered the callback.
    """
    logger.info("Button pressed on GPIO '%s'. Raspberry Pi will reboot.", channel)
    os.system("sudo reboot")


def monitor_button(logger, button_pin):
    """
    Monitors the button press and sets up GPIO configurations.

    Initializes GPIO mode, sets up the button pin, and adds event detection 
    for falling edge signals. The function continuously monitors the GPIO 
    pin for changes and logs relevant information or errors.

    Args:
        logger (Logger): The logger object to log messages.
        button_pin (int): The GPIO pin number to monitor.

    Raises:
        GPIO.InvalidChannelException: Raised when an invalid GPIO channel is specified.
        RuntimeError: Raised when there is a runtime issue adding edge detection.
        KeyboardInterrupt: Raised when the program is manually interrupted.
        ValueError: Raised when an invalid GPIO mode or setup parameter is provided.
    """
    try:
        logger.info("Set GPIO mode.")
        GPIO.setmode(GPIO.BCM)
        logger.info("Configuration of the pin as an input pin with pull-up resistor.")
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        logger.info("Add event monitoring.")
        GPIO.add_event_detect(
            button_pin,
            GPIO.FALLING,
            callback=lambda channel: button_callback(logger, channel),
            bouncetime=300
        )

        while True:
            time.sleep(1)
    except ValueError as err:
        logger.error("Invalid GPIO configuration: %s", err)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user.")
    except RuntimeError as err:
        logger.error("Runtime error occurred: %s", err)
    finally:
        GPIO.cleanup()
        logger.info("GPIO cleanup done.")


def main():
    """
    Main entry point for this module.
    """
    logging.info("this script is not meant to be run directly")
    sys.exit(1)

if __name__ == "__main__":
    main()
