from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.stacklayout import StackLayout
from kivymd.button import MDRaisedButton
from pythonosc import udp_client

from samples import sample_path


class SamplesScreen(Screen):
    pass


class SynthsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = 'synths'

        grid = GridLayout()
        grid.cols = 8

        for i in range(64):
            grid.add_widget(Button())

        self.add_widget(grid)


class SamplesKeyboard(StackLayout):

    def __init__(self, samples, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'lr-tb'
        self.padding = ['8dp', '12dp']
        self.spacing = ['8dp', '5dp']

        for sample in samples:
            btn = PlayButton(text=sample)
            self.add_widget(btn)


class PlayButton(MDRaisedButton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sender = udp_client.SimpleUDPClient("127.0.0.1", 4559)

    def play(self):
        self.sender.send_message('/sample', sample_path(self.text))
