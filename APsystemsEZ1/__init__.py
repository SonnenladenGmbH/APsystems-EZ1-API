from dataclasses import dataclass
from enum import IntEnum

from aiohttp import ClientSession
from aiohttp.http_exceptions import HttpBadRequest


class Status(IntEnum):
    normal = 0
    alarm = 1


class InverterReturnedError(Exception):
    pass


@dataclass
class ReturnDeviceInfo:
    deviceId: str
    devVer: str
    ssid: str
    ipAddr: str
    minPower: int
    maxPower: int


@dataclass
class ReturnAlarmInfo:
    og: Status
    isce1: Status
    isce2: Status
    oe: Status


@dataclass
class ReturnOutputData:
    p1: float
    e1: float
    te1: float
    p2: float
    e2: float
    te2: float


class APsystemsEZ1M:
    """This class represents an EZ1 Microinverter and provides methods to interact with it
    over a network. The class allows for getting and setting various device parameters like
    power status, alarm information, device information, and power limits.
    """

    def __init__(
        self,
        ip_address: str,
        port: int = 8050,
        timeout: int = 10,
        session: ClientSession | None = None,
    ):
        """
        Initializes a new instance of the EZ1Microinverter class with the specified IP address
        and port.

        :param ip_address: The IP address of the EZ1 Microinverter.
        :param port: The port on which the microinverter's server is running. Default is 8050.
        :param timeout: The timeout for all requests. The default of 10 seconds should be plenty.
        """
        self.base_url = f"http://{ip_address}:{port}"
        self.timeout = timeout
        self.session = session

    async def _request(self, endpoint: str, retry: bool | None = True) -> dict | None:
        """
        A private method to send HTTP requests to the specified endpoint of the microinverter.
        This method is used internally by other class methods to perform GET or POST requests.

        :param endpoint: The API endpoint to make the request to.

        :return: The JSON response from the microinverter as a dictionary.
        :raises: Prints an error message if the HTTP request fails for any reason.
        """
        url = f"{self.base_url}/{endpoint}"
        if self.session is None:
            ses = ClientSession()
        else:
            ses = self.session
        try:
            async with ses.get(url, timeout=self.timeout) as resp:
                data = await resp.json()

                # Handle reponse
                if resp.status != 200:
                    raise HttpBadRequest(f"HTTP Error: {resp.status}")
                if data["message"] == "SUCCESS":
                    return data
                if (
                    retry
                ):  # Re-run request when the inverter returned failed because of unknown reason
                    return await self._request(endpoint, retry=False)
                raise InverterReturnedError
        finally:
            # Close if session created on per-execution base

            if self.session is None:
                await ses.close()

    async def get_device_info(self) -> ReturnDeviceInfo | None:
        """
        Retrieves detailed information about the device. This method sends a request to the
        "getDeviceInfo" endpoint and returns a dictionary containing various details about the device.

        The returned data includes the device ID, device version, the SSID it is connected to, its IP
        address, and its minimum and maximum power settings. This information can be used for monitoring
        and configuring the device.

        The response contains the following attributes:

        - __deviceId__ (`str`): The unique identifier for the device.
        - __devVer__ (`str`): The version of the device firmware or software.
        - __ssid__ (`str`): The SSID of the network to which the device is currently connected.
        - __ipAddr__ (`str`): The current IP address of the device.
        - __minPower__ (`int`): The minimum power output that the device can be set to, measured in watts.
        - __maxPower__ (`int`): The maximum power output that the device can be set to, also in watts.



        :return: Different information about the inverter
        :rtype: ReturnDeviceInfo

        """
        response = await self._request("getDeviceInfo")
        return (
            ReturnDeviceInfo(
                deviceId=response["data"]["deviceId"],
                devVer=response["data"]["devVer"],
                ssid=response["data"]["ssid"],
                ipAddr=response["data"]["ipAddr"],
                minPower=int(response["data"]["minPower"]),
                maxPower=int(response["data"]["maxPower"]),
            )
            if response and response.get("data")
            else None
        )

    async def get_alarm_info(self) -> ReturnAlarmInfo | None:
        """
        Retrieves the alarm status information for various components of the device. This method
        makes a request to the "getAlarm" endpoint and returns a dictionary containing the alarm
        status for different parameters.

        The 'data' field in the returned dictionary includes the status of several components,
        each represented as a string indicating whether there is an alarm ('1') or normal operation ('0').

        The response contains the following attributes:
        - __og__ (`Status`): Off-Grid Status (normal/0 when okay)
        _ __isce1__ (`Status`): DC 1 Short Circuit Error status (normal/0 when okay)
        _ __isce2__ (`Status`): DC 2 Short Circuit Error status (normal/0 when okay)
        - __oe__ (`Status`): Output fault status (normal/0 when okay)

        :return: Information about possible point of failures
        """
        response = await self._request("getAlarm")
        return (
            ReturnAlarmInfo(
                og=Status(int(response["data"]["og"])),
                isce1=Status(int(response["data"]["isce1"])),
                isce2=Status(int(response["data"]["isce2"])),
                oe=Status(int(response["data"]["oe"])),
            )
            if response
            else None
        )

    async def get_output_data(self) -> ReturnOutputData | None:
        """
        Retrieves the output data from the device. This method calls a private method `_request`
        with the endpoint "getOutputData" to fetch the device's output data.

        The returned data includes various parameters such as power output status ('p1', 'p2'),
        energy readings ('e1', 'e2'), and total energy ('te1', 'te2') for two different inputs
        of the inverter. Additionally, it provides a status message and the device ID.

        The response contains the following attributes:
        - __p1__ (`float`): Power output status of inverter input 1
        - __e1__ (`float`): Energy reading for inverter input 1
        - __te1__ (`float`): Total energy for inverter input 1
        - __p2__ (`float`): Power output status of inverter input 2
        - __e2__ (`float`): Energy reading for inverter input 2
        - __te2__ (`float`): Total energy for inverter input 2

        :return: Information about energy/power-related information
        """
        response = await self._request("getOutputData")
        return ReturnOutputData(**response["data"]) if response else None

    async def get_total_output(self) -> float | None:
        """
        Retrieves and calculates the combined power output status of inverter inputs 1 and 2.
        This method first calls get_output_data() to fetch the output data from the device, which
        includes individual power output values for 'p1' and 'p2'. It then sums these values to
        provide the total combined power output.

        :return: The sum of power output values 'p1' and 'p2' as a float.
        """
        data = await self.get_output_data()
        return float(data.p1 + data.p2) if data else None

    async def get_total_energy_today(self) -> float | None:
        """
        Retrieves and calculates the total energy generated today by both inverter inputs, 1 and 2.
        This method first calls get_output_data() to fetch the output data from the device, which
        includes individual energy readings for 'e1' and 'e2', each representing the energy in
        kilowatt-hours (kWh) generated by the respective inverter inputs.

        :return: The sum of the energy readings 'e1' and 'e2' as a float, representing the total energy
                 generated today in kWh by both inverter inputs.
        """
        data = await self.get_output_data()
        return float(data.e1 + data.e2) if data else None

    async def get_total_energy_lifetime(self) -> float | None:
        """
        Retrieves and calculates the total lifetime energy generated by both inverter inputs 1 and 2.
        This method first calls get_output_data() to fetch the output data from the device, which
        includes individual lifetime energy readings for 'te1' and 'te2'. Each of these values
        represents the total lifetime energy generated by the respective inverter inputs, reported
        in kilowatt-hours (kWh).

        :return: The sum of the lifetime energy readings 'te1' and 'te2' as a float, representing the
                 total lifetime energy in kWh generated by both inverter inputs.
        """
        data = await self.get_output_data()
        return float(data.te1 + data.te2) if data else None

    async def get_max_power(self) -> int | None:
        """Retrieves the set maximum power setting of the device. This method makes a request to the
        "getMaxPower" endpoint and returns a dictionary containing the maximum power limit of the device set by the user.

        :return: Max output power in watts
        """
        response = await self._request("getMaxPower")
        if response is None or response["data"]["maxPower"] == "":
            return None
        return int(response["data"]["maxPower"])

    async def set_max_power(self, power_limit: int) -> int | None:
        """
        Sets the maximum power limit of the device. This method sends a request to the "setMaxPower"
        endpoint with the specified power limit as a parameter. The power limit must be an integer
        within the range of 30 to 800 watts.

        If the provided power limit is outside this range, the method raises a ValueError.

        :param power_limit: The desired maximum power setting for the device, in watts.
                            Must be an integer between 30 and 800.

        :return: (Newly) set max output power in watts
        :raises ValueError: If 'power_limit' is not within the range of 30 to 800.

        The key in the 'data' object is:
        - 'maxPower': Indicates the newly set maximum power output of the device in watts.
        """
        if not 30 <= power_limit <= 800:
            raise ValueError(
                f"Invalid setMaxPower value: expected int between '30' and '800', got '{power_limit}'"
            )
        request = await self._request(f"setMaxPower?p={power_limit}")
        return int(request["data"]["maxPower"]) if request else None

    async def get_device_power_status(self) -> Status | None:
        """
        Retrieves the current power status of the device. This method sends a request to the
        "getOnOff" endpoint and returns a dictionary containing the power status of the device.

        The 'data' field in the returned dictionary includes the 'status' key, representing the
        current power status of the device, where '0' indicates that the device is on, and '1'
        indicates that it is off.

        :return: 0/normal when on, 1/alarm when off
        """
        response = await self._request("getOnOff")
        return Status(int(response["data"]["status"])) if response else None

    async def set_device_power_status(
        self, power_status: Status | None
    ) -> Status | None:
        """
        Sets the power status of the device to either on or off. This method sends a request to the
        "setOnOff" endpoint with a specified power status parameter. The power status accepts multiple
        string representations: '0' or 'ON' to start the inverter, and '1', 'SLEEP', or 'OFF' to stop
        the inverter.

        If the provided power status does not match any of the accepted representations, the method
        raises a ValueError with a descriptive message.

        :param power_status: The desired power status for the device, specified as '0', 'ON' for
                             starting the inverter, or '1', 'SLEEP', 'OFF' for stopping it.
        :return: 0/normal when on, 1/alarm when off
        :raises ValueError: If 'power_status' does not match the accepted values. The error message
                            explains the valid values and their meanings.

        Note: Internally, the method treats '0' and 'ON' as equivalent, both setting the power status
        to '0'. Similarly, '1', 'SLEEP', and 'OFF' are treated as equivalent, setting the power status
        to '1'.
        """
        status_map = {"0": "0", "ON": "0", "1": "1", "SLEEP": "1", "OFF": "1"}
        status_value = status_map.get(str(power_status))
        if status_value is None:
            raise ValueError(
                f"Invalid power status: expected '0', 'ON' or '1','SLEEP' or 'OFF', got '{str(power_status)}"
                + "'\n Set '0' or 'ON' to start the inverter | Set '1' or 'SLEEP' or 'OFF' to stop the inverter."
            )
        request = await self._request(f"setOnOff?status={status_value}")
        return Status(int(request["data"]["status"])) if request else None
