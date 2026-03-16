from model.model import PatibotModel
from view.view import AppView
from controller.controller import AppController
from utils.settings_manager import SettingsManager

def main():
    settings_manager = SettingsManager()
    app_settings = settings_manager.load_settings()

    model = PatibotModel() 
    view = AppView(app_settings) 
    
    controller = AppController(model, view, settings_manager)
    
    view.mainloop()

if __name__ == "__main__":
    main()