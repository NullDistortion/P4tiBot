class PatibotModel:
    def __init__(self):
        # Datos MOCK listos para transicionar a SQL
        self.categorias_mock = ["Electrónica", "Periféricos", "Cables", "Componentes"]
        
        self.productos_mock = [
            {"id": 1, "nombre": "Teclado Mecánico RGB", "precio": 45.0, "stock": 10, "categoria": "Periféricos", "estado": "on", "descripcion": "Teclado RGB switch blue."},
            {"id": 2, "nombre": "Ratón Inalámbrico", "precio": 25.0, "stock": 15, "categoria": "Periféricos", "estado": "off", "descripcion": ""},
            {"id": 3, "nombre": "Monitor 24 Pulgadas", "precio": 150.0, "stock": 5, "categoria": "Electrónica", "estado": "on", "descripcion": "Monitor 144hz."},
        ]

        self.bancos_mock = [
            ("B001", "Banco Pichincha", "1234567890", "Juan Perez", "1101234567"),
            ("B002", "Banco Guayaquil", "0987654321", "Maria Lopez", "1107654321")
        ]

        self.usuarios_mock = []
        print("[SISTEMA] Modelo inicializado en modo MOCK (Datos en memoria).")

    def get_categories(self):
        """FUTURO SQL: SELECT nombre FROM categorias"""
        return self.categorias_mock

    def get_banks_and_owners(self):
        """FUTURO SQL: SELECT codigo_banco, banco, cuenta, titular, cedula FROM bancos"""
        return self.bancos_mock

    def get_products(self, search_term=""):
        """FUTURO SQL: SELECT * FROM productos WHERE nombre LIKE '%search_term%'"""
        if not search_term:
            return self.productos_mock
        
        resultados = []
        term_lower = search_term.lower()
        for p in self.productos_mock:
            if term_lower in p["nombre"].lower():
                resultados.append(p)
        return resultados

    def get_product_by_id(self, prod_id):
        """FUTURO SQL: SELECT * FROM productos WHERE id = ?"""
        for p in self.productos_mock:
            if str(p["id"]) == str(prod_id):
                return p
        return None

    def update_product_info(self, prod_id, descripcion, estado):
        """FUTURO SQL: UPDATE productos SET descripcion = ?, estado = ? WHERE id = ?"""
        for p in self.productos_mock:
            if str(p["id"]) == str(prod_id):
                p["descripcion"] = descripcion
                p["estado"] = estado
                print(f"[MOCK DB] Producto {prod_id} actualizado.")
                return True
        return False

    def registrar_usuario(self, telegram_id, nombre_usuario):
        """FUTURO SQL: INSERT OR IGNORE INTO usuarios (telegram_id, nombre_usuario) VALUES (?, ?)"""
        for u in self.usuarios_mock:
            if u["telegram_id"] == telegram_id:
                return False 
        self.usuarios_mock.append({"telegram_id": telegram_id, "nombre_usuario": nombre_usuario})
        return True
    
    def search_categories(self, search_term=""):
        """
        FUTURO SQL: 
        SELECT nombre FROM categorias WHERE nombre LIKE '%search_term%'
        """
        if not search_term:
            return self.categorias_mock
        
        term_lower = search_term.lower()
        return [c for c in self.categorias_mock if term_lower in c.lower()]

    def get_products_by_category(self, category_name):
        """
        FUTURO SQL: 
        SELECT * FROM productos WHERE categoria = ?
        """
        return [p for p in self.productos_mock if p.get("categoria") == category_name]