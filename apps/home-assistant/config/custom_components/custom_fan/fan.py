import logging
from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.util.percentage import int_states_in_range, percentage_to_ranged_value

_LOGGER = logging.getLogger(__name__)
DOMAIN = "custom_fan"
SPEED_RANGE = (1, 6)  # 6 speeds

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Custom Fan platform with multiple entities."""
    fans = [
        CustomFan("ventilador_salon", "ventilador_salon"),
        CustomFan("ventilador_dormitorio", "ventilador_dormitorio"),
        CustomFan("ventilador_invitados", "ventilador_invitados"),
        CustomFan("ventilador_despacho", "ventilador_despacho")
    ]
    async_add_entities(fans)

class CustomFan(FanEntity):
    def __init__(self, name, unique_id):
        """Initialize the fan."""
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._attr_is_on = False
        self._attr_percentage = 20  # Initialize with speed 1
        self._attr_supported_features = (
            FanEntityFeature.SET_SPEED
            | FanEntityFeature.DIRECTION
            | FanEntityFeature.TURN_ON
            | FanEntityFeature.TURN_OFF
        )
        self._attr_direction = "forward"

    @property
    def percentage(self):
        """Return the current speed percentage."""
        return self._attr_percentage

    @property
    def speed_count(self):
        """Return the number of speeds the fan supports."""
        return int_states_in_range(SPEED_RANGE)

    async def async_set_percentage(self, percentage):
        """Set the speed of the fan, as a percentage."""
        if self._attr_is_on == False:
            await self.send_command('off')
        else:
            self._attr_percentage = percentage
            speed_command = f"velocidad_{self.calculate_speed(percentage)}"
            await self.send_command(speed_command)

    def calculate_speed(self, percentage):
        """Calculate speed based on percentage."""
        return percentage_to_ranged_value(SPEED_RANGE, percentage)

    async def async_set_direction(self, direction: str):
        """Set the direction of the fan."""
        self._attr_direction = direction
        await self.send_command("reverse")

    async def async_turn_on(self, speed=None, percentage=None, preset_mode=None, **kwargs):
        """Turn on the fan."""
        self._attr_is_on = True
        await self.async_set_percentage(self._attr_percentage)

    async def async_turn_off(self, **kwargs):
        """Turn the fan off."""
        self._attr_is_on = False
        await self.async_set_percentage(self._attr_percentage)

    async def send_command(self, command):
        """Send command to Broadlink device."""
        service_data = {
            "entity_id": "remote.rfbridge_broadlink",
            "device": self._attr_unique_id,
            "command": command,
            "num_repeats": 1,
            "delay_secs": 0.4
        }
        await self.hass.services.async_call("remote", "send_command", service_data)