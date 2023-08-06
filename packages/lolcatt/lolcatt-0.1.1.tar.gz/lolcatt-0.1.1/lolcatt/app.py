from textual.app import App
from textual.containers import Container

from lolcatt.casting.caster import Caster
from lolcatt.ui.lolcatt_controls import LolCattControls
from lolcatt.ui.lolcatt_device_info import LolCattDeviceInfo
from lolcatt.ui.lolcatt_playback_info import LolCattPlaybackInfo
from lolcatt.ui.lolcatt_progress import LolCattProgress
from lolcatt.ui.lolcatt_url_input import LolCattUrlInput


class LolCatt(App):
    """The main application class for lolcatt."""

    CSS_PATH = 'ui/lolcatt.css'

    def __init__(self, device_name: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.caster = Caster(device_name)
        self._components = [
            LolCattDeviceInfo(caster=self.caster),
            LolCattPlaybackInfo(caster=self.caster),
            LolCattProgress(caster=self.caster),
            LolCattControls(caster=self.caster, exit_cb=self.exit),
            LolCattUrlInput(caster=self.caster),
        ]

    def compose(self):
        yield Container(
            *self._components,
            id='app',
        )


if __name__ == '__main__':
    LolCatt('default').run()
