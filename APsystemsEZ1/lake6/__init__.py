"""APsystems Lake_6 local API client.

Lake_6 is the APsystems balcony battery. Its local API answers with
``{"data": {...}, "code": 200}`` envelopes, so success is decided by the
business code in the body rather than by the HTTP status.
"""

from .client import (
    Lake6Alarms,
    Lake6ApiClient,
    Lake6ApiError,
    Lake6ControlPanel,
    Lake6ControlPanelWindow,
    Lake6Device,
    Lake6Energies,
    Lake6Modes,
    Lake6TouRule,
    parse_alarms,
    parse_control_panel,
    parse_device,
    parse_energies,
    parse_modes,
)
from .tou import (
    Lake6TouPlanRow,
    build_payload,
    format_weekdays,
    has_multi_slot_rules,
    parse_plan,
    parse_weekdays,
    render_plan,
)

__all__ = [
    "Lake6Alarms",
    "Lake6ApiClient",
    "Lake6ApiError",
    "Lake6ControlPanel",
    "Lake6ControlPanelWindow",
    "Lake6Device",
    "Lake6Energies",
    "Lake6Modes",
    "Lake6TouPlanRow",
    "Lake6TouRule",
    "build_payload",
    "format_weekdays",
    "has_multi_slot_rules",
    "parse_alarms",
    "parse_control_panel",
    "parse_device",
    "parse_energies",
    "parse_modes",
    "parse_plan",
    "parse_weekdays",
    "render_plan",
]
