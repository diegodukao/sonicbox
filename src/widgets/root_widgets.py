from kivy.uix.screenmanager import ScreenManager


class CustomScreenManager(ScreenManager):

    def open_dropdown(self, caller):
        screen = self.get_screen(self.current)
        if hasattr(screen, 'dropdown'):
            return screen.dropdown.open(caller)
