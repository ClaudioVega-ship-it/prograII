class Usuario:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    @classmethod
    def crear_anonimo(cls):
        return cls("Anonimo", 0)

invitado = Usuario.crear_anonimo()
print(invitado.nombre)
print(invitado.edad)
