# APsystems EZ1 -  Python Library

## Overview
The APsystems EZ1 Python library can be used to interact with APsystems EZ1 Microinverters. It provides a convenient way to communicate with the microinverter over your **local network**, allowing you to read and set various device parameters like power status, alarm information, device information, and power limits.

---

## About Sonnenladen GmbH
This library is published, maintained, and developed by Sonnenladen GmbH. Our collaboration with the APsystems R&D Team has been instrumental in making this API a reality. At Sonnenladen GmbH, we are committed to providing top-notch solar energy solutions and are excited to offer this library to enhance the experience of using APsystems inverters.

## Purchase APsystems Inverters
For those interested in purchasing APsystems inverters, please visit our German online shop at [Sonnenladen](https://www.sonnenladen.de/). We offer a range of APsystems products, backed by our expertise in solar energy solutions.

---
## Features
- **Get detailed device information**
- **Retrieve alarm status information**
- **Fetch output data** (power output, energy readings)
- **Set and get maximum power limits** (30 W up to 800 W)
- **Manage device power status** (sleep_mode/on/off)
- **Calculate combined power output and total energy generated**
- and much more...</br></br>
- **See our Home Assistant Integration based on this library:**
- https://github.com/SonnenladenGmbH/APsystems-EZ1-API-HomeAssistant

## Device Compatibility
- This table includes all micro-inverters we tested and can confirm 100 % compatbility with this library.
<table>
<tbody>
<tr>
<th>Device</th>
<th>Name</th>
<th>Support / Compatibility</th>
<th>Available to purchase at:</th>
</tr>
<tr>
<td align="center"><img src="https://github.com/SonnenladenGmbH/APsystems-EZ1-API/raw/main/assets/images/APsystems-EZ1-M.png" alt="APsystems EZ1-M Inverter" width="150" /></td>
<td align="center">
<p><strong>APsystems EZ1-M</strong></p>
<p>(Firmware: EZ1 1.6.0)</p>

</td>
<td align="center"><img src="https://img.icons8.com/color/48/000000/checkmark.png" alt="Compatible-Checkmark" width="30" /></td>
<td align="center"><a href="https://www.sonnenladen.de/APsystems-EZ1-M-600-800-W-Mikrowechselrichter-ohne-Anschlusskabel/AP-07-000-0" target="_blank" rel="noopener"><strong>Sonnenladen GmbH - Online Shop</strong></a><br /><a href="https://www.sonnenladen.de/APsystems-EZ1-M-600-800-W-Mikrowechselrichter-ohne-Anschlusskabel/AP-07-000-0" target="_blank" rel="noopener">IN STOCK | AUF LAGER</a></td>
</tr>
</tbody>
</table>

## Setup your Inverter
The local API access needs to be activated once in the settings of the EZ1. Please follow our Step-By-Step Guide to do so:
<p><img src="https://github.com/SonnenladenGmbH/APsystems-EZ1-API/raw/main/assets/images/APsystems-Lokale-API-Aktivieren-Schritt1-3.png" alt="APsystems EZ1-M Inverter Setup" width="820" /></p>
<ul>
<li>Step 1: Connect to the inverter using the "Direct Connection" method.</li>
<li>Step 2: Establish a connection with your inverter.</li>
<li>Step 3: Select the Settings menu.</li>
</ul>
<p><img src="https://github.com/SonnenladenGmbH/APsystems-EZ1-API/raw/main/assets/images/APsystems-Lokale-API-Aktivieren-Schritt4-6.png" alt="APsystems EZ1-M Inverter Setup" width="820" /></p>
<ul>
<li>Step 4: Switch to the "Local Mode" section.</li>
<li>Step 5: Activate local mode and select "Continuous"</li>
<li>Step 6: Done! Make a note of the IP address for future reference.</li>
(To ensure a successful connection to your Wi-Fi network, it's essential to first set up your device using the standard procedure outlined in the APsystems Quickstart Guide. This initial setup is a crucial step before proceeding with any further configurations or usage.)
</ul>

---
## Installation
- To use the APsystemsEZ1 library, you need to have Python >=3.8 installed on your system.
- See the following guide to install the latest Python release: https://www.python.org/downloads <br><br>
- You can easily install the `apsystems-ez1` library via pip. The package is hosted on PyPI, making it straightforward to install and update. To install, run the following command:


```bash
pip install apsystems-ez1
```
- NOTE: You need to have pip installed on your system. See the following guide to do so: https://pip.pypa.io/en/stable/installation/

## Python Compatibility
- We tested our library on multiple platforms and python versions and can confirm functionality:
<table>
<tbody>
<tr>
<th>Language</th>
<th> -Version- </th>
<th>OS</th>
<th>Plattform</th>
<th>Support / Compatibility</th>
</tr>
<tr>
<td align="center">
<p><strong>Python:</strong></p>

<td align="center">
<p>Python 3.11+</p>
</td>
<td align="center">
<p>MacOS</p>
<p>Linux</p>
<p>Windows</p>
<p>etc.</p>
</td>
<td align="center">
<p>PCs and Laptops</p>
<p>Home Servers</p>
<p>Virtual Machines</p>
<p>Single Board Computers (Raspberry Pi)</p>
</td>
<td align="center"><img src="https://img.icons8.com/?size=96&id=sz8cPVwzLrMP&format=png" alt="Compatible-Checkmark" width="30" /></td>
</tr>
<tr>
<td align="center">
<p><strong>MicroPython:</strong></p>
<td align="center">
<p>N/A</p>
</td>
<td align="center">
<p>MicroPython as a Firmware</p>
</td>
<td align="center">
<p>Raspbery Pi Pico</p>
<p>ESP8266 and ESP32</p>
<p>STM32 Microcontrollers</p>
<p>Teensy, Pyboard</p>

<p>and many more..</p>
</td>
<td align="center"><img src="https://img.icons8.com/?size=96&id=T9nkeADgD3z6&format=png" alt="Compatible-Checkmark" width="30" />
<p>We're working on it...</p>
</td>
</tr>
</tbody>
</table>

---
## Documentation
For a complete understanding of the APsystems EZ1 Python Library, refer to our online documentation. It includes detailed descriptions of the library's functionality, usage examples, and regular updates on new features and improvements.

**Access the Documentation: [APsystems EZ1M Python Library Documentation 📖](https://sonnenladengmbh.github.io/APsystems-EZ1-API/)**

This resource is designed to support both new and experienced users in implementing and optimizing the library in their projects.

---
## Usage
Here's a quick example of how to use the APsystemsEZ1 library:

```python
from APsystemsEZ1 import APsystemsEZ1M # import the APsystemsEZ1 library
import asyncio

# Initialize the inverter with the specified IP address and port number.
inverter = APsystemsEZ1M("192.168.1.100", 8050)

async def main():
    try:
        # Get device information
        device_info = await inverter.get_device_info()
        print("Device Information:", device_info)

        # Get alarm information
        alarm_info = await inverter.get_alarm_info()
        print("Alarm Information:", alarm_info)

        # Get output data
        output_data = await inverter.get_output_data()
        print("Output Data:", output_data)

        # Set maximum power limit (ensure the value is within valid range)
        set_power_response = await inverter.set_max_power(500)
        print("Set Power Response:", set_power_response)

        # Set power status (ensure "ON" or other value is valid)
        set_power_status_response = await inverter.set_device_power_status("ON")
        print("Set Power Status Response:", set_power_status_response)

        # Get current power status
        power_status = await inverter.get_device_power_status()
        print("Power Status:", power_status)
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the main coroutine
asyncio.run(main())
```
---
## Examples - Retrieve Basic Data
Fetch and display data from the inverter.<br>
This function performs the following tasks:<br>
1. Fetches output data from the inverter.
2. Extracts relevant information from the fetched data.
3. Prints the power input from two PV inputs and the total generation for the day.

```python
from APsystemsEZ1 import APsystemsEZ1M
import asyncio

# Initialize the inverter with the specified IP address and port number.
inverter = APsystemsEZ1M("192.168.178.168", 8050)

async def main():
    try:
        # Fetch output data from the inverter.
        response = await inverter.get_output_data()

        # Display power input from PV-Input 1 and 2.
        print("Power PV-Input 1: " + str(response.p1) + " W")
        print("Power PV-Input 2: " + str(response.p2) + " W")

        # Display total energy generation for the current day.
        print("Generation today " + str(round(response.e1 + response.e2, 3)) + " kWh")
    except Exception as e:
        # Handle any exceptions that occur during the data fetch and print the error.
        print(f"An error occurred: {e}")

# Run the main coroutine.
# This is the entry point of the script and it runs the main function in an asynchronous manner.
asyncio.run(main())

```
Example Output:<br>
`Power PV-Input 1: 126 W`<br>
`Power PV-Input 2: 161 W`<br>
`Generation today: 3.167 kWh`<br>

---
## Examples - Set a maximum power output limit
Set the maximum power output limit of the inverter and display the response.<br>
This script performs the following tasks:<br>
1. Sets the maximum output power of the inverter to a specified value (e.g., 60 Watts).
2. Awaits the response from the inverter after setting the power limit.
3. Prints the response from the inverter to confirm the change or indicate any errors.
```python
from APsystemsEZ1 import APsystemsEZ1M
import asyncio

# Initialize the inverter with the specified IP address and port number.
inverter = APsystemsEZ1M("192.168.178.168", 8050)

async def main():
    try:
        # Fetch output data from the inverter.
        response = await inverter.get_output_data()

        # Display power input from PV-Input 1 and 2.
        print("Power PV-Input 1: " + str(response.p1) + " W")
        print("Power PV-Input 2: " + str(response.p2) + " W")

        # Display total energy generation for the current day.
        print("Generation today " + str(round(response.e1 + response.e2, 3)) + " kWh")
    except Exception as e:
        # Handle any exceptions that occur during the data fetch and print the error.
        print(f"An error occurred: {e}")

# Run the main coroutine.
# This is the entry point of the script and it runs the main function in an asynchronous manner.
asyncio.run(main())

```
---

- More examples can be found in our Wiki.

## Methods
The library includes several methods to interact with the microinverter. You can find all of them with comprehensive docs ion our GitHub Pages.

* `get_device_info()`: Retrieves detailed information about the device.
* `get_alarm_info()`: Fetches the alarm status information for various components of the device.
* `get_output_data()`: Retrieves the output data from the device.
* `get_total_energy_today()`: Retrieves the total energy generated today by inverter inputs.
* `get_total_energy_lifetime()`: Retrieves the total lifetime energy generated by inverter inputs.
* `get_max_power()`: Retrieves the set maximum power setting of the device.
* `set_max_power(power_limit)`: Sets the maximum power limit of the device.
* `get_device_power_status()`: Retrieves the current power status of the device.
* `set_device_power_status(power_status)`: Sets the power status of the device.
* **for a more detailed documentation see our GitHub Pages.**
## Recommendations
- We highly recommend to set a **static IP** for the inverter you want to interact with. This can be achieved be accessing your local router, searching for the inverters IP and setting it to "static ip" or similar. A quick Google search will tell you how to do it exactly for your specific router model.

## Contribute to this project
- Everyone is invited to commit changes to this library. This is considered a community project to realise countless projects that may need very specific new functionality. We're happy to see your ideas ;)
- You're also welcome to request new features to be built natively into the inverters API. We're in close contact with APsystems and happy to add new features in the future.
## License
This library is released under the MIT License.

---
