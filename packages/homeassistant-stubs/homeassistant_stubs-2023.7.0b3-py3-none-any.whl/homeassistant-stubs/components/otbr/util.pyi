import python_otbr_api
from .const import DOMAIN as DOMAIN
from _typeshed import Incomplete
from collections.abc import Callable as Callable, Coroutine
from homeassistant.components.homeassistant_hardware.silabs_multiprotocol_addon import MultiprotocolAddonManager as MultiprotocolAddonManager, get_addon_manager as get_addon_manager, is_multiprotocol_url as is_multiprotocol_url, multi_pan_addon_using_device as multi_pan_addon_using_device
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from typing import Any, Concatenate, TypeVar

_R = TypeVar('_R')
_P: Incomplete
INFO_URL_SKY_CONNECT: str
INFO_URL_YELLOW: str
INSECURE_NETWORK_KEYS: Incomplete
INSECURE_PASSPHRASES: Incomplete

def _handle_otbr_error(func: Callable[Concatenate[OTBRData, _P], Coroutine[Any, Any, _R]]) -> Callable[Concatenate[OTBRData, _P], Coroutine[Any, Any, _R]]: ...

class OTBRData:
    url: str
    api: python_otbr_api.OTBR
    entry_id: str
    async def set_enabled(self, enabled: bool) -> None: ...
    async def get_active_dataset(self) -> python_otbr_api.ActiveDataSet | None: ...
    async def get_active_dataset_tlvs(self) -> bytes | None: ...
    async def get_pending_dataset_tlvs(self) -> bytes | None: ...
    async def create_active_dataset(self, dataset: python_otbr_api.ActiveDataSet) -> None: ...
    async def delete_active_dataset(self) -> None: ...
    async def set_active_dataset_tlvs(self, dataset: bytes) -> None: ...
    async def set_channel(self, channel: int, delay: float = ...) -> None: ...
    async def get_extended_address(self) -> bytes: ...
    def __init__(self, url, api, entry_id) -> None: ...

async def get_allowed_channel(hass: HomeAssistant, otbr_url: str) -> int | None: ...
async def _warn_on_channel_collision(hass: HomeAssistant, otbrdata: OTBRData, dataset_tlvs: bytes) -> None: ...
def _warn_on_default_network_settings(hass: HomeAssistant, otbrdata: OTBRData, dataset_tlvs: bytes) -> None: ...
async def update_issues(hass: HomeAssistant, otbrdata: OTBRData, dataset_tlvs: bytes) -> None: ...
