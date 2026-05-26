from typing import final

class Padre:
    @final
    def metodo_sagrado(self):
        print("No me cambies.")

class Hijo(Padre):
    def metodo_sagrado(self):
        print("Intentando cambiarlo.")

p = Padre()
p.metodo_sagrado()

h = Hijo()
h.metodo_sagrado()
print("Python lo ejecuta igual, pero un linter como MyPy marcaria esto como error.")
