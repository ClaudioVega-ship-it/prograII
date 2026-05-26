from abc import ABC, abstractmethod

class Encriptador(ABC):
    @abstractmethod
    def encriptar(self, datos: str) -> str:
        pass

    @abstractmethod
    def desencriptar(self, datos: str) -> str:
        pass

class EncriptadorAES(Encriptador):
    def encriptar(self, datos: str) -> str:
        return f"AES({datos})"

    def desencriptar(self, datos: str) -> str:
        return datos.replace("AES(", "").replace(")", "")

enc = EncriptadorAES()
resultado = enc.encriptar("Hola")
print(resultado)
print(enc.desencriptar(resultado))
