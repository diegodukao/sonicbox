from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivymd.navigationdrawer import MDNavigationDrawer


Builder.load_file('ui/root.kv')


class Drawer(MDNavigationDrawer):
    pass


class ScreenArea(BoxLayout):
    pass


class CustomScreenManager(ScreenManager):

    def open_dropdown(self, caller):
        screen = self.get_screen(self.current)
        if hasattr(screen, 'dropdown'):
            return screen.dropdown.open(caller)
