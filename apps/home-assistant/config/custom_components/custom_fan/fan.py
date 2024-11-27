from homeassistant.components.fan import FanEntity, SUPPORT_SET_SPEED
from homeassistant.helpers.entity import Entity
from homeassistant.util.percentage import (
    ordered_list_item_to_percentage,
    percentage_to_ordered_list_item,
)

SPEED_LIST = ["off", "speed_1", "speed_2", "speed_3", "speed_4", "speed_5", "speed_6"]

async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities([CustomFan()])

class CustomFan(FanEntity):
    def __init__(self):
        self._state = False
        self._speed = SPEED_LIST[0]

    @property
    def name(self):
        return "Custom Fan"

    @property
    def is_on(self):
        return self._state

    @property
    def percentage(self):
        return ordered_list_item_to_percentage(SPEED_LIST, self._speed)

    @property
    def speed_count(self):
        return len(SPEED_LIST) - 1

    async def async_turn_on(self, speed=None, percentage=None, preset_mode=None, **kwargs):
        self._state = True
        if percentage is not None:
            self._speed = percentage_to_ordered_list_item(SPEED_LIST, percentage)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._state = False
        self._speed = SPEED_LIST[0]
        self.async_write_ha_state()

    async def async_set_percentage(self, percentage):
        self._speed = percentage_to_ordered_list_item(SPEED_LIST, percentage)
        self._state = self._speed != SPEED_LIST[0]
        self.async_write_ha_state()