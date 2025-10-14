# dominio/alumno.py

class Alumno:
    def __init__(self, nombre):
        # El guion bajo (_) indica que es un atributo "protegido" o "privado".
        # Corresponde a '- nombre: str' en el UML.
        self._nombre = nombre

    @property
    def nombre(self):
        """ Getter para el atributo nombre. """
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        """ Setter para el atributo nombre. """
        self._nombre = nuevo_nombre

    def __str__(self):
        """
        Corresponde a '+ __str__()' en el UML.
        Devuelve una representación en string del objeto.
        """
        return f'Alumno: {self._nombre}'