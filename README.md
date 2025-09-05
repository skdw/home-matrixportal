# MatrixPortal Home Assistant Display

This project connects an Adafruit MatrixPortal to Wi-Fi and Home Assistant via MQTT, subscribes to events, and displays messages on an RGB matrix. It uses a custom character map for extended character support and handles display updates.

## Features
- Connects to Wi-Fi and Home Assistant using MQTT
- Subscribes to events and displays messages on an RGB matrix
- Supports extended characters via a custom character map
- Designed for CircuitPython on Adafruit MatrixPortal

## Setup
1. **Install CircuitPython** on your Adafruit MatrixPortal.
2. **Copy the following files to your CIRCUITPY drive:**
   - `code.py` (main application)
   - `character_map.py` (generated character mapping)
   - `settings.toml` (contains secrets; copy from your password manager)
   - All required libraries in the `lib/` folder (see below)
3. **Required Libraries:**
   - See `requirements.txt` for the full list of required libraries.

   The easiest way to install these libraries is with [circup](https://github.com/adafruit/circup):
   ```bash
   circup install -r requirements.txt
   ```
   Alternatively, you can manually download them from the [Adafruit CircuitPython Bundle](https://circuitpython.org/libraries).

4. **Configure Wi-Fi and MQTT:**
   - Set your Wi-Fi credentials and MQTT broker details in the appropriate environment variables or configuration section in `code.py`.

5. **Character Map:**
   - Generate `character_map.py` using the provided PC script and copy it to the CIRCUITPY drive.

## Usage
- Power on the MatrixPortal. The display will connect to Wi-Fi and Home Assistant, then show messages/events received via MQTT.
- If `character_map.py` is missing, the device will halt and display an error message.

## Troubleshooting
- Ensure all required libraries are present in the `lib/` folder.
- Make sure `character_map.py` is generated and copied to the device.
- Check Wi-Fi and MQTT credentials if connection fails.

## License
This project is open source and available under the MIT License.
