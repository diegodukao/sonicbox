from kivy.app import App
from kivy.lang import Builder
from kivy.properties import DictProperty, ListProperty, ObjectProperty, \
    StringProperty
from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivymd.selectioncontrols import MDCheckbox

from constants.samples import SAMPLES_GROUPS


Builder.load_file('ui/samples_screen.kv')


class SamplesScreen(Screen):
    favorites = ListProperty()

    def add_favorite(self, sample_name):
        if sample_name not in self.favorites:
            self.favorites.append(sample_name)
            self.carousel.add_favorite_btn(sample_name)

    def remove_favorite(self, sample_name):
        if sample_name in self.favorites:
            self.carousel.remove_favorite_btn(sample_name)


class SamplesCarousel(Carousel):
    title = StringProperty()
    favorites_keyboard = ObjectProperty()
    favorites_buttons = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.loop = True

        for samples_group in SAMPLES_GROUPS:
            self.add_widget(SamplesKeyboard(samples_group))

        # empty keyboard to store user's favorite samples
        fav_keyboard = SamplesKeyboard()
        self.favorites_keyboard = fav_keyboard
        self.add_widget(fav_keyboard)

        self.title = self.current_slide.title

    def on_index(self, *args):
        """Updating Carousel title everytime the slide is changed"""
        super().on_index(*args)
        self.title = self.current_slide.title

    def add_favorite_btn(self, sample_name):
        btn = Button(text=sample_name)
        self.favorites_buttons[sample_name] = btn
        self.favorites_keyboard.add_widget(btn)

    def remove_favorite_btn(self, sample_name):
        btn = self.favorites_buttons[sample_name]
        self.favorites_keyboard.remove_widget(btn)
        del self.favorites_buttons[sample_name]


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


class FavoriteCheckbox(MDCheckbox):

    def __init__(self, **kwargs):
        super().__init__(*kwargs)
        self.app = App.get_running_app()

    def on_active(self, instance, active):
        super().on_active(instance, active)

        if self.app.root:
            screen = self.app.root.screens.samples
            if active:
                screen.add_favorite(self.parent.text)
            else:
                screen.remove_favorite(self.parent.text)


class PlayButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        self.fav_checkbox = FavoriteCheckbox()
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
