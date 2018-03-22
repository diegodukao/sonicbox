from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.stacklayout import StackLayout
from kivymd.bottomsheet import MDListBottomSheet
from kivymd.button import MDRaisedButton
from pythonosc import udp_client

from samples import sample_path
from synths import SCALES, TONICS


class SynthsScreen(Screen):
    pass


class SynthButton(Button):

    def change_current(self, new_value):
        self.current = new_value

    def open_bottom_sheet(self, option):
        bs = MDListBottomSheet()

        if option == 'tonics':
            items = TONICS
        elif option == 'scales':
            items = SCALES

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
        self.sender = udp_client.SimpleUDPClient("127.0.0.1", 4559)
        self.note = note
        # self.text = str(note)

    def play(self):
        self.sender.send_message(
            '/synth',
            [self.parent.tonic, self.parent.scale, self.note])


class SamplesScreen(Screen):
    pass


class SamplesKeyboard(StackLayout):

    def __init__(self, samples, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'lr-tb'
        self.padding = ['8dp', '12dp']
        self.spacing = ['8dp', '5dp']

        for sample in samples:
            btn = PlayButton(text=sample)
            self.add_widget(btn)


class PlayButton(MDRaisedButton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sender = udp_client.SimpleUDPClient("127.0.0.1", 4559)

    def play(self):
        self.sender.send_message('/sample', sample_path(self.text))
