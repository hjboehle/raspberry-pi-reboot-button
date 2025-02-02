"""module: test_button_handler"""

import time
import pytest
from reboot_button.button_handler import button_callback


def test_button_callback(mocker):
    """
    Test the button_callback function to ensure logging and system call behave as expected.
    """
    # Mock logger.info
    mock_logger_info = mocker.patch("reboot_button.button_handler.logger.info")

    # Mock os.system
    mock_os_system = mocker.patch("reboot_button.button_handler.os.system")

    # Simulate a GPIO channel
    test_channel = 17

    # Call the function
    button_callback(test_channel)

    # Assert logger.info was called with the correct arguments
    mock_logger_info.assert_called_once_with(
        "Button pressed on GPIO '%s'. Raspberry Pi will reboot.", test_channel
    )

    # Assert os.system (reboot command) was called with the correct argument
    mock_os_system.assert_called_once_with("sudo reboot")
