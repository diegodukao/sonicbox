from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from pythonosc import udp_client

from samples import SAMPLES_GROUPS, sample_path


class SamplesScreen(Screen):
    pass


class SamplesCarousel(Carousel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.loop = True

        for samples_group in SAMPLES_GROUPS:
            sk = SamplesKeyboard(samples_group)
            self.add_widget(sk)


class SamplesKeyboard(GridLayout):

    def __init__(self, samples, **kwargs):
        super().__init__(**kwargs)

        self.cols = 3

        for sample in samples:
            btn = PlayButton(text=sample)
            self.add_widget(btn)


class PlayButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sender = udp_client.SimpleUDPClient("127.0.0.1", 4559)

    def on_press(self):
        self.play()

    def play(self):
        self.sender.send_message('/sample', sample_path(self.text))
