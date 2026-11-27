## Introduction to APsystems EZ1M Python Library

Welcome to the documentation for the APsystems EZ1M Python Library. This library provides a comprehensive interface for interacting with the EZ1 Microinverters from APsystems. Designed with simplicity and efficiency in mind, it enables users to easily monitor and control various aspects of their EZ1 Microinverters over a network.

## Key Features

- **Device Information Retrieval:** Fetch detailed information about your microinverter, including device ID, firmware version, network details, and power settings.<br><br>
- **Alarm Status Monitoring:** Keep track of the alarm status for critical components, ensuring timely identification and response to potential issues.<br><br>
- **Output Data Analysis:** Access real-time data on power output, energy readings, and total energy accumulation for efficient energy management.<br><br>
- **Power Management:** Adjust and monitor the power output settings of your microinverter to optimize performance.<br><br>
- **Network Communication:** Utilize the async capabilities of Python to communicate with your device seamlessly over a network.

## Lake 6 series

The `APsystemsEZ1.lake6` module covers the local API of the Lake 6 balcony
battery. It lives in the same package because both devices expose a local API of
the same vendor, but it has its own transport: Lake 6 answers with
`{"data": ..., "code": 200}` envelopes, so success is decided by the business
code in the body rather than by the HTTP status.

```python
import asyncio

import aiohttp

from APsystemsEZ1.lake6 import Lake6ApiClient


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        client = Lake6ApiClient("192.168.1.100", session)
        device = await client.async_get_device()
        energies = await client.async_get_energies()
        print(device.dev_id, energies.battery_soc)


asyncio.run(main())
```

The parsed payload helpers (`parse_device`, `parse_energies`, `parse_alarms`,
`parse_modes`, `parse_control_panel`) and the time-of-use text format
(`parse_plan`, `render_plan`, `build_payload`) are exposed by the same module.
