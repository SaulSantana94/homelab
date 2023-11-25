from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import groupby
from statistics import mean
from typing import List

import appdaemon.plugins.hass.hassapi as hass
import pytz

"""
Requirements:
- button for enable or disable automated control.
- calculate number of minimum hours needed: can be fixed at the beginning ~ 5, then we can use
    outside temperatures and then we can combine it with predictions and sun hours in the morning.
- calculate cheapest hours (use price moving average for last week -> lower than that is OK)
    if cheapest hours are much cheaper for more hours add more hours.
"""


@dataclass
class Price:
    value: float
    datetime: datetime

    def __post_init__(self):
        if self.value < 0:
            raise ValueError


class ClimateControl(hass.Hass):
    async def initialize(self):
        self.log("Starting")
        self.stop_app
        self.timers = []
        self._logging
        input_boolean_enable = self.args["input_boolean"]["enable"]
        is_enabled = await self.get_state(input_boolean_enable, attribute="state") == "on"
        self.log(f"Climate control is {'enabled' if is_enabled else 'disabled'}")
        if is_enabled:
            await self._register_schedulers()

        # Register schedulers if climate control is enabled
        await self.listen_state(self._register_schedulers, input_boolean_enable, new="on", old="off")
        # Unregister schedulers if climate control is enabled
        await self.listen_state(self._unregister_schedulers, input_boolean_enable, new="off", old="on")

        # Register schedulers every day
        # give enough time to get new data
        await self.run_daily(self._register_schedulers, "00:00:05")

    async def _get_prices(self) -> List[Price]:
        pvpc = await self.get_state(self.args["sensor"]["pvpc_price"], attribute="all")
        self.log(f"{pvpc=}", level="DEBUG")
        now = datetime.now(pytz.timezone(self.get_timezone()))

        prices = [
            Price(
                datetime=datetime(now.year, now.month, now.day) + timedelta(hours=i),
                value=pvpc["attributes"][f"price_{i:02d}h"],
            )
            for i in range(24)
        ]
        return prices

    async def _change_hvac_mode(self, mode):
        dry_run_msg = "" if self.args["climate"]["enabled"] else " (dry run mode)"
        msg = f"Set HVAC mode to `{mode}`{dry_run_msg}"
        self.log(msg)
        if self.args["notify"]["enabled"]:
            await self.notify(msg, name=self.args["notify"]["target"])
        if self.args["climate"]["enabled"]:
            await self.set_state(self.args["climate"]["entity"], state=mode)

    async def _start_hvac(self, kwargs={}):
        await self._change_hvac_mode(self.args["climate"]["on_mode"])

    async def _stop_hvac(self, kwargs={}):
        await self._change_hvac_mode(self.args["climate"]["off_mode"])

    def _cheaper_hours(self, prices: List[Price], min_hours: int) -> List[Price]:
        return sorted(prices, key=lambda x: x.value)[:min_hours]

    def _group_for_scheduling(self, datetimes: List[datetime]):
        group_consecutives = []
        for _, group in groupby(
            enumerate(sorted(datetimes)), lambda idx_date: idx_date[1] - timedelta(hours=idx_date[0])
        ):
            group_consecutives.append([date for _, date in group])

        return group_consecutives

    async def _register_schedulers(self, _entity="", _attribute="", _old="", _new="", _kwargs={}):
        await self._unregister_schedulers()
        self.log("Registering schedulers")

        prices = await self._get_prices()
        self.log(f"{prices=}", level="DEBUG")

        historical_data = await self.get_history(entity_id=self.args["sensor"]["pvpc_price"], days=10)
        historical_prices = [
            Price(value=float(j["state"]), datetime=j["last_changed"]) for i in historical_data for j in i
        ]

        self.log(f"{historical_prices=}", level="DEBUG")
        price_10dma = mean([p.value for p in historical_prices])
        self.log(f"{price_10dma=}", level="DEBUG")

        cheap_price_limit = price_10dma * 2 / 3
        cheapest_prices = list(filter(lambda x: x.value < cheap_price_limit, prices))
        self.log(f"{cheapest_prices=}", level="DEBUG")

        min_hours = int(float(await self.get_state(self.args["input_number"]["min_hours_per_day"])))
        is_cheap = len(cheapest_prices) >= min_hours

        prices_to_schedule = cheapest_prices if is_cheap else self._cheaper_hours(prices, min_hours)

        self.log(f"{prices_to_schedule=}", level="DEBUG")
        self.log(f"{len(prices_to_schedule)}", level="DEBUG")
        datetimes_to_schedule = [price.datetime for price in prices_to_schedule]

        groups_to_schedule = self._group_for_scheduling(datetimes_to_schedule)
        now = datetime.now(pytz.timezone(self.get_timezone()))
        current_hour = datetime(now.year, now.month, now.day, now.hour)

        async def register(*args):
            self.log(f"Registering {args[0].__name__} at {args[1]}", level="INFO")
            self.timers.append(await self.run_at(*args))

        for group in groups_to_schedule:
            self.log(f"{current_hour=}", level="DEBUG")
            self.log(f"{group[0]=}", level="DEBUG")
            if current_hour in group:
                await self._start_hvac()
            elif current_hour > group[0]:
                continue
            else:
                await register(self._start_hvac, group[0].strftime("%H:%M:%S"))

            await register(self._stop_hvac, (group[-1] + timedelta(hours=1)).strftime("%H:%M:%S"))

    async def _unregister_schedulers(self, _entity="", _attribute="", _old="", _new="", _kwargs={}):
        self.log("Unregistering schedulers")

        # get a list to iterate because keys change dynamically while iterating
        timers = list(self.AD.sched.schedule.get(self.name, {}).keys())
        [await self.cancel_timer(timer) for timer in timers]

    async def terminate(self):
        await self._unregister_schedulers()
