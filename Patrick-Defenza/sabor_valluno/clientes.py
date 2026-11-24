class Cliente:
    def __init__(self, nombre: str, telefono: str):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del cliente es obligatorio")
        if not telefono or not telefono.strip():
            raise ValueError("El teléfono del cliente es obligatorio")
        self._nombre = nombre.strip()
        self._telefono = telefono.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def telefono(self) -> str:
        return self._telefono

    def __str__(self) -> str:
        return f"{self._nombre} (Tel: {self._telefono})"