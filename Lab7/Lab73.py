import string

def contar_palabras_unicas(texto):
    for signo in string.punctuation:
        texto = texto.replace(signo, "")
    texto = texto.lower()
    palabras = texto.split()
    unicas = set(palabras)
    return len(unicas)

def palabra_mas_larga(texto):
    for signo in string.punctuation:
        texto = texto.replace(signo, "")
    palabras = texto.split()
    mas_larga = ""
    for p in palabras:
        if len(p) > len(mas_larga):
            mas_larga = p
    return mas_larga

def frecuencia_caracteres(texto):
    texto = texto.lower()
    conteo = {}
    total = 0
    for c in texto:
        if c != " " and c.isalpha():
            total += 1
            if c in conteo:
                conteo[c] += 1
            else:
                conteo[c] = 1

    print("Frecuencia de caracteres:")
    for letra in conteo:
        porcentaje = (conteo[letra] / total) * 100
        print(letra, "->", conteo[letra], "veces (", round(porcentaje, 2), "%)")

texto = input("Ingrese un texto: ")

print("Palabras unicas:", contar_palabras_unicas(texto))
print("Palabra mas larga:", palabra_mas_larga(texto))
frecuencia_caracteres(texto)
