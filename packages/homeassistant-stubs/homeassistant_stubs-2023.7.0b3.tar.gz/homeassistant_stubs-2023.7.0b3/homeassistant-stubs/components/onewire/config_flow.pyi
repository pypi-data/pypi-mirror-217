from .const import DEFAULT_HOST as DEFAULT_HOST, DEFAULT_PORT as DEFAULT_PORT, DEVICE_SUPPORT_OPTIONS as DEVICE_SUPPORT_OPTIONS, DOMAIN as DOMAIN, INPUT_ENTRY_CLEAR_OPTIONS as INPUT_ENTRY_CLEAR_OPTIONS, INPUT_ENTRY_DEVICE_SELECTION as INPUT_ENTRY_DEVICE_SELECTION, OPTION_ENTRY_DEVICE_OPTIONS as OPTION_ENTRY_DEVICE_OPTIONS, OPTION_ENTRY_SENSOR_PRECISION as OPTION_ENTRY_SENSOR_PRECISION, PRECISION_MAPPING_FAMILY_28 as PRECISION_MAPPING_FAMILY_28
from .onewirehub import CannotConnect as CannotConnect, OneWireHub as OneWireHub
from _typeshed import Incomplete
from homeassistant.config_entries import ConfigEntry as ConfigEntry, ConfigFlow as ConfigFlow, OptionsFlowWithConfigEntry as OptionsFlowWithConfigEntry
from homeassistant.const import CONF_HOST as CONF_HOST, CONF_PORT as CONF_PORT
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.data_entry_flow import FlowResult as FlowResult
from homeassistant.helpers.device_registry import DeviceEntry as DeviceEntry
from typing import Any

DATA_SCHEMA: Incomplete

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, str]: ...

class OneWireFlowHandler(ConfigFlow, domain=DOMAIN):
    VERSION: int
    onewire_config: Incomplete
    def __init__(self) -> None: ...
    async def async_step_user(self, user_input: dict[str, Any] | None = ...) -> FlowResult: ...
    @staticmethod
    def async_get_options_flow(config_entry: ConfigEntry) -> OnewireOptionsFlowHandler: ...

class OnewireOptionsFlowHandler(OptionsFlowWithConfigEntry):
    configurable_devices: dict[str, str]
    devices_to_configure: dict[str, str]
    current_device: str
    async def async_step_init(self, user_input: dict[str, Any] | None = ...) -> FlowResult: ...
    async def async_step_device_selection(self, user_input: dict[str, Any] | None = ...) -> FlowResult: ...
    async def async_step_configure_device(self, user_input: dict[str, Any] | None = ...) -> FlowResult: ...
    @staticmethod
    def _get_device_friendly_name(entry: DeviceEntry, onewire_id: str) -> str: ...
    def _get_current_configured_sensors(self) -> list[str]: ...
    def _get_current_setting(self, device_id: str, setting: str, default: Any) -> Any: ...
    def _update_device_options(self, user_input: dict[str, Any]) -> None: ...
