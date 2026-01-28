import psycopg2
from src.config import Config


class DBConnection:
    _connection = None

    @classmethod
    def get_connection(cls):
        # Si no hay conexión o está cerrada, creamos una nueva
        if cls._connection is None or cls._connection.closed != 0:
            try:
                print("Creando nueva conexión a la base de datos...")
                cls._connection = psycopg2.connect(
                    host=Config.DB_HOST,
                    database=Config.DB_NAME,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    port=Config.DB_PORT
                )
                cls._connection.autocommit = False  # Manejo manual de transacciones
            except Exception as e:
                print(f"Error al conectar: {e}")
                raise e
        else:
            print("Reutilizando conexión existente (Singleton).")

        return cls._connection