import psycopg2
from src.config import Config

class ConexionDB:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConexionDB, cls).__new__(cls)
            cls._instancia.conexion = None
        return cls._instancia

    def conectar(self):
        if self.conexion is None or self.conexion.closed:
            credenciales = Config.load()
            self.conexion = psycopg2.connect(**credenciales)
        return self.conexion

    def cerrar(self):
        if self.conexion is not None and not self.conexion.closed:
            self.conexion.close()