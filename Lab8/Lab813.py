class Externa:
    def __init__(self):
        self.name = "Externa"

    class Interna:
        def __init__(self):
            self.name = "Interna"

        def display(self):
            print("Hola desde la clase interna")

ext = Externa()
int_ = ext.Interna()
int_.display()
