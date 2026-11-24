from abc import ABC, abstractmethod
from clientes import Cliente
from productos import Producto
from pagos import Pago


class ItemPedido:
    def __init__(self, producto: Producto, cantidad: int = 1):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        if not producto.esta_disponible():
            raise ValueError(f"El producto '{producto.nombre}' no está disponible")
        self._producto = producto
        self._cantidad = int(cantidad)

    @property
    def producto(self) -> Producto:
        return self._producto

    @property
    def cantidad(self) -> int:
        return self._cantidad

    def subtotal(self) -> float:
        return round(self._producto.calcular_precio() * self._cantidad, 2)


class Pedido(ABC):
    ESTADOS_VALIDOS = ("Pendiente", "En preparación", "Listo", "Entregado", "Cancelado")
    COSTO_ENVASE = 2.0  # Bs 2 por envase

    def __init__(self, numero_pedido: int, cliente: Cliente):
        self._numero_pedido = numero_pedido
        self._cliente = cliente
        self._estado = "Pendiente"
        self._items: list[ItemPedido] = []
        self._pago: Pago | None = None

    @property
    def numero_pedido(self) -> int:
        return self._numero_pedido

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def items(self) -> tuple[ItemPedido, ...]:
        return tuple(self._items)

    @property
    def pago(self) -> Pago | None:
        return self._pago

    def _validar_modificable(self):
        if self._estado != "Pendiente" or self._pago is not None:
            raise ValueError("No se pueden modificar ítems de un pedido ya pagado o en curso")

    def agregar_item(self, producto: Producto, cantidad: int = 1):
        self._validar_modificable()
        for item in self._items:
            if item.producto.codigo == producto.codigo:
                item._cantidad += cantidad
                return
        self._items.append(ItemPedido(producto, cantidad))

    def quitar_item(self, codigo_producto: str):
        self._validar_modificable()
        for i, item in enumerate(self._items):
            if item.producto.codigo == codigo_producto:
                self._items.pop(i)
                return
        raise ValueError("El producto no se encuentra en el pedido")

    def cambiar_estado(self, nuevo_estado: str):
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: {nuevo_estado}")
        if self._estado == "Cancelado":
            raise ValueError("No se puede cambiar el estado de un pedido cancelado")
        if nuevo_estado == "Entregado" and self._pago is None:
            raise ValueError("No se puede entregar un pedido sin pago registrado")
        self._estado = nuevo_estado

    def calcular_subtotal(self) -> float:
        return round(sum(item.subtotal() for item in self._items), 2)

    def total_unidades(self) -> int:
        return sum(item.cantidad for item in self._items)

    @abstractmethod
    def calcular_cargo_extra(self) -> float:
        pass

    def calcular_total(self) -> float:
        if not self._items:
            raise ValueError("El pedido no tiene productos")
        return round(self.calcular_subtotal() + self.calcular_cargo_extra(), 2)

    def registrar_pago(self, pago: Pago):
        if self._pago is not None:
            raise ValueError("Este pedido ya tiene un pago registrado")
        if self._estado == "Cancelado":
            raise ValueError("No se puede pagar un pedido cancelado")
        total = self.calcular_total()
        if round(pago.monto, 2) != total:
            raise ValueError(f"El monto del pago (Bs {pago.monto:.2f}) debe ser igual al total (Bs {total:.2f})")
        pago.confirmar()
        self._pago = pago


class Local(Pedido):
    def __init__(self, numero_pedido: int, cliente: Cliente, nro_mesa: int):
        super().__init__(numero_pedido, cliente)
        if nro_mesa <= 0:
            raise ValueError("El número de mesa debe ser positivo")
        self._nro_mesa = nro_mesa

    @property
    def nro_mesa(self) -> int:
        return self._nro_mesa

    def calcular_cargo_extra(self) -> float:
        return 0.0


class Llevar(Pedido):
    def calcular_cargo_extra(self) -> float:
        # Bs 2 por cada envase
        return round(self.total_unidades() * self.COSTO_ENVASE, 2)


class Delivery(Pedido):
    MONTO_MINIMO = 40.0
    ENVIO_GRATIS_DESDE = 150.0
    COSTO_ENVIO_BASE = 15.0

    def __init__(self, numero_pedido: int, cliente: Cliente, direccion: str, zona: str = "Cercado"):
        super().__init__(numero_pedido, cliente)
        if not direccion or not direccion.strip():
            raise ValueError("La dirección es obligatoria para Delivery")
        self._direccion = direccion.strip()
        self._zona = zona.strip()

    @property
    def direccion(self) -> str:
        return self._direccion

    @property
    def zona(self) -> str:
        return self._zona

    def costo_envio(self) -> float:
        return 0.0 if self.calcular_subtotal() >= self.ENVIO_GRATIS_DESDE else self.COSTO_ENVIO_BASE

    def calcular_cargo_extra(self) -> float:
        subtotal = self.calcular_subtotal()
        if subtotal < self.MONTO_MINIMO:
            raise ValueError(f"El monto mínimo para Delivery es Bs {self.MONTO_MINIMO:.2f}")
        envases = self.total_unidades() * self.COSTO_ENVASE
        return round(envases + self.costo_envio(), 2)

    def registrar_pago(self, pago: Pago):
        if not pago.permite_delivery():
            raise ValueError("Delivery solo acepta pagos en Efectivo o QR")
        super().registrar_pago(pago)