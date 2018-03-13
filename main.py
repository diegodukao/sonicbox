import kivy

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from pythonosc import udp_client

kivy.require('1.10.0')


def sample_path(sample_str):
    path = '/home/diego/Applications/src/sonic-pi/etc/samples/'
    ext = ".flac"
    return f"{path}{sample_str}{ext}"


class Main(GridLayout):
    cols = 2


class PlayButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sender = udp_client.SimpleUDPClient("127.0.0.1", 4559)

    def play(self, note):
        print(note)
        self.sender.send_message('/sample', sample_path('ambi_choir'))


class SonicBox(App):
    pass


SonicBox().run()
