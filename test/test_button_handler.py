"""module test_button_handler"""

import pytest


# Mock the module so that it does not try to load real GPIO
@pytest.fixture(autouse=True)
def mock_gpio(mocker):
    """
    Fixture to mock the RPi and RPi.GPIO modules.
    
    This fixture automatically applies to all tests in the module. It uses the `mocker` 
    ixture to patch the `sys.modules` dictionary, replacing the `RPi` and `RPi.GPIO` 
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

    import reboot_button.button_handler as bh
    bh.button_callback(17)

    mock_logger.info.assert_called_once_with(
        "Button pressed on GPIO '%s'. Raspberry Pi will reboot.", 17
    )
    mock_os_system.assert_called_once_with("sudo reboot")
