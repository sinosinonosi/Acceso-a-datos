from src.conexion_db import DBConnection


def crear_tabla():
    print("Conectando a la base de datos...")
    conn = DBConnection.get_connection()
    cursor = conn.cursor()

    sql_crear_tabla = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        foto_bytes BYTEA NOT NULL,
        cara_bytes BYTEA NOT NULL
    );
    """

    try:
        print("Creando tabla 'usuarios'...")
        cursor.execute(sql_crear_tabla)
        conn.commit()
        print("¡Tabla creada con éxito! Ya puedes ejecutar la aplicación.")
    except Exception as e:
        conn.rollback()
        print(f"Error al crear la tabla: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    crear_tabla()