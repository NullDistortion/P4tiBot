class PatibotModel:
    def __init__(self):
        # 1. Categorías (Ahora incluyen descripción y estado)
        self.categorias_mock = [
            {"id": 1, "nombre": "Electrónica", "sigla": "ELE", "descripcion": "Artículos electrónicos generales.", "estado": "on"},
            {"id": 2, "nombre": "Periféricos", "sigla": "PER", "descripcion": "Teclados, ratones, etc.", "estado": "on"},
            {"id": 3, "nombre": "Cables", "sigla": "CAB", "descripcion": "Cables de todo tipo.", "estado": "on"}
        ]
        
        # 2. Productos (Sin descripción, solo mantienen el estado de visibilidad)
        self.productos_mock = [
            {"id": 1, "nombre": "Teclado Mecánico RGB", "precio": 45.0, "stock": 10, "categoria": "Periféricos", "estado": "on"},
            {"id": 2, "nombre": "Ratón Inalámbrico", "precio": 25.0, "stock": 15, "categoria": "Periféricos", "estado": "off"},
            {"id": 3, "nombre": "Monitor 24 Pulgadas", "precio": 150.0, "stock": 5, "categoria": "Electrónica", "estado": "on"}
        ]

        # 3. Bancos (Beneficiarios para CRUD completo + estado)
        self.bancos_mock = [
            {"id": 1, "banco": "Banco Pichincha", "cuenta": "1234567890", "titular": "Juan Perez", "cedula": "1101234567", "estado": "on"}
        ]

        self.usuarios_mock = []
        print("[SISTEMA] Modelo inicializado en modo MOCK (Datos en memoria).")

    # --- PRODUCTOS ---
    def get_products(self, search_term=""):
        """FUTURO SQL: SELECT id, nombre, precio, stock, estado, categoria FROM productos WHERE nombre LIKE ?"""
        if not search_term: return self.productos_mock
        term_lower = search_term.lower()
        return [p for p in self.productos_mock if term_lower in p["nombre"].lower()]

    def get_product_by_id(self, prod_id):
        for p in self.productos_mock:
            if str(p["id"]) == str(prod_id): return p
        return None

    def update_product_visibility(self, prod_id, estado):
        """FUTURO SQL: UPDATE productos SET estado = ? WHERE id = ?"""
        for p in self.productos_mock:
            if str(p["id"]) == str(prod_id):
                p["estado"] = estado
                return True
        return False

    # --- CATEGORÍAS ---
    def search_categories(self, search_term=""):
        """FUTURO SQL: SELECT id, nombre, sigla, descripcion, estado FROM categorias WHERE nombre LIKE ?"""
        if not search_term: return self.categorias_mock
        term_lower = search_term.lower()
        return [c for c in self.categorias_mock if term_lower in c.lower()]

    def get_category_by_id(self, cat_id):
        for c in self.categorias_mock:
            if str(c["id"]) == str(cat_id): return c
        return None

    def get_products_by_category(self, category_name):
        """FUTURO SQL: SELECT id, nombre, precio, stock FROM productos WHERE categoria = ?"""
        return [p for p in self.productos_mock if p.get("categoria") == category_name]

    def update_category_info(self, cat_id, descripcion):
        """FUTURO SQL: UPDATE categorias SET descripcion = ? WHERE id = ?"""
        for c in self.categorias_mock:
            if str(c["id"]) == str(cat_id):
                c["descripcion"] = descripcion
                return True
        return False

    # --- BANCOS (CRUD COMPLETO) ---
    def get_banks(self):
        """FUTURO SQL: SELECT id, banco, cuenta, titular, cedula, estado FROM bancos"""
        return self.bancos_mock

    def get_bank_by_id(self, bank_id):
        for b in self.bancos_mock:
            if str(b["id"]) == str(bank_id): return b
        return None

    def save_bank(self, bank_id, banco, cuenta, titular, cedula, estado):
        """FUTURO SQL: INSERT INTO bancos (...) VALUES (...) O UPDATE bancos SET ... WHERE id = ?"""
        if bank_id: # Actualizar
            for b in self.bancos_mock:
                if str(b["id"]) == str(bank_id):
                    b.update({"banco": banco, "cuenta": cuenta, "titular": titular, "cedula": cedula, "estado": estado})
                    print(f"[MOCK DB] Banco {bank_id} actualizado.")
                    return True
        else: # Crear Nuevo
            nuevo_id = max([b["id"] for b in self.bancos_mock] + [0]) + 1
            self.bancos_mock.append({
                "id": nuevo_id, "banco": banco, "cuenta": cuenta, 
                "titular": titular, "cedula": cedula, "estado": estado
            })
            print(f"[MOCK DB] Nuevo Banco creado: {banco}")
            return True
        return False

    def delete_bank(self, bank_id):
        """FUTURO SQL: DELETE FROM bancos WHERE id = ?"""
        self.bancos_mock = [b for b in self.bancos_mock if str(b["id"]) != str(bank_id)]
        print(f"[MOCK DB] Banco {bank_id} eliminado.")

    # --- TELEGRAM ---
    def registrar_usuario(self, telegram_id, nombre_usuario):
        for u in self.usuarios_mock:
            if u["telegram_id"] == telegram_id: return False 
        self.usuarios_mock.append({"telegram_id": telegram_id, "nombre_usuario": nombre_usuario})
        return True