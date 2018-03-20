import kivy

from kivy.app import App
from kivy.uix.carousel import Carousel
from kivymd.theming import ThemeManager

from samples import SAMPLES_GROUPS
from widgets import SamplesKeyboard

kivy.require('1.10.0')


class SamplesCarousel(Carousel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.loop = True

        for samples_group in SAMPLES_GROUPS:
            sk = SamplesKeyboard(samples_group)
            self.add_widget(sk)


class SonicBox(App):
    theme_cls = ThemeManager()

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return self.root


SonicBox().run()
