with open("archivo_demo.txt", "w") as f:
    f.write("Hola! Bienvenido a archivo_demo.txt\n")
    f.write("Este archivo es para fines de prueba.\n")
    f.write("Buena suerte!\n")

with open("archivo_demo.txt", "a") as f:
    f.write("Ahora el archivo tiene mas contenido!")

with open("archivo_demo.txt") as f:
    print(f.read())

with open("archivo_demo.txt", "w") as f:
    f.write("Ups! He borrado el contenido!")

with open("archivo_demo.txt") as f:
    print(f.read())
