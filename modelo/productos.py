from abc import ABC, abstractmethod

DIAS_VALIDOS = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]


class Producto(ABC):
    def __init__(self, nombre, precio, cantidad=1):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = nombre.strip()

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, precio):
        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
        self._precio = round(float(precio), 2)

    @property
    def cantidad(self):
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, cantidad):
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("La cantidad no puede ser menor a cero.")
        self.__cantidad = cantidad

    @abstractmethod
    def calcular_precio(self):
        pass

    @abstractmethod
    def esta_disponible(self, dia):
        pass

    @abstractmethod
    def contar_platos(self):
        pass


class Plato(Producto):
    def __init__(self, nombre, precio, dias_disponibles, cantidad=1):
        super().__init__(nombre, precio, cantidad)
        self.dias_disponibles = dias_disponibles

    @property
    def dias_disponibles(self):
        return self.__dias_disponibles

    @dias_disponibles.setter
    def dias_disponibles(self, dias_disponibles):
        if not dias_disponibles:
            raise ValueError("Debe indicar al menos un día disponible.")
        dias_norm = []
        for d in dias_disponibles:
            d_limpio = d.strip().lower()
            if d_limpio not in DIAS_VALIDOS:
                raise ValueError("Día inválido: " + d)
            dias_norm.append(d_limpio)

        if "chicharron" in self._nombre.lower() or "chicharrón" in self._nombre.lower():
            if dias_norm != ["domingo"]:
                raise ValueError("El chicharrón solo se vende los domingos.")
        self.__dias_disponibles = dias_norm

    def calcular_precio(self):
        return round(self._precio, 2)

    def esta_disponible(self, dia):
        return dia.strip().lower() in self.__dias_disponibles

    def contar_platos(self):
        return 1


class Bebida(Producto):
    def __init__(self, nombre, precio, tipo="vaso", cantidad=1):
        super().__init__(nombre, precio, cantidad)
        self.tipo = tipo

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo):
        tipo_norm = tipo.strip().lower()
        if tipo_norm not in ["vaso", "jarra"]:
            raise ValueError("El tipo de bebida debe ser 'vaso' o 'jarra'.")
        self.__tipo = tipo_norm

    def calcular_precio(self):
        if self.__tipo == "jarra":
            return round(self._precio * 3, 2)
        return round(self._precio, 2)

    def esta_disponible(self, dia):
        return dia.strip().lower() in DIAS_VALIDOS

    def contar_platos(self):
        return 0


class Combo(Producto):
    def __init__(self, nombre, lista_productos=None, cantidad=1):
        super().__init__(nombre, 0.01, cantidad)
        self.__lista_productos = []
        if lista_productos is not None:
            for p in lista_productos:
                self.agregar_producto(p)

    @property
    def lista_productos(self):
        return list(self.__lista_productos)

    def agregar_producto(self, producto):
        if producto is self:
            raise ValueError("Un combo no puede contenerse a sí mismo.")
        if isinstance(producto, Combo) and self._contiene_a(producto):
            raise ValueError("Ciclo detectado: este combo ya forma parte del subcombo.")
        self.__lista_productos.append(producto)
        if len(self.__lista_productos) >= 2:
            self._precio = self.calcular_precio()

    def _contiene_a(self, otro_combo):
        for item in otro_combo.lista_productos:
            if item is self:
                return True
            if isinstance(item, Combo) and self._contiene_a(item):
                return True
        return False

    def calcular_descuento(self):
        suma = 0
        for p in self.__lista_productos:
            suma += p.calcular_precio()
        return round(suma * 0.10, 2)

    def calcular_precio(self):
        if len(self.__lista_productos) < 2:
            raise ValueError("Un combo debe contener 2 o más productos.")
        suma = 0
        for p in self.__lista_productos:
            suma += p.calcular_precio()
        return round(suma - self.calcular_descuento(), 2)

    def esta_disponible(self, dia):
        if len(self.__lista_productos) < 2:
            return False
        for p in self.__lista_productos:
            if not p.esta_disponible(dia):
                return False
        return True

    def contar_platos(self):
        total = 0
        for p in self.__lista_productos:
            total += p.contar_platos()
        return total