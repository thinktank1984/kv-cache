# File: components/status_bar.py
import flet as ft
from flet.user_control import UserControl

class StatusBar(UserControl):
    def __init__(self, initial_sura, initial_aya, initial_suffix=""):
        super().__init__()
        self.sura = initial_sura
        self.aya = initial_aya
        self.suffix = initial_suffix

    def build(self):
        self.text = ft.Text(
            self._get_status_text(),
            size=16,
            weight="bold"
        )
        return self.text

    def _get_status_text(self):
        suffix_display = f" - {self.suffix}" if self.suffix else ""
        return f"Surah {self.sura} - Ayah {self.aya}{suffix_display}"

    def update_status(self, sura=None, aya=None, suffix=None):
        if sura:
            self.sura = sura
        if aya:
            self.aya = aya
        if suffix is not None:
            self.suffix = suffix
        
        if self.text:
            self.text.value = self._get_status_text()
            self.update()