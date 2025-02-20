"""module test_logger_config"""

import logging
import pytest
from reboot_button.logger_config import setup_file_logger


@pytest.fixture
def reset_logger():
    """
    Fixture to reset the logger before each test.
    """
    logger = logging.getLogger("reboot_button")
    logger.handlers = []
    yield
    logger.handlers = []


def test_setup_file_logger_creates_file_handler(mocker):
    """
    Test that setup_file_logger adds a FileHandler to the logger.

    - Mocks `logging.FileHandler` to avoid writing to a real file.
    - Ensures that `setup_file_logger` creates a FileHandler with the correct log file.
    """
    # Patch both FileHandler and getLogger to monitor their behavior
    mock_file_handler = mocker.patch("logging.FileHandler")
    mock_get_logger = mocker.patch("logging.getLogger")

    # Create the logger mock
    mock_logger = mock_get_logger.return_value
    mock_logger.hasHandlers.return_value = False  # Ensure no handlers are present

    # add debugging information
    setup_file_logger()

    # Check if logging.FileHandler was created with the correct file
    mock_file_handler.assert_called_once_with(LOG_FILE)

    # Ensure that the handler was added to the logger
    mock_logger.addHandler.assert_called_once_with(mock_file_handler.return_value)


def test_setup_file_logger_does_not_add_handler_if_exists(mocker):
    """
    Test that setup_file_logger does not add a FileHandler if one already exists.
    """
    # Patch both FileHandler and getLogger to monitor their behavior
    mock_file_handler = mocker.patch("logging.FileHandler")
    mock_get_logger = mocker.patch("logging.getLogger")

    # Erstelle den Logger mock
    mock_logger = mock_get_logger.return_value
    mock_logger.hasHandlers.return_value = True  # Simulate existing handlers

    # Debugging-Informationen hinzufügen
    print("Calling setup_file_logger()")
    setup_file_logger()
    print("setup_file_logger() called")

    # Debugging-Informationen hinzufügen
    print(f"mock_file_handler.call_count: {mock_file_handler.call_count}")
    print(f"mock_file_handler.call_args_list: {mock_file_handler.call_args_list}")

    # Prüfen, ob logging.FileHandler nicht erstellt wurde
    mock_file_handler.assert_not_called()

    # Sicherstellen, dass kein neuer Handler zum Logger hinzugefügt wurde
    mock_logger.addHandler.assert_not_called()
