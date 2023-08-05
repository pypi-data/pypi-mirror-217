from .oauth import GeocachingOAuth2Implementation as GeocachingOAuth2Implementation
from homeassistant.components.application_credentials import ClientCredential as ClientCredential
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow as config_entry_oauth2_flow

async def async_get_auth_implementation(hass: HomeAssistant, auth_domain: str, credential: ClientCredential) -> config_entry_oauth2_flow.AbstractOAuth2Implementation: ...
