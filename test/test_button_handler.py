"""module test_button_handler"""

import pytest


# Mock the module so that it does not try to load real GPIO
@pytest.fixture(autouse=True)
def mock_gpio(mocker):
    """
    Fixture to mock the RPi and RPi.GPIO modules.
    
    This fixture automatically applies to all tests in the module. It uses the `mocker` 
    fixture to patch the `sys.modules` dictionary, replacing the `RPi` and `RPi.GPIO` 
    modules with `MagicMock` objects. This allows tests to run without requiring the 
    actual RPi.GPIO library, which is useful for testing on non-Raspberry Pi systems.
    
    Args:
        mocker (pytest_mock.MockerFixture): The mocker fixture provided by the pytest-mock plugin.
    
    Returns:
        None
    """
    mocker.patch.dict("sys.modules", {"RPi": mocker.MagicMock(), "RPi.GPIO": mocker.MagicMock()})


def test_button_callback(mocker):
    """
    Test the button_callback function.

    This test verifies that the button_callback function logs the correct message
    and calls the os.system function with the correct command to reboot the Raspberry Pi
    when a button press is detected on a specified GPIO pin.

    Args:
        mocker: A pytest-mock fixture used to patch the logger and os.system functions.

    Asserts:
        - The logger.info method is called once with the expected log message.
        - The os.system function is called once with the command "sudo reboot".
    """
    mock_logger = mocker.patch("reboot_button.button_handler.logger")
    mock_os_system = mocker.patch("os.system")

    import reboot_button.button_handler as bh # pylint: disable=import-outside-toplevel
    bh.button_callback(17)

    mock_logger.info.assert_called_once_with(
        "Button pressed on GPIO '%s'. Raspberry Pi will reboot.", 17
    )
    mock_os_system.assert_called_once_with("sudo reboot")


def test_monitor_button(mocker):
    """
    Test the monitor_button function.

    This test verifies that the monitor_button function correctly initializes
    GPIO, sets up event detection, and handles different exceptions properly.
    It ensures that the function does not attempt to run indefinitely during the test.

    Args:
        mocker: A pytest-mock fixture used to patch logging, GPIO functions, and time.sleep.

    Asserts:
        - GPIO.setmode is called once with GPIO.BCM.
        - GPIO.setup is called once with the correct pin and parameters.
        - GPIO.add_event_detect is called with the correct arguments.
        - The function correctly logs setup steps.
        - GPIO.cleanup is called at the end.
    """
    # Mock dependencies
    mock_logger = mocker.patch("reboot_button.button_handler.logging")
    mocked_gpio = mocker.patch("reboot_button.button_handler.GPIO")
    mocker.patch("time.sleep", side_effect=InterruptedError)

    import reboot_button.button_handler as bh # pylint: disable=import-outside-toplevel

    # Run the function (will exit early due to mock_time_sleep raising InterruptedError)
    with pytest.raises(InterruptedError):
        bh.monitor_button()

    # Assertions to verify GPIO setup
    mocked_gpio.setmode.assert_called_once_with(mocked_gpio.BCM)
    mocked_gpio.setup.assert_called_once_with(
        bh.BUTTON_PIN,
        mocked_gpio.IN,
        pull_up_down=mocked_gpio.PUD_UP
    )
    mocked_gpio.add_event_detect.assert_called_once_with(
        bh.BUTTON_PIN, mocked_gpio.FALLING,
        callback=bh.button_callback,
        bouncetime=300
    )
    mock_logger.info.assert_any_call("Set GPIO mode.")
    mock_logger.info.assert_any_call(
        "Configuration of the pin as an input pin with pull-up resistor."
    )
    mock_logger.info.assert_any_call("Add event monitoring.")

    # Ensure GPIO cleanup is called
    mocked_gpio.cleanup.assert_called_once()
