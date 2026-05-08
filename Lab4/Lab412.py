PERMISOS_LECTURA = frozenset(["leer", "buscar", "exportar"])
# PERMISOS_LECTURA.add("borrar")  # Error: no se puede modificar
print(PERMISOS_LECTURA)
print("leer" in PERMISOS_LECTURA)
