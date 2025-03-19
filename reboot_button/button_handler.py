"""module button_handler"""

import time
import sys
import logging
import os
from RPi import GPIO


def reboot_system(logger) -> bool:
    """
    Initiates a system reboot using os.execlp.

    Args:
        logger (Logger): The logger object to log messages.

    Returns:
        bool: True if reboot command was executed (or attempted), False otherwise.
    """
    try:
        os.execlp("sudo", "sudo", "reboot")
        # This line should never be reached if reboot command is successful
        return True  # Should never be reached
    except FileNotFoundError as err:
        logger.error("Command not found: sudo")
        logger.error(
            "Error Type: '%s', Message: '%s'",
            type(err).__name__,
            str(err)
        )
        return False
    except PermissionError as err:
        logger.error(f"Permission error occurred during reboot execution: {err}")
        logger.error(
            "Error Type: '%s', Message: '%s'",
            type(err).__name__,
            str(err)
        )
        return False
    except OSError as err:
        logger.error(f"OS error occurred during reboot execution: {err}")
        logger.error(
            "Error Type: '%s', Message: '%s'",
            type(err).__name__,
            str(err)
        )
        return False


def is_system_alive(logger) -> bool:
    """
    Checks if the system is still responsive by attempting to run /bin/true.

    Args:
        logger (Logger): The logger object to log messages.

    Returns:
        bool: True if /bin/true runs successfully, False otherwise.
    """
    try:
        os.execlp("/bin/true", "/bin/true")
        logger.info("System is still up and running.")
        return True  # Should never be reached
    except OSError:
        logger.error("System is likely down or unresponsive.")
        return False


def button_callback(logger, channel) -> bool:
    """
    Callback function for the button press event.

    Logs a message and attempts to reboot the system.
    If the reboot fails, it checks if the system is responsive and logs accordingly.

    Args:
        logger (Logger): The logger object to log messages.
        channel (int): The GPIO pin number that triggered the callback.

    Returns:
        bool: True if reboot was initiated (or attempted), False if an error occurred.
    """
    logger.info("Button pressed on GPIO '%s'. Attempting to reboot.", channel)

    reboot_result = reboot_system(logger)
    if reboot_result:
        # The system is rebooting. This should not be reached.
        return True

    logger.error("Maybe a password is required for sudo.")
    logger.info("Waiting for a second and trying to run /bin/true.")
    time.sleep(1)

    if is_system_alive(logger):
        logger.error(
            "Test with '/bin/true' successful. System is still up and waiting for " \
                "password input for sudo."
            )
    else:
        logger.error("Ping failed, the system is likely down or unresponsive.")
        logger.error("Assuming the system is rebooting.")
    return False


def monitor_button(logger, pin: int) -> None:
    """
    Monitors the button press and sets up GPIO configurations.

    Initializes GPIO mode, configures the specified pin as an input with
    a pull-up resistor, and adds event detection for falling edge signals.
    The function continuously monitors the GPIO pin for changes.

    Args:
        logger (Logger): The logger object to log messages.
        pin (int): The GPIO pin number to monitor.

    Raises:
        GPIO.InvalidChannelException: Raised when an invalid GPIO channel is specified.
        RuntimeError: Raised when there is a runtime issue adding edge detection.
        ValueError: Raised when an invalid GPIO mode or setup parameter is provided.
    """
    bouncetime = 500
    event_added = False
    try:
        logger.debug("Set GPIO mode.")
        GPIO.setmode(GPIO.BCM)
        logger.debug("GPIO mode set successfully.")
        logger.debug(
            "Configuration of the pin as an input pin with pull-up resistor."
        )
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        logger.debug("GPIO setup done.")
        logger.debug("Add event monitoring.")
        logger.info("GPIO Version is '%s', pin is '%i'", GPIO.VERSION, pin)
        GPIO.add_event_detect(
            pin,
            GPIO.FALLING,
            callback=lambda channel: button_callback(logger, channel),
            bouncetime=bouncetime
        )
        event_added = True
        logger.debug("Event detection added.")
        logger.info("Button monitoring started. Waiting for events...")
        # Keep the script running to detect button presses.
        while True:
            time.sleep(1)

    except ValueError as err:
        logger.error("Invalid GPIO configuration: %s", err)
    except KeyError as err:
        logger.error("Missing key in Result: %s", err)
    except TypeError as err:
        logger.error("Type Error: %s", err)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user.")
    except RuntimeError as err:
        logger.error("Runtime error occurred: %s", err)
        logger.error(
            "Error Type: '%s', Message: '%s'",
            type(err).__name__,
            str(err)
        )
    except GPIO.InvalidChannelException as err:
        logger.error("Invalid GPIO channel specified: %s", err)
    except SystemExit:
        logger.info("Program exited by system.")
    finally:
        if event_added:
            GPIO.remove_event_detect(pin)
            logger.debug("Event detection removed.")
        logger.debug("GPIO cleanup done.")
        GPIO.cleanup()


def main():
    """
    Main entry point for this module.
    """
    logging.info("this script is not meant to be run directly")
    sys.exit(1)


if __name__ == "__main__":
    main()
