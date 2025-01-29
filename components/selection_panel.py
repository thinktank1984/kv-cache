# File: components/selection_panel.py
import flet as ft
from flet.user_control import UserControl

class SelectionPanel(UserControl):
    def __init__(self, sura_data, initial_sura, initial_aya, on_sura_change, on_aya_change):
        super().__init__()
        self.sura_data = sura_data
        self.initial_sura = initial_sura
        self.initial_aya = initial_aya
        self.on_sura_change = on_sura_change
        self.on_aya_change = on_aya_change

    def build(self):
        self.sura_dropdown = ft.Dropdown(
            width=200,
            label="Select Surah",
            value=self.initial_sura,
            options=[
                ft.dropdown.Option(text=sura_name)
                for sura_name in sorted(self.sura_data.keys())
            ],
            on_change=self.on_sura_change
        )

        self.aya_dropdown = ft.Dropdown(
            width=100,
            label="Select Ayah",
            value=str(self.initial_aya),
            options=self._build_aya_options(self.initial_sura),
            on_change=self.on_aya_change
        )

        return ft.Row(
            [self.sura_dropdown, self.aya_dropdown],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def _build_aya_options(self, sura_name):
        max_aya = self.sura_data[sura_name]['last_aya']
        return [
            ft.dropdown.Option(text=str(i))
            for i in range(1, max_aya + 1)
        ]

    def update_aya_options(self, sura_name, selected_aya="1"):
        self.aya_dropdown.options = self._build_aya_options(sura_name)
        self.aya_dropdown.value = selected_aya
        self.update()