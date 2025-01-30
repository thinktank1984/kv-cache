import flet as ft
import traceback

def create_page(app, page: ft.Page):
    """Create and configure the main application page"""
    print("\n=== Starting Quran Audio Image App ===")
    page.title = "Quran Audio Image App"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.padding = 20
    page.theme_mode = "light"

    try:
        # Initialize database and load data
        app.init_db()
        app.aya_data = app.load_aya_data()
        if not app.aya_data:
            raise ValueError("No aya data found in database")
        app.current_index = app.get_current_aya() - 1

        # Get unique sura names and their first ayah indices
        for item in app.aya_data:
            if item['sura_name'] not in app.sura_map:
                app.sura_map[item['sura_name']] = {
                    'first_index': app.aya_data.index(item),
                    'last_aya': max(x['aya'] for x in app.aya_data if x['sura_name'] == item['sura_name'])
                }

        status_text = ft.Text(
            f"Surah {app.aya_data[app.current_index]['sura_name']} - Ayah {app.aya_data[app.current_index]['aya']}", 
            size=16,
            weight="bold"
        )

        # Create dropdowns
        sura_dropdown = app.build_sura_dropdown()
        aya_dropdown = app.build_aya_dropdown(app.aya_data[app.current_index]['sura_name'])

        app.audio_player = app.create_audio_player(app.aya_data[app.current_index]['audio'])
        page.overlay.append(app.audio_player)

        img_display = ft.Image(
            src=app.aya_data[app.current_index]['image'],
            width=400,
            height=400,
            fit=ft.ImageFit.CONTAIN,
        )

        def update_content():
            """Update the UI content"""
            print(f"\n=== Updating content for index {app.current_index} ===")
            
            # Update audio player source if it exists
            if app.audio_player:
                app.audio_player.src = app.aya_data[app.current_index]['audio']
            
            # Update image and text
            img_display.src = app.aya_data[app.current_index]['image']
            suffix = app.aya_data[app.current_index]['aya_suffix']
            suffix_display = f" - {suffix}" if suffix else ""
            status_text.value = f"Surah {app.aya_data[app.current_index]['sura_name']} - Ayah {app.aya_data[app.current_index]['aya']}{suffix_display}"
            
            # Update dropdown selections
            sura_dropdown.value = app.aya_data[app.current_index]['sura_name']
            aya_dropdown.value = str(app.aya_data[app.current_index]['aya'])
            
            # Update database
            app.update_current_aya(app.aya_data[app.current_index]['id'])
            
            # Update the page
            page.update()
            print("Content update complete")

        def on_sura_change(e):
            """Handle surah selection change"""
            selected_sura = sura_dropdown.value
            # Update ayah dropdown with new range
            aya_dropdown.options = [
                ft.dropdown.Option(text=str(i)) 
                for i in range(1, app.sura_map[selected_sura]['last_aya'] + 1)
            ]
            aya_dropdown.value = "1"
            go_to_selection(None)
            page.update()

        def on_aya_change(e):
            """Handle ayah selection change"""
            go_to_selection(e)

        def go_to_selection(e):
            """Navigate to selected ayah"""
            if not sura_dropdown.value or not aya_dropdown.value:
                return

            new_index = app.find_aya_index(sura_dropdown.value, int(aya_dropdown.value))
            if new_index is not None:
                app.current_index = new_index
                update_content()

        def prev_item(e=None):
            """Move to previous item without playing"""
            app.current_index = (app.current_index - 1) % len(app.aya_data)
            print(f"Moving to previous item, new index: {app.current_index}")
            update_content()

        # Store update_content method on app instance for use in callbacks
        app.update_content = update_content
        
        sura_dropdown.on_change = on_sura_change
        aya_dropdown.on_change = on_aya_change

        # Add elements to page
        page.add(
            ft.Column(
                [
                    status_text,
                    ft.Row(
                        [sura_dropdown, aya_dropdown],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    img_display,
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.SKIP_PREVIOUS,
                                icon_size=30,
                                on_click=prev_item,
                            ),
                            ft.IconButton(
                                icon=ft.icons.PLAY_ARROW,
                                icon_size=30,
                                on_click=lambda e: app.next_item_and_play(),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
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
