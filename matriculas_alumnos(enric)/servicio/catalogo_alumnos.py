# servicio/catalogo_alumnos.py
import os
from dominio.alumno import Alumno

# --- CÁLCULO DE LA RUTA SIMPLIFICADO ---
# Se calcula la ruta al archivo una sola vez, de forma clara.
_RUTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_NOMBRE_ARCHIVO = 'alumnos.txt'
_RUTA_ARCHIVO_COMPLETA = os.path.join(_RUTA_BASE, _NOMBRE_ARCHIVO)


class CatalogoAlumnos:
    ruta_archivo = _RUTA_ARCHIVO_COMPLETA

    @classmethod
    def matricular_alumno(cls, alumno):
        try:
            # --- SOLUCIÓN CLAVE ---
            # 1. Obtenemos la carpeta donde irá el archivo.
            carpeta = os.path.dirname(cls.ruta_archivo)
            # 2. Nos aseguramos de que esa carpeta exista JUSTO ANTES de escribir.
            os.makedirs(carpeta, exist_ok=True)
            
            # 3. Ahora abrimos el archivo para escribir con total seguridad.
            with open(cls.ruta_archivo, 'a+', encoding='utf8') as archivo:
                archivo.write(f'{alumno.nombre}\n')
            print(f'¡Alumno "{alumno.nombre}" matriculado correctamente!')
        
        except Exception as e:
            print(f'Ocurrió un error al matricular: {e}')

    @classmethod
    def listar_alumnos(cls):
        try:
            with open(cls.ruta_archivo, 'r', encoding='utf8') as archivo:
                print('--- Lista de Alumnos Matriculados ---')
                contenido = archivo.read()
                if not contenido:
                    print('No hay alumnos matriculados.')
                else:
                    print(contenido.strip())
                print('-------------------------------------')
        except FileNotFoundError:
            print('Aún no hay alumnos matriculados (el archivo no existe).')
        except Exception as e:
            print(f'Ocurrió un error al listar: {e}')

    @classmethod
    def eliminar_archivo(cls):
        try:
            os.remove(cls.ruta_archivo)
            print(f'Archivo "{cls.ruta_archivo}" eliminado con éxito.')
        except FileNotFoundError:
            print('El archivo no existe, no hay nada que eliminar.')
        except Exception as e:
            print(f'Ocurrió un error al eliminar el archivo: {e}')