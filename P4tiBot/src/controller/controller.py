class AppController:
    def __init__(self, model, view, settings_manager):
        self.model = model
        self.view = view
        self.settings_manager = settings_manager
        
        self.current_selected_code = None

        self.view.bind_search_action(self.handle_search)
        self.view.bind_save_action(self.handle_save)
        self.view.bind_tree_select(self.handle_product_selection)

        self.load_all_data()
        self.view.bind_search_cat_action(self.handle_search_cat)
        self.view.bind_tree_cat_select(self.handle_category_selection)

    def load_all_data(self):
        self.handle_search()
        
        categorias = self.model.get_categories()
        # [Inferencia] Se mapean las listas a tuplas requeridas por la vista
        cat_tuples = [(i+1, c, c[:3].upper()) for i, c in enumerate(categorias)]
        self.view.populate_categories(cat_tuples)
        
        bancos = self.model.get_banks_and_owners()
        self.view.populate_banks(bancos)

    def handle_search(self):
        term = self.view.search_entry.get()
        rows = self.model.get_products(term)
        
        formatted_rows = []
        for r in rows:
            formatted_rows.append((
                r["id"], 
                r["nombre"], 
                r["stock"], 
                r["precio"], 
                r.get("estado", "off"), 
                r["categoria"]
            ))
            
        self.view.populate_products(formatted_rows)

    def handle_product_selection(self, event):
        selection = self.view.tree_prod.selection()
        if not selection:
            return
            
        item = self.view.tree_prod.item(selection[0])
        values = item.get("values")
        
        # Corrección del IndexError: se verifica que la lista contenga elementos
        if not values or len(values) < 2:
            return

        self.current_selected_code = values[0]
        self.view.lbl_codigo.configure(text=f"Código: {values[0]}")
        self.view.lbl_nombre.configure(text=f"Nombre: {values[1]}")

        # Rellenar la caja de texto y el interruptor
        producto = self.model.get_product_by_id(self.current_selected_code)
        if producto:
            self.view.txt_descripcion.delete("1.0", "end")
            self.view.txt_descripcion.insert("1.0", producto.get("descripcion", ""))
            self.view.switch_var.set(producto.get("estado", "off"))

    def handle_save(self):
        if not self.current_selected_code:
            return
            
        desc = self.view.txt_descripcion.get("1.0", "end-1c")
        estado = self.view.switch_var.get()
        
        self.model.update_product_info(self.current_selected_code, desc, estado)
        self.handle_search() # Refresca la tabla para ver el estado actualizado

    def handle_search_cat(self):
        term = self.view.search_entry_cat.get()
        categorias = self.model.search_categories(term)
        
        # Mapeo de la lista a tuplas para la tabla
        cat_tuples = [(i+1, c, c[:3].upper()) for i, c in enumerate(categorias)]
        self.view.populate_categories(cat_tuples)

    def handle_category_selection(self, event):
        selection = self.view.tree_cat.selection()
        if not selection:
            return

        item = self.view.tree_cat.item(selection[0])
        values = item.get("values")

        if not values or len(values) < 2:
            return

        categoria_nombre = values[1]
        self.view.lbl_cat_sel.configure(text=f"Productos de la Categoría: {categoria_nombre}")

        # Obtener y formatear los productos cruzados por categoría
        productos = self.model.get_products_by_category(categoria_nombre)
        formatted_rows = [(p["id"], p["nombre"], p["precio"], p["stock"]) for p in productos]
        self.view.populate_category_products(formatted_rows)