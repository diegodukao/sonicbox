from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

from constants.samples import SAMPLES_GROUPS


Builder.load_file('ui/samples_screen.kv')


class SamplesScreen(Screen):
    pass


class SamplesCarousel(Carousel):

    title = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.loop = True

        for samples_group in SAMPLES_GROUPS:
            sk = SamplesKeyboard(samples_group)
            self.add_widget(sk)

        self.title = self.current_slide.title

    def on_index(self, *args):
        """Updating Carousel title everytime the slide is changed"""
        super().on_index(*args)
        self.title = self.current_slide.title


class SamplesKeyboard(GridLayout):

    def __init__(self, samples_group, **kwargs):
        super().__init__(**kwargs)

        self.cols = 3
        self.title = samples_group.name

        for sample in samples_group.samples:
            btn = PlayButton(text=sample)
            self.add_widget(btn)


class PlayButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = App.get_running_app()
        self.sender = app.sender

    def on_press(self):
        self.play()

    def play(self):
        self.sender.send_message('/sample', self.text)
