"""Tests for the Lake_6 local API client."""

from http import HTTPStatus
from typing import Any

import aiohttp
import pytest

from APsystemsEZ1.lake6 import (
    Lake6ApiClient,
    Lake6ApiError,
    Lake6TouRule,
    parse_alarms,
    parse_control_panel,
    parse_device,
    parse_energies,
    parse_modes,
)
from APsystemsEZ1.lake6.const import LAKE6_DEFAULT_PORT

DEV_ID = "LAKE6_SERIAL_NUMBER"

DEVICES: dict[str, object] = {
    "dev_id": DEV_ID,
    "type": "Ema",
    "dev_ver": "V1.5.2",
    "bat_cap": "5.0",
    "rssi": -52,
}

ENERGIES: dict[str, object] = {
    "bat_soc": "30.0",
    "bat_temp": "25.0",
    "dev_temp": "31.0",
    "bat_impE": "57.28800",
    "bat_expE": "12.50000",
    "ongrid_expE": "100.10000",
    "ongrid_impE": "200.20000",
    "offgrid_expE": "0.00000",
    "offgrid_impE": "0.00000",
    "bat_power": "-486",
    "ongrid_power": "1200",
    "offgrid_power": "0",
    "bat_status": "2",
}

ALARMS: dict[str, object] = {
    "bat_overtemp": "1",
    "bat_undertemp": "0",
    "bat_comm_err": "0",
    "bat_overvolt": "0",
    "bat_undervolt": "0",
    "bat_overcur": "0",
    "bat_ie": "0",
    "dev_temp": "0",
    "dev_sys_err": "0",
    "bat_shutdown": "0",
    "grid_anomaly": "0",
    "offgrid_overcur": "0",
    "offgrid_shortcir": "0",
    "bat_cal": "0",
}

MODES: dict[str, object] = {
    "mode": "3",
    "eco": "0",
    "dod": "15",
    "time_cfg": [
        {
            "E": "1",
            "W": [1, 2, 3, 4, 5],
            "TM": [{"T": "09000910", "F": "2", "FI": {"P": "200", "GD": 1}}],
        },
        {"E": "1", "W": [6, 7], "TM": [{"T": "10001010", "F": "3", "FI": {}}]},
    ],
}

IDLE: dict[str, object] = {"mode": "0", "MI1": {}}

ACTIVE: dict[str, object] = {
    "mode": "1",
    "MI1": {
        "time": ["2026112510000020261125103000"],
        "power": ["500"],
    },
}


class FakeResponse:
    """Minimal stand-in for an aiohttp response."""

    def __init__(
        self,
        body: Any = None,
        status: int = HTTPStatus.OK,
        *,
        invalid_json: bool = False,
    ) -> None:
        """Initialize the response."""
        self._body = body
        self.status = status
        self._invalid_json = invalid_json

    async def json(self, content_type: str | None = None) -> Any:
        """Return the canned body, or blow up like a broken body does."""
        if self._invalid_json:
            raise ValueError("not json")
        return self._body


class FakeRequest:
    """Async context manager handed out by FakeSession.request."""

    def __init__(self, response: FakeResponse) -> None:
        """Initialize the request."""
        self._response = response

    async def __aenter__(self) -> FakeResponse:
        """Enter the response context."""
        return self._response

    async def __aexit__(self, *exc_info: object) -> None:
        """Leave the response context."""


class FakeSession:
    """Records calls and replays canned responses in order."""

    def __init__(
        self,
        *responses: FakeResponse,
        error: Exception | None = None,
    ) -> None:
        """Initialize the session."""
        self._responses = list(responses)
        self._error = error
        self.calls: list[tuple[str, str, Any]] = []

    def request(self, method: str, url: str, **kwargs: Any) -> FakeRequest:
        """Record the call and return the next canned response."""
        self.calls.append((method, url, kwargs.get("json")))
        if self._error is not None:
            raise self._error
        return FakeRequest(self._responses.pop(0))


def _client(session: FakeSession, port: int = LAKE6_DEFAULT_PORT) -> Lake6ApiClient:
    return Lake6ApiClient("127.0.0.1", session, port)  # type: ignore[arg-type]


def test_parse_device() -> None:
    """A /devices payload is decoded."""
    device = parse_device(DEVICES)

    assert device.dev_id == DEV_ID
    assert device.device_type == "Ema"
    assert device.sw_version == "V1.5.2"
    assert device.battery_capacity == 5.0
    assert device.rssi == -52


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param({}, id="missing"),
        pytest.param({"dev_id": ""}, id="blank"),
        pytest.param({"dev_id": 1}, id="not-a-string"),
    ],
)
def test_parse_device_requires_dev_id(payload: dict[str, object]) -> None:
    """A payload without a usable device id is rejected."""
    with pytest.raises(ValueError, match="no usable dev_id"):
        parse_device(payload)


def test_parse_device_blank_firmware() -> None:
    """An empty firmware version becomes None so the row can be hidden."""
    device = parse_device({"dev_id": DEV_ID, "dev_ver": "  "})

    assert device.sw_version is None
    assert device.device_type == ""


def test_parse_device_ignores_non_string_firmware() -> None:
    """A firmware field that is not text is ignored instead of raising."""
    device = parse_device({"dev_id": DEV_ID, "dev_ver": 152})

    assert device.sw_version is None


def test_parse_energies() -> None:
    """The /energies payload is decoded, ints and floats apart."""
    energies = parse_energies(ENERGIES)

    assert energies.battery_soc == 30.0
    assert energies.battery_temperature == 25.0
    assert energies.device_temperature == 31.0
    assert energies.battery_charge_energy == 57.288
    assert energies.battery_discharge_energy == 12.5
    assert energies.grid_export_energy == 100.1
    assert energies.grid_import_energy == 200.2
    assert energies.offgrid_export_energy == 0.0
    assert energies.offgrid_import_energy == 0.0
    # Power fields are plain integers on the wire.
    assert energies.battery_power == -486
    assert energies.grid_power == 1200
    assert energies.offgrid_power == 0
    assert energies.battery_status == "charging"


@pytest.mark.parametrize(
    "value",
    [
        pytest.param("not-a-number", id="text"),
        pytest.param("NaN", id="nan"),
        pytest.param("inf", id="infinity"),
        pytest.param(None, id="null"),
        pytest.param(True, id="bool"),
        pytest.param([], id="list"),
    ],
)
def test_parse_energies_drops_unusable_numbers(value: object) -> None:
    """One bad field becomes None without affecting the response."""
    energies = parse_energies({"bat_soc": value, "bat_power": value})

    assert energies.battery_soc is None
    assert energies.battery_power is None


def test_parse_energies_accepts_json_numbers() -> None:
    """Numbers and numeric strings are both accepted."""
    energies = parse_energies({"bat_soc": 30, "bat_power": "486.7"})

    assert energies.battery_soc == 30.0
    # Fractional power is truncated, matching how the device rounds.
    assert energies.battery_power == 486


def test_parse_alarms() -> None:
    """The /alarms payload is decoded to booleans."""
    alarms = parse_alarms(ALARMS)

    assert alarms.battery_over_temperature is True
    assert alarms.battery_under_temperature is False
    assert alarms.device_temperature_protection is False


def test_parse_alarms_accepts_ints() -> None:
    """The device quoting is not relied upon."""
    alarms = parse_alarms({"bat_overtemp": 1, "bat_undertemp": 0, "bat_ie": 2})

    assert alarms.battery_over_temperature is True
    assert alarms.battery_under_temperature is False
    assert alarms.battery_internal_error is None


def test_parse_alarms_accepts_bools() -> None:
    """JSON booleans are taken as they are."""
    alarms = parse_alarms({"bat_overtemp": True, "bat_undertemp": False})

    assert alarms.battery_over_temperature is True
    assert alarms.battery_under_temperature is False


def test_parse_modes() -> None:
    """The /modes payload is decoded, including the schedule."""
    modes = parse_modes(MODES)

    assert modes.operating_mode == "time_of_use"
    assert modes.eco is False
    assert modes.depth_of_discharge == 15
    assert len(modes.time_cfg) == 2
    assert modes.tou_rules == [
        Lake6TouRule(
            enabled=True,
            weekdays=[1, 2, 3, 4, 5],
            start="09:00",
            end="09:10",
            function="discharge",
            power=200,
        ),
        Lake6TouRule(
            enabled=True,
            weekdays=[6, 7],
            start="10:00",
            end="10:10",
            function="self_consumption",
            power=None,
        ),
    ]


def test_parse_modes_unknown_codes() -> None:
    """Unknown enumerations do not break the data layer."""
    modes = parse_modes({"mode": "9", "eco": "yes", "dod": "abc", "time_cfg": "x"})

    assert modes.operating_mode is None
    assert modes.eco is None
    assert modes.depth_of_discharge is None
    assert modes.time_cfg == []
    assert modes.tou_rules == []


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(3, "time_of_use", id="int-code"),
        pytest.param({}, None, id="not-a-code"),
    ],
)
def test_parse_modes_reads_int_codes(value: object, expected: str | None) -> None:
    """An int code reads like its string form; other types are ignored."""
    assert parse_modes({"mode": value}).operating_mode == expected


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(float("nan"), id="nan"),
        pytest.param({}, id="not-a-number"),
    ],
)
def test_parse_modes_ignores_unusable_dod(value: object) -> None:
    """A depth of discharge that is not a finite number becomes None."""
    assert parse_modes({"dod": value}).depth_of_discharge is None


@pytest.mark.parametrize(
    "time_range",
    [
        pytest.param("24600000", id="hour-out-of-range"),
        pytest.param("09600000", id="minute-out-of-range"),
    ],
)
def test_parse_modes_drops_out_of_range_slots(time_range: str) -> None:
    """An impossible start time is dropped instead of raising."""
    modes = parse_modes(
        {"time_cfg": [{"E": "1", "W": [1], "TM": [{"T": time_range, "F": "2"}]}]}
    )

    assert modes.tou_rules[0].start is None


def test_parse_modes_drops_non_object_rules() -> None:
    """A schedule entry that is not an object is dropped."""
    modes = parse_modes({"time_cfg": ["junk"]})

    assert modes.time_cfg == []
    assert modes.tou_rules == []


def test_parse_control_panel_idle() -> None:
    """An idle panel reports no window and no timestamp width."""
    panel = parse_control_panel(IDLE)

    assert panel.active is False
    assert panel.windows == []
    assert panel.timestamp_width is None


def test_parse_control_panel_active() -> None:
    """A running window is decoded, 28 digits echoed back as 28."""
    panel = parse_control_panel(ACTIVE)

    assert panel.active is True
    assert panel.timestamp_width == 14
    assert len(panel.windows) == 1
    window = panel.windows[0]
    assert window.start.isoformat() == "2026-11-25T10:00:00"
    assert window.end.isoformat() == "2026-11-25T10:30:00"
    assert window.power == 500


def test_parse_control_panel_minute_form() -> None:
    """The 24 digit form from the manual is accepted."""
    panel = parse_control_panel(
        {"mode": "1", "MI1": {"time": ["202611251000202611251030"], "power": ["0"]}}
    )

    assert panel.timestamp_width == 12
    assert panel.windows[0].start.isoformat() == "2026-11-25T10:00:00"
    assert panel.windows[0].end.isoformat() == "2026-11-25T10:30:00"


def test_parse_control_panel_drops_malformed_pairs() -> None:
    """A power without its slot does not shift the following pairs."""
    panel = parse_control_panel(
        {
            "mode": "1",
            "MI1": {
                "time": ["2026112510000020261125103000", "garbage"],
                "power": ["500", "20"],
            },
        }
    )

    assert len(panel.windows) == 1
    assert panel.windows[0].power == 500


@pytest.mark.parametrize(
    "entry",
    [
        pytest.param(2026112510000020261125103000, id="not-a-string"),
        pytest.param("2026132510000020261325103000", id="month-out-of-range"),
    ],
)
def test_parse_control_panel_drops_invalid_windows(entry: object) -> None:
    """A non-string or impossible timestamp is dropped like a malformed one."""
    panel = parse_control_panel(
        {"mode": "1", "MI1": {"time": [entry], "power": ["500"]}}
    )

    assert panel.windows == []


def test_parse_control_panel_keeps_leftover_width_when_idle() -> None:
    """The width is read even though the leftover window is not reported."""
    panel = parse_control_panel(ACTIVE | {"mode": "0"})

    assert panel.active is False
    assert panel.windows == []
    assert panel.timestamp_width == 14


@pytest.mark.asyncio
async def test_async_get_returns_data_object() -> None:
    """A success envelope yields its `data` object."""
    session = FakeSession(
        FakeResponse({"data": {"a": 1}, "code": 200, "message": "SUCCESS"})
    )

    assert await _client(session).async_get("/devices") == {"a": 1}
    assert session.calls == [
        ("GET", f"http://127.0.0.1:{LAKE6_DEFAULT_PORT}/devices", None)
    ]


@pytest.mark.asyncio
async def test_async_get_uses_custom_port() -> None:
    """The port given at construction replaces the default."""
    session = FakeSession(FakeResponse({"data": {}, "code": 200}))

    await _client(session, 8080).async_get("/devices")

    assert session.calls[0][1] == "http://127.0.0.1:8080/devices"


@pytest.mark.asyncio
async def test_async_get_raises_on_error_code() -> None:
    """A non-success business code becomes a Lake6ApiError carrying the code."""
    session = FakeSession(
        FakeResponse({"data": {}, "code": 1002, "message": "FAILED"})
    )

    with pytest.raises(Lake6ApiError, match="data format error") as err:
        await _client(session).async_get("/devices")

    assert err.value.code == 1002


@pytest.mark.asyncio
async def test_async_get_rejects_missing_code() -> None:
    """A body without a numeric code is never treated as success."""
    session = FakeSession(FakeResponse({"data": {"a": 1}, "message": "SUCCESS"}))

    with pytest.raises(Lake6ApiError, match="no numeric code"):
        await _client(session).async_get("/devices")


@pytest.mark.asyncio
async def test_control_panel_accepts_missing_code() -> None:
    """/control-panels may omit `code`; the message is then the only signal."""
    session = FakeSession(
        FakeResponse({"data": {"mode": "0", "MI1": {}}, "message": "SUCCESS"})
    )

    assert await _client(session).async_get("/control-panels", code_optional=True) == {
        "mode": "0",
        "MI1": {},
    }


@pytest.mark.asyncio
async def test_control_panel_rejects_missing_code_when_not_ok() -> None:
    """A missing code with a non-success message still fails."""
    session = FakeSession(
        FakeResponse({"data": {"mode": "0"}, "message": "OPERATION FAILED"})
    )

    with pytest.raises(Lake6ApiError, match="reported 'OPERATION FAILED'"):
        await _client(session).async_get("/control-panels", code_optional=True)


@pytest.mark.asyncio
async def test_non_ok_http_status_raises() -> None:
    """HTTP failures are surfaced before the body is parsed."""
    session = FakeSession(FakeResponse({"code": 200}, status=HTTPStatus.INTERNAL_SERVER_ERROR))

    with pytest.raises(Lake6ApiError, match="HTTP 500"):
        await _client(session).async_get("/devices")


@pytest.mark.asyncio
async def test_invalid_json_raises() -> None:
    """A body that is not JSON is reported as such."""
    session = FakeSession(FakeResponse(invalid_json=True))

    with pytest.raises(Lake6ApiError, match="invalid JSON"):
        await _client(session).async_get("/devices")


@pytest.mark.asyncio
async def test_non_object_body_raises() -> None:
    """A JSON array is not an envelope."""
    session = FakeSession(FakeResponse(["data"]))

    with pytest.raises(Lake6ApiError, match="non-object body"):
        await _client(session).async_get("/devices")


@pytest.mark.asyncio
async def test_missing_data_object_raises() -> None:
    """A body without a `data` object fails before parsing."""
    session = FakeSession(FakeResponse({"code": 200, "data": []}))

    with pytest.raises(Lake6ApiError, match="no data object"):
        await _client(session).async_get("/devices")


@pytest.mark.asyncio
async def test_timeout_maps_to_api_error() -> None:
    """A timeout on the wire becomes a Lake6ApiError with the endpoint."""
    session = FakeSession(error=TimeoutError())

    with pytest.raises(Lake6ApiError, match="timed out"):
        await _client(session).async_get("/devices")


@pytest.mark.asyncio
async def test_client_error_maps_to_api_error() -> None:
    """An aiohttp failure becomes a Lake6ApiError with the reason."""
    session = FakeSession(error=aiohttp.ClientConnectionError("boom"))

    with pytest.raises(Lake6ApiError, match="failed: boom"):
        await _client(session).async_get("/devices")


@pytest.mark.asyncio
async def test_get_device_parse_failure_wraps_value_error() -> None:
    """A malformed /devices payload becomes a Lake6ApiError, not a ValueError."""
    session = FakeSession(FakeResponse({"code": 200, "data": {}}))

    with pytest.raises(Lake6ApiError, match="no usable dev_id"):
        await _client(session).async_get_device()


@pytest.mark.parametrize(
    ("method", "endpoint", "payload"),
    [
        pytest.param("async_get_device", "/devices", DEVICES, id="devices"),
        pytest.param("async_get_energies", "/energies", ENERGIES, id="energies"),
        pytest.param("async_get_alarms", "/alarms", ALARMS, id="alarms"),
        pytest.param("async_get_modes", "/modes", MODES, id="modes"),
        pytest.param(
            "async_get_control_panel",
            "/control-panels",
            ACTIVE,
            id="control-panels",
        ),
    ],
)
@pytest.mark.asyncio
async def test_async_get_helpers_hit_their_endpoint(
    method: str, endpoint: str, payload: dict[str, object]
) -> None:
    """Every convenience getter reads its own endpoint and parses the answer."""
    session = FakeSession(FakeResponse({"code": 200, "data": payload}))

    result = await getattr(_client(session), method)()

    assert result is not None
    assert session.calls == [
        ("GET", f"http://127.0.0.1:{LAKE6_DEFAULT_PORT}{endpoint}", None)
    ]


@pytest.mark.asyncio
async def test_async_set_modes_posts_payload() -> None:
    """Writers POST the payload as JSON and accept the success envelope."""
    session = FakeSession(FakeResponse({"data": {}, "code": 200}))

    await _client(session).async_set_modes(time_cfg=[{"E": "1"}])

    method, url, payload = session.calls[0]
    assert method == "POST"
    assert url == f"http://127.0.0.1:{LAKE6_DEFAULT_PORT}/modes"
    assert payload == {"time_cfg": [{"E": "1"}]}


@pytest.mark.asyncio
async def test_set_control_panel_posts_payload() -> None:
    """A manual control write accepts the message-only envelope."""
    session = FakeSession(FakeResponse({"message": "SUCCESS"}))
    payload = {"mode": "0", "MI1": {}}

    await _client(session).async_set_control_panel(payload)

    assert session.calls == [
        (
            "POST",
            f"http://127.0.0.1:{LAKE6_DEFAULT_PORT}/control-panels",
            payload,
        )
    ]
