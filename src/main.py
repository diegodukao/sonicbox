import kivy

from kivy.app import App
from kivymd.theming import ThemeManager
from pythonosc import udp_client

from services import storage


kivy.require('1.10.0')


class Sonicbox(App):
    theme_cls = ThemeManager()
    _favorite_samples = None
    _sample_buttons = {}
    _sender = None

    def create_sender(self, ip):
        self._sender = udp_client.SimpleUDPClient(ip, 4559)

    @property
    def sender(self):
        if not self._sender:
            self.create_sender("127.0.0.1")
        return self._sender

    def _get_favorite_samples(self):
        store = storage.get_storage()

        if store.exists('samples') and ('favorites' in store.get('samples')):
            fav_list = store.get('samples')['favorites']
        else:
            fav_list = []
            store.put('samples', favorites=fav_list)
        self._favorite_samples = fav_list

    @property
    def favorite_samples(self):
        if self._favorite_samples is None:
            self._get_favorite_samples()
        return self._favorite_samples

    def update_favorite_samples(self, caller, favorites):
        self._favorite_samples = favorites
        storage.update_favorite_samples(favorites)

    @property
    def sample_buttons(self):
        return self._sample_buttons

    def add_sample_button(self, sample_btn):
        self._sample_buttons[sample_btn.text] = sample_btn

    def build(self):
        self._favorite_samples = self._get_favorite_samples()
        self.theme_cls.theme_style = "Dark"
        return self.root


Sonicbox().run()
