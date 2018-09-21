from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.navigationdrawer import NavigationLayout


Builder.load_file('ui/root.kv')


class RootWidget(NavigationLayout):
    pass


class CustomScreenManager(ScreenManager):

    def open_dropdown(self, caller):
        screen = self.get_screen(self.current)
        if hasattr(screen, 'dropdown'):
            return screen.dropdown.open(caller)
