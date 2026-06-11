class Figura:
    def __init__(self, color):
        self.color = color
    def area(self):
        pass

class Cuadrado(Figura):
    def __init__(self, color, lado):
        super().__init__(color)
        self.lado = lado
    def area(self):  # sobreescritura
        return self.lado * self.lado

class Triangulo(Figura):
    def __init__(self, color, base, altura):
        super().__init__(color)
        self.base = base
        self.altura = altura
    def area(self):  # sobreescritura
        return (self.base * self.altura) / 2

c = Cuadrado("rojo", 5)
t = Triangulo("azul", 4, 3)
print(f"Area cuadrado: {c.area()}")
print(f"Area triangulo: {t.area()}")
