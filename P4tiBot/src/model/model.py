class PatibotModel:
    def __init__(self):
        # --- DATOS MOCK ---
        self.categorias_mock = [
            {"id": 1, "nombre": "Electrónica", "sigla": "ELE", "descripcion": "Artículos electrónicos generales."},
            {"id": 2, "nombre": "Periféricos", "sigla": "PER", "descripcion": "Teclados, ratones, etc."},
            {"id": 3, "nombre": "Cables", "sigla": "CAB", "descripcion": "Cables de todo tipo."},
            {"id": 4, "nombre": "Componentes", "sigla": "COM", "descripcion": "Hardware interno."}
        ]
        
        self.productos_mock = [
            {"id": 1, "nombre": "Teclado Mecánico RGB", "precio": 45.0, "stock": 10, "categoria": "Periféricos", "estado": "on"},
            {"id": 2, "nombre": "Ratón Inalámbrico", "precio": 25.0, "stock": 15, "categoria": "Periféricos", "estado": "off"},
            {"id": 3, "nombre": "Monitor 24 Pulgadas", "precio": 150.0, "stock": 5, "categoria": "Electrónica", "estado": "on"},
            {"id": 4, "nombre": "Cable HDMI 2m", "precio": 8.0, "stock": 50, "categoria": "Cables", "estado": "on"}
        ]

        self.bancos_mock = [
            {"id": 1, "banco": "Banco Pichincha", "cuenta": "1234567890", "titular": "Juan Perez", "cedula": "1101234567", "estado": "on"},
            {"id": 2, "banco": "Banco Guayaquil", "cuenta": "0987654321", "titular": "Maria Lopez", "cedula": "1107654321", "estado": "off"}
        ]

        self.usuarios_mock = []
        print("[SISTEMA] Modelo inicializado en modo MOCK (Datos en memoria).")

    # ================= EVENTOS PRODUCTOS =================
    def get_products(self, search_term=""):
        """FUTURO SQL: SELECT id, nombre, stock, precio, estado, categoria FROM productos WHERE nombre LIKE ?"""
        if not search_term: return self.productos_mock
        term_lower = search_term.lower()
        return [p for p in self.productos_mock if term_lower in p["nombre"].lower()]

    def get_product_by_id(self, prod_id):
        """FUTURO SQL: SELECT * FROM productos WHERE id = ?"""
        for p in self.productos_mock:
            if str(p["id"]) == str(prod_id): return p
        return None

    def update_product_visibility(self, prod_id, estado):
        """FUTURO SQL: UPDATE productos SET estado = ? WHERE id = ?"""
        for p in self.productos_mock:
            if str(p["id"]) == str(prod_id):
                if p["estado"] != estado:
                    p["estado"] = estado
                    print(f"[MOCK DB] Producto {prod_id}: estado actualizado a '{estado}'.")
                    return "updated"
                return "no_change"
        return False

    # ================= EVENTOS CATEGORÍAS =================
    def search_categories(self, search_term=""):
        """FUTURO SQL: SELECT id, nombre, sigla, descripcion FROM categorias WHERE nombre LIKE ?"""
        if not search_term: return self.categorias_mock
        term_lower = search_term.lower()
        return [c for c in self.categorias_mock if term_lower in c["nombre"].lower()]

    def get_category_by_id(self, cat_id):
        """FUTURO SQL: SELECT * FROM categorias WHERE id = ?"""
        for c in self.categorias_mock:
            if str(c["id"]) == str(cat_id): return c
        return None

    def get_products_by_category(self, category_name):
        """FUTURO SQL: SELECT id, nombre, precio, stock FROM productos WHERE categoria = ?"""
        return [p for p in self.productos_mock if p.get("categoria") == category_name]

    def update_category_desc(self, cat_id, descripcion):
        """FUTURO SQL: UPDATE categorias SET descripcion = ? WHERE id = ?"""
        for c in self.categorias_mock:
            if str(c["id"]) == str(cat_id):
                if c.get("descripcion", "") != descripcion:
                    c["descripcion"] = descripcion
                    print(f"[MOCK DB] Categoría {cat_id}: descripción actualizada.")
                    return "updated"
                return "no_change"
        return False

    # ================= EVENTOS BANCOS (CRUD) =================
    def get_banks(self):
        """FUTURO SQL: SELECT id, banco, cuenta, titular, cedula, estado FROM bancos"""
        return self.bancos_mock

    def get_bank_by_id(self, bank_id):
        """FUTURO SQL: SELECT * FROM bancos WHERE id = ?"""
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
        else: # Crear
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
        print(f"[MOCK DB] Banco {bank_id} borrado de los registros.")