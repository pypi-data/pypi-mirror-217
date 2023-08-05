from ..coordinator import OverkizDataUpdateCoordinator as OverkizDataUpdateCoordinator
from .generic_cover import COMMANDS_CLOSE_TILT as COMMANDS_CLOSE_TILT, COMMANDS_OPEN_TILT as COMMANDS_OPEN_TILT, COMMANDS_STOP as COMMANDS_STOP, OverkizGenericCover as OverkizGenericCover
from _typeshed import Incomplete
from homeassistant.components.cover import ATTR_POSITION as ATTR_POSITION, CoverDeviceClass as CoverDeviceClass, CoverEntityFeature as CoverEntityFeature
from typing import Any

COMMANDS_OPEN: Incomplete
COMMANDS_CLOSE: Incomplete
OVERKIZ_DEVICE_TO_DEVICE_CLASS: Incomplete

class VerticalCover(OverkizGenericCover):
    @property
    def supported_features(self) -> CoverEntityFeature: ...
    @property
    def device_class(self) -> CoverDeviceClass: ...
    @property
    def current_cover_position(self) -> int | None: ...
    async def async_set_cover_position(self, **kwargs: Any) -> None: ...
    async def async_open_cover(self, **kwargs: Any) -> None: ...
    async def async_close_cover(self, **kwargs: Any) -> None: ...
    @property
    def is_opening(self) -> bool | None: ...
    @property
    def is_closing(self) -> bool | None: ...

class LowSpeedCover(VerticalCover):
    _attr_name: str
    _attr_unique_id: Incomplete
    def __init__(self, device_url: str, coordinator: OverkizDataUpdateCoordinator) -> None: ...
    async def async_set_cover_position(self, **kwargs: Any) -> None: ...
    async def async_open_cover(self, **kwargs: Any) -> None: ...
    async def async_close_cover(self, **kwargs: Any) -> None: ...
    async def async_set_cover_position_low_speed(self, **kwargs: Any) -> None: ...
