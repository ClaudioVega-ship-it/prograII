def convertir(metros):
    if metros < 0:
        print("Error: el valor no puede ser negativo")
        return
    pulgadas = metros * 39.37
    print(f"{metros} metros = {pulgadas:.2f} pulgadas")

try:
    metros = float(input("Ingrese los metros: "))
    convertir(metros)
except ValueError:
    print("Error: debe ingresar un número")
