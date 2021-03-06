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
from kivymd.button import MDIconButton
from kivymd.menu import MDDropdownMenu
from kivymd.selectioncontrols import MDCheckbox

from constants.samples import SAMPLES_GROUPS, SamplesGroup

Builder.load_file('ui/samples_screen.kv')


class SamplesScreen(Screen):
    favorites = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        menu_items = [
            {'viewclass': 'SamplesDropdownMenuCheckbox'},
        ]
        self.dropdown = SamplesSettingsDropdown(
            items=menu_items, width_mult=4)

        self.favorites = self.app.favorite_samples
        self.bind(favorites=self.app.update_favorite_samples)

    def add_favorite(self, sample_name):
        if sample_name not in self.favorites:
            self.favorites.append(sample_name)
            self.carousel.add_favorite_btn(sample_name)

    def remove_favorite(self, sample_name):
        if sample_name in self.favorites:
            self.favorites.remove(sample_name)
            self.carousel.remove_favorite_btn(sample_name)
            self.app.sample_buttons[sample_name].toggle_checkbox_active(False)

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
        self.app = App.get_running_app()

        keyboards_list = []
        for samples_group in SAMPLES_GROUPS:
            kb = SamplesKeyboard(samples_group)
            self.add_widget(kb)
            keyboards_list.append(kb)

        fav_keyboard = self.create_favorite_samples_keyboard()
        self.favorites_buttons = {
            btn.text: btn for btn in fav_keyboard.children
        }
        self.favorites_keyboard = fav_keyboard
        self.add_widget(fav_keyboard)
        keyboards_list.append(fav_keyboard)

        for kb in keyboards_list:
            self.bind(edit_favorites=kb.toggle_edit_favorites)

        self.title = self.current_slide.title

    def on_index(self, *args):
        """Updating Carousel title everytime the slide is changed"""
        super().on_index(*args)
        self.title = self.current_slide.title

    def create_favorite_samples_keyboard(self):
        fav_list = self.app.favorite_samples
        samples_group = SamplesGroup("Favorites", fav_list)

        return SamplesKeyboard(samples_group, favorites=True)

    def add_favorite_btn(self, sample_name):
        btn = FavoritePlayButton(text=sample_name)
        self.favorites_buttons[sample_name] = btn
        self.favorites_keyboard.add_widget(btn)

    def remove_favorite_btn(self, sample_name):
        btn = self.favorites_buttons[sample_name]
        self.favorites_keyboard.remove_widget(btn)
        del self.favorites_buttons[sample_name]


class SamplesKeyboard(GridLayout):
    edit_favorites = BooleanProperty()

    def __init__(self, samples_group, favorites=False, **kwargs):
        super().__init__(**kwargs)

        self.cols = 3
        self.title = samples_group.name

        for sample in samples_group.samples:
            if favorites:
                btn = FavoritePlayButton(text=sample)
            else:
                btn = PlayButton(text=sample)
            self.bind(edit_favorites=btn.toggle_edit_favorite_input)
            self.add_widget(btn)

    def toggle_edit_favorites(self, caller, edit: bool):
        self.edit_favorites = edit


class PlayButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        self.fav_checkbox = FavoriteCheckbox()
        self.fav_checkbox.size = self.fav_checkbox.texture_size
        self.fav_checkbox.active = self.is_favorite()
        self.add_widget(self.fav_checkbox)
        self.bind(pos=self.update_checkbox_pos,
                  size=self.update_checkbox_pos)

        self.app.add_sample_button(self)

    def on_press(self):
        self.play()

    def is_favorite(self):
        fav_list = self.app.favorite_samples

        return self.text in fav_list

    def update_checkbox_pos(self, *args):
        self.fav_checkbox.size = self.fav_checkbox.texture_size
        self.fav_checkbox.pos = (
            self.x + self.width - self.fav_checkbox.width,
            self.y + self.height - self.fav_checkbox.height,
        )

    def toggle_checkbox_active(self, value):
        self.fav_checkbox.active = value

    def toggle_edit_favorite_input(self, caller, show_checkboxes):
        if show_checkboxes and self.fav_checkbox not in self.children:
            self.add_widget(self.fav_checkbox)
        elif not show_checkboxes and self.fav_checkbox in self.children:
            self.remove_widget(self.fav_checkbox)

    def play(self):
        self.app.sender.send_message('/sample', self.text)


class FavoritePlayButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        self.remove_btn = RemoveButton()
        self.add_widget(self.remove_btn)
        self.bind(pos=self.update_remove_btn_pos,
                  size=self.update_remove_btn_pos)

    def on_press(self):
        self.play()

    def update_remove_btn_pos(self, *args):
        self.remove_btn.pos = (
            self.x + self.width - self.remove_btn.width,
            self.y + self.height - self.remove_btn.height,
        )

    def toggle_edit_favorite_input(self, caller, show_remove_btn):
        if show_remove_btn and self.remove_btn not in self.children:
            self.add_widget(self.remove_btn)
        elif not show_remove_btn and self.remove_btn in self.children:
            self.remove_widget(self.remove_btn)

    def play(self):
        self.app.sender.send_message('/sample', self.text)


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


class RemoveButton(MDIconButton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        self.icon = 'close-box-outline'
        self.size = (24, 24)

    def on_press(self):
        screen = self.app.root.screens.samples
        screen.remove_favorite(self.parent.text)


class SamplesSettingsDropdown(MDDropdownMenu):
    pass


class SamplesDropdownMenuCheckbox(BoxLayout):
    edit_favorites = BooleanProperty()

    def on_edit_favorites(self, instance, value):
        app = App.get_running_app()
        app.root.screens.samples.toggle_edit_favorites(value)
