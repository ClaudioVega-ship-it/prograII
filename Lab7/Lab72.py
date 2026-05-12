n = int(input("Ingrese un numero par: "))

if n % 2 != 0:
    print("El numero no es par")
else:
    matriz = []
    for i in range(n):
        fila = []
        for j in range(n):
            if i == j:
                fila.append(1)
            else:
                fila.append(0)
        matriz.append(fila)

    print("Matriz identidad de", n, "x", n)
    for fila in matriz:
        print(fila)
