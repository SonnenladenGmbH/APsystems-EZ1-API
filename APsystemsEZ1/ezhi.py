from pydantic import BaseModel, Field, field_validator
from enum import IntEnum
from aiohttp import ClientSession
from aiohttp.http_exceptions import HttpBadRequest
from . import InverterReturnedError
from typing import Any


class ReturnDeviceInfo(BaseModel):
    deviceId: str
    dev_type: str  # Rename to type
    batteryCompany: str
    batteryModel: str
    batteryCapacity: float  # Needs casting from str
    devVer: str
    ssid: str  # Wifi SSID
    ip: str


class BatteryStatusEnum(IntEnum):
    IDLE = 1
    CHARGING = 2
    DISCHARGING = 3
    ERROR = 4
    SHUTDOWN = 5
    NO_COMMUNICATION = 6


class BatteryStatusData(BaseModel):
    battery_status: BatteryStatusEnum = Field(alias="batS")
    battery_state_of_charge: int = Field(alias="batSoc")  # Battery State of Charge in %
    battery_state_of_health: int = Field(alias="batSoh")  # Battery State of Health in %
    battery_temperature: int = Field(alias="batTemp")  # Battery Temperature in °C
    device_temperature: int = Field(alias="devTemp")  # Device Temperature in °C
    pv_input_power: int = Field(alias="pvP")  # PV input power
    total_input_energy: int = Field(alias="pvTE")  # Total input energy in kWh
    battery_power: int = Field(alias="batP")  # Battery power, may be negative
    total_charge_energy: int = Field(
        alias="batCTE"
    )  # Total battery charge energy in kWh
    total_discharge_energy: int = Field(
        alias="batDTE"
    )  # Total battery discharge energy in kWh
    on_grid_power: int = Field(alias="ogP")  # On-grid power, may be negative in Watts
    total_on_grid_output_energy: int = Field(
        alias="ogOTE"
    )  # Total on-grid output energy in kWh
    total_on_grid_input_energy: int = Field(
        alias="ogITE"
    )  # Total on-grid input energy in kWh
    off_grid_power: int = Field(alias="ofgP")  # Off-grid power in Watts
    total_off_grid_output_energy: int = Field(
        alias="ofgOTE"
    )  # Total off-grid output energy in kWh
    total_off_grid_input_energy: int = Field(
        alias="ofgITE"
    )  # Total off-grid input energy in kWh

    @field_validator("*", mode="before")
    def parse_int(cls, value: Any) -> int:
        return int(value)


class BatteryAlarmInfo(BaseModel):
    high_temp_protection: bool = Field(alias="BatHTP")  # High Temperature Protection
    low_temp_protection: bool = Field(alias="BatLTP")  # Low Temperature Protection
    communication_error: bool = Field(alias="BatCE")  # Communication Error
    battery_overvoltage: bool = Field(alias="BatHV")  # Battery Overvoltage
    battery_undervoltage: bool = Field(alias="BatLV")  # Battery Undervoltage
    battery_overcurrent: bool = Field(alias="BatHI")  # Battery Overcurrent
    battery_error: bool = Field(alias="BatE")  # Battery Error
    device_temp_protection: bool = Field(alias="DTP")  # Device Temperature Protection
    device_error: bool = Field(alias="EE")  # Device Error
    battery_shutdown: bool = Field(alias="sbs")  # Battery Shutdown
    ac_abnormal: bool = Field(alias="aca")  # AC Abnormal
    off_grid_overcurrent: bool = Field(alias="OfOI")  # Off-grid Overcurrent
    pv_high_voltage: bool = Field(alias="PvHV")  # PV High Voltage
    pv_overcurrent: bool = Field(alias="PvOC")  # PV Overcurrent
    ir_error: bool = Field(alias="IRDE")  # IRD Error
    pv_wiring_error: bool = Field(alias="PVWE")  # PV Wiring Error
    off_grid_short: bool = Field(alias="OfGs")  # Off-grid Short

    @field_validator("*", mode="before")
    def parse_bool(cls, value: Any) -> bool:
        return value == "1"


class APsystemsEZHI:
    def __init__(
        self,
        ip_address: str,
        port: int = 8050,
        timeout: int = 10,
        session: ClientSession | None = None,
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
                if retry:  # Re-run request when the inverter returned failed because of unknown reason
                    return await self._request(endpoint, retry=False)
                raise InverterReturnedError
        finally:
            # Close if session created on per-execution base

            if self.session is None:
                await ses.close()

    async def get_device_info(self) -> BatteryStatusData | None:
        response = await self._request("getDeviceInfo")
        return (
            BatteryStatusData.model_validate(response["data"])
            if response and response.get("data")
            else None
        )

    async def get_alarm_info(self) -> BatteryAlarmInfo | None:
        response = await self._request("getAlarm")
        return (
            BatteryAlarmInfo.model_validate(response["data"])
            if response and response.get("data")
            else None
        )