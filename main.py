import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivymd.theming import ThemeManager
from pythonosc import udp_client

from samples import sample_path, SAMPLES_GROUPS

kivy.require('1.10.0')


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

    def play(self):
        self.sender.send_message('/sample', sample_path(self.text))


class SonicBox(App):
    theme_cls = ThemeManager()

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return self.root


SonicBox().run()
