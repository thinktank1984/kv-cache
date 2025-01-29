# File: components/audio_player.py
import flet as ft

def create_audio_player(initial_src, on_state_changed, volume=1.0):
    audio = ft.Audio(
        src=initial_src,
        autoplay=False,
        volume=volume,
        on_state_changed=on_state_changed
    )
    
    def update_source(new_src):
        audio.src = new_src
        audio.update()
    
    audio.update_source = update_source
    return audio
