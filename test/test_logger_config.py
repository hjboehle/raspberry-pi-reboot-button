"""module test_logger_config"""

import logging
import pytest
from reboot_button.logger_config import setup_file_logger


@pytest.fixture(name="log_file")
def log_file_path(tmp_path):
    """
    Generates the file path for the test log file.

    Args:
        tmp_path (pathlib.Path): The temporary directory path provided by pytest.

    Returns:
        pathlib.Path: The complete file path for the test log file.
    """
    return tmp_path / "test_log.log"


def test_setup_file_logger_creates_logger(log_file):
    """
    Test that setup_file_logger creates a logger instance.
    """
    logger = setup_file_logger(log_file)
    assert isinstance(logger, logging.Logger), "Logger not created."
    assert logger.name == "reboot_button", "Logger name not set correctly."


def test_setup_file_logger_creates_file_handler(log_file):
    """
    Test that setup_file_logger creates a file handler.
    """
    logger = setup_file_logger(log_file)
    handlers = logger.handlers
    assert len(handlers) == 1, "No handlers created."
    assert isinstance(handlers[0], logging.FileHandler), "Handler not a FileHandler."
    assert handlers[0].baseFilename == str(log_file), "File path not set correctly."


def test_setup_file_logger_uses_correct_formatter(log_file):
    """
    Test that setup_file_logger uses the correct formatter
    """
    logger = setup_file_logger(log_file)
    formatter = logger.handlers[0].formatter
    test_record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=0,
        msg="test",
        args=(),
        exc_info=None
    )
    formatted_message = formatter.format(test_record)
    expected_message = f"{test_record.asctime} - {test_record.levelname} - {test_record.msg}"
    assert formatted_message == expected_message, "Formatter format not set correctly."


def test_setup_file_logger_logs_info_level(log_file):
    """
    Test that setup_file_logger logs at the INFO level.
    """
    logger = setup_file_logger(log_file)
    assert logger.level == logging.INFO, "Logger level not set to INFO."


def test_setup_file_logger_logs_messages(log_file):
    """
    Test that setup_file_logger logs messages to the file.
    """
    logger = setup_file_logger(log_file)
    test_message = "This is a test log message."
    logger.info(test_message)
    with open(log_file, "r", encoding="utf-8") as tested_log_file:
        log_contents = tested_log_file.read()
    assert test_message in log_contents
