import kivy

from kivy.app import App
from kivymd.theming import ThemeManager
from pythonosc import udp_client


kivy.require('1.10.0')


class SonicBox(App):
    theme_cls = ThemeManager()
    _sender = None

    @property
    def sender(self):
        if not self._sender:
            self._sender = udp_client.SimpleUDPClient("127.0.0.1", 4559)
        return self._sender

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return self.root


SonicBox().run()
