import pytest
from APsystemsEZ1.ezhi import BatteryStatusData


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_data, expected_result, test_id",
    [
        # Happy path tests with various realistic test values
        (
            {
                "data": {
                    "batS": 2,
                    "batSoc": "75",
                    "batSoh": "90",
                    "batTemp": "30",
                    "devTemp": "25",
                    "pvP": "500",
                    "pvTE": "1000",
                    "batP": "200",
                    "batCTE": "1500",
                    "batDTE": "1000",
                    "ogP": "-100",
                    "ogOTE": "2000",
                    "ogITE": "1500",
                    "ofgP": "300",
                    "ofgOTE": "2500",
                    "ofgITE": "2000",
                },
                "status": 0,
            },
            BatteryStatusData(
                batS=2,
                batSoc=75,
                batSoh=90,
                batTemp=30,
                devTemp=25,
                pvP=500,
                pvTE=1000,
                batP=200,
                batCTE=1500,
                batDTE=1000,
                ogP=-100,
                ogOTE=2000,
                ogITE=1500,
                ofgP=300,
                ofgOTE=2500,
                ofgITE=2000,
            ),
            "happy_path_1",
        ),
        # Edge cases
        (
            {
                "data": {
                    "batS": 1,
                    "batSoc": "0",
                    "batSoh": "0",
                    "batTemp": "0",
                    "devTemp": "0",
                    "pvP": "0",
                    "pvTE": "0",
                    "batP": "0",
                    "batCTE": "0",
                    "batDTE": "0",
                    "ogP": "0",
                    "ogOTE": "0",
                    "ogITE": "0",
                    "ofgP": "0",
                    "ofgOTE": "0",
                    "ofgITE": "0",
                },
                "status": 0,
            },
            BatteryStatusData(
                battery_status=1,
                battery_state_of_charge=0,
                battery_state_of_health=0,
                battery_temperature=0,
                device_temperature=0,
                pv_input_power=0,
                total_input_energy=0,
                battery_power=0,
                total_charge_energy=0,
                total_discharge_energy=0,
                on_grid_power=0,
                total_on_grid_output_energy=0,
                total_on_grid_input_energy=0,
                off_grid_power=0,
                total_off_grid_output_energy=0,
                total_off_grid_input_energy=0,
            ),
            "edge_case_empty_values",
        ),
        # Error cases
        (None, None, "error_case_none_response"),
    ],
)
async def test_get_battery_status(
    response_data, expected_result, test_id, mock_response_ezhi
):
    # Arrange
    ez1m = mock_response_ezhi(response_data)

    # Act
    result = await ez1m.get_device_info()  # Adjust method name if necessary

    # Assert
    assert result == expected_result, f"Failed test case: {test_id}"
