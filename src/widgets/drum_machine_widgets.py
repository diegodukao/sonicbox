from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton


Builder.load_file('ui/drum_machine_screen.kv')


class DrumMachineScreen(Screen):
    pass


class DMPlayButton(Button):

    def on_release(self):
        panel = self.parent.panel
        dt = (60 / int(self.bpm_value) / 4)
        panel.play(dt)


class DMStopButton(Button):

    def on_release(self):
        panel = self.parent.panel
        panel.stop()


class DMKeyboardColumn(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.app = App.get_running_app()

        for i in range(8):
            tb = ToggleButton()
            tb.value = i
            self.add_widget(tb)

    def add_overlay(self):
        self.canvas.add(Color(0, 0.5, 0, 0.4, group='overlay'))
        self.canvas.add(Rectangle(size=self.size, pos=self.pos,
                                  group='overlay'))
        self.canvas.ask_update()

    def remove_overlay(self):
        self.canvas.remove_group('overlay')
        self.canvas.ask_update()

    def get_pressed_buttons(self):
        return [button.value
                for button in self.children
                if button.state == 'down']

    def send_notes(self):
        self.app.sender.send_message(
            '/drum-machine',
            self.get_pressed_buttons()
        )


class DrumMachinePanel(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.playing = False
        self.current_column_number = -1
        self.dt = 0
        self.column_event = None

        for c in range(8):
            column = DMKeyboardColumn()
            self.add_widget(column)

        self.reset_current_column_number()

    def reset_current_column_number(self):
        self.current_column_number = len(self.children) - 1

    def update_current_column_number(self):
        self.current_column_number -= 1
        if self.current_column_number < 0:
            self.reset_current_column_number()

    @property
    def curr_column(self):
        return self.children[self.current_column_number]

    def play_curr_column(self):
        self.curr_column.add_overlay()
        self.curr_column.send_notes()

    def column_callback(self, dt):
        self.curr_column.remove_overlay()
        self.update_current_column_number()
        self.play_curr_column()

    def play(self, dt):
        if not self.playing:
            self.play_curr_column()
            self.column_event = Clock.schedule_interval(
                self.column_callback, dt)
            self.dt = dt
            self.playing = True
        elif dt != self.dt:
            self.column_event.cancel()
            self.column_event = Clock.schedule_interval(
                self.column_callback, dt)
            self.dt = dt

    def stop(self):
        self.column_event.cancel()
        self.curr_column.remove_overlay()
        self.reset_current_column_number()
        self.playing = False
