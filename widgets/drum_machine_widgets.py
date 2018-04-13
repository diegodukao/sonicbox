from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from pythonosc import udp_client


Builder.load_file('ui/drum_machine_screen.kv')


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


class DMKeyboardColumn(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.sender = udp_client.SimpleUDPClient("127.0.0.1", 4559)

        for i in range(8):
            tb = ToggleButton()
            tb.value = i
            self.add_widget(tb)

    def get_pressed_buttons(self):
        return [button.value
                for button in self.children
                if button.state == 'down']

    def play(self):
        self.sender.send_message(
            '/drum-machine',
            self.get_pressed_buttons()
        )


class DrumMachineKeyboard(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.playing = False
        self.current_column = -1
        self.dt = 0

        for c in range(8):
            column = DMKeyboardColumn()
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

    # TODO: refactor it
    def curr_col(self):
        return self.children[self.current_column]

    def update_overlay(self, dt):
        self.remove_col_overlay()
        self.update_current_column()
        self.add_col_overlay()
        # TODO: refactor it
        col = self.curr_col()
        col.play()

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
