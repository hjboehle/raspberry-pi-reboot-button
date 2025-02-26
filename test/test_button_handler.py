"""module test_button_handler"""

import logging
import sys
from unittest import mock
import os
import threading
import time
import pytest


# Ensure the project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


# Mock RPi.GPIO module BEFORE importing button_handler
sys.modules["RPi"] = mock.Mock()
sys.modules["RPi.GPIO"] = mock.Mock()

from reboot_button.button_handler import ( # pylint: disable=wrong-import-position
    button_callback,
    monitor_button
)


@pytest.fixture(name="logger_mock")
def logger():
    """Fixture to create a logger mock."""
    return mock.Mock(spec=logging.Logger)


@pytest.fixture(name="button_pin_mock")
def button_pin():
    """Fixture to define a test GPIO pin."""
    return 17  # Example GPIO pin number


def test_button_callback(mocker, logger_mock, button_pin_mock):
    """Test the button_callback function."""
    mock_os_system = mocker.patch("os.system")

    button_callback(logger_mock, button_pin_mock)

    # Check if logger.info was called with the expected message
    logger_mock.info.assert_called_with(
        "Button pressed on GPIO '%s'. Raspberry Pi will reboot.",
        button_pin_mock
    )

    # Ensure os.system("sudo reboot") was not actually executed
    mock_os_system.assert_called_once_with("sudo reboot")

def test_monitor_button(mocker, logger_mock, button_pin_mock):
    """Test the monitor_button function with GPIO mocks."""
    gpio_mock = mock.Mock()
    mocker.patch("reboot_button.button_handler.GPIO", gpio_mock)
    mocker.patch("os.system")  # Prevents actual system calls

    gpio_mock.setmode.reset_mock()
    gpio_mock.setup.reset_mock()
    gpio_mock.add_event_detect.reset_mock()
    gpio_mock.cleanup.reset_mock()

    # Create an event to signal the loop to stop
    stop_event = threading.Event()

    # Store original sleep function
    original_sleep = time.sleep

    # Patch time.sleep to periodically check stop_event
    def stop_sleep(duration):
        if stop_event.is_set():
            raise KeyboardInterrupt  # Simulate a manual interruption
        original_sleep(duration)

    mocker.patch("time.sleep", side_effect=stop_sleep)

    # Run monitor_button in a separate thread
    thread = threading.Thread(target=monitor_button, args=(logger_mock, button_pin_mock))
    thread.start()

    # Let it run for a short time, then stop it
    original_sleep(0.5)
    stop_event.set()

    # Wait for the thread to exit
    thread.join(timeout=1)
    if thread.is_alive():
        raise RuntimeError("monitor_button thread did not terminate correctly")

    # Check if GPIO functions were called correctly
    gpio_mock.setmode.assert_called_once_with(gpio_mock.BCM)
    gpio_mock.setup.assert_called_once_with(button_pin_mock, gpio_mock.IN, pull_up_down=gpio_mock.PUD_UP)
    gpio_mock.add_event_detect.assert_called_once_with(
        button_pin_mock,
        gpio_mock.FALLING,
        callback=mocker.ANY,
        bouncetime=300
    )

    # Ensure cleanup is called
    gpio_mock.cleanup.assert_called_once()
