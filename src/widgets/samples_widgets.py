from kivy.app import App
from kivy.lang import Builder
from kivy.properties import (
    BooleanProperty, DictProperty, ListProperty, ObjectProperty,
    StringProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivymd.menu import MDDropdownMenu
from kivymd.selectioncontrols import MDCheckbox

from constants.samples import SAMPLES_GROUPS
from services import storage

Builder.load_file('ui/samples_screen.kv')


class SamplesScreen(Screen):
    favorites = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        menu_items = [
            {'viewclass': 'SamplesDropdownMenuCheckbox'},
        ]
        self.dropdown = SamplesSettingsDropdown(
            items=menu_items, width_mult=4)

    def add_favorite(self, sample_name):
        if sample_name not in self.favorites:
            self.favorites.append(sample_name)
            self.carousel.add_favorite_btn(sample_name)
            storage.save_favorite_sample(sample_name)

    def remove_favorite(self, sample_name):
        if sample_name in self.favorites:
            self.carousel.remove_favorite_btn(sample_name)
            storage.remove_favorite_sample(sample_name)

    def toggle_edit_favorites(self, edit: bool):
        """ Called by `edit favorites` checkbox on the dropdown menu"""
        self.carousel.edit_favorites = edit


class SamplesCarousel(Carousel):
    title = StringProperty()
    favorites_keyboard = ObjectProperty()
    favorites_buttons = DictProperty()
    edit_favorites = BooleanProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.loop = True

        keyboards_list = []
        for samples_group in SAMPLES_GROUPS:
            kb = SamplesKeyboard(samples_group)
            self.add_widget(kb)
            keyboards_list.append(kb)

        # empty keyboard to store user's favorite samples
        fav_keyboard = SamplesKeyboard()
        self.favorites_keyboard = fav_keyboard
        self.add_widget(fav_keyboard)
        keyboards_list.append(fav_keyboard)

        for kb in keyboards_list:
            self.bind(edit_favorites=kb.toggle_checkboxes)

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
    show_checkboxes = BooleanProperty()

    def __init__(self, samples_group=None, **kwargs):
        super().__init__(**kwargs)

        self.cols = 3
        if samples_group:
            self.title = samples_group.name

            for sample in samples_group.samples:
                btn = PlayButton(text=sample)
                self.add_widget(btn)
                self.bind(show_checkboxes=btn.toggle_checkboxes)
        else:
            self.title = "Favorites"

    def toggle_checkboxes(self, caller, show_checkboxes):
        self.show_checkboxes = show_checkboxes


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

    def toggle_checkboxes(self, caller, show_checkboxes):
        if show_checkboxes and self.fav_checkbox not in self.children:
            self.add_widget(self.fav_checkbox)
        elif not show_checkboxes and self.fav_checkbox in self.children:
            self.remove_widget(self.fav_checkbox)

    def play(self):
        self.app.sender.send_message('/sample', self.text)


class SamplesDropdownMenuCheckbox(BoxLayout):
    edit_favorites = BooleanProperty()

    def on_edit_favorites(self, instance, value):
        app = App.get_running_app()
        app.root.screens.samples.toggle_edit_favorites(value)


class SamplesSettingsDropdown(MDDropdownMenu):
    pass
