# Aplicacion: orden fijo de provincias y comarcas de Panama
# Se usa tupla porque NO permite cambiar el orden en tiempo de ejecucion

provincias_y_comarcas = (
    "Bocas del Toro",
    "Chiriqui",
    "Cocle",
    "Colon",
    "Darien",
    "Herrera",
    "Los Santos",
    "Panama",
    "Panama Oeste",
    "Veraguas",
    "Comarca Guna Yala",
    "Comarca Embera-Wounaan",
    "Comarca Ngabe-Bugle"
)

print("Provincias y Comarcas de Panama (orden oficial fijo):")
print("-" * 50)
for i, nombre in enumerate(provincias_y_comarcas, start=1):
    print(f"{i:2}. {nombre}")

print("-" * 50)
print(f"Total: {len(provincias_y_comarcas)} provincias y comarcas")
print(f"Tipo de dato: {type(provincias_y_comarcas)}")
