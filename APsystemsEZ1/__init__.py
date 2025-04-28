from dataclasses import dataclass
import re
import logging
import datetime
from aiohttp import ClientSession
from aiohttp.http_exceptions import HttpBadRequest

_LOGGER = logging.getLogger(__name__)

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
    isBatterySystem: bool


@dataclass
class ReturnAlarmInfo:
    offgrid: bool
    shortcircuit_1: bool
    shortcircuit_2: bool
    operating: bool


@dataclass
class ReturnOutputData:
    p1: float
    e1: float
    te1: float
    p2: float
    e2: float
    te2: float

    def __init__(self, **data):
        '''The data attribute needs to be set manually because the inverter local interface 
        may return more results than the existing data attributes (such as originalData),
          resulting in an error. '''
        self.p1 = data.get("p1", 0.0)
        self.e1 = data.get("e1", 0.0)
        self.te1 = data.get("te1", 0.0)
        self.p2 = data.get("p2", 0.0)
        self.e2 = data.get("e2", 0.0)
        self.te2 = data.get("te2", 0.0)

IS_BATTERY_REGEX = re.compile("^.*_b$")

class APsystemsEZ1M:
    """This class represents an EZ1 Microinverter and provides methods to interact with it
    over a network. The class allows for getting and setting various device parameters like
    power status, alarm information, device information, and power limits.
    """

    @dataclass
    class _DebounceVal:
        old_state: float = 0.0
        base_state: float = 0.0
        last_update: int = 0

    def __init__(
        self,
        ip_address: str,
        port: int = 8050,
        timeout: int = 10,
        max_power: int = 800,
        min_power: int = 30,
        session: ClientSession | None = None,
        enable_debounce: bool = False,
    ) -> None:
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
        self.max_power = max_power
        self.min_power = min_power
        self.enable_debounce = enable_debounce
        self._e1 = self._DebounceVal()
        self._e2 = self._DebounceVal()

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
                _LOGGER.debug("%s: %s", endpoint, data)

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

    def _debounce(self, state: _DebounceVal, new_state: float) -> float:
        """Recover total value in case state is reset during a day."""
        if (
            isinstance(state.old_state, float)
            and isinstance(new_state, float)
            and state.old_state > new_state
        ):
            state.base_state = state.base_state + state.old_state

        state.old_state = new_state

        # reset basis each day
        if state.last_update != datetime.datetime.now().day:
            state.last_update = datetime.datetime.now().day
            state.base_state = 0.0

        if isinstance(new_state, float):
            return new_state + state.base_state

        return new_state

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
                isBatterySystem=bool(IS_BATTERY_REGEX.match(response["data"]["devVer"]))
            )
            if response and response.get("data")
            else None
        )

    async def get_alarm_info(self) -> ReturnAlarmInfo | None:
        """
        Retrieves the alarm status information for various components of the device. This method
        makes a request to the "getAlarm" endpoint and returns a dictionary containing the alarm
        status for different parameters.


        The response contains the following attributes:
        - __offgrid__ (`bool`): Off-Grid Status
        _ __shortcircuit_1__ (`bool`): DC 1 Short Circuit Error status
        _ __shortcircuit_2__ (`bool`): DC 2 Short Circuit Error status
        - __operating__ (`bool`): All okay

        :return: Information about possible point of failures
        """
        response = await self._request("getAlarm")
        return (
            ReturnAlarmInfo(
                offgrid=bool(int(response["data"]["og"])),
                shortcircuit_1=bool(int(response["data"]["isce1"])),
                shortcircuit_2=bool(int(response["data"]["isce2"])),
                operating=not bool(int(response["data"]["oe"])),
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
        if response:
            response["data"] = {
                key: float(value)
                if isinstance(value, int)
                else value
                for key, value
                in response["data"].items()
            }

        if self.enable_debounce and response:
            response["data"].update(
                {
                    "e1": self._debounce(self._e1, response["data"]["e1"]),
                    "e2": self._debounce(self._e2, response["data"]["e2"]),
                }
            )

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
        if not self.min_power <= power_limit <= self.max_power:
            raise ValueError(
                f"Invalid setMaxPower value: expected int between '30' and '800', got '{power_limit}'"
            )
        request = await self._request(f"setMaxPower?p={power_limit}")
        return int(request["data"]["maxPower"]) if request else None

    async def get_device_power_status(self) -> bool:
        """
        Retrieves the current power status of the device. This method sends a request to the
        "getOnOff" endpoint and returns a dictionary containing the power status of the device.

        The 'data' field in the returned dictionary includes the 'status' key, representing the
        current power status of the device, where '0' indicates that the device is on, and '1'
        indicates that it is off.

        :return: 0/normal when on, 1/alarm when off
        """
        response = await self._request("getOnOff")

        match (status := response["data"]["status"]):
            case int():
                return not bool(status)
            case str() if status.isdigit():
                return not bool(int(status))
            case _:
                raise InverterReturnedError

    async def set_device_power_status(self, power_status: bool) -> bool | None:
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
        if power_status:
            status_value = "0"
        else:
            status_value = "1"
        request = await self._request(f"setOnOff?status={status_value}")
        return not bool(int(request["data"]["status"])) if request else None
