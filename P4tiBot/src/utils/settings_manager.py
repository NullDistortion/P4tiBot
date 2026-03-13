# src/utils/settings_manager.py
import json
import os

class SettingsManager:
    def __init__(self, filepath="settings.json"):
        self.filepath = filepath
        # Valores por defecto en caso de que el archivo JSON no exista aún
        self.default_settings = {
            "theme": "dark",
            "window_size": "1024x768",
            "auto_refresh_data": True
        }

    def load_settings(self):
        if not os.path.exists(self.filepath):
            self.save_settings(self.default_settings)
            return self.default_settings
        
        with open(self.filepath, "r") as file:
            return json.load(file)

    def save_settings(self, settings_dict):
        with open(self.filepath, "w") as file:
            json.dump(settings_dict, file, indent=4)