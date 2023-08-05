from _typeshed import Incomplete
from datetime import datetime
from homeassistant.components.vacuum import ATTR_CLEANED_AREA as ATTR_CLEANED_AREA, STATE_CLEANING as STATE_CLEANING, STATE_DOCKED as STATE_DOCKED, STATE_IDLE as STATE_IDLE, STATE_PAUSED as STATE_PAUSED, STATE_RETURNING as STATE_RETURNING, StateVacuumEntity as StateVacuumEntity, VacuumEntity as VacuumEntity, VacuumEntityFeature as VacuumEntityFeature
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.helpers import event as event
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType as ConfigType, DiscoveryInfoType as DiscoveryInfoType
from typing import Any

SUPPORT_MINIMAL_SERVICES: Incomplete
SUPPORT_BASIC_SERVICES: Incomplete
SUPPORT_MOST_SERVICES: Incomplete
SUPPORT_ALL_SERVICES: Incomplete
SUPPORT_STATE_SERVICES: Incomplete
FAN_SPEEDS: Incomplete
DEMO_VACUUM_COMPLETE: str
DEMO_VACUUM_MOST: str
DEMO_VACUUM_BASIC: str
DEMO_VACUUM_MINIMAL: str
DEMO_VACUUM_NONE: str
DEMO_VACUUM_STATE: str

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...
async def async_setup_platform(hass: HomeAssistant, config: ConfigType, async_add_entities: AddEntitiesCallback, discovery_info: DiscoveryInfoType | None = ...) -> None: ...

class DemoVacuum(VacuumEntity):
    _attr_should_poll: bool
    _attr_translation_key: str
    _attr_name: Incomplete
    _attr_supported_features: Incomplete
    _state: bool
    _status: str
    _fan_speed: Incomplete
    _cleaned_area: int
    _battery_level: int
    def __init__(self, name: str, supported_features: VacuumEntityFeature) -> None: ...
    @property
    def is_on(self) -> bool: ...
    @property
    def status(self) -> str: ...
    @property
    def fan_speed(self) -> str: ...
    @property
    def fan_speed_list(self) -> list[str]: ...
    @property
    def battery_level(self) -> int: ...
    @property
    def extra_state_attributes(self) -> dict[str, Any]: ...
    def turn_on(self, **kwargs: Any) -> None: ...
    def turn_off(self, **kwargs: Any) -> None: ...
    def stop(self, **kwargs: Any) -> None: ...
    def clean_spot(self, **kwargs: Any) -> None: ...
    def locate(self, **kwargs: Any) -> None: ...
    def start_pause(self, **kwargs: Any) -> None: ...
    def set_fan_speed(self, fan_speed: str, **kwargs: Any) -> None: ...
    def return_to_base(self, **kwargs: Any) -> None: ...
    def send_command(self, command: str, params: dict[str, Any] | list[Any] | None = ..., **kwargs: Any) -> None: ...

class StateDemoVacuum(StateVacuumEntity):
    _attr_should_poll: bool
    _attr_supported_features = SUPPORT_STATE_SERVICES
    _attr_translation_key: str
    _attr_name: Incomplete
    _state: Incomplete
    _fan_speed: Incomplete
    _cleaned_area: int
    _battery_level: int
    def __init__(self, name: str) -> None: ...
    @property
    def state(self) -> str: ...
    @property
    def battery_level(self) -> int: ...
    @property
    def fan_speed(self) -> str: ...
    @property
    def fan_speed_list(self) -> list[str]: ...
    @property
    def extra_state_attributes(self) -> dict[str, Any]: ...
    def start(self) -> None: ...
    def pause(self) -> None: ...
    def stop(self, **kwargs: Any) -> None: ...
    def return_to_base(self, **kwargs: Any) -> None: ...
    def clean_spot(self, **kwargs: Any) -> None: ...
    def set_fan_speed(self, fan_speed: str, **kwargs: Any) -> None: ...
    def __set_state_to_dock(self, _: datetime) -> None: ...
