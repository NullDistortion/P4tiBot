class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Conectar los botones y eventos de la vista con métodos del controlador
        self.view.bind_search_action(self.handle_search)
        self.view.bind_save_action(self.handle_save)
        self.view.bind_tree_select(self.handle_product_selection)

        self.current_selected_code = None

        # Cargar datos iniciales al arrancar
        self.load_all_data()

    def load_all_data(self):
        self.handle_search() # Carga productos
        
        # Cargar categorías
        categories = self.model.get_categories()
        self.view.populate_categories(categories)

        # Cargar bancos (JOIN)
        banks = self.model.get_banks_and_owners()
        self.view.populate_banks(banks)

    def handle_search(self):
        search_term = self.view.search_entry.get()
        rows = self.model.get_products(search_term)
        self.view.populate_products(rows)

    def handle_product_selection(self, event):
        selected = self.view.tree_prod.selection()
        if selected:
            item = self.view.tree_prod.item(selected[0])
            values = item['values']
            self.current_selected_code = values[0]
            
            # Actualizar panel de lectura en la vista
            self.view.lbl_codigo.configure(text=f"Código: {values[0]}")
            self.view.lbl_nombre.configure(text=f"Nombre: {values[1]}")
            
            # Cargar estado en el switch
            estado_actual = str(values[4])
            if estado_actual == "1" or estado_actual == "True":
                self.view.switch_estado.select()
            else:
                self.view.switch_estado.deselect()
            
            self.view.txt_descripcion.delete("0.0", "end")
            # [Inferencia] En un entorno real, aquí pedirías al modelo la descripción actual para mostrarla

    def handle_save(self):
        if not self.current_selected_code:
            return
            
        desc = self.view.txt_descripcion.get("0.0", "end").strip()
        estado = 1 if self.view.switch_var.get() == "on" else 0
        
        # El controlador ordena al modelo actualizar la BD
        self.model.update_product_info(self.current_selected_code, desc, estado)
        
        # Recargar la tabla para mostrar los cambios
        self.handle_search()