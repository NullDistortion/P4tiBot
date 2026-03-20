import customtkinter as ctk
from tkinter import ttk

class AppView(ctk.CTk):
    def __init__(self, app_settings):
        super().__init__()
        self.app_settings = app_settings

        self.title("Gestor P4tiBot - Administrador")
        self.geometry(self.app_settings.get("window_size", "1024x768"))
        ctk.set_appearance_mode(self.app_settings.get("theme", "dark"))

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab_prod = self.tabview.add("Catálogo de Productos")
        self.tab_cat = self.tabview.add("Categorías")
        self.tab_bank = self.tabview.add("Bancos y Métodos de Pago")

        self._build_productos_tab()
        self._build_categorias_tab()
        self._build_bancos_tab()

    # ================= TAB PRODUCTOS =================
    def _build_productos_tab(self):
        self.tab_prod.grid_columnconfigure(0, weight=3)
        self.tab_prod.grid_columnconfigure(1, weight=1)
        self.tab_prod.grid_rowconfigure(0, weight=1)

        self.left_panel_prod = ctk.CTkFrame(self.tab_prod)
        self.left_panel_prod.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.search_entry_prod = ctk.CTkEntry(self.left_panel_prod, placeholder_text="Buscar producto...")
        self.search_entry_prod.pack(fill="x", padx=10, pady=10)
        self.btn_search_prod = ctk.CTkButton(self.left_panel_prod, text="Buscar")
        self.btn_search_prod.pack(padx=10, pady=(0, 10))

        columns = ("id", "nombre", "cantidad", "precio", "estado", "categoria")
        self.tree_prod = ttk.Treeview(self.left_panel_prod, columns=columns, show="headings")
        for col in columns:
            self.tree_prod.heading(col, text=col.upper())
            self.tree_prod.column(col, width=100)
        self.tree_prod.pack(fill="both", expand=True, padx=10, pady=10)

        # Panel Derecho: Solo Visibilidad
        self.right_panel_prod = ctk.CTkFrame(self.tab_prod)
        self.right_panel_prod.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.lbl_codigo_prod = ctk.CTkLabel(self.right_panel_prod, text="ID: -")
        self.lbl_codigo_prod.pack(anchor="w", padx=10, pady=2)
        self.lbl_nombre_prod = ctk.CTkLabel(self.right_panel_prod, text="Nombre: -", wraplength=200)
        self.lbl_nombre_prod.pack(anchor="w", padx=10, pady=2)

        self.switch_var_prod = ctk.StringVar(value="off")
        self.switch_estado_prod = ctk.CTkSwitch(self.right_panel_prod, text="Visible en Telegram", variable=self.switch_var_prod, onvalue="on", offvalue="off")
        self.switch_estado_prod.pack(anchor="w", padx=10, pady=20)

        self.btn_save_prod = ctk.CTkButton(self.right_panel_prod, text="Guardar Visibilidad", fg_color="green")
        self.btn_save_prod.pack(fill="x", padx=10, pady=10)

    # ================= TAB CATEGORÍAS =================
    def _build_categorias_tab(self):
        self.tab_cat.grid_columnconfigure(0, weight=1)
        self.tab_cat.grid_columnconfigure(1, weight=2)
        self.tab_cat.grid_rowconfigure(0, weight=1)

        self.left_panel_cat = ctk.CTkFrame(self.tab_cat)
        self.left_panel_cat.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.search_entry_cat = ctk.CTkEntry(self.left_panel_cat, placeholder_text="Buscar categoría...")
        self.search_entry_cat.pack(fill="x", padx=10, pady=10)
        self.btn_search_cat = ctk.CTkButton(self.left_panel_cat, text="Buscar")
        self.btn_search_cat.pack(padx=10, pady=(0, 10))

        columns_cat = ("id", "nombre", "sigla")
        self.tree_cat = ttk.Treeview(self.left_panel_cat, columns=columns_cat, show="headings")
        for col in columns_cat:
            self.tree_cat.heading(col, text=col.upper())
            self.tree_cat.column(col, width=80)
        self.tree_cat.pack(fill="both", expand=True, padx=10, pady=10)

        # Panel Derecho: Editor de Descripción y Lista de Productos
        self.right_panel_cat = ctk.CTkFrame(self.tab_cat)
        self.right_panel_cat.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.lbl_cat_sel = ctk.CTkLabel(self.right_panel_cat, text="Categoría: -", font=("Arial", 14, "bold"))
        self.lbl_cat_sel.pack(anchor="w", padx=10, pady=5)
        
        ctk.CTkLabel(self.right_panel_cat, text="Descripción para Telegram:").pack(anchor="w", padx=10, pady=(5,0))
        self.txt_cat_desc = ctk.CTkTextbox(self.right_panel_cat, height=80)
        self.txt_cat_desc.pack(fill="x", padx=10, pady=5)
        
        self.btn_save_cat = ctk.CTkButton(self.right_panel_cat, text="Guardar Descripción", fg_color="green")
        self.btn_save_cat.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.right_panel_cat, text="Productos Asociados:").pack(anchor="w", padx=10, pady=(15,0))
        columns_prod = ("id", "nombre", "precio", "stock")
        self.tree_cat_prod = ttk.Treeview(self.right_panel_cat, columns=columns_prod, show="headings")
        for col in columns_prod:
            self.tree_cat_prod.heading(col, text=col.upper())
            self.tree_cat_prod.column(col, width=100)
        self.tree_cat_prod.pack(fill="both", expand=True, padx=10, pady=10)

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

        # Panel Derecho: Formulario CRUD
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

        self.btn_new_bank = ctk.CTkButton(self.right_panel_bank, text="Limpiar (Nuevo)", fg_color="gray")
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

    # --- VINCULACIÓN DE EVENTOS ---
    def bind_prod_actions(self, search_cb, select_cb, save_cb):
        self.btn_search_prod.configure(command=search_cb)
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