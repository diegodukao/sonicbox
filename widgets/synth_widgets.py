from kivy.app import App
from kivy.graphics import Ellipse
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.bottomsheet import MDListBottomSheet
from kivymd.menu import MDDropdownMenu
from kivymd.selectioncontrols import MDCheckbox  # NOQA

from constants.synth import SCALES, SYNTHS, TONICS


Builder.load_file('ui/synth_screen.kv')


class DropdownMenuCheckbox(BoxLayout):
    pass


class SynthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        menu_items = [
            {'viewclass': 'DropdownMenuCheckbox'},
        ]
        self.dropdown = SynthSettingsDropdown(
            items=menu_items, width_mult=4)


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

        note_button_list = []
        for i in range(49):
            note_button = NoteButton(i)
            self.add_widget(note_button)
            note_button_list.append(note_button)

        # when the synth scale is changed, the circles that mark the octaves on
        # the NoteButtons will be updated
        for nb in note_button_list:
            self.bind(scale=nb.draw_circle)


class NoteLabel(Label):
    pass


class NoteButton(Button):

    def __init__(self, note, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.note = note

        self.circle = Ellipse()
        self.bind(pos=self.update_circle,
                  size=self.update_circle)

        self.note_label = NoteLabel()
        self.add_widget(self.note_label)
        self.bind(pos=self.update_note_label,
                  size=self.update_note_label)

    def on_press(self):
        self.play()

    def update_circle(self, *args):
        diameter = self.height / 2
        self.circle.size = diameter, diameter
        self.circle.pos = (self.center[0] - diameter / 2,
                           self.center[1] - diameter / 2)

    def draw_circle(self, *args):
        self.note_label.text = str(
            self.note % SCALES[self.parent.scale] + 1)

        if self._is_octave:
            self._draw_on_canvas(self.circle)
        else:
            self._erase_from_canvas(self.circle)

    def update_note_label(self, *args):
        self.note_label.size = self.size
        self.note_label.pos = self.pos

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

    @property
    def _is_octave(self):
        return bool(self.note % SCALES[self.parent.scale] == 0)

    def _draw_on_canvas(self, instruction):
        if instruction not in self.canvas.children:
            self.canvas.add(instruction)

    def _erase_from_canvas(self, instruction):
        if instruction in self.canvas.children:
            self.canvas.remove(instruction)


class SynthSettingsDropdown(MDDropdownMenu):
    pass
