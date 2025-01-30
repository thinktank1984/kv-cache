import flet as ft
import sqlite3
import traceback
import os
from components.page import create_page

class QuranApp:
    def __init__(self):
        self.current_index = 0
        self.aya_data = []
        self.sura_map = {}
        self.audio_player = None
        
    def init_db(self):
        """Initialize the database and create current_aya table if it doesn't exist"""
        print("\n=== Initializing Database ===")
        try:
            conn = sqlite3.connect('aya.db')
            cursor = conn.cursor()
            
            create_current_aya_sql = '''
            CREATE TABLE IF NOT EXISTS current_aya (
                current_aya INTEGER
            );
            '''
            
            create_all_aya_sql = '''
            CREATE TABLE IF NOT EXISTS all_aya (
                id INTEGER,
                audio TEXT,
                image TEXT,
                sura INTEGER,
                aya INTEGER,
                aya_suffix INTEGER,
                sura_name TEXT
            );
            '''
            
            print("Creating tables if they don't exist...")
            cursor.execute(create_current_aya_sql)
            cursor.execute(create_all_aya_sql)
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"Existing tables in database: {tables}")
            
            cursor.execute('SELECT COUNT(*) FROM current_aya')
            count = cursor.fetchone()[0]
            print(f"Number of rows in current_aya: {count}")
            
            if count == 0:
                print("Initializing current_aya with first aya")
                cursor.execute('INSERT INTO current_aya (current_aya) VALUES (1)')
            
            conn.commit()
            print("Database initialization completed successfully")
        except Exception as e:
            print(f"Error in init_db: {str(e)}")
            print("Traceback:")
            print(traceback.format_exc())
            raise
        finally:
            if conn:
                conn.close()

    def update_current_aya(self, aya_id):
        """Update the current aya in the database"""
        print(f"\n=== Updating current aya to {aya_id} ===")
        conn = None
        try:
            conn = sqlite3.connect('aya.db')
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM current_aya')
            cursor.execute('INSERT INTO current_aya (current_aya) VALUES (?)', (aya_id,))
            
            conn.commit()
            print("Update successful")
        except Exception as e:
            print(f"Error in update_current_aya: {str(e)}")
            print(traceback.format_exc())
            raise
        finally:
            if conn:
                conn.close()

    def get_current_aya(self):
        """Get the current aya from the database"""
        print("\n=== Getting current aya ===")
        conn = None
        try:
            conn = sqlite3.connect('aya.db')
            cursor = conn.cursor()
            
            cursor.execute('SELECT current_aya FROM current_aya LIMIT 1')
            result = cursor.fetchone()
            print(f"Current aya query result: {result}")
            
            if result is None:
                cursor.execute('INSERT INTO current_aya (current_aya) VALUES (1)')
                conn.commit()
                return 1
                
            return result[0]
        except Exception as e:
            print(f"Error in get_current_aya: {str(e)}")
            print(traceback.format_exc())
            raise
        finally:
            if conn:
                conn.close()

    def load_aya_data(self):
        """Load aya data from SQLite database"""
        print("\n=== Loading aya data ===")
        conn = None
        try:
            conn = sqlite3.connect('aya.db')
            cursor = conn.cursor()
            
            select_sql = '''
                SELECT id, audio, image, sura, aya, aya_suffix, sura_name 
                FROM all_aya 
                ORDER BY id
            '''
            print(f"Executing SQL: {select_sql}")
            cursor.execute(select_sql)
            
            rows = cursor.fetchall()
            print(f"Number of rows fetched: {len(rows)}")
            if rows:
                print(f"Sample first row: {rows[0]}")
            
            self.aya_data = [{
                'id': row[0],
                'audio': os.path.join('q_files', row[1]),
                'image': os.path.join('q_files', row[2]),
                'sura': row[3],
                'aya': row[4],
                'aya_suffix': row[5],
                'sura_name': row[6]
            } for row in rows]
            
            return self.aya_data
        except Exception as e:
            print(f"Error in load_aya_data: {str(e)}")
            print(traceback.format_exc())
            raise
        finally:
            if conn:
                conn.close()

    def build_sura_dropdown(self):
        """Create dropdown for surah selection"""
        return ft.Dropdown(
            width=200,
            label="Select Surah",
            value=self.aya_data[self.current_index]['sura_name'],
            options=[
                ft.dropdown.Option(text=sura_name) 
                for sura_name in sorted(self.sura_map.keys())
            ],
        )

    def build_aya_dropdown(self, sura_name):
        """Create dropdown for ayah selection"""
        max_aya = self.sura_map[sura_name]['last_aya']
        return ft.Dropdown(
            width=100,
            label="Select Ayah",
            value=str(self.aya_data[self.current_index]['aya']),
            options=[
                ft.dropdown.Option(text=str(i)) 
                for i in range(1, max_aya + 1)
            ],
        )

    def find_aya_index(self, sura_name, aya_number):
        """Find the index of a specific ayah in a surah"""
        for i, item in enumerate(self.aya_data):
            if item['sura_name'] == sura_name and item['aya'] == aya_number:
                return i
        return None

    def page(self, page: ft.Page):
        """Create and configure the main application page"""
        create_page(self, page)
