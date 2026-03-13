import sqlite3

class DatabaseModel:
    def __init__(self, db_path="p4tibot_local.db"):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    # --- Consultas para Tab 1: Productos ---
    def get_products(self, search_term=""):
        conn = self._get_connection()
        cursor = conn.cursor()
        query = """
            SELECT p.codigo, p.nombre, p.cantidad, p.pvp, p.estado, c.nombre 
            FROM producto p
            LEFT JOIN categoria c ON p.categoria_FK = c.codigo
            WHERE p.nombre LIKE ? OR p.codigo LIKE ?
        """
        cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def update_product_info(self, codigo, descripcion, estado):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE producto 
            SET descripcion = ?, estado = ? 
            WHERE codigo = ?
        """, (descripcion, estado, codigo))
        conn.commit()
        conn.close()

    # --- Consultas para Tab 2: Categorías ---
    def get_categories(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT codigo, nombre, sigla FROM categoria")
        rows = cursor.fetchall()
        conn.close()
        return rows

    # --- Consultas para Tab 3: Bancos (Vista Combinada JOIN) ---
    def get_banks_and_owners(self):
        # [Inferencia] Asumiendo que 'titular_FK' en banco conecta con 'codigo' en persona
        conn = self._get_connection()
        cursor = conn.cursor()
        query = """
            SELECT b.codigo, b.nombre, b.cuenta, p.nombre, p.cedula 
            FROM banco b
            JOIN persona p ON b.titular_FK = p.codigo
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows