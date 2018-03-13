import kivy

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from pythonosc import udp_client

from samples import sample_path, SOUNDS_TABLA_DRUM as SAMPLES

kivy.require('1.10.0')


class SamplesKeyboard(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 3

        for sample in SAMPLES:
            btn = PlayButton(text=sample)
            self.add_widget(btn)


class PlayButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sender = udp_client.SimpleUDPClient("127.0.0.1", 4559)

    def play(self, note):
        print(note)
        self.sender.send_message('/sample', sample_path(self.text))


class SonicBox(App):
    pass


SonicBox().run()
