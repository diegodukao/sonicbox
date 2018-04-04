from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from kivymd.bottomsheet import MDListBottomSheet
from pythonosc import udp_client

from samples import sample_path
from synths import SCALES, SYNTHS, TONICS


class DrumMachineScreen(Screen):
    pass


class DMPlayButton(Button):

    def on_release(self):
        col = self.parent.parent.parent.keyboard.children[7]
        col.canvas.add(Color(0, 0.5, 0, 0.4))
        col.canvas.add(Rectangle(size=col.size, pos=col.pos))
        col.canvas.ask_update()


class DrumMachineKeyboard(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"

        for c in range(8):
            column = BoxLayout(
                orientation="vertical",
                id="column_{}".format(c))

            for l in range(8):
                tb = ToggleButton()
                column.add_widget(tb)

            self.add_widget(column)


class SynthsScreen(Screen):
    pass


class SynthButton(Button):

    def change_current(self, new_value):
        self.current = new_value

    def open_bottom_sheet(self, option):
        bs = MDListBottomSheet()

        if option == 'synths':
            items = SYNTHS
        elif option == 'tonics':
            items = TONICS
        elif option == 'scales':
            items = SCALES
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
        self.sender = udp_client.SimpleUDPClient("127.0.0.1", 4559)
        self.note = note
        # self.text = str(note)

    def play(self):
        self.sender.send_message(
            '/synth',
            [
                self.parent.synth,
                self.parent.tonic,
                self.parent.scale,
                self.note,
            ]
        )


class SamplesScreen(Screen):
    pass


class SamplesKeyboard(GridLayout):

    def __init__(self, samples, **kwargs):
        super().__init__(**kwargs)

        self.cols = 3

        for sample in samples:
            btn = PlayButton(text=sample)
            self.add_widget(btn)


class PlayButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sender = udp_client.SimpleUDPClient("127.0.0.1", 4559)

    def play(self):
        self.sender.send_message('/sample', sample_path(self.text))
