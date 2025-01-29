# File: components/navigation_controls.py
import flet as ft
from flet.user_control import UserControl

class NavigationControls(UserControl):
    def __init__(self, on_previous, on_play, on_next):
        super().__init__()
        self.on_previous = on_previous
        self.on_play = on_play
        self.on_next = on_next

    def build(self):
        return ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.SKIP_PREVIOUS,
                    icon_size=30,
                    on_click=self.on_previous,
                ),
                ft.IconButton(
                    icon=ft.icons.PLAY_ARROW,
                    icon_size=30,
                    on_click=self.on_play,
                ),
                ft.IconButton(
                    icon=ft.icons.SKIP_NEXT,
                    icon_size=30,
                    on_click=self.on_next,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )