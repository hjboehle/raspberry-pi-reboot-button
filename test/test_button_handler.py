"""module test_button_handler.py"""

import logging
from unittest.mock import patch, Mock
import pytest


# pylint: disable=import-outside-toplevel


@pytest.fixture(name="logger")
def mock_logger():
    """Fixture to create a mock logger."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    return logger


@patch.dict('sys.modules', {'RPi': Mock(), 'RPi.GPIO': Mock()})
def test_reboot_system_success(logger):
    """Test reboot_system with successful os.execlp call."""
    # The modules can only be imported now, because RPi and RPi.GPIO are only mocked here.
    # RPi and RPi.GPIO must be mocked, because they can only be imported on a Raspberry Pi
    from reboot_button.button_handler import reboot_system

    with patch("reboot_button.button_handler.os.execlp") as mock_execlp:
        mock_execlp.return_value = None
        result = reboot_system(logger)
        mock_execlp.assert_called_once_with("sudo", "sudo", "reboot")
        assert result is True, f"Expected reboot_system to return True, but got {result}"


@patch.dict('sys.modules', {'RPi': Mock(), 'RPi.GPIO': Mock()})
def test_reboot_system_file_not_found(logger):
    """Test reboot_system with FileNotFoundError."""
    # The modules can only be imported now, because RPi and RPi.GPIO are only mocked here.
    # RPi and RPi.GPIO must be mocked, because they can only be imported on a Raspberry Pi
    from reboot_button.button_handler import reboot_system

    with patch("reboot_button.button_handler.os.execlp") as mock_execlp:
        mock_execlp.side_effect = FileNotFoundError
        result = reboot_system(logger)
        assert result is False, \
            f"Expected reboot_system to return False on FileNotFoundError, but got {result}"


@patch.dict('sys.modules', {'RPi': Mock(), 'RPi.GPIO': Mock()})
def test_reboot_system_permission_error(logger):
    """Test reboot_system with PermissionError."""
    # The modules can only be imported now, because RPi and RPi.GPIO are only mocked here.
    # RPi and RPi.GPIO must be mocked, because they can only be imported on a Raspberry Pi
    from reboot_button.button_handler import reboot_system

    with patch("reboot_button.button_handler.os.execlp") as mock_execlp:
        mock_execlp.side_effect = PermissionError
        result = reboot_system(logger)
        assert result is False, \
            f"Expected reboot_system to return False on PermissionError, but got {result}"


@patch.dict('sys.modules', {'RPi': Mock(), 'RPi.GPIO': Mock()})
def test_reboot_system_os_error(logger):
    """Test reboot_system with OSError."""
    # The modules can only be imported now, because RPi and RPi.GPIO are only mocked here.
    # RPi and RPi.GPIO must be mocked, because they can only be imported on a Raspberry Pi
    from reboot_button.button_handler import reboot_system

    with patch("reboot_button.button_handler.os.execlp") as mock_execlp:
        mock_execlp.side_effect = OSError
        result = reboot_system(logger)
        assert result is False, \
            f"Expected reboot_system to return False on OSError, but got {result}"


@patch.dict('sys.modules', {'RPi': Mock(), 'RPi.GPIO': Mock()})
def test_is_system_alive_success(logger):
    """Test is_system_alive with successful os.execlp call."""
    # The modules can only be imported now, because RPi and RPi.GPIO are only mocked here.
    # RPi and RPi.GPIO must be mocked, because they can only be imported on a Raspberry Pi
    from reboot_button.button_handler import is_system_alive

    with patch("reboot_button.button_handler.os.execlp") as mock_execlp:
        mock_execlp.return_value = None
        result = is_system_alive(logger)
        mock_execlp.assert_called_once_with("/bin/true", "/bin/true")
        assert result is True, f"Expected is_system_alive to return True, but got {result}"


@patch.dict('sys.modules', {'RPi': Mock(), 'RPi.GPIO': Mock()})
def test_is_system_alive_os_error(logger):
    """Test is_system_alive with OSError."""
    # The modules can only be imported now, because RPi and RPi.GPIO are only mocked here.
    # RPi and RPi.GPIO must be mocked, because they can only be imported on a Raspberry Pi
    from reboot_button.button_handler import is_system_alive

    with patch("reboot_button.button_handler.os.execlp") as mock_execlp:
        mock_execlp.side_effect = OSError
        result = is_system_alive(logger)
        assert result is False, \
            f"Expected is_system_alive to return False on OSError, but got {result}"


@patch.dict('sys.modules', {'RPi': Mock(), 'RPi.GPIO': Mock()})
@patch("reboot_button.button_handler.time.sleep")
@patch("reboot_button.button_handler.is_system_alive")
@patch("reboot_button.button_handler.reboot_system")
def test_button_callback_reboot_success(
    mock_reboot_system, mock_is_system_alive, mock_sleep, logger
):
    """Test button_callback with successful reboot_system."""
    # The modules can only be imported now, because RPi and RPi.GPIO are only mocked here.
    # RPi and RPi.GPIO must be mocked, because they can only be imported on a Raspberry Pi
    from reboot_button.button_handler import button_callback

    mock_reboot_system.return_value = True
    result = button_callback(logger, 17)
    mock_reboot_system.assert_called_once_with(logger)
    mock_is_system_alive.assert_not_called()
    mock_sleep.assert_not_called()
    assert result is True, f"Expected button_callback to return True, but got {result}"


@patch.dict('sys.modules', {'RPi': Mock(), 'RPi.GPIO': Mock()})
@patch("reboot_button.button_handler.time.sleep")
@patch("reboot_button.button_handler.is_system_alive")
@patch("reboot_button.button_handler.reboot_system")
def test_button_callback_reboot_failed_system_alive(
    mock_reboot_system, mock_is_system_alive, mock_sleep, logger
):
    """Test button_callback with failed reboot and system alive."""
    # The modules can only be imported now, because RPi and RPi.GPIO are only mocked here.
    # RPi and RPi.GPIO must be mocked, because they can only be imported on a Raspberry Pi
    from reboot_button.button_handler import button_callback

    mock_reboot_system.return_value = False
    mock_is_system_alive.return_value = True
    result = button_callback(logger, 17)
    mock_reboot_system.assert_called_once_with(logger)
    mock_is_system_alive.assert_called_once_with(logger)
    mock_sleep.assert_called_once_with(1)
    assert result is False


@patch.dict('sys.modules', {'RPi': Mock(), 'RPi.GPIO': Mock()})
@patch("reboot_button.button_handler.time.sleep")
@patch("reboot_button.button_handler.is_system_alive")
@patch("reboot_button.button_handler.reboot_system")
def test_button_callback_reboot_failed_system_dead(
    mock_reboot_system, mock_is_system_alive, mock_sleep, logger
):
    """Test button_callback with failed reboot and system dead."""
    # The modules can only be imported now, because RPi and RPi.GPIO are only mocked here.
    # RPi and RPi.GPIO must be mocked, because they can only be imported on a Raspberry Pi
    from reboot_button.button_handler import button_callback

    mock_reboot_system.return_value = False
    mock_is_system_alive.return_value = False
    result = button_callback(logger, 17)
    mock_reboot_system.assert_called_once_with(logger)
    mock_is_system_alive.assert_called_once_with(logger)
    mock_sleep.assert_called_once_with(1)
    assert result is False
