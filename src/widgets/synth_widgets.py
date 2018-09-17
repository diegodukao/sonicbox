from kivy.app import App
from kivy.graphics import Ellipse
from kivy.lang import Builder
from kivy.properties import BooleanProperty
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
from services import get_note_name, is_octave


Builder.load_file('ui/synth_screen.kv')


class DropdownMenuCheckbox(BoxLayout):
    show_notes = BooleanProperty()

    def on_show_notes(self, instance, value):
        app = App.get_running_app()
        app.root.screens.synth.keyboard.show_notes = value


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
    show_notes = BooleanProperty()

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
            self.bind(tonic=nb.update_note_label_text,
                      scale=nb.update_note_label_text)
            self.bind(scale=nb.draw_circle)
            self.bind(show_notes=nb.toggle_note_label)


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
        self.bind(pos=self.update_note_label_pos,
                  size=self.update_note_label_pos)

    def toggle_note_label(self, caller, show_notes):
        if show_notes and self.note_label not in self.children:
            self.update_note_label_text()
            self.add_widget(self.note_label)
        elif not show_notes and self.note_label in self.children:
            self.remove_widget(self.note_label)

    def on_press(self):
        self.play()

    def update_circle(self, *args):
        diameter = self.height / 2
        self.circle.size = diameter, diameter
        self.circle.pos = (self.center[0] - diameter / 2,
                           self.center[1] - diameter / 2)

    def draw_circle(self, *args):
        if is_octave(self.note, self.parent.scale):
            self._draw_on_canvas(self.circle)
        else:
            self._erase_from_canvas(self.circle)

    def update_note_label_pos(self, *args):
        self.note_label.size = self.size
        self.note_label.pos = self.pos

    def update_note_label_text(self, *args):
        if self.parent.show_notes:
            tonic = self.parent.tonic
            scale = self.parent.scale
            degree = self.note % SCALES[self.parent.scale]  # TODO: refactor
            self.note_label.text = get_note_name(
                tonic=tonic, scale=scale, degree=degree)

    def play(self):
        tonic = self.parent.tonic.replace('#', 's')

        self.app.sender.send_message(
            '/synth',
            [
                self.parent.synth,
                tonic,
                self.parent.scale,
                self.note,
            ]
        )

    def _draw_on_canvas(self, instruction):
        if instruction not in self.canvas.children:
            self.canvas.add(instruction)

    def _erase_from_canvas(self, instruction):
        if instruction in self.canvas.children:
            self.canvas.remove(instruction)


class SynthSettingsDropdown(MDDropdownMenu):
    pass
