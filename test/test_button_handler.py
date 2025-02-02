import pytest
import time
from reboot_button.button_handler import button_callback
import reboot_button.button_handler as bh


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


@pytest.fixture
def mock_gpio(pytest_mock):
    """Fixture to mock RPi.GPIO."""
    return pytest_mock.patch.object(bh, "GPIO")


@pytest.fixture
def mock_time(pytest_mock):
    """Fixture to mock time.sleep."""
    return pytest_mock.patch.object(time, "sleep")


@pytest.fixture
def mock_logger(pytest_mock):
    """Fixture to mock logging."""
    return pytest_mock.patch.object(bh, "logger")


def test_monitor_button(mock_gpio, mock_time, mock_logger, pytest_mock):
    """
    Testet die monitor_button-Funktion:
    - Überprüft GPIO-Setup
    - Stellt sicher, dass GPIO.cleanup() aufgerufen wird
    - Prüft, ob Logging-Meldungen erscheinen
    """
    # Simuliert GPIO Event Detection
    mock_gpio.add_event_detect.side_effect = lambda *args, **kwargs: None

    # Simuliert einen manuellen Abbruch mit KeyboardInterrupt nach einer Sekunde
    mock_time.side_effect = KeyboardInterrupt

    # Test ausführen und Abbruch erwarten
    with pytest.raises(KeyboardInterrupt):
        bh.monitor_button()

    # Testet, ob GPIO richtig konfiguriert wurde
    mock_gpio.setmode.assert_called_once_with(mock_gpio.BCM)
    mock_gpio.setup.assert_called_once_with(bh.BUTTON_PIN, mock_gpio.IN, pull_up_down=mock_gpio.PUD_UP)
    mock_gpio.add_event_detect.assert_called_once_with(
        bh.BUTTON_PIN, mock_gpio.FALLING, callback=bh.button_callback, bouncetime=300
    )

    # Überprüft die Log-Ausgaben
    mock_logger.info.assert_any_call("Set GPIO mode.")
    mock_logger.info.assert_any_call("Configuration of the pin as an input pin with pull-up resistor.")
    mock_logger.info.assert_any_call("Add event monitoring.")
    mock_logger.info.assert_any_call("GPIO cleanup done.")

    # Prüft, ob GPIO.cleanup() aufgerufen wurde
    mock_gpio.cleanup.assert_called_once()