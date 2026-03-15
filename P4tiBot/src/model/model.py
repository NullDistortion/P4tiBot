import sqlite3
import os

class PatibotModel:
    def __init__(self, db_name="patibot_datos.db"):
        """
        Inicializa el modelo y establece el nombre del archivo de la base de datos.
        """
        # [Inferencia] Se asume que el archivo de la base de datos debe crearse en el mismo directorio desde donde se ejecuta el script de arranque.
        self.db_name = db_name
        self.inicializar_base_datos()

    def _obtener_conexion(self):
        """
        Retorna una conexión activa a SQLite.
        """
        return sqlite3.connect(self.db_name)

    def inicializar_base_datos(self):
        """
        Crea las tablas necesarias para el bot si no existen en el archivo físico.
        """
        conexion = self._obtener_conexion()
        cursor = conexion.cursor()
        
        query = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id TEXT NOT NULL UNIQUE,
            nombre_usuario TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(query)
        conexion.commit()
        conexion.close()

    def registrar_usuario(self, telegram_id, nombre_usuario):
        """
        Inserta un nuevo usuario en la base de datos.
        Ignora la inserción si el telegram_id ya existe debido a la restricción UNIQUE.
        """
        conexion = self._obtener_conexion()
        cursor = conexion.cursor()
        
        query = "INSERT OR IGNORE INTO usuarios (telegram_id, nombre_usuario) VALUES (?, ?)"
        datos = (telegram_id, nombre_usuario)
        
        try:
            cursor.execute(query, datos)
            conexion.commit()
            exito = cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error de base de datos: {e}")
            exito = False
        finally:
            conexion.close()
        
        return exito

    def obtener_usuarios(self):
        """
        Retorna la lista completa de usuarios registrados.
        """
        conexion = self._obtener_conexion()
        cursor = conexion.cursor()
        
        query = "SELECT id, telegram_id, nombre_usuario, fecha_registro FROM usuarios"
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        conexion.close()
        return resultados
    
    # Agrega este bloque dentro de la clase PatibotModel en model.py
    def get_products(self, search_term=""):
        conexion = self._obtener_conexion()
        cursor = conexion.cursor()
        
        # [Especulación] Se asume que tu base de datos tiene una tabla llamada 'productos' con una columna 'nombre'.
        query = "SELECT * FROM productos WHERE nombre LIKE ?"
        cursor.execute(query, ('%' + search_term + '%',))
        
        resultados = cursor.fetchall()
        conexion.close()
        
        return resultados