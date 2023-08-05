from .const import ATTR_PAYLOAD as ATTR_PAYLOAD, ATTR_QOS as ATTR_QOS, ATTR_RETAIN as ATTR_RETAIN, ATTR_TOPIC as ATTR_TOPIC, CONF_CERTIFICATE as CONF_CERTIFICATE, CONF_CLIENT_CERT as CONF_CLIENT_CERT, CONF_CLIENT_KEY as CONF_CLIENT_KEY, DATA_MQTT as DATA_MQTT, DATA_MQTT_AVAILABLE as DATA_MQTT_AVAILABLE, DEFAULT_ENCODING as DEFAULT_ENCODING, DEFAULT_QOS as DEFAULT_QOS, DEFAULT_RETAIN as DEFAULT_RETAIN, DOMAIN as DOMAIN
from .models import MqttData as MqttData
from _typeshed import Incomplete
from homeassistant.config_entries import ConfigEntryState as ConfigEntryState
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.helpers import template as template
from homeassistant.helpers.typing import ConfigType as ConfigType
from typing import Any

AVAILABILITY_TIMEOUT: float
TEMP_DIR_NAME: Incomplete
_VALID_QOS_SCHEMA: Incomplete

def mqtt_config_entry_enabled(hass: HomeAssistant) -> bool | None: ...
async def async_wait_for_mqtt_client(hass: HomeAssistant) -> bool: ...
def valid_topic(topic: Any) -> str: ...
def valid_subscribe_topic(topic: Any) -> str: ...
def valid_subscribe_topic_template(value: Any) -> template.Template: ...
def valid_publish_topic(topic: Any) -> str: ...
def valid_qos_schema(qos: Any) -> int: ...

_MQTT_WILL_BIRTH_SCHEMA: Incomplete

def valid_birth_will(config: ConfigType) -> ConfigType: ...
def get_mqtt_data(hass: HomeAssistant) -> MqttData: ...
async def async_create_certificate_temp_files(hass: HomeAssistant, config: ConfigType) -> None: ...
def get_file_path(option: str, default: str | None = ...) -> str | None: ...
def migrate_certificate_file_to_content(file_name_or_auto: str) -> str | None: ...
