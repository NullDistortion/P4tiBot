import json
import os

class SettingsManager:
    def __init__(self, config_file="settings.json"):
        self.config_file = config_file

    def load_settings(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        return {"window_size": "1024x768", "theme": "🌑  Oscuro"}

    def save_settings(self, settings):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)