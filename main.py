import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from pythonosc import udp_client

kivy.require('1.10.0')


class Main(BoxLayout):
    pass


class PlayButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sender = udp_client.SimpleUDPClient("127.0.0.1", 4559)

    def play(self, note):
        print(note)
        self.sender.send_message('/play', 55)


class SonicBox(App):
    pass


SonicBox().run()
