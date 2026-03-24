import customtkinter as ctk
from tkinter import ttk

THEMES = {
    "🌑  Oscuro":       ("dark",  "#2c3e50", "#34495e", "#1f538d"),
    "🔵  Azul Oscuro":  ("dark",  "#0a5dde", "#0847b0", "#3498db"),
    "🟢  Verde Oscuro": ("dark",  "#1e8449", "#155d34", "#27ae60"),
    "🔴  Rojo Oscuro":  ("dark",  "#b03a2e", "#8b2a20", "#e74c3c")
}

class AppView(ctk.CTk):
    def __init__(self, app_settings):
        super().__init__()
        self.app_settings = app_settings
        self._on_tab_change_callback    = None
        self._on_theme_change_callback  = None
        self._on_field_changed_callback = None

        self.title("Gestor P4tiBot - Administrador")
        self.geometry(self.app_settings.get("window_size", "1024x768"))

        saved_theme = self.app_settings.get("theme", "🌑  Oscuro")
        if saved_theme not in THEMES: saved_theme = "🌑  Oscuro"
        self._current_theme = saved_theme
        
        mode, primary, secondary, _ = THEMES[saved_theme]
        ctk.set_appearance_mode(mode)
        ctk.set_default_color_theme("dark-blue")

        # Top Bar
        self.top_bar = ctk.CTkFrame(self, height=52, corner_radius=0)
        self.top_bar.pack(fill="x", padx=0, pady=0)
        self.top_bar.pack_propagate(False)

        ctk.CTkLabel(self.top_bar, text="🎨 Tema:", font=("Arial", 12)).pack(side="left", padx=(14, 4))
        
        self.theme_menu = ctk.CTkOptionMenu(self.top_bar, values=list(THEMES.keys()), width=185, command=self._on_theme_selected)
        self.theme_menu.set(saved_theme)
        self.theme_menu.pack(side="left", padx=(0, 10), pady=8)

        self.lbl_title = ctk.CTkLabel(self.top_bar, text="⚙  Gestor P4tiBot — Administrador", font=("Arial", 15, "bold"))
        self.lbl_title.pack(side="left", padx=20)

        # Tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(8, 20))
        self.tab_prod = self.tabview.add("Catálogo de Productos")
        self.tab_cat  = self.tabview.add("Categorías")
        self.tab_bank = self.tabview.add("Bancos y Métodos de Pago")

        self._build_productos_tab()
        self._build_categorias_tab()
        self._build_bancos_tab()

        self.tabview.configure(command=self._on_tab_changed)
        self._apply_accent(saved_theme)

# ================= TAB PRODUCTOS =================
    def _build_productos_tab(self):
        # 1. Se añade 'minsize' para forzar que el panel derecho nunca se encoja o expanda
        self.tab_prod.grid_columnconfigure(0, weight=3, minsize=500)
        self.tab_prod.grid_columnconfigure(1, weight=1, minsize=300)
        self.tab_prod.grid_rowconfigure(0, weight=1)

        self.left_panel_prod = ctk.CTkFrame(self.tab_prod)
        self.left_panel_prod.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        search_row = ctk.CTkFrame(self.left_panel_prod, fg_color="transparent")
        search_row.pack(fill="x", padx=10, pady=10)

        self.search_entry = ctk.CTkEntry(search_row, placeholder_text="Buscar producto...")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.btn_search = ctk.CTkButton(search_row, text="Buscar", width=80)
        self.btn_search.pack(side="left")

        #Botón Limpiar Productos
        self.btn_clear_prod = ctk.CTkButton(search_row, text="Limpiar", width=80, fg_color="gray40")
        self.btn_clear_prod.pack(side="left", padx=(4, 0))

        columns = ("id", "nombre", "cantidad", "pvp", "estado", "categoria")
        self.tree_prod = ttk.Treeview(self.left_panel_prod, columns=columns, show="headings")
        for col in columns:
            self.tree_prod.heading(col, text=col.upper())
            self.tree_prod.column(col, width=100)
        self.tree_prod.pack(fill="both", expand=True, padx=10, pady=10)

        self.right_panel_prod = ctk.CTkFrame(self.tab_prod)
        self.right_panel_prod.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.lbl_codigo = ctk.CTkLabel(self.right_panel_prod, text="ID: -")
        self.lbl_codigo.pack(anchor="w", padx=10, pady=2)
        
        # 2. Se fija el ancho (width) y el corte de texto (wraplength) estrictamente a 280 píxeles
        self.lbl_nombre = ctk.CTkLabel(
            self.right_panel_prod, 
            text="Nombre: -", 
            width=280, 
            wraplength=280, 
            justify="left",
            anchor="w"
        )
        self.lbl_nombre.pack(anchor="w", padx=10, pady=2)

        self.switch_var = ctk.StringVar(value="off")
        self.switch_estado = ctk.CTkSwitch(self.right_panel_prod, text="Visible en Telegram", variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch_estado.pack(anchor="w", padx=10, pady=20)

        self.lbl_save_status_prod = ctk.CTkLabel(self.right_panel_prod, text="", text_color="gray60", font=("Arial", 11))
        self.lbl_save_status_prod.pack(anchor="w", padx=10)

        self.btn_save_prod = ctk.CTkButton(self.right_panel_prod, text="Guardar Estado", fg_color="gray40", state="disabled")
        self.btn_save_prod.pack(fill="x", padx=10, pady=10)

        self.switch_var.trace_add("write", lambda *a: self._notify_field_changed())

# ================= TAB CATEGORÍAS =================
    def _build_categorias_tab(self):
        # 1. Se añade 'minsize' en las columnas
        self.tab_cat.grid_columnconfigure(0, weight=1, minsize=400)
        self.tab_cat.grid_columnconfigure(1, weight=2, minsize=400)
        self.tab_cat.grid_rowconfigure(0, weight=1)

        self.left_panel_cat = ctk.CTkFrame(self.tab_cat)
        self.left_panel_cat.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        search_row_cat = ctk.CTkFrame(self.left_panel_cat, fg_color="transparent")
        search_row_cat.pack(fill="x", padx=10, pady=10)

        self.search_entry_cat = ctk.CTkEntry(search_row_cat, placeholder_text="Buscar categoría...")
        self.search_entry_cat.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.btn_search_cat = ctk.CTkButton(search_row_cat, text="Buscar", width=80)
        self.btn_search_cat.pack(side="left")

        #Botón Limpiar Categorías
        self.btn_clear_cat = ctk.CTkButton(search_row_cat, text="Limpiar", width=80, fg_color="gray40")
        self.btn_clear_cat.pack(side="left", padx=(4, 0))

        columns_cat = ("id", "nombre", "sigla")
        self.tree_cat = ttk.Treeview(self.left_panel_cat, columns=columns_cat, show="headings")
        for col in columns_cat:
            self.tree_cat.heading(col, text=col.upper())
            self.tree_cat.column(col, width=80)
        self.tree_cat.pack(fill="both", expand=True, padx=10, pady=10)

        self.right_panel_cat = ctk.CTkFrame(self.tab_cat)
        self.right_panel_cat.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # 2. Se fija el ancho máximo para evitar que una categoría larga expanda el marco
        self.lbl_cat_sel = ctk.CTkLabel(
            self.right_panel_cat, 
            text="Categoría: -", 
            font=("Arial", 14, "bold"),
            width=380,
            wraplength=380,
            justify="left",
            anchor="w"
        )
        self.lbl_cat_sel.pack(anchor="w", padx=10, pady=5)
        
        ctk.CTkLabel(self.right_panel_cat, text="Descripción para Telegram:").pack(anchor="w", padx=10, pady=(5,0))
        self.txt_cat_desc = ctk.CTkTextbox(self.right_panel_cat, height=80)
        self.txt_cat_desc.pack(fill="x", padx=10, pady=5)
        
        self.lbl_save_status_cat = ctk.CTkLabel(self.right_panel_cat, text="", text_color="gray60", font=("Arial", 11))
        self.lbl_save_status_cat.pack(anchor="w", padx=10)

        self.btn_save_cat = ctk.CTkButton(self.right_panel_cat, text="Guardar Descripción", fg_color="gray40", state="disabled")
        self.btn_save_cat.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.right_panel_cat, text="Productos Asociados:").pack(anchor="w", padx=10, pady=(15,0))
        columns_prod = ("id", "nombre", "precio", "stock")
        self.tree_cat_prod = ttk.Treeview(self.right_panel_cat, columns=columns_prod, show="headings")
        for col in columns_prod:
            self.tree_cat_prod.heading(col, text=col.upper())
            self.tree_cat_prod.column(col, width=100)
        self.tree_cat_prod.pack(fill="both", expand=True, padx=10, pady=10)

        self.txt_cat_desc.bind("<KeyRelease>", lambda e: self._notify_field_changed())

    # ================= TAB BANCOS (CRUD) =================
    def _build_bancos_tab(self):
        self.tab_bank.grid_columnconfigure(0, weight=2)
        self.tab_bank.grid_columnconfigure(1, weight=1)
        self.tab_bank.grid_rowconfigure(0, weight=1)

        self.left_panel_bank = ctk.CTkFrame(self.tab_bank)
        self.left_panel_bank.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        columns = ("id", "banco", "cuenta", "titular", "cedula", "estado")
        self.tree_bank = ttk.Treeview(self.left_panel_bank, columns=columns, show="headings")
        for col in columns:
            self.tree_bank.heading(col, text=col.upper())
            self.tree_bank.column(col, width=100)
        self.tree_bank.pack(fill="both", expand=True, padx=10, pady=10)

        self.right_panel_bank = ctk.CTkFrame(self.tab_bank)
        self.right_panel_bank.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.lbl_bank_id = ctk.CTkLabel(self.right_panel_bank, text="ID: (Nuevo)", font=("Arial", 12, "bold"))
        self.lbl_bank_id.pack(anchor="w", padx=10, pady=10)

        self.entry_banco = ctk.CTkEntry(self.right_panel_bank, placeholder_text="Nombre del Banco")
        self.entry_banco.pack(fill="x", padx=10, pady=5)
        self.entry_cuenta = ctk.CTkEntry(self.right_panel_bank, placeholder_text="Número de Cuenta")
        self.entry_cuenta.pack(fill="x", padx=10, pady=5)
        self.entry_titular = ctk.CTkEntry(self.right_panel_bank, placeholder_text="Nombre del Titular")
        self.entry_titular.pack(fill="x", padx=10, pady=5)
        self.entry_cedula = ctk.CTkEntry(self.right_panel_bank, placeholder_text="Cédula o RUC")
        self.entry_cedula.pack(fill="x", padx=10, pady=5)

        self.switch_var_bank = ctk.StringVar(value="on")
        self.switch_estado_bank = ctk.CTkSwitch(self.right_panel_bank, text="Visible en Telegram", variable=self.switch_var_bank, onvalue="on", offvalue="off")
        self.switch_estado_bank.pack(anchor="w", padx=10, pady=15)

        self.btn_save_bank = ctk.CTkButton(self.right_panel_bank, text="Guardar / Actualizar", fg_color="green")
        self.btn_save_bank.pack(fill="x", padx=10, pady=5)
        self.btn_new_bank = ctk.CTkButton(self.right_panel_bank, text="Nuevo", fg_color="gray")
        self.btn_new_bank.pack(fill="x", padx=10, pady=5)
        self.btn_delete_bank = ctk.CTkButton(self.right_panel_bank, text="Eliminar", fg_color="red")
        self.btn_delete_bank.pack(fill="x", padx=10, pady=20)

    # --- POBREZA DE TABLAS ---
    def _populate_tree(self, tree, rows):
        for item in tree.get_children(): tree.delete(item)
        for row in rows: tree.insert("", "end", values=row)

    def populate_products(self, rows): self._populate_tree(self.tree_prod, rows)
    def populate_categories(self, rows): self._populate_tree(self.tree_cat, rows)
    def populate_category_products(self, rows): self._populate_tree(self.tree_cat_prod, rows)
    def populate_banks(self, rows): self._populate_tree(self.tree_bank, rows)

    # --- ESTADOS VISUALES (BOTONES) ---
    def set_save_button_state_prod(self, enabled: bool):
        color = THEMES[self._current_theme][1] if enabled else "gray40"
        self.btn_save_prod.configure(state="normal" if enabled else "disabled", fg_color=color)

    def set_save_button_state_cat(self, enabled: bool):
        color = THEMES[self._current_theme][1] if enabled else "gray40"
        self.btn_save_cat.configure(state="normal" if enabled else "disabled", fg_color=color)

    def set_save_status_prod(self, msg, color="gray60"): self.lbl_save_status_prod.configure(text=msg, text_color=color)
    def set_save_status_cat(self, msg, color="gray60"): self.lbl_save_status_cat.configure(text=msg, text_color=color)

    # --- VINCULACIÓN ---
    def _notify_field_changed(self):
        if self._on_field_changed_callback: self._on_field_changed_callback()

    def bind_field_changed(self, callback): self._on_field_changed_callback = callback
    def _on_tab_changed(self):
        if self._on_tab_change_callback: self._on_tab_change_callback(self.tabview.get())
    def bind_tab_change(self, callback): self._on_tab_change_callback = callback
    def bind_theme_change(self, callback): self._on_theme_change_callback = callback

    def bind_prod_actions(self, search_cb, select_cb, save_cb):
        self.btn_search.configure(command=search_cb)
        self.tree_prod.bind("<<TreeviewSelect>>", select_cb)
        self.btn_save_prod.configure(command=save_cb)

    def bind_cat_actions(self, search_cb, select_cb, save_cb):
        self.btn_search_cat.configure(command=search_cb)
        self.tree_cat.bind("<<TreeviewSelect>>", select_cb)
        self.btn_save_cat.configure(command=save_cb)

    def bind_bank_actions(self, select_cb, save_cb, new_cb, del_cb):
        self.tree_bank.bind("<<TreeviewSelect>>", select_cb)
        self.btn_save_bank.configure(command=save_cb)
        self.btn_new_bank.configure(command=new_cb)
        self.btn_delete_bank.configure(command=del_cb)

    # --- TEMAS ---
    def _apply_accent(self, theme_name):
        mode, primary, secondary, hover = THEMES.get(theme_name, THEMES["🌑  Oscuro"])
        ctk.set_appearance_mode(mode)
        
        style = ttk.Style()
        style.theme_use('clam')
        bg_color, fg_color = ("#2b2b2b", "#ffffff") if mode == "dark" else ("#ffffff", "#000000")
        
        style.configure("Treeview", background=bg_color, foreground=fg_color, fieldbackground=bg_color, rowheight=25)
        style.configure("Treeview.Heading", background=primary, foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[('active', hover)])
        style.map("Treeview", background=[('selected', primary)], foreground=[('selected', "#ffffff")])
        
        self.top_bar.configure(fg_color=primary)
        
        # 1. Configurar botones regulares (tienen hover_color)
        for w in [self.btn_search, self.btn_search_cat]:
            w.configure(fg_color=primary, hover_color=hover)
            
        # 2. Configurar el menú de opciones (tiene button_color y button_hover_color)
        self.theme_menu.configure(fg_color=primary, button_color=primary, button_hover_color=hover)
        
        # 3. Configurar texto de etiquetas
        self.lbl_title.configure(text_color=primary)

    def _on_theme_selected(self, theme_name):
        if theme_name == self._current_theme: return
        self._current_theme = theme_name
        self._apply_accent(theme_name)
        if self._on_theme_change_callback: self._on_theme_change_callback(theme_name)

    def bind_clear_search_prod(self, callback):
        self.btn_clear_prod.configure(command=callback)

    def bind_clear_search_cat(self, callback):
        self.btn_clear_cat.configure(command=callback)