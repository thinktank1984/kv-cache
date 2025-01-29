# File: components/audio_player.py
import flet as ft
from flet.user_control import UserControl

class AudioPlayer(UserControl):
    def __init__(self, initial_src, on_state_changed, volume=1.0):
        super().__init__()
        self.audio_src = initial_src
        self.on_state_changed = on_state_changed
        self.volume = volume
        self.audio = None

    def build(self):
        self.audio = ft.Audio(
            src=self.audio_src,
            autoplay=False,
            volume=self.volume,
            on_state_changed=self.on_state_changed
        )
        return self.audio

    def play(self):
        if self.audio:
            self.audio.play()
            self.update()

    def update_source(self, new_src):
        if self.audio:
            self.audio.src = new_src
            self.update()