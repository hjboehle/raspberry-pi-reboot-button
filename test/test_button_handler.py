"""module test_button_handler.py"""

import logging
import os
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


#@patch.dict('sys.modules', {'RPi': Mock(), 'RPi.GPIO': Mock()})
#def test_is_system_alive_success(mock_logger):
#    """Test is_system_alive with successful os.execlp call."""
#    # Da die Module importiert wurden, müssen wir sie jetzt importieren
#    from reboot_button.button_handler import is_system_alive
#
#    with patch("reboot_button.button_handler.os.execlp") as mock_execlp:
#        mock_execlp.return_value = None
#        result = is_system_alive(mock_logger)
#        mock_execlp.assert_called_once_with("/bin/true", "/bin/true")
#        assert result is True
#
#@patch.dict('sys.modules', {'RPi': Mock(), 'RPi.GPIO': Mock()})
#def test_is_system_alive_os_error(mock_logger):
#    """Test is_system_alive with OSError."""
#    # Da die Module importiert wurden, müssen wir sie jetzt importieren
#    from reboot_button.button_handler import is_system_alive
#
#    with patch("reboot_button.button_handler.os.execlp") as mock_execlp:
#        mock_execlp.side_effect = OSError
#        result = is_system_alive(mock_logger)
#        assert result is False
#
#@patch.dict('sys.modules', {'RPi': Mock(), 'RPi.GPIO': Mock()})
#@patch("reboot_button.button_handler.time.sleep")
#@patch("reboot_button.button_handler.is_system_alive")
#@patch("reboot_button.button_handler.reboot_system")
#def test_button_callback_reboot_success(
#    mock_reboot_system, mock_is_system_alive, mock_sleep, mock_logger
#):
#    """Test button_callback with successful reboot_system."""
#    # Da die Module importiert wurden, müssen wir sie jetzt importieren
#    from reboot_button.button_handler import button_callback
#
#    mock_reboot_system.return_value = True
#    result = button_callback(mock_logger, 17)
#    mock_reboot_system.assert_called_once_with(mock_logger)
#    mock_is_system_alive.assert_not_called()
#    mock_sleep.assert_not_called()
#    assert result is True
#
#@patch.dict('sys.modules', {'RPi': Mock(), 'RPi.GPIO': Mock()})
#@patch("reboot_button.button_handler.time.sleep")
#@patch("reboot_button.button_handler.is_system_alive")
#@patch("reboot_button.button_handler.reboot_system")
#def test_button_callback_reboot_failed_system_alive(
#    mock_reboot_system, mock_is_system_alive, mock_sleep, mock_logger
#):
#    """Test button_callback with failed reboot and system alive."""
#    # Da die Module importiert wurden, müssen wir sie jetzt importieren
#    from reboot_button.button_handler import button_callback
#
#    mock_reboot_system.return_value = False
#    mock_is_system_alive.return_value = True
#    result = button_callback(mock_logger, 17)
#    mock_reboot_system.assert_called_once_with(mock_logger)
#    mock_is_system_alive.assert_called_once_with(mock_logger)
#    mock_sleep.assert_called_once_with(1)
#    assert result is False
#
#@patch.dict('sys.modules', {'RPi': Mock(), 'RPi.GPIO': Mock()})
#@patch("reboot_button.button_handler.time.sleep")
#@patch("reboot_button.button_handler.is_system_alive")
#@patch("reboot_button.button_handler.reboot_system")
#def test_button_callback_reboot_failed_system_dead(
#    mock_reboot_system, mock_is_system_alive, mock_sleep, mock_logger
#):
#    """Test button_callback with failed reboot and system dead."""
#    # Da die Module importiert wurden, müssen wir sie jetzt importieren
#    from reboot_button.button_handler import button_callback
#
#    mock_reboot_system.return_value = False
#    mock_is_system_alive.return_value = False
#    result = button_callback(mock_logger, 17)
#    mock_reboot_system.assert_called_once_with(mock_logger)
#    mock_is_system_alive.assert_called_once_with(mock_logger)
#    mock_sleep.assert_called_once_with(1)
#    assert result is False
#
#@patch.dict('sys.modules', {'RPi': Mock(), 'RPi.GPIO': Mock()})
#@patch("reboot_button.button_handler.GPIO")
#@patch("reboot_button.button_handler.time.sleep")
#def test_monitor_button(mock_time_sleep, mock_gpio, mock_logger):
#    """
#    Test case for the monitor_button function.
#
#    Verifies that monitor_button correctly configures GPIO and adds event detection.
#    """
#    # Da die Module importiert wurden, müssen wir sie jetzt importieren
#    from reboot_button.button_handler import monitor_button, button_callback
#
#    mock_gpio.setmode = Mock()
#    mock_gpio.setup = Mock()
#    mock_gpio.add_event_detect = Mock()
#
#    # Ersetze GPIO.FALLING, damit der Test auf allen Systemen läuft
#    setattr(mock_gpio, 'FALLING', 1)
#
#    mock_callback = Mock()
#    mock_gpio.add_event_detect.side_effect = lambda pin, edge, callback, bouncetime: mock_callback(callback)
#
#    monitor_button(mock_logger, 17)
#    mock_gpio.setmode.assert_called_once_with(mock_gpio.BCM)
#    mock_gpio.setup.assert_called_once_with(17, mock_gpio.IN, pull_up_down=mock_gpio.PUD_UP)
#    mock_gpio.add_event_detect.assert_called_once()
#    mock_callback.assert_called_once()
#    mock_callback.call_args[0][0]()
