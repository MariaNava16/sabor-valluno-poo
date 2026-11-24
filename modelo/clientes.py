class Cliente:
    def __init__(self, nombre, telefono):
        self.nombre = nombre
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")
        self.__nombre = nombre.strip()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, telefono):
        tel = str(telefono).strip()
        if not (tel.isdigit() and len(tel) == 8 and tel[0] in ["6", "7"]):
            raise ValueError("El teléfono debe tener 8 dígitos y empezar en 6 o 7.")
        self.__telefono = tel