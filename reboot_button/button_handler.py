"""module button_handler"""

import time
import sys
import logging
import subprocess
from RPi import GPIO
from reboot_button.config import (
    SUCCESS_KEY,
    PROCESS_KEY,
    ERROR_TYPE_KEY,
    ERROR_MESSAGE_KEY,
    EXCEPTION_KEY,
)


def run_subprocess_command(logger, command) -> dict:
    """
    Runs a subprocess command and returns the process or error details.

    Args:
        logger (logging.Logger): The logger object for logging.
        command (list): The command to run as a list of strings.

    Returns:
        dict: A dictionary containing either the successful process or error details.
              - {"success": True, "process": subprocess.Popen} 
                on success.
              - {"success": False, "error_type": str, "error_message": str,"exception": exception}
                on failure.
    """
    logger.debug(f"Starting subprocess with command: {command}")
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return {SUCCESS_KEY: True, PROCESS_KEY: process}
    except FileNotFoundError as err:
        logger.error(f"Command not found: {command}")
        return {
            SUCCESS_KEY: False,
            ERROR_TYPE_KEY: type(err).__name__,
            ERROR_MESSAGE_KEY: str(err),
            EXCEPTION_KEY: err
        }
    except OSError as err:
        logger.error(f"OS error occurred during subprocess execution: {err}")
        return {
            SUCCESS_KEY: False,
            ERROR_TYPE_KEY: type(err).__name__,
            ERROR_MESSAGE_KEY: str(err),
            EXCEPTION_KEY: err
        }


def button_callback(logger, channel):
    """
    Callback function for the button press event.

    Logs a message and initiates a system reboot using subprocess.
    The reboot process is cancelled if the ping is successful, indicating
    that the system is still available.

    Args:
        logger (Logger): The logger object to log messages.
        channel (int): The GPIO pin number that triggered the callback.
    """
    logger.info("Button pressed on GPIO '%s'. Raspberry Pi will reboot.", channel)
    reboot_process = None
    ping_process = None
    try:
        # Starte den Reboot-Prozess im Hintergrund.
        reboot_result = run_subprocess_command(logger, ["sudo", "reboot"])
        if not reboot_result[SUCCESS_KEY]:
            logger.error(
                "Reboot process could not be started. Exiting function. " \
                    "Error Type: '%s', Message: '%s'",
                reboot_result[ERROR_TYPE_KEY],
                reboot_result[ERROR_MESSAGE_KEY]
            )
            return
        reboot_process = reboot_result[PROCESS_KEY]
        logger.debug("Reboot process started with PID: %s", reboot_process.pid)

        # Warte kurz, damit das System etwas Zeit hat, mit dem Reboot zu beginnen.
        time.sleep(1)

        # Versuche zu pingen, um zu sehen, ob das System noch erreichbar ist.
        ping_result = run_subprocess_command(logger, ["ping", "-c", "1", "-W", "1", "localhost"])

        if not ping_result[SUCCESS_KEY]:
            logger.error(
                "Ping process could not be started. Assuming reboot is in progress. " \
                    "Error Type: '%s', Message: '%s'",
                ping_result[ERROR_TYPE_KEY],
                ping_result[ERROR_MESSAGE_KEY]
            )
            return
        ping_process = ping_result[PROCESS_KEY]
        with ping_process:
            ping_process.wait()
            ping_exit_code = ping_process.returncode
            logger.debug("Ping process finished with exit code: %s", ping_exit_code)

        if ping_exit_code == 0:
            # Ping erfolgreich, System ist noch erreichbar.
            logger.error("Reboot failed: System still available. Cancelling reboot process.")

            # Versuche den Reboot-Prozess zu beenden.
            try:
                reboot_process.terminate()
                logger.debug("Reboot process terminated.")
                reboot_process.wait(timeout=5)  # Warte bis der Prozess beendet ist oder Time out
                logger.debug("Reboot process terminated successfully.")
            except subprocess.TimeoutExpired:
                logger.error(
                    "Failed to terminate the reboot process in time. Will kill process now."
                )
                reboot_process.kill()
                logger.debug("Reboot process killed.")

        else:
            logger.info("Ping failed, assuming reboot is in progress.")

    except ValueError as err:
        logger.error("Invalid value provided: %s", err)
    finally:
        if reboot_process and reboot_process.poll() is None:
            reboot_process.kill()
            logger.debug("Reboot process killed during exception handling or finalization")
        if ping_process and ping_process.poll() is None:
            ping_process.kill()
            logger.debug("Ping process killed during exception handling or finalization")


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
        logger.debug("Set GPIO mode.")
        GPIO.setmode(GPIO.BCM)
        logger.debug("Configuration of the pin as an input pin with pull-up resistor.")
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        logger.debug("Add event monitoring.")
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
    except SystemExit:
        logger.info("Program exited by system.")
    finally:
        GPIO.cleanup()
        logger.debug("GPIO cleanup done.")


def main():
    """
    Main entry point for this module.
    """
    logging.info("this script is not meant to be run directly")
    sys.exit(1)

if __name__ == "__main__":
    main()
