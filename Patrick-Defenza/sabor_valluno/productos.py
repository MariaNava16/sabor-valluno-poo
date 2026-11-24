from abc import ABC, abstractmethod


class Producto(ABC):
    def __init__(self, codigo: str, nombre: str, precio_base: float):
        if not codigo or not nombre:
            raise ValueError("El código y el nombre son obligatorios")
        if precio_base < 0:
            raise ValueError("El precio base no puede ser negativo")
        self._codigo = codigo
        self._nombre = nombre
        self._precio_base = float(precio_base)
        self._disponible = True

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        self._disponible = bool(valor)

    @abstractmethod
    def calcular_precio(self) -> float:
        pass

    def esta_disponible(self) -> bool:
        return self._disponible

    def __str__(self) -> str:
        estado = "Disponible" if self.esta_disponible() else "Agotado"
        return f"[{self._codigo}] {self._nombre} - Bs {self.calcular_precio():.2f} ({estado})"


class Plato(Producto):
    def __init__(self, codigo: str, nombre: str, precio_base: float, descripcion: str = ""):
        super().__init__(codigo, nombre, precio_base)
        self._descripcion = descripcion

    @property
    def descripcion(self) -> str:
        return self._descripcion

    def calcular_precio(self) -> float:
        return round(self._precio_base, 2)


class Bebida(Producto):
    def __init__(self, codigo: str, nombre: str, precio_base: float, tipo: str = "Fría"):
        super().__init__(codigo, nombre, precio_base)
        self._tipo = tipo

    @property
    def tipo(self) -> str:
        return self._tipo

    def calcular_precio(self) -> float:
        return round(self._precio_base, 2)


class Combo(Producto):
    DESCUENTO_VARIANTE_A = 0.10  # 10% de descuento

    def __init__(self, codigo: str, nombre: str, productos: list[Producto] | None = None):
        super().__init__(codigo, nombre, 0.0)
        self._productos: list[Producto] = []
        if productos:
            for p in productos:
                self.agregar_producto(p)

    @property
    def productos(self) -> tuple[Producto, ...]:
        return tuple(self._productos)

    def agregar_producto(self, producto: Producto):
        if producto is self:
            raise ValueError("Un combo no puede contenerse a sí mismo")
        self._productos.append(producto)

    def esta_disponible(self) -> bool:
        if not self._disponible or not self._productos:
            return False
        return all(p.esta_disponible() for p in self._productos)

    def calcular_precio(self) -> float:
        subtotal = sum(p.calcular_precio() for p in self._productos)
        return round(subtotal * (1 - self.DESCUENTO_VARIANTE_A), 2)