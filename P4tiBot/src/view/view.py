import customtkinter as ctk
from tkinter import ttk

class AppView(ctk.CTk):
    def __init__(self, app_settings):
        super().__init__()
       # Asigna el diccionario a una variable de clase para poder usarlo
        self.app_settings = app_settings

        self.title("Gestor P4tiBot - Administrador")
        
        # [Especulación] Ahora puedes aplicar los valores guardados en el JSON
        resolucion = self.app_settings.get("window_size", "1024x768")
        self.geometry(resolucion)
        
        tema = self.app_settings.get("theme", "dark")
        ctk.set_appearance_mode(tema)

        # Configurar TabView
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

    def _build_productos_tab(self):
        self.tab_prod.grid_columnconfigure(0, weight=3)
        self.tab_prod.grid_columnconfigure(1, weight=1)
        self.tab_prod.grid_rowconfigure(0, weight=1)

        # Panel Izquierdo (Tabla)
        self.left_panel = ctk.CTkFrame(self.tab_prod)
        self.left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.search_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Buscar producto...")
        self.search_entry.pack(fill="x", padx=10, pady=10)
        
        self.btn_search = ctk.CTkButton(self.left_panel, text="Buscar")
        self.btn_search.pack(padx=10, pady=(0, 10))

        columns = ("codigo", "nombre", "cantidad", "pvp", "estado", "categoria")
        self.tree_prod = ttk.Treeview(self.left_panel, columns=columns, show="headings")
        for col in columns:
            self.tree_prod.heading(col, text=col.upper())
            self.tree_prod.column(col, width=100)
        self.tree_prod.pack(fill="both", expand=True, padx=10, pady=10)

        # Panel Derecho (Edición)
        self.right_panel = ctk.CTkFrame(self.tab_prod)
        self.right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.lbl_codigo = ctk.CTkLabel(self.right_panel, text="Código: -")
        self.lbl_codigo.pack(anchor="w", padx=10, pady=2)
        self.lbl_nombre = ctk.CTkLabel(self.right_panel, text="Nombre: -")
        self.lbl_nombre.pack(anchor="w", padx=10, pady=2)

        ctk.CTkLabel(self.right_panel, text="Descripción para Telegram:").pack(anchor="w", padx=10, pady=(15,0))
        self.txt_descripcion = ctk.CTkTextbox(self.right_panel, height=100)
        self.txt_descripcion.pack(fill="x", padx=10, pady=5)

        self.switch_var = ctk.StringVar(value="off")
        self.switch_estado = ctk.CTkSwitch(self.right_panel, text="Visible en Telegram", variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch_estado.pack(anchor="w", padx=10, pady=15)

        self.btn_save = ctk.CTkButton(self.right_panel, text="Guardar Cambios", fg_color="green")
        self.btn_save.pack(fill="x", padx=10, pady=20)

    def _build_categorias_tab(self):
        # [Inferencia] Estructura básica solicitada para Tab 2
        columns = ("codigo", "nombre", "sigla")
        self.tree_cat = ttk.Treeview(self.tab_cat, columns=columns, show="headings")
        for col in columns:
            self.tree_cat.heading(col, text=col.upper())
        self.tree_cat.pack(fill="both", expand=True, padx=10, pady=10)

    def _build_bancos_tab(self):
        # [Inferencia] Estructura básica solicitada para Tab 3 con datos del JOIN
        columns = ("codigo_banco", "banco", "cuenta", "titular", "cedula")
        self.tree_bank = ttk.Treeview(self.tab_bank, columns=columns, show="headings")
        for col in columns:
            self.tree_bank.heading(col, text=col.upper())
        self.tree_bank.pack(fill="both", expand=True, padx=10, pady=10)

    # --- Métodos de llenado de datos ---
    def populate_products(self, rows):
        for item in self.tree_prod.get_children():
            self.tree_prod.delete(item)
        for row in rows:
            self.tree_prod.insert("", "end", values=row)

    def populate_categories(self, rows):
        for item in self.tree_cat.get_children():
            self.tree_cat.delete(item)
        for row in rows:
            self.tree_cat.insert("", "end", values=row)

    def populate_banks(self, rows):
        for item in self.tree_bank.get_children():
            self.tree_bank.delete(item)
        for row in rows:
            self.tree_bank.insert("", "end", values=row)

    # --- Vinculación de Eventos (Se configuran desde el controlador) ---
    def bind_search_action(self, callback):
        self.btn_search.configure(command=callback)

    def bind_save_action(self, callback):
        self.btn_save.configure(command=callback)

    def bind_tree_select(self, callback):
        self.tree_prod.bind("<<TreeviewSelect>>", callback)