# File: main.py
import flet as ft
import traceback
import os
from db_functions import DatabaseConnection, init_db, load_aya_data, get_current_aya, update_current_aya
from components import (
    NavigationControls,
    SelectionPanel,
    AudioPlayer,
    ImageDisplay,
    StatusBar
)

def main(page: ft.Page):
    print("\n=== Starting Quran Audio Image App ===")
    page.title = "Quran Audio Image App"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.padding = 20
    page.theme_mode = "light"

    try:
        # Initialize database and load data
        page.db = DatabaseConnection('aya.db')
        conn = page.db.get_connection()
        init_db(conn)
        
        aya_data = load_aya_data(conn)
        if not aya_data:
            raise ValueError("No aya data found in database")
        
        current_index = get_current_aya(conn) - 1

        # Store data in page object
        page.conn = conn
        page.aya_data = aya_data
        page.current_index = current_index

        # Build sura map for dropdown
        sura_map = {}
        for item in aya_data:
            if item['sura_name'] not in sura_map:
                sura_map[item['sura_name']] = {
                    'first_index': aya_data.index(item),
                    'last_aya': max(x['aya'] for x in aya_data if x['sura_name'] == item['sura_name'])
                }

        def find_aya_index(sura_name, aya_number):
            """Find the index of a specific ayah"""
            for i, item in enumerate(page.aya_data):
                if item['sura_name'] == sura_name and item['aya'] == aya_number:
                    return i
            return None

        def update_content():
            """Update all UI components"""
            current_aya = page.aya_data[page.current_index]
            
            # Update components
            audio_player.update_source(current_aya['audio'])
            image_display.update_source(current_aya['image'])
            status_bar.update_status(
                current_aya['sura_name'],
                current_aya['aya'],
                current_aya.get('aya_suffix', '')
            )
            selection_panel.sura_dropdown.value = current_aya['sura_name']
            selection_panel.aya_dropdown.value = str(current_aya['aya'])
            
            # Update database
            update_current_aya(page.conn, current_aya['id'])
            page.update()

        def on_sura_change(e):
            """Handle surah selection change"""
            selected_sura = selection_panel.sura_dropdown.value
            selection_panel.update_aya_options(selected_sura)
            go_to_selection(None)

        def on_aya_change(e):
            """Handle ayah selection change"""
            go_to_selection(e)

        def go_to_selection(e):
            """Navigate to selected ayah"""
            sura_value = selection_panel.sura_dropdown.value
            aya_value = selection_panel.aya_dropdown.value
            
            if not sura_value or not aya_value:
                return

            new_index = find_aya_index(sura_value, int(aya_value))
            if new_index is not None:
                page.current_index = new_index
                update_content()

        def play_current(e=None):
            """Play current aya"""
            audio_player.play()

        def next_item_and_play(e=None):
            """Move to next item and play"""
            page.current_index = (page.current_index + 1) % len(page.aya_data)
            update_content()
            play_current()

        def prev_item(e=None):
            """Move to previous item"""
            page.current_index = (page.current_index - 1) % len(page.aya_data)
            update_content()

        def on_audio_state_changed(e):
            """Handle audio completion"""
            if e.data == "completed":
                next_item_and_play()

        # Initialize UI Components
        current_aya = aya_data[current_index]
        
        status_bar = StatusBar(
            current_aya['sura_name'],
            current_aya['aya'],
            current_aya.get('aya_suffix', '')
        )

        selection_panel = SelectionPanel(
            sura_map,
            current_aya['sura_name'],
            current_aya['aya'],
            on_sura_change,
            on_aya_change
        )

        audio_player = AudioPlayer(
            current_aya['audio'],
            on_audio_state_changed
        )
        page.overlay.append(audio_player.build())

        image_display = ImageDisplay(
            current_aya['image']
        )

        navigation_controls = NavigationControls(
            prev_item,
            play_current,
            next_item_and_play
        )

        # Add cleanup handler
        def cleanup(e):
            if hasattr(page, 'db'):
                page.db.close()
        
        page.on_close = cleanup

        # Build page layout
        page.add(
            ft.Column(
                [
                    status_bar,
                    selection_panel,
                    image_display,
                    navigation_controls,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            )
        )

    except Exception as e:
        error_msg = f"Error initializing app: {str(e)}"
        print("\n=== ERROR ===")
        print(error_msg)
        print("Detailed traceback:")
        print(traceback.format_exc())
        page.add(ft.Text(error_msg, color="red", size=16, weight="bold"))
        if hasattr(page, 'db'):
            page.db.close()

if __name__ == "__main__":
    print("\n=== Starting Application ===")
    ft.app(target=main)