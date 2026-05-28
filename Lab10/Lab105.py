class Factorial:
    def __init__(self, n):
        self.n = n

    def calcular(self):
        resultado = 1
        for i in range(1, self.n + 1):
            resultado = resultado * i
        return resultado

n = int(input("Ingrese un numero: "))
f = Factorial(n)
print("El factorial de", n, "es:", f.calcular())
