# test_matriculas_alumnos.py

from dominio.alumno import Alumno
from servicio.catalogo_alumnos import CatalogoAlumnos

def mostrar_menu():
    print("\n*** Menú de Opciones ***")
    print("1) Matricular alumno")
    print("2) Listar alumnos")
    print("3) Eliminar archivo de alumnos")
    print("4) Salir")
    print("************************")

def main():
    while True:
        mostrar_menu()
        try:
            opcion = int(input('Selecciona una opción: '))

            if opcion == 1:
                nombre_alumno = input('Introduce el nombre del alumno a matricular: ')
                alumno = Alumno(nombre_alumno)
                CatalogoAlumnos.matricular_alumno(alumno)
            elif opcion == 2:
                CatalogoAlumnos.listar_alumnos()
            elif opcion == 3:
                CatalogoAlumnos.eliminar_archivo()
            elif opcion == 4:
                print('Saliendo del programa. ¡Hasta pronto!')
                break
            else:
                print('Opción no válida. Por favor, introduce un número del 1 al 4.')
        except ValueError:
            print('Error: Debes introducir un número.')
        except Exception as e:
            print(f'Ocurrió un error inesperado: {e}')

if __name__ == '__main__':
    main()