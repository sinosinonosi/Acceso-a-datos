import csv
import os

ruta_actual = os.getcwd()
archivo_uf1 = os.path.join(ruta_actual, 'Notas_Alumnos_UF1.csv')
archivo_uf2 = os.path.join(ruta_actual, 'Notas_Alumnos_UF2.csv')
archivo_salida = os.path.join(ruta_actual, 'notas_alumnos.csv')

datos_alumnos = {}
DELIMITADOR = ';' 

try:
    with open(archivo_uf1, mode='r', encoding='latin-1') as file:
        reader_uf1 = csv.DictReader(file, delimiter=DELIMITADOR)
        
        for fila in reader_uf1:
            student_id = fila['Id']
            datos_alumnos[student_id] = {
                'Apellidos': fila['Apellidos'],
                'Nombre': fila['Nombre'],
                'UF1': fila['UF1'],
                'UF2': '' 
            }

    with open(archivo_uf2, mode='r', encoding='latin-1') as file:
        reader_uf2 = csv.DictReader(file, delimiter=DELIMITADOR)
        
        for fila in reader_uf2:
            student_id = fila['Id']
            if student_id in datos_alumnos:
                datos_alumnos[student_id]['UF2'] = fila['UF2']
            else:
                print(f"Advertencia: Alumno con Id {student_id} no encontrado en archivo UF1.")

    fieldnames = ['Id', 'Apellidos', 'Nombre', 'UF1', 'UF2']

    with open(archivo_salida, mode='w', encoding='latin-1', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=DELIMITADOR)
        
        writer.writeheader()
        
        for student_id, data in datos_alumnos.items():
            fila_para_escribir = {
                'Id': student_id,
                'Apellidos': data['Apellidos'],
                'Nombre': data['Nombre'],
                'UF1': data['UF1'],
                'UF2': data['UF2']
            }
            writer.writerow(fila_para_escribir)

    print(f"¡Éxito! Se ha generado el archivo: {archivo_salida}")

except FileNotFoundError:
    print("Error: No se pudo encontrar uno de los archivos de entrada.")
except PermissionError:
    print("Error: No tienes permisos para leer o escribir los archivos.")
except Exception as e:
    print(f"Ha ocurrido un error inesperado: {e}")