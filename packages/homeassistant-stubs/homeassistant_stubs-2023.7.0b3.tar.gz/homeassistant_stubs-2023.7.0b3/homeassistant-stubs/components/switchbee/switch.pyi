from .const import DOMAIN as DOMAIN
from .coordinator import SwitchBeeCoordinator as SwitchBeeCoordinator
from .entity import SwitchBeeDeviceEntity as SwitchBeeDeviceEntity
from homeassistant.components.switch import SwitchEntity as SwitchEntity
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from switchbee.device import SwitchBeeGroupSwitch, SwitchBeeSwitch, SwitchBeeTimedSwitch, SwitchBeeTimerSwitch
from typing import Any, TypeVar

_DeviceTypeT = TypeVar('_DeviceTypeT', bound=SwitchBeeTimedSwitch | SwitchBeeGroupSwitch | SwitchBeeSwitch | SwitchBeeTimerSwitch)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class SwitchBeeSwitchEntity(SwitchBeeDeviceEntity[_DeviceTypeT], SwitchEntity):
    _attr_is_on: bool
    def __init__(self, device: _DeviceTypeT, coordinator: SwitchBeeCoordinator) -> None: ...
    def _handle_coordinator_update(self) -> None: ...
    def _update_from_coordinator(self) -> None: ...
    async def async_turn_on(self, **kwargs: Any) -> None: ...
    async def async_turn_off(self, **kwargs: Any) -> None: ...
    async def _async_set_state(self, state: str) -> None: ...
