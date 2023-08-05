from .adapter import MatterAdapter as MatterAdapter
from .helpers import get_matter as get_matter
from collections.abc import Callable as Callable
from homeassistant.components import websocket_api as websocket_api
from homeassistant.components.websocket_api import ActiveConnection as ActiveConnection
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from typing import Any

ID: str
TYPE: str

def async_register_api(hass: HomeAssistant) -> None: ...
def async_get_matter_adapter(func: Callable) -> Callable: ...
def async_handle_failed_command(func: Callable) -> Callable: ...
async def websocket_commission(hass: HomeAssistant, connection: ActiveConnection, msg: dict[str, Any], matter: MatterAdapter) -> None: ...
async def websocket_commission_on_network(hass: HomeAssistant, connection: ActiveConnection, msg: dict[str, Any], matter: MatterAdapter) -> None: ...
async def websocket_set_thread_dataset(hass: HomeAssistant, connection: ActiveConnection, msg: dict[str, Any], matter: MatterAdapter) -> None: ...
async def websocket_set_wifi_credentials(hass: HomeAssistant, connection: ActiveConnection, msg: dict[str, Any], matter: MatterAdapter) -> None: ...
