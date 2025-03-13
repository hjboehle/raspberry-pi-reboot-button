"""module test_button_handler.py"""

import logging
import os
from unittest.mock import patch, Mock
import pytest

# Import der Modul um den Import Fehler zu beheben.
import sys
sys.modules['RPi'] = Mock()
sys.modules['RPi.GPIO'] = Mock()

from reboot_button.button_handler import (
    reboot_system,
    is_system_alive,
    button_callback,
    monitor_button
)


@pytest.fixture
def mock_logger():
    """Fixture to create a mock logger."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    return logger


def test_reboot_system_success(mock_logger):
    """Test reboot_system with successful os.execlp call."""
    with patch("reboot_button.button_handler.os.execlp") as mock_execlp:
        mock_execlp.return_value = None
        result = reboot_system(mock_logger)
        mock_execlp.assert_called_once_with("sudo", "sudo", "reboot")
        assert result is True


def test_reboot_system_file_not_found(mock_logger):
    """Test reboot_system with FileNotFoundError."""
    with patch("reboot_button.button_handler.os.execlp") as mock_execlp:
        mock_execlp.side_effect = FileNotFoundError
        result = reboot_system(mock_logger)
        assert result is False


def test_reboot_system_permission_error(mock_logger):
    """Test reboot_system with PermissionError."""
    with patch("reboot_button.button_handler.os.execlp") as mock_execlp:
        mock_execlp.side_effect = PermissionError
        result = reboot_system(mock_logger)
        assert result is False


def test_reboot_system_os_error(mock_logger):
    """Test reboot_system with OSError."""
    with patch("reboot_button.button_handler.os.execlp") as mock_execlp:
        mock_execlp.side_effect = OSError
        result = reboot_system(mock_logger)
        assert result is False


def test_is_system_alive_success(mock_logger):
    """Test is_system_alive with successful os.execlp call."""
    with patch("reboot_button.button_handler.os.execlp") as mock_execlp:
        mock_execlp.return_value = None
        result = is_system_alive(mock_logger)
        mock_execlp.assert_called_once_with("/bin/true", "/bin/true")
        assert result is True


def test_is_system_alive_os_error(mock_logger):
    """Test is_system_alive with OSError."""
    with patch("reboot_button.button_handler.os.execlp") as mock_execlp:
        mock_execlp.side_effect = OSError
        result = is_system_alive(mock_logger)
        assert result is False


@patch("reboot_button.button_handler.time.sleep")
@patch("reboot_button.button_handler.is_system_alive")
@patch("reboot_button.button_handler.reboot_system")
def test_button_callback_reboot_success(
    mock_reboot_system, mock_is_system_alive, mock_sleep, mock_logger
):
    """Test button_callback with successful reboot_system."""
    mock_reboot_system.return_value = True
    result = button_callback(mock_logger, 17)
    mock_reboot_system.assert_called_once_with(mock_logger)
    mock_is_system_alive.assert_not_called()
    mock_sleep.assert_not_called()
    assert result is True


@patch("reboot_button.button_handler.time.sleep")
@patch("reboot_button.button_handler.is_system_alive")
@patch("reboot_button.button_handler.reboot_system")
def test_button_callback_reboot_failed_system_alive(
    mock_reboot_system, mock_is_system_alive, mock_sleep, mock_logger
):
    """Test button_callback with failed reboot and system alive."""
    mock_reboot_system.return_value = False
    mock_is_system_alive.return_value = True
    result = button_callback(mock_logger, 17)
    mock_reboot_system.assert_called_once_with(mock_logger)
    mock_is_system_alive.assert_called_once_with(mock_logger)
    mock_sleep.assert_called_once_with(1)
    assert result is False


@patch("reboot_button.button_handler.time.sleep")
@patch("reboot_button.button_handler.is_system_alive")
@patch("reboot_button.button_handler.reboot_system")
def test_button_callback_reboot_failed_system_dead(
    mock_reboot_system, mock_is_system_alive, mock_sleep, mock_logger
):
    """Test button_callback with failed reboot and system dead."""
    mock_reboot_system.return_value = False
    mock_is_system_alive.return_value = False
    result = button_callback(mock_logger, 17)
    mock_reboot_system.assert_called_once_with(mock_logger)
    mock_is_system_alive.assert_called_once_with(mock_logger)
    mock_sleep.assert_called_once_with(1)
    assert result is False


@patch("reboot_button.button_handler.GPIO")
@patch("reboot_button.button_handler.time.sleep")
def test_monitor_button(mock_time_sleep, mock_gpio, mock_logger):
    """
    Test case for the monitor_button function.

    Verifies that monitor_button correctly configures GPIO and adds event detection.
    """

    mock_gpio.setmode = Mock()
    mock_gpio.setup = Mock()
    mock_gpio.add_event_detect = Mock()

    # Ersetze GPIO.FALLING, damit der Test auf allen Systemen läuft
    setattr(mock_gpio, 'FALLING', 1)

    mock_callback = Mock()
    mock_gpio.add_event_detect.side_effect = lambda pin, edge, callback, bouncetime: mock_callback(callback)

    monitor_button(mock_logger, 17)
    mock_gpio.setmode.assert_called_once_with(mock_gpio.BCM)
    mock_gpio.setup.assert_called_once_with(17, mock_gpio.IN, pull_up_down=mock_gpio.PUD_UP)
    mock_gpio.add_event_detect.assert_called_once()
    mock_callback.assert_called_once()
    mock_callback.call_args[0][0]()
