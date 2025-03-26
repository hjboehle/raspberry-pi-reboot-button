# Raspberry Pi reboot-button

This project provides a Python script to monitor a physical button connected to a Raspberry Pi's GPIO pin. When the button is pressed, the Raspberry Pi performs a clean reboot. The script is designed to be run as a systemd service to ensure it starts automatically on boot.

## Features

* Monitors a GPIO pin for button presses.
* Executes a controlled reboot on button press.
* Logs all actions to the Raspberry Pi system log for easy troubleshooting.
* Implements debouncing to avoid false triggers.

## Requirements

### Hardware

* Raspberry Pi (any model with GPIO support).
* A physical push button.
* Resistors for pull-up/pull-down configuration (optional, depending on your circuit).

### Software

* Python 3.x
* `RPi.GPIO` Python library for Raspberry Pi GPIO access.

## Hardware installation

A two-pole pushbutton with two wires terminated at a two-pole plug socket or two single-pole plug sockets is required. The plug socket or the plug sockets must be able to be plugged into the GPIO pin header of a Raspberry pi. The plug socket or the plug sockets must be plugged in so that one contact is connected to a pin and the other contact is connected to GND.

### Button test

Raspberry Pi OS should be installed on the Raspberry Pi. In principle, however, the “reboot-button” software should also work with other operating systems. However, there may be differences in the procedure.

To check the button and its installation, the standard pre-installed software `Pigpio` must be used. First, the `Pigpio` daemon should be stopped if it is running:

    sudo killall pigpiod

The daemon is restarted with the following command:

    sudo pigpiod

The pin you have selected is then read out with the following command:

    pigs r <pin>

For `<pin>`, please enter the pin you have selected. The value then output must be `1`. Then press the button and enter the previous command again:

    pigs r <pin>

The output value must now be '0'. If this is the case, the push-button is correctly installed on the pin you selected and you can start the software installation.

## Software Installation

First change to a directory of your choice. A recommendation would be the directory `/opt`. In this document, it is assumed that this will be used. If you use a different directory, you must adapt the following procedure accordingly.

    cd /opt

Use the following command to copy the `reboot-button` software to your Raspberry Pi:

    git clone https://github.com/hjboehle/reboot-button.git

Then change to the cloned directory with the following command:

    cd reboot-button

The `reboot-button` software consists of Python modules that require additional Python packages. A virtual Python environment is created so that the Python installation on the Raspberry Pi remains unaffected. As the software is ultimately executed by the superuser root, the virtual environment is created using `sudo` with the following command:

    sudo python3 -m venv .venv

The required Python packages are now installed in the virtual Python environment using the following commands:

    source .venv/bin/activate
    sudo chown -R $(whoami) .venv
    pip install -r requirements.txt
    deactivate

The `reboot-button` software is installed as a service so that it is reliably available again after every reboot. To do this, the service file must be copied to the directory intended for services using the following command:

    sudo cp /opt/reboot-button/service/reboot-button.service /etc/systemd/system/

To reload and activate the service, the following commands are executed:

    sudo systemctl daemon-reload
    sudo systemctl enable reboot-button.service
    sudo systemctl start reboot-button.service

## Log Files

Da die Software `reboot-button` über keine GUI verfügt, werden alle Ereignisse nach dessen Initialisierung in eine Log Datei geschrieben. Die Log Dateien sind einzusehen in den Logdateien des Verzeichnisses `/var/log/reboot-button`. Die aktuelle Logdatei hat den Namen `reboot-button.log`.

## Development

If you are interested in the development of the `reboot-button` software or even want to participate, here is some information.

### Run Unit Tests

This project includes unit tests written with pytest. To run the tests in the root directory of this project, use the following command:

    pytest reboot_button/test

### Project Structure

The project has the following structure:

* `reboot-button/` (root directory)
  * `reboot_button/` (directory for the Python source code)
    * `__init__.py` (module initialization)
    * `button_handler.py` (Python script to handle the reboot button)
    * `config.py` (Python script with configuration data)
    * `log_file.py` (Python script for log file logging)
    * `logger_config.py` (Python script to configure the logging)
    * `main.py` (main Python script)
  * `service/` (directory for the systemd service file)
    * `reboot-button.service` (systemd service configuration)
  * `test/` (directory for the Python unit tests)
* `.gitignore` (file with ignored files for git)
* `.pylintrc` (file with Python linting rules)
* `LICENSE` (license)
* `README.md` (readme file - this file)
* `requirements.txt` (file with the required Python packages)

## Troubleshooting

### Common Issues

Here are some common issues that may occur when setting up or using the `reboot-button`, along with possible solutions:

#### `RuntimeError: Failed to add edge detection`

* **Problem:** This error occurs when the script is not run with root privileges. The `RPi.GPIO` library requires root privileges to access the GPIO pins and configure edge detection.
* **Solution:** Ensure that the script is run as root. Since the script is started as a systemd service, this should be the case automatically. However, check the configuration of the service file (`reboot-button.service`) and make sure that `User=root` or no `User` is specified.
* **Verification:** Check with `ps aux | grep reboot-button` if the process is running as `root`.

#### No response when pressing the button

* **Problem:** The script does not react when the button is pressed.
* **Possible Causes:**
  * **Incorrect wiring:** The button wiring is faulty.
  * **Incorrect GPIO pin number:** The GPIO pin number configured in the script does not match the actual pin used.
  * **Defective button:** The button itself is defective.
  * **Debouncing issue:** Debouncing is not configured correctly, and too many or no signals are detected.
  * **Incorrect Pull-Up/Pull-Down Configuration:** The configuration of the Pull-Up/Pull-Down resistors is incorrect.
* **Solutions:**
  * **Check wiring:** Check the button wiring and make sure it is correctly connected to the GPIO pin and GND.
  * **Check GPIO pin number:** Make sure the GPIO pin number configured in the script matches the actual pin used.
  * **Test button:** Test the button with a multimeter or another test device to make sure it works.
  * **Check debouncing settings:** Check the debouncing settings in the script and adjust them if necessary.
  * **Check Pull-Up/Pull-Down Configuration:** Check the configuration of the Pull-Up/Pull-Down resistors and adjust them if necessary.
  * **Button Test:** Perform the button test as described in the "Button Test" section.
* **Verification:** Check with `pigs r <pin>` if the button works correctly.

#### **Script does not start on boot**

* **Problem:** The `reboot-button` service does not start automatically when the Raspberry Pi boots.
* **Possible Causes:**
  * **Service not enabled:** The service was not enabled with `systemctl enable`.
  * **Error in the service file:** The service file (`reboot-button.service`) contains errors.
  * **Error in the script:** The script itself contains errors that prevent it from starting.
* **Solutions:**
  * **Enable service:** Make sure the service has been enabled with `sudo systemctl enable reboot-button.service`.
  * **Check service file:** Check the service file for syntax errors or incorrect paths.
  * **Check script for errors:** Check the script for errors, e.g., with `sudo journalctl -u reboot-button.service`.
* **Verification:** Check with `sudo systemctl status reboot-button.service` if the service is running and if there are any errors.

#### **Unexpected reboots**

* **Problem:** The Raspberry Pi reboots unexpectedly without the button being pressed.
* **Possible Causes:**
  * **Incorrect wiring:** The button wiring is faulty and causes unwanted signals.
  * **Electrical interference:** Electrical interference in the environment can lead to false signals.
  * **Debouncing issue:** Debouncing is not configured correctly, and too many signals are detected.
* **Solutions:**
  * **Check wiring:** Check the button wiring and make sure it is correct.
  * **Minimize electrical interference:** Try to keep the wiring away from other electronic devices.
  * **Check debouncing settings:** Check the debouncing settings in the script and adjust them if necessary.
* **Verification:** Check the log file `/var/log/reboot-button/reboot-button.log` for unusual entries.

#### **Missing Log File**

* **Problem:** The log file `/var/log/reboot-button/reboot-button.log` is not created or is empty.
* **Possible Causes:**
  * **Missing Permissions:** The script does not have permission to write to the `/var/log/reboot-button` directory.
  * **Error in the Script:** The script has an error that prevents writing to the log file.
  * **Incorrect Configuration:** The logging configuration is incorrect.
* **Solutions:**
  * **Check Permissions:** Make sure the script has permission to write to the `/var/log/reboot-button` directory.
  * **Check Script for Errors:** Check the script for errors, e.g., with `sudo journalctl -u reboot-button.service`.
  * **Check Configuration:** Check the logging configuration in the script.
* **Verification:** Check with `sudo journalctl -u reboot-button.service` if there are errors when starting the service.

### Debugging

Enable verbose logging by editing the `logger_config.py` file and adjusting the log level:

    ```python
    logging.basicConfig(level=logging.DEBUG)
    ```

**Caution:** This setting should only be used for troubleshooting, as it generates a lot of log entries.

You can also view the log file `/var/log/reboot-button/reboot-button.log` or the service log file with `sudo journalctl -u reboot-button.service`.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
