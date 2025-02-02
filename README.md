# Raspberry Pi Button-Controlled Reboot Script

This project provides a Python script to monitor a physical button connected to a Raspberry Pi's GPIO pin. When the button is pressed, the Raspberry Pi performs a clean reboot. The script is designed to be run as a systemd service to ensure it starts automatically on boot.

## Features

- Monitors a GPIO pin for button presses.
- Executes a controlled reboot on button press.
- Logs all actions to the Raspberry Pi system log for easy troubleshooting.
- Implements debouncing to avoid false triggers.

## Requirements

### Hardware

- Raspberry Pi (any model with GPIO support).
- A physical push button.
- Resistors for pull-up/pull-down configuration (optional, depending on your circuit).

### Software

- Python 3.x
- `RPi.GPIO` Python library
- Logging to system log (`logging` library)

## Installation

1. **Set up the hardware:**
    - Connect the button to a GPIO pin (e.g., GPIO 17) and GND.

2. **Clone this repository:**
    ```bash
    git clone https://github.com/yourusername/raspberry-pi-reboot-button.git
    cd raspberry-pi-reboot-button
    ```

3. **Set up the Python environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

4. **Test the script:** Run the script manually to ensure it detects button presses:
    ```bash
    python3 reboot_button.py
    ```

5. **Set up as a systemd service:**
    - Copy the reboot-button.service file to /etc/systemd/system/.
    - Enable and start the service:
    ```bash
    sudo systemctl enable reboot-button.service
    sudo systemctl start reboot-button.service
    ```

## Usage

Once installed, the service will run automatically on startup and monitor the button press events. The button must be pressed for the configured action (reboot) to be triggered.

## Log Files

Logs are written to the system log and can be accessed using:

```bash
journalctl -u reboot-button.service
```

## Development

### Run Unit Tests

This project includes unit tests written with pytest. To run the tests:

```bash
pytest
```

### Project Structure

raspberry-pi-reboot-button/
│
├── reboot_button.py          # Main script
├── requirements.txt          # Python dependencies
├── test_reboot_button.py     # Unit tests
├── reboot-button.service     # systemd service configuration
└── README.md                 # Project documentation

## Troubleshooting

### Common Issues

- RuntimeError: Failed to add edge detection: Ensure the script is running with root permissions.
- No response on button press: Double-check the wiring and GPIO pin number in the script.

### Debugging

Enable verbose logging by editing the reboot_button.py file and adjusting the log level:

```bash
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
