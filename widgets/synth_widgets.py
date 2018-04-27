from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivymd.bottomsheet import MDListBottomSheet

from constants.synth import SCALES, SYNTHS, TONICS


Builder.load_file('ui/synth_screen.kv')


class SynthScreen(Screen):
    pass


class SynthButton(Button):

    def change_current(self, new_value):
        self.current = new_value

    def open_bottom_sheet(self, option):
        bs = MDListBottomSheet()

        if option == 'synth':
            items = sorted(SYNTHS)
        elif option == 'tonics':
            items = TONICS
        elif option == 'scales':
            items = sorted(SCALES)
        else:
            raise Exception

        for item in items:
            bs.add_item(item, lambda x: self.change_current(x.text),
                        icon='nfc')

        bs.open()


class SynthKeyboard(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 7

        for i in range(49):
            self.add_widget(NoteButton(i))


class NoteButton(Button):

    def __init__(self, note, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.note = note

    def on_press(self):
        self.play()

    def play(self):
        self.app.sender.send_message(
            '/synth',
            [
                self.parent.synth,
                self.parent.tonic,
                self.parent.scale,
                self.note,
            ]
        )
