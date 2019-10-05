import asyncio

import gpiozero

from yaqd_core import BaseDaemon, set_action


class PinDaemon(BaseDaemon):
    _kind = "rpi-gpio-pin"
    defaults = {}

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self.index = config["index"]
        self.mode = config["mode"]
        self.pull_up = config["pull up"]
        self.controller = gpiozero.DigitalInputDevice(
            pin=self.index, pull_up=self.pull_up, active_state=True
        )

    def _load_state(self, state):
        """Load an initial state from a dictionary (typically read from the state.toml file).

        Must be tolerant of missing fields, including entirely empty initial states.

        Parameters
        ----------
        state: dict
            The saved state to load.
        """
        # TODO:
        super()._load_state(state)
        self.set_value(state.get("value", default=0))

    def get_state(self):
        state = super().get_state()
        state["value"] = get_value()
        return state

    def get_value(self):
        return self.value

    @set_action
    def set_value(self, value):
        # TODO: consider if error should be raised in certain modes
        self.controller.value = value

    async def update_state(self):
        """Continually monitor and update the current daemon state."""
        while True:
            self.value = self.controller.value
            self._busy = False
            if mode != "in":
                await self._busy_sig()
            else:
                await asyncio.sleep(0.01)
