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
- and much more...

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
<td align="center"><img src="assets/images/APsystems-EZ1-M.png" alt="APsystems EZ1-M Inverter" width="150" /></td>
<td align="center">
<p><strong>APsystems EZ1-M</strong></p>
<p>(Firmware: V1.17)</p>
</td>
<td align="center"><img src="https://img.icons8.com/color/48/000000/checkmark.png" alt="Compatible-Checkmark" width="30" /></td>
<td align="center"><a href="https://www.sonnenladen.de/APsystems-EZ1-M-600-800-W-Mikrowechselrichter-ohne-Anschlusskabel/AP-07-000-0" target="_blank" rel="noopener"><strong>Sonnenladen GmbH - Online Shop</strong></a><br /><a href="https://www.sonnenladen.de/APsystems-EZ1-M-600-800-W-Mikrowechselrichter-ohne-Anschlusskabel/AP-07-000-0" target="_blank" rel="noopener">IN STOCK | AUF LAGER</a></td>
</tr>
</tbody>
</table>

## Setup your Inverter
The local API access needs to be activated once in the settings of the EZ1. Please follow our Step-By-Step Guide to do so:
<p><img src="assets/images/APsystems-Lokale-API-Aktivieren-Schritt1-3.png" alt="APsystems EZ1-M Inverter" width="820" /></p>
<ul>
<li>Step 1: Connect to the inverter using the "Direct Connection" method.</li>
<li>Step 2: Establish a connection with your inverter.</li>
<li>Step 3: Select the Settings menu.</li>
</ul>
<p><img src="assets/images/APsystems-Lokale-API-Aktivieren-Schritt4-6.png" alt="APsystems EZ1-M Inverter" width="820" /></p>
<ul>
<li>Step 4: Switch to the "Local Mode" section.</li>
<li>Step 5: Activate local mode and select "Continuous"</li>
<li>Step 6: Done! Make a note of the IP address for future reference.</li>
(To ensure a successful connection to your Wi-Fi network, it's essential to first set up your device using the standard procedure outlined in the APsystems Quickstart Guide. This initial setup is a crucial step before proceeding with any further configurations or usage.)
</ul>

## Installation
- To use the APsystemsEZ1 library, you need to have Python >=3.8 installed on your system.
- - See the following guide to install the latest Python release: https://www.python.org/downloads/
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
<p>Python 3.8</p>
<p>Python 3.9</p>
<p>Python 3.10</p>
<p>Python 3.11</p>
<p>Python 3.12</p>
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

## Usage
Here's a quick example of how to use the APsystemsEZ1 library:

```python
from APsystemsEZ1 import APsystemsEZ1M # import the library
import asyncio # this is an async based lib so we have to import asynchio

inverter = APsystemsEZ1M("192.168.1.100", 8050) # initialize an inverter on "192.168.1.100"

async def main():
    # Get device information
    device_info = await inverter.get_device_info()
    print("Device Information:", device_info)

    # Get device information
    device_info = await inverter.get_device_info()
    print("Device Information:", device_info)

    # Get alarm information
    alarm_info = await inverter.get_alarm_info()
    print("Alarm Information:", alarm_info)

    # Get output data
    output_data = await inverter.get_output_data()
    print("Output Data:", output_data)

    # Set maximum power limit
    await inverter.set_max_power(500)

    # Get current power status
    power_status = await inverter.get_device_power_status()
    print("Power Status:", power_status)

# Run the main coroutine
asyncio.run(main())
```

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
* for a more detailed documentation see our GitHub Pages.
## Recommendations
- We highly recommend to set a **static IP** for the inverter you want to interact with. This can be achieved be accessing your local router, searching for the inverters IP and setting it to "static ip" or similar. A quick Google search will tell you how to do it exactly for your specific router model.
## Error Handling
The library includes basic error handling for HTTP and connection errors.

## Contribute to this project
- Everyone is invited to commit changes to this library. This is considered a community project to realise countless projects that may need very specific new functionality. We're happy to see your ideas ;)
- You're also welcome to request new features to be built natively into the inverters API. We're in close contact with APsystems and happy to add new features in the future.
## License
This library is released under the MIT License.

---
