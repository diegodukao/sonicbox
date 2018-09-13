import kivy

from kivy.app import App
from kivymd.theming import ThemeManager
from pythonosc import udp_client


kivy.require('1.10.0')


class SonicBox(App):
    theme_cls = ThemeManager()
    _sender = None

    def create_sender(self, ip):
        self._sender = udp_client.SimpleUDPClient(ip, 4559)

    @property
    def sender(self):
        if not self._sender:
            self.create_sender("127.0.0.1")
        return self._sender

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return self.root


SonicBox().run()
