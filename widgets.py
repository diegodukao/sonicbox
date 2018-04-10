from kivy.clock import Clock
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
        # TODO: Find a better way to get the dm keyboard reference
        keyboard = self.parent.parent.parent.parent.keyboard
        dt = (60 / int(self.bpm_value) / 4)
        keyboard.play(dt)


class DMStopButton(Button):

    def on_release(self):
        pass
        # TODO: Find a better way to get the dm keyboard reference
        keyboard = self.parent.parent.parent.parent.keyboard
        keyboard.stop()


class DrumMachineKeyboard(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.playing = False
        self.current_column = -1
        self.dt = 0

        for c in range(8):
            column = BoxLayout(
                orientation="vertical",
                id="column_{}".format(c))

            for l in range(8):
                tb = ToggleButton()
                column.add_widget(tb)

            self.add_widget(column)

        self.reset_current_column()

    def reset_current_column(self):
        self.current_column = len(self.children) - 1

    def update_current_column(self):
        self.current_column -= 1
        if self.current_column < 0:
            self.reset_current_column()

    def add_col_overlay(self):
        col = self.children[self.current_column]
        col.canvas.add(Color(0, 0.5, 0, 0.4, group='overlay'))
        col.canvas.add(Rectangle(size=col.size, pos=col.pos,
                                 group='overlay'))
        col.canvas.ask_update()

    def remove_col_overlay(self):
        col = self.children[self.current_column]
        col.canvas.remove_group('overlay')
        col.canvas.ask_update()

    def update_overlay(self, dt):
        self.remove_col_overlay()
        self.update_current_column()
        self.add_col_overlay()

    def play(self, dt):
        if not self.playing:
            self.add_col_overlay()
            self.overlay_event = Clock.schedule_interval(
                self.update_overlay, dt)
            self.dt = dt
            self.playing = True
        elif dt != self.dt:
            self.overlay_event.cancel()
            self.overlay_event = Clock.schedule_interval(
                self.update_overlay, dt)
            self.dt = dt

    def stop(self):
        self.overlay_event.cancel()
        self.remove_col_overlay()
        self.reset_current_column()
        self.playing = False


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
