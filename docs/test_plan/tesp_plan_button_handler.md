# Test Plan for button_handler.py

**Document Version:** 1.0
**Last Updated:** 2025-03-18
**Author:** Hans Jürgen Böhle

## 1. Introduction

This document outlines the test plan for the `button_handler.py` module, which is responsible for monitoring a button connected to a GPIO pin on a Raspberry Pi and initiating a system reboot upon button press. The module also handles logging and error scenarios.

## 2. Scope

### 2.1 In Scope

* Functionality of the `reboot_system()` function.
* Functionality of the `is_system_alive()` function.
* Functionality of the `button_callback()` function.
* Functionality of the `monitor_button()` function.
* GPIO configuration and event detection.
* Logging functionality and error handling within the module.
* Handling of different `sudo` scenarios (with and without password).
* Handling of system unresponsiveness.
* Handling of incorrect GPIO configuration.
* Correct GPIO Cleanup.

### 2.2 Out of Scope

* Testing of external dependencies (e.g., the `RPi.GPIO` library itself).
* Testing of the operating system's reboot process.
* Detailed test of the underlying system functions.
* Test of the main.py file or log_file.py

## 3. Test Objectives

* Verify that the system reboots correctly when the button is pressed.
* Verify correct handling of scenarios where `sudo reboot` fails (e.g., due to password requirement).
* Verify that the system responsiveness check (`is_system_alive()`) works as expected.
* Verify that logging is performed correctly at different levels (INFO, ERROR, DEBUG).
* Verify that errors and exceptions are handled gracefully and logged properly.
* Verify that incorrect GPIO configurations are handled correctly.
* Verify that GPIO pins are released properly.

## 4. Test Environment

* **Hardware:** Raspberry Pi (Model [Specify Model if relevant])
* **Operating System:** Raspberry Pi OS (Version [Specify Version if relevant])
* **Python Version:** [Specify Version]
* **Libraries:** `RPi.GPIO`, `logging`, `time`, `os`, `sys`
* **GPIO Pin:** GPIO [Specify Pin Number, e.g., 17] connected to a physical button.
* **sudo** configured with or without Password.
* **Path** the `sudo` binary.
* **Logfile** with write permission for the user running the script.
* **Home** directory configured correctly.

## 5. Test Strategy

* **Test Type:** Primarily System Testing and some Integration Testing
* **Test Method:** Manual testing (with potential for automation in the future).
* **Coverage:** Functionality-based testing, aiming for high code coverage within the `button_handler.py` module.
* **Logging:** Every test step and its expected output should be logged.
* **Error Handling:** Error cases will be produced manually.

## 6. Test Cases

The following table describes the test cases:

| Test Case ID | Test Case Name                              | Test Case Description                                                                                                                                | Test Case Prerequisites                                                                                                                                      | Test Steps                                                                                                                                                                                                                                                                                 | Expected Result                                                                                                                                                                                                                                                                      |
| :----------- | :------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TC_BH_001    | Normal Reboot                             | Verify that the system reboots when the button is pressed under normal conditions.                                                              | - Raspberry Pi is powered on.<br> - The script is running.<br> - Button is correctly wired to the specified GPIO pin.<br>- `sudo` is requiring a password.               | 1. Start the script. <br> 2. Press the button.                                                                                                                                                                                                                                            | - The Raspberry Pi reboots.<br> - The log file contains an entry like "Button pressed on GPIO '17'. Attempting to reboot." and the Reboot information.                                                                                                                                      |
| TC_BH_002    | Sudo Error (Password Required)              | Verify that the script handles the scenario where `sudo reboot` fails due to a password requirement.                                                | - Raspberry Pi is powered on.<br> - The script is running.<br> - Button is correctly wired.<br> - `sudo` requires a password.                                      | 1. Start the script. <br> 2. Press the button.                                                                                                                                                                                                                                            | - The script logs an error message (e.g., "Maybe a password is required for sudo.").<br> - A Test with `/bin/true` is done. <br> - The script log information on the test.<br> - The Raspberry Pi does not reboot.<br> - The script continues to run and wait for a button press. |
| TC_BH_003    | Sudo Success (No Password Required)        | Verify that the system reboots correctly when `sudo reboot` works without a password prompt.                                                      | - Raspberry Pi is powered on.<br> - The script is running.<br> - Button is correctly wired.<br> - `sudo` does not require a password (configured in `/etc/sudoers`). | 1. Configure `/etc/sudoers` to allow `sudo` without a password. <br> 2. Start the script. <br> 3. Press the button.                                                                                                                                                                | - The Raspberry Pi reboots directly.<br> - The log file contains an entry like "Button pressed on GPIO '17'. Attempting to reboot." and the Reboot information.                                                                                                                                |
| TC_BH_004    | Button Debounce                            | Verify that button debouncing works as expected.                                                                                                       | - Raspberry Pi is powered on.<br> - The script is running.<br> - Button is correctly wired.                                                                        | 1. Press the button very quickly multiple times.                                                                                                                                                                                                                                     | - Only one reboot is triggered. <br> - Only one button press log entry.                                                                                                                                                                                                                |
| TC_BH_005    | System Unresponsiveness                   | Verify that the script handles system unresponsiveness.                                                                                           | - Raspberry Pi is powered on.<br> - The script is running.<br> - Button is correctly wired.<br> - A System error is produced.                                           | 1. Trigger a system error/crash. <br> 2. Start the script. <br> 3. Press the button.                                                                                                                                                                                                    | - The log file contains messages indicating unresponsiveness, e.g., "System is likely down or unresponsive." and "Assuming the system is rebooting."<br>- No reboot is triggered.                                                                                                              |
| TC_BH_006    | Log File Creation and Write               | Verify that the log file is created and written to correctly.                                                                                           | - Raspberry Pi is powered on.<br> - The script is running.<br> - No log file exists yet.                                                                            | 1. Start the script. <br> 2. Check if the log file (`/var/log/reboot_button.log` or `~/reboot_button/log/reboot_button.log`) is created. <br> 3. Perform actions (button press, cause errors). <br> 4. Verify log file content.                             | - The log file is created. <br> - All log entries are written correctly, including timestamps.                                                                                                                                                                                                  |
| TC_BH_007    | Logging Levels                            | Verify that messages are logged at the correct levels (DEBUG, INFO, ERROR).                                                                             | - Raspberry Pi is powered on.<br> - The script is running.                                                                                                       | 1. Set the logger level to `logging.DEBUG` in `log_file.py`. <br> 2. Start the script. <br> 3. Perform actions. <br> 4. Check the log file for DEBUG messages. <br> 5. Change the logger level back to `logging.INFO`. <br> 6. repeat steps and check that no debug messages are visible | - DEBUG messages appear only when the level is set to `DEBUG`. <br> - Only INFO or ERROR messages are logged otherwise.                                                                                                                                                               |
| TC_BH_008    | Logging with Errors                        | Verify correct logging when errors occur (e.g., `sudo` not in PATH, no write permissions).                                                              | - Raspberry Pi is powered on.<br> - The script is running.                                                                                                       | 1. Remove `sudo` from PATH. <br> 2. Start the script. <br> 3. Press the button. <br> 4. Check log file. <br> 5. Restore `sudo` to PATH.<br> 6. Remove write permissions from the log directory.<br>7. Repeat steps. <br> 8. Restore write permissions. | - Correct error messages are logged (e.g., "Command not found: sudo", "Failed to create or append to log file").                                                                                                                                                            |
| TC_BH_009    | Invalid GPIO Pin                          | Verify that the script handles an invalid GPIO pin configuration.                                                                                     | - Raspberry Pi is powered on.<br> - The script is running.<br> - The GPIO is not correct configured.                                                                | 1. Set `BUTTON_PIN` in `config.py` to an invalid value (e.g., -1 or 999). <br> 2. Start the script.                                                                                                                                                                              | - The script catches the `GPIO.InvalidChannelException`. <br> - An error message is logged (e.g., "Invalid GPIO channel specified: ..."). <br> - The script terminates gracefully.                                                                                                              |
| TC_BH_010    | GPIO Cleanup                              | Verify that GPIO pins are released properly after the script terminates.                                                                                 | - Raspberry Pi is powered on.<br> - The script is running.<br> - GPIO correctly configured                                                                        | 1. Start the script. <br> 2. Check if the GPIO is in use.<br> 3. Terminate the script.<br> 4. Check if the GPIO is in use.                                                                                                                                                                              | - The GPIO pins are released after the script terminates.                                                                                                                                                                                                                            |
| TC_BH_011    | Incorrect Home variable                     | Simulate an incorrect Home variable to verify if the script still logs.                                                                              | Raspberry Pi is powered on.<br> The script is running.<br> The Home variable is not correct.                                                                        | 1. Run `export HOME=/tmp`.<br> 2. Start the script. <br> 3. Check if a logfile in `/var/log` has been created.<br> 4. Set Home back to normal with `export HOME=/home/username`.                                                                                                                        | The script uses the system wide log file `/var/log` instead of the home path.                                                                                                                                                                                                            |
| TC_BH_012    | Incorrect Permissions for logfile directory | Simulate incorrect permission on the logfile directory, to check how the script is handling this case.                                               | Raspberry Pi is powered on.<br> The script is running.<br> The log directory has incorrect rights.                                                                        | 1. Run `sudo chmod 000 /var/log`.<br> 2. Start the script. <br> 3. Check if an error message is shown and a user specific log file has been created.<br> 4. Set the permissions back to normal with `sudo chmod 755 /var/log`.                                                                  | The script outputs a message to the console.<br> The script tries to use a user specific log file.                                                                                                                                                                                 |

## 7. Test Data

* Valid GPIO pin number (e.g., 17).
* Invalid GPIO pin numbers (e.g., -1, 999).
* Scenarios where `sudo` requires or does not require a password.
* Scenarios where the logfile directory has incorrect permissions.
* Scenarios where the home variable is not set correctly.

## 8. Test Deliverables

* This Test Plan document.
* Executed Test Case list with test results.
* Log files generated during testing.

## 9. Roles and Responsibilities

* [Your Name/Team Name]: Responsible for creating, maintaining, and executing this test plan.

## 10. Entry and Exit Criteria

### 10.1 Entry Criteria

* The `button_handler.py` module is implemented.
* The test environment is set up and available.
* This test plan is reviewed and approved.

### 10.2 Exit Criteria

* All test cases have been executed.
* All test results have been documented.
* All critical and high priority issues are resolved.
* The test plan is updated with test results.

## 11. Risks and Mitigation

| Risk                                                | Mitigation                                                                                                         |
| :-------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| Hardware failure (Raspberry Pi, button)            | Use a backup Raspberry Pi and button.                                                                              |
| Incorrect GPIO wiring                             | Double-check the wiring before starting the tests.                                                                 |
| Errors in the test script itself                   | Use code reviews and testing to ensure the script works as expected.                                              |
| Time constraints                                   | Prioritize test cases and allocate sufficient time for testing.                                                      |
| Wrong sudo configuration                           | Double check the sudoers file                                                                                      |
| Wrong rights on the logfile or directory           | Double check the rights before running the test and correct them afterwards.                                       |
| Wrong Home variable                                | Double check that the correct Home variable is set and correct it afterwards.                                       |
