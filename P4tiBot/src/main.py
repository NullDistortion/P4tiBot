from model.model import DatabaseModel
from view.view import AppView
from controller.controller import AppController
from utils.settings_manager import SettingsManager

def main():
    # 1. Cargar configuraciones del JSON primero
    settings_manager = SettingsManager()
    app_settings = settings_manager.load_settings()

    # 2. Crear el Modelo
    model = DatabaseModel() 
    
    # 3. Crear la Vista (pasándole las configuraciones cargadas)
    # La clase AppView deberá modificarse para aceptar 'app_settings'
    view = AppView(app_settings) 
    
    # 4. Crear el Controlador y conectarlos
    # El controlador también puede recibir el settings_manager si necesita modificarlo luego
    controller = AppController(model, view, settings_manager)
    
    # 5. Iniciar la interfaz
    view.mainloop()

if __name__ == "__main__":
    main()