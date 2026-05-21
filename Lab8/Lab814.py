class Externa:
    def __init__(self):
        self.name = "EML"

    class Interna:
        def __init__(self, ext):
            self.ext = ext

        def display(self):
            print(f"El nombre de la clase exterior: {self.ext.name}")

ext = Externa()
int_ = ext.Interna(ext)
int_.display()
