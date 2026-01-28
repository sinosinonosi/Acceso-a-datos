import psycopg2
from src.conexion_db import DBConnection


class UsuarioDAO:

    @staticmethod
    def registrar_usuario(nombre, foto_bytes, cara_bytes):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
                INSERT INTO usuarios (nombre, foto_bytes, cara_bytes)
                VALUES (%s, %s, %s)
            """
            # psycopg2.Binary convierte los bytes crudos al formato BYTEA de Postgres
            cursor.execute(sql, (nombre, psycopg2.Binary(foto_bytes), psycopg2.Binary(cara_bytes)))
            conn.commit()
            print(f"Usuario {nombre} registrado exitosamente.")
        except Exception as e:
            conn.rollback()
            print(f"Error al registrar: {e}")
        finally:
            cursor.close()

    @staticmethod
    def obtener_todos():
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        try:
            sql = "SELECT id, nombre, cara_bytes FROM usuarios"
            cursor.execute(sql)
            usuarios = cursor.fetchall()
            return usuarios  # Retorna lista de tuplas
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []
        finally:
            cursor.close()