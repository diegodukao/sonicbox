import kivy

from kivy.app import App
from kivymd.theming import ThemeManager


kivy.require('1.10.0')


class SonicBox(App):
    theme_cls = ThemeManager()

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return self.root


SonicBox().run()
