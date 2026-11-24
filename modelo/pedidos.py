from abc import ABC, abstractmethod
from productos import Producto
from pagos import Pago, Tarjeta
from clientes import Cliente

ESTADOS_VALIDOS = ["REGISTRADO", "EN_PREPARACION", "LISTO", "ENTREGADO", "CANCELADO"]
TRANSICIONES_VALIDAS = {
    "REGISTRADO": ["EN_PREPARACION", "CANCELADO"],
    "EN_PREPARACION": ["LISTO"],
    "LISTO": ["ENTREGADO"],
    "ENTREGADO": [],
    "CANCELADO": [],
}

TARIFAS_DELIVERY = {
    "cercado": 8.0,
    "quillacollo": 15.0,
    "sacaba": 15.0,
    "vinto": 20.0,
}


class PedidoProducto:
    def __init__(self, producto, pedido):
        self.producto = producto
        self.pedido = pedido

    @property
    def producto(self):
        return self.__producto

    @producto.setter
    def producto(self, producto):
        if not isinstance(producto, Producto):
            raise ValueError("Debe asociar un Producto válido.")
        self.__producto = producto

    @property
    def pedido(self):
        return self.__pedido

    @pedido.setter
    def pedido(self, pedido):
        if not isinstance(pedido, Pedido):
            raise ValueError("Debe asociar un Pedido válido.")
        self.__pedido = pedido

    def subtotal_item(self):
        return round(self.__producto.calcular_precio() * self.__producto.cantidad, 2)


class Pedido(ABC):
    def __init__(self, numero_pedido, cliente, dia="lunes"):
        if numero_pedido <= 0:
            raise ValueError("El número de pedido debe ser mayor a cero.")
        self._numero_pedido = numero_pedido
        self._estado = "REGISTRADO"
        self._pago = None
        self._items = []
        self.cliente = cliente
        self.dia = dia.strip().lower()

    @property
    def numero_pedido(self):
        return self._numero_pedido

    @property
    def estado(self):
        return self._estado

    @property
    def pago(self):
        return self._pago

    @property
    def items(self):
        return list(self._items)

    def agregar_producto(self, producto, cantidad=1):
        if self._estado != "REGISTRADO":
            raise ValueError("Solo se pueden agregar productos cuando el pedido está REGISTRADO.")
        if not isinstance(cantidad, int) or not (1 <= cantidad <= 20):
            raise ValueError("La cantidad de un producto en el pedido debe ir de 1 a 20.")
        if not producto.esta_disponible(self.dia):
            raise ValueError("El producto no está disponible ese día.")
        producto.cantidad = cantidad
        item = PedidoProducto(producto, self)
        self._items.append(item)

    def quitar_producto(self, nombre_producto):
        if self._estado != "REGISTRADO":
            raise ValueError("Solo se pueden quitar productos cuando el pedido está REGISTRADO.")
        nombre_norm = nombre_producto.strip().lower()
        for i in range(len(self._items)):
            if self._items[i].producto.nombre.lower() == nombre_norm:
                self._items.pop(i)
                return
        raise ValueError("No se encontró ese producto en el pedido.")

    def cambiar_estado(self, nuevo_estado):
        estado_norm = nuevo_estado.strip().upper()
        if estado_norm not in ESTADOS_VALIDOS:
            raise ValueError("Estado inválido.")
        if estado_norm not in TRANSICIONES_VALIDAS[self._estado]:
            raise ValueError("Transición de estado inválida.")
        self._estado = estado_norm

    def registrar_pedido(self):
        if len(self._items) == 0:
            raise ValueError("El pedido debe tener al menos un producto registrado.")
        self._estado = "REGISTRADO"

    def cancelar_pedido(self):
        self.cambiar_estado("CANCELADO")

    def asignar_pago(self, pago):
        if not pago.validar_pago():
            raise ValueError("El pago no es válido.")
        if round(pago.monto, 2) != self.calcular_total():
            raise ValueError("El monto del pago debe coincidir con el total del pedido.")
        self._pago = pago

    def calcular_subtotal(self):
        subtotal = 0
        for item in self._items:
            subtotal += item.subtotal_item()
        return round(subtotal, 2)

    @abstractmethod
    def calcular_cargos(self):
        pass

    def calcular_total(self):
        return round(self.calcular_subtotal() + self.calcular_cargos(), 2)


class Local(Pedido):
    def __init__(self, numero_pedido, cliente, n_mesa, dia="lunes"):
        super().__init__(numero_pedido, cliente, dia)
        self.n_mesa = n_mesa

    @property
    def n_mesa(self):
        return self.__n_mesa

    @n_mesa.setter
    def n_mesa(self, n_mesa):
        if not isinstance(n_mesa, int) or not (1 <= n_mesa <= 15):
            raise ValueError("El número de mesa debe estar entre 1 y 15.")
        self.__n_mesa = n_mesa

    def calcular_cargos(self):
        return 0.0


class Llevar(Pedido):
    def __init__(self, numero_pedido, cliente, dia="lunes"):
        super().__init__(numero_pedido, cliente, dia)
        self.__n_envases = 0

    @property
    def n_envases(self):
        total_platos = 0
        for item in self._items:
            total_platos += item.producto.contar_platos() * item.producto.cantidad
        self.__n_envases = total_platos
        return self.__n_envases

    def calcular_cargos(self):
        return round(self.n_envases * 2.0, 2)


class Delivery(Pedido):
    def __init__(self, numero_pedido, cliente, zona, dia="lunes"):
        super().__init__(numero_pedido, cliente, dia)
        self.zona = zona
        self.__cargo_minimo = 40.0

    @property
    def zona(self):
        return self.__zona

    @zona.setter
    def zona(self, zona):
        zona_norm = zona.strip().lower()
        if zona_norm not in TARIFAS_DELIVERY:
            raise ValueError("Zona inválida. Debe ser Cercado, Quillacollo, Sacaba o Vinto.")
        self.__zona = zona_norm

    @property
    def cargo_minimo(self):
        return self.__cargo_minimo

    def costo_envio(self):
        return TARIFAS_DELIVERY[self.__zona]

    def calcular_cargos(self):
        subtotal = self.calcular_subtotal()
        if subtotal < self.__cargo_minimo:
            raise ValueError("El pedido mínimo para delivery es Bs 40.00.")
        if self.__zona == "cercado" and subtotal >= 150.0:
            return 0.0
        return round(self.costo_envio(), 2)

    def asignar_pago(self, pago):
        if isinstance(pago, Tarjeta):
            raise ValueError("El delivery solo acepta pago en efectivo o QR.")
        super().asignar_pago(pago)