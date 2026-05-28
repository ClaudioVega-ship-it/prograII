with open("archivo_demo.txt", "w") as f:
    f.write("Hola! Bienvenido a archivo_demo.txt\n")
    f.write("Este archivo es para fines de prueba.\n")
    f.write("Buena suerte!\n")

with open("archivo_demo.txt") as f:
    print(f.readline())
    print(f.readline())

with open("archivo_demo.txt") as f:
    for x in f:
        print(x)
