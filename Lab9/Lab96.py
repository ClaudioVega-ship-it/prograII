from typing import final

@final
class Base:
    pass

class Derivada(Base):
    pass

b = Base()
print("Clase Base creada correctamente")
d = Derivada()
print("Clase Derivada creada (Python no lo bloquea en ejecucion, solo un linter lo marcaria como error)")
