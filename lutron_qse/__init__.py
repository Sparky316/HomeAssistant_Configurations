"""
2022/10/6  Support for Lutron "QS Standalone", by directly connecting to Lutron QSE-CI-NWK-E over Telnet.
  Warning: This "QS Standalone" is different than Homeworks, or Homeworks QS!
  
This component formed by combining code from the following:
  Python library wrapping the telnet interface:
        https://github.com/deustis/pylutron-qse
  https://github.com/home-assistant/core/pull/9121
  https://github.com/deustis/homeassistant-config/blob/master/custom_components/lutron_qse.py
  https://github.com/deustis/homeassistant-config/blob/master/custom_components/cover/lutron_qse.py
  https://github.com/deustis/homeassistant-config/blob/master/devices/lutron_qse.yaml
  
"""
import asyncio
import logging
import voluptuous as vol


from homeassistant.const import (
    CONF_HOST,
    CONF_ID,
    CONF_NAME,
    EVENT_HOMEASSISTANT_STOP,
    Platform,
)
from homeassistant.core import HomeAssistant, callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_connect, dispatcher_send
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import slugify


from homeassistant.helpers import discovery

from custom_components.lutron_qse.devices import (ALL_STATES, Device, Roller)


DOMAIN = "lutron_qse"

LUTRON_QSE_INSTANCE = DOMAIN + '_instance'
LUTRON_QSE_IGNORE = DOMAIN + '_ignore'
LUTRON_QSE_COMPONENTS = [
    'cover'
]
CONF_IGNORE = 'ignore'


""" ======== Configuration variables: ======== """
CONF_DIMMERS = "dimmers"
#CONF_KEYPADS = "keypads"
CONF_ADDR = "addr"
CONF_RATE = "rate"

FADE_RATE = 1.0
CV_FADE_RATE = vol.All(vol.Coerce(float), vol.Range(min=0, max=20))


DIMMER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ADDR): cv.string,
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_RATE, default=FADE_RATE): CV_FADE_RATE,
    }
)



CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_HOST): cv.string,
                #vol.Required(CONF_PORT): cv.port,
                #vol.Required(CONF_DIMMERS): vol.All(cv.ensure_list, [DIMMER_SCHEMA]),
                #vol.Optional(CONF_KEYPADS, default=[]): vol.All( cv.ensure_list, [KEYPAD_SCHEMA] ),
                vol.Optional(CONF_IGNORE, default=[]): vol.All(cv.ensure_list, [cv.string]),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


_LOGGER = logging.getLogger(__name__)


def setup(hass: HomeAssistant, base_config: ConfigType) -> bool:
    from custom_components.lutron_qse.qse import QSE
    from custom_components.lutron_qse import devices

    config = base_config.get(DOMAIN)
    
    _LOGGER.info(" Custom Lutron QSE has started (Info). Host IP set to: %s", config[CONF_HOST])
    
    hass.data[LUTRON_QSE_INSTANCE] = QSE(config[CONF_HOST])
    hass.data[LUTRON_QSE_IGNORE] = config[CONF_IGNORE]
    if not hass.data[LUTRON_QSE_INSTANCE].connected():
        _LOGGER.error("Unable to connect to Lutron QSE at %s", str(config[CONF_HOST]))
        return False


    _LOGGER.info("Connected to Lutron QSE at %s", config[CONF_HOST])
    for component in LUTRON_QSE_COMPONENTS:
        discovery.load_platform(hass, component, DOMAIN, {}, config)
    return True


class LutronQSEDevice(Entity):
    """Common base class for all Lutron QSE devices."""

    def __init__(self, device):
        """Set up the base class.
        [:param]device the pylutron_qse.Device instance
        """
        self._device = device
        self._state = None

    @asyncio.coroutine
    def async_added_to_hass(self):
        """Register callbacks."""
        self.hass.async_add_job(
            self._device.add_subscriber, self._update_callback)

    def _update_callback(self):
        self._update()
        self.schedule_update_ha_state()

    @property
    def name(self):
        """Return the name of the device."""
        if self._device.integration_id is not None:
            return self._device.integration_id
        return self._device.serial_number

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        attr = {
            'serial_number': self._device.serial_number,
        }
        return attr

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    def _update(self):
        pass
        
        
