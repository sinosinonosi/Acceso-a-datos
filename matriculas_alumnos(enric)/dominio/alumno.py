# dominio/alumno.py

class Alumno:
    def __init__(self, nombre):
        self._nombre = nombre

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre

    def __str__(self):
        return f'Alumno: {self._nombre}'