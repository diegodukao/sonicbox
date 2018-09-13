from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


Builder.load_file('ui/settings_screen.kv')


class SettingsScreen(Screen):

    def update_sender(self, ip):
        app = App.get_running_app()
        app.create_sender(ip)
