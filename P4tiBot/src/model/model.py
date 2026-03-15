import sqlite3
import os

class PatibotModel:
    def __init__(self, db_name="patibot_datos.db"):
        self.db_name = db_name
        self.inicializar_base_datos()

    def _obtener_conexion(self):
        return sqlite3.connect(self.db_name)

    def inicializar_base_datos(self):
        """Crea las tablas necesarias si no existen."""
        conexion = self._obtener_conexion()
        cursor = conexion.cursor()
        
        # Tabla para el Bot de Telegram
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id TEXT NOT NULL UNIQUE,
            nombre_usuario TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Tabla para la interfaz gráfica y los productos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
        """)
        
        conexion.commit()
        conexion.close()

    # ==========================================
    # MÉTODOS PARA PRODUCTOS (Requeridos por controller)
    # ==========================================
    def get_products(self, search_term=""):
        """
        Retorna los productos que coincidan con la búsqueda.
        Si search_term está vacío, retorna todos.
        """
        conexion = self._obtener_conexion()
        cursor = conexion.cursor()
        
        query = "SELECT id, nombre, precio, stock FROM productos WHERE nombre LIKE ?"
        parametro = ('%' + search_term + '%',)
        
        cursor.execute(query, parametro)
        resultados = cursor.fetchall()
        conexion.close()
        
        return resultados

    def add_product(self, nombre, precio, stock):
        """Inserta un nuevo producto."""
        conexion = self._obtener_conexion()
        cursor = conexion.cursor()
        
        query = "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)"
        cursor.execute(query, (nombre, precio, stock))
        
        conexion.commit()
        conexion.close()

    # ==========================================
    # MÉTODOS PARA EL BOT (Usuarios)
    # ==========================================
    def registrar_usuario(self, telegram_id, nombre_usuario):
        conexion = self._obtener_conexion()
        cursor = conexion.cursor()
        
        query = "INSERT OR IGNORE INTO usuarios (telegram_id, nombre_usuario) VALUES (?, ?)"
        
        try:
            cursor.execute(query, (telegram_id, nombre_usuario))
            conexion.commit()
            exito = cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error BD: {e}")
            exito = False
        finally:
            conexion.close()
        
        return exito