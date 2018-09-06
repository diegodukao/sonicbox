from kivy.app import App
from kivy.graphics import Ellipse
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivymd.bottomsheet import MDListBottomSheet

from constants.synth import SCALES, SYNTHS, TONICS


Builder.load_file('ui/synth_screen.kv')


class SynthScreen(Screen):
    pass


class SynthButton(Button):
    current = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bottom_sheets = {
            "synth": self._create_bottom_sheet("synth"),
            "tonics": self._create_bottom_sheet("tonics"),
            "scales": self._create_bottom_sheet("scales"),
        }

    def change_current(self, new_value):
        self.current = new_value

    def open_bottom_sheet(self, option):
        bs = self.bottom_sheets[option]

        bs.open()

    def _create_bottom_sheet(self, option):
        bs = MDListBottomSheet()

        if option == 'synth':
            items = sorted(SYNTHS)
        elif option == 'tonics':
            items = TONICS
        elif option == 'scales':
            items = [scale_name for scale_name in sorted(SCALES.keys())]
        else:
            raise Exception

        for item in items:
            bs.add_item(item, lambda x: self.change_current(x.text),
                        icon='nfc')

        return bs


class SynthKeyboard(GridLayout):
    synth = StringProperty()
    tonic = StringProperty()
    scale = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 7

        nb_list = []
        for i in range(49):
            nb = NoteButton(i)
            self.add_widget(nb)
            nb_list.append(nb)

        for nb in nb_list:
            self.bind(scale=nb.update_circle)


class NoteButton(Button):

    def __init__(self, note, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.note = note

        with self.canvas:
            self.circle = Ellipse()

        self.bind(pos=self.update_circle,
                  size=self.update_circle)

    def update_circle(self, *args):
        # TODO: erase circle from canvas when updating scale

        # TODO: use number of notes of the scale to determine where to draw
        # the circle
        # if self.note % SCALES[self.parent.scale] == 0:
        if self.note % 5 == 0:
            diameter = self.height / 2
            self.circle.size = diameter, diameter
            self.circle.pos = (self.center[0] - diameter / 2,
                               self.center[1] - diameter / 2)
        else:
            self.circle.size = (0, 0)

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
