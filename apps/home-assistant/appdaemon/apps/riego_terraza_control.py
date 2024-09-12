import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime

class RiegoTerrazaControl(hass.Hass):

    async def initialize(self):
        self.log("Initializing Riego Terraza Control")

        # Schedule to turn on riego_terraza at 09:00:00 every day
        await self.run_daily(self._turn_on_riego, "09:00:00")

        # Schedule to turn off riego_terraza at 09:00:15 every day
        await self.run_daily(self._turn_off_riego, "09:00:15")

    async def _turn_on_riego(self, kwargs):
        self.log("Turning on riego_terraza at 09:00:00")
        #await self.call_service("switch/turn_on", entity_id="switch.riego_terraza")

    async def _turn_off_riego(self, kwargs):
        # Check if riego_terraza is still on
        state = await self.get_state("switch.riego_terraza")
        
        if state == "on":
            self.log("Turning off riego_terraza at 09:00:15")
            #await self.call_service("switch/turn_off", entity_id="switch.riego_terraza")
        else:
            self.log("riego_terraza is already off")