# File: components/image_display.py
import flet as ft
from flet.user_control import UserControl

class ImageDisplay(UserControl):
    def __init__(self, initial_src, width=400, height=400):
        super().__init__()
        self.image_src = initial_src
        self.width = width
        self.height = height

    def build(self):
        return ft.Image(
            src=self.image_src,
            width=self.width,
            height=self.height,
            fit=ft.ImageFit.CONTAIN,
        )

    def update_source(self, new_src):
        self.image_src = new_src
        self.update()