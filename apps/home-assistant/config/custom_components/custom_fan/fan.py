from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.util.percentage import (
    int_states_in_range,
    percentage_to_ranged_value,
    ranged_value_to_percentage,
)

DOMAIN = "custom_fan"
SPEED_RANGE = (1, 6)  # 6 speeds

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Custom Fan platform."""
    async_add_entities([CustomFan()])

class CustomFan(FanEntity):
    def __init__(self):
        """Initialize the fan."""
        self._attr_name = "Custom Fan"
        self._attr_unique_id = "custom_fan_01"
        self._attr_is_on = False
        self._attr_percentage = 0
        self._attr_supported_features = (
            FanEntityFeature.SET_SPEED
            | FanEntityFeature.TURN_ON
            | FanEntityFeature.TURN_OFF
        )

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
        if percentage == 0:
            self._attr_is_on = False
            self._attr_percentage = 0
        else:
            self._attr_is_on = True
            self._attr_percentage = percentage

    async def async_turn_on(self, speed=None, percentage=None, preset_mode=None, **kwargs):
        """Turn on the fan."""
        if percentage is None:
            percentage = 17  # Default to lowest speed (1/6 ≈ 17%)
        await self.async_set_percentage(percentage)

    async def async_turn_off(self, **kwargs):
        """Turn the fan off."""
        await self.async_set_percentage(0)