class AppController:
    def __init__(self, model, view, settings_manager):
        self.model = model
        self.view = view
        self.settings_manager = settings_manager
        
        # Estado Selecciones
        self.current_prod_id = None
        self.current_cat_id = None
        self.current_bank_id = None

        # Snapshots Anti-spam
        self._snap_prod_estado = "off"
        self._snap_cat_desc = ""

        # Control Búsquedas
        self._busqueda_activa_prod = False
        self._busqueda_activa_cat  = False

        # Bindings
        self.view.bind_tab_change(self.handle_tab_change)
        self.view.bind_theme_change(self.handle_theme_change)
        self.view.bind_field_changed(self.handle_field_changed)
        self.view.bind_prod_actions(self.search_products, self.select_product, self.save_product)
        self.view.bind_cat_actions(self.search_categories, self.select_category, self.save_category)
        self.view.bind_bank_actions(self.select_bank, self.save_bank, self.new_bank_form, self.delete_bank)
        self.view.bind_clear_search_prod(self.clear_search_prod)
        self.view.bind_clear_search_cat(self.clear_search_cat)

        self.load_all_data()

    def load_all_data(self):
        self.search_products()
        self.search_categories()
        self.load_banks()

    def handle_theme_change(self, theme_name):
        settings = self.settings_manager.load_settings()
        settings["theme"] = theme_name
        self.settings_manager.save_settings(settings)

    def handle_tab_change(self, tab_name):
        print(f"[SISTEMA] Cambio de pestaña -> '{tab_name}'. Limpiando contextos...")
        if tab_name == "Catálogo de Productos":
            if not self._busqueda_activa_prod: self.view.search_entry.delete(0, "end")
            self.search_products()
            self.current_prod_id = None
            self._snap_prod_estado = "off"
            self.view.lbl_codigo.configure(text="ID: -")
            self.view.lbl_nombre.configure(text="Nombre: -")
            self.view.switch_var.set("off")
            self.view.set_save_status_prod("")
            self.view.set_save_button_state_prod(False)

        elif tab_name == "Categorías":
            if not self._busqueda_activa_cat: self.view.search_entry_cat.delete(0, "end")
            self.search_categories()
            self.current_cat_id = None
            self._snap_cat_desc = ""
            self.view.lbl_cat_sel.configure(text="Categoría: -")
            self.view.txt_cat_desc.delete("1.0", "end")
            self.view.populate_category_products([])
            self.view.set_save_status_cat("")
            self.view.set_save_button_state_cat(False)

        elif tab_name == "Bancos y Métodos de Pago":
            self.load_banks()
            self.new_bank_form()

    def handle_field_changed(self):
        # Productos
        if self.current_prod_id:
            cambio_prod = self.view.switch_var.get() != self._snap_prod_estado
            self.view.set_save_button_state_prod(cambio_prod)
        # Categorías
        if self.current_cat_id:
            cambio_cat = self.view.txt_cat_desc.get("1.0", "end-1c") != self._snap_cat_desc
            self.view.set_save_button_state_cat(cambio_cat)

    # ================= EVENTOS PRODUCTOS =================
    def search_products(self):
        term = self.view.search_entry.get()
        self._busqueda_activa_prod = bool(term.strip())
        productos = self.model.get_products(term)
        rows = [(p["id"], p["nombre"], p["stock"], p["precio"], p.get("estado", "off"), p["categoria"]) for p in productos]
        self.view.populate_products(rows)

    def select_product(self, event):
        selection = self.view.tree_prod.selection()
        if not selection: return
        values = self.view.tree_prod.item(selection[0]).get("values")
        if not values or len(values) < 2: return

        self.current_prod_id = values[0]
        self.view.lbl_codigo.configure(text=f"ID: {values[0]}")
        self.view.lbl_nombre.configure(text=f"Nombre: {values[1]}")
        self.view.set_save_status_prod("")
        
        prod = self.model.get_product_by_id(self.current_prod_id)
        if prod:
            estado = prod.get("estado", "off")
            self.view.switch_var.set(estado)
            self._snap_prod_estado = estado
        self.view.set_save_button_state_prod(False)

    def save_product(self):
        if not self.current_prod_id: return
        estado = self.view.switch_var.get()
        resultado = self.model.update_product_visibility(self.current_prod_id, estado)
        if resultado == "updated":
            self.view.set_save_status_prod("✔ Visibilidad guardada.", "#4CAF50")
            self._snap_prod_estado = estado
            self.search_products()
        self.view.set_save_button_state_prod(False)

    # ================= EVENTOS CATEGORÍAS =================
    def search_categories(self):
        term = self.view.search_entry_cat.get()
        self._busqueda_activa_cat = bool(term.strip())
        categorias = self.model.search_categories(term)
        rows = [(c["id"], c["nombre"], c.get("sigla", "")) for c in categorias]
        self.view.populate_categories(rows)

    def select_category(self, event):
        selection = self.view.tree_cat.selection()
        if not selection: return
        values = self.view.tree_cat.item(selection[0]).get("values")
        if not values or len(values) < 2: return

        self.current_cat_id = values[0]
        cat_nombre = values[1]
        self.view.lbl_cat_sel.configure(text=f"Categoría: {cat_nombre}")
        self.view.set_save_status_cat("")
        
        cat = self.model.get_category_by_id(self.current_cat_id)
        if cat:
            desc = cat.get("descripcion", "")
            self.view.txt_cat_desc.delete("1.0", "end")
            self.view.txt_cat_desc.insert("1.0", desc)
            self._snap_cat_desc = desc
        
        self.view.set_save_button_state_cat(False)
        prods = self.model.get_products_by_category(cat_nombre)
        prod_rows = [(p["id"], p["nombre"], p["precio"], p["stock"]) for p in prods]
        self.view.populate_category_products(prod_rows)

    def save_category(self):
        if not self.current_cat_id: return
        desc = self.view.txt_cat_desc.get("1.0", "end-1c")
        resultado = self.model.update_category_desc(self.current_cat_id, desc)
        if resultado == "updated":
            self.view.set_save_status_cat("✔ Descripción guardada.", "#4CAF50")
            self._snap_cat_desc = desc
        self.view.set_save_button_state_cat(False)

    # ================= EVENTOS BANCOS (CRUD) =================
    def load_banks(self):
        bancos = self.model.get_banks()
        rows = [(b["id"], b["banco"], b["cuenta"], b["titular"], b["cedula"], b["estado"]) for b in bancos]
        self.view.populate_banks(rows)

    def select_bank(self, event):
        selection = self.view.tree_bank.selection()
        if not selection: return
        values = self.view.tree_bank.item(selection[0]).get("values")
        if not values or len(values) < 2: return

        self.current_bank_id = values[0]
        self.view.lbl_bank_id.configure(text=f"ID: {values[0]}")
        self.view.entry_banco.delete(0, "end"); self.view.entry_banco.insert(0, values[1])
        self.view.entry_cuenta.delete(0, "end"); self.view.entry_cuenta.insert(0, values[2])
        self.view.entry_titular.delete(0, "end"); self.view.entry_titular.insert(0, values[3])
        self.view.entry_cedula.delete(0, "end"); self.view.entry_cedula.insert(0, str(values[4]))
        self.view.switch_var_bank.set(values[5])

    def new_bank_form(self):
        self.current_bank_id = None
        self.view.lbl_bank_id.configure(text="ID: (Nuevo)")
        self.view.entry_banco.delete(0, "end")
        self.view.entry_cuenta.delete(0, "end")
        self.view.entry_titular.delete(0, "end")
        self.view.entry_cedula.delete(0, "end")
        self.view.switch_var_bank.set("on")

    def save_bank(self):
        banco = self.view.entry_banco.get().strip()
        cuenta = self.view.entry_cuenta.get().strip()
        titular = self.view.entry_titular.get().strip()
        cedula = self.view.entry_cedula.get().strip()
        estado = self.view.switch_var_bank.get()

        if not banco or not cuenta:
            print("[GUI] Error: Banco y Cuenta son obligatorios.")
            return

        self.model.save_bank(self.current_bank_id, banco, cuenta, titular, cedula, estado)
        self.load_banks()
        self.new_bank_form()

    def delete_bank(self):
        if not self.current_bank_id: return
        self.model.delete_bank(self.current_bank_id)
        self.load_banks()
        self.new_bank_form()
    
    def clear_search_prod(self):
        """Limpia la barra de búsqueda de productos y recarga la tabla completa."""
        self.view.search_entry.delete(0, "end")
        self.search_products()

    def clear_search_cat(self):
        """Limpia la barra de búsqueda de categorías y recarga la tabla completa."""
        self.view.search_entry_cat.delete(0, "end")
        self.search_categories()