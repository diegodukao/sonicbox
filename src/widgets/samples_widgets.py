from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivymd.selectioncontrols import MDCheckbox

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
            self.add_widget(SamplesKeyboard(samples_group))

        # empty keyboard to store user's favorite samples
        self.add_widget(SamplesKeyboard())

        self.title = self.current_slide.title

    def on_index(self, *args):
        """Updating Carousel title everytime the slide is changed"""
        super().on_index(*args)
        self.title = self.current_slide.title


class SamplesKeyboard(GridLayout):

    def __init__(self, samples_group=None, **kwargs):
        super().__init__(**kwargs)

        self.cols = 3
        if samples_group:
            self.title = samples_group.name

            for sample in samples_group.samples:
                btn = PlayButton(text=sample)
                self.add_widget(btn)
        else:
            self.title = "Favorites"


class PlayButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        self.fav_checkbox = MDCheckbox()
        self.fav_checkbox.size = self.fav_checkbox.texture_size
        self.add_widget(self.fav_checkbox)
        self.bind(pos=self.update_checkbox_pos,
                  size=self.update_checkbox_pos)

    def on_press(self):
        self.play()

    def update_checkbox_pos(self, *args):
        self.fav_checkbox.size = self.fav_checkbox.texture_size
        self.fav_checkbox.pos = (
            self.x + self.width - self.fav_checkbox.width,
            self.y + self.height - self.fav_checkbox.height,
        )

    def play(self):
        self.app.sender.send_message('/sample', self.text)
