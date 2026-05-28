import os

with open("archivo_demo.txt", "w") as f:
    f.write("archivo de prueba")

if os.path.exists("archivo_demo.txt"):
    os.remove("archivo_demo.txt")
else:
    print("The file does not exist")
