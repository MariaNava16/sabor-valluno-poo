from productos import Producto, Plato, Bebida, Combo
from clientes import Cliente
from pedidos import Pedido


class Restaurante:
    def __init__(self, nombre: str = "Sabor Valluno"):
        self._nombre = nombre
        self._menu: dict[str, Producto] = {}
        self._clientes: dict[str, Cliente] = {}
        self._pedidos: list[Pedido] = []
        self._contador_pedidos = 1

    @property
    def nombre(self) -> str:
        return self._nombre

    def registrar_producto(self, producto: Producto):
        if producto.codigo in self._menu:
            raise ValueError(f"Ya existe un producto con el código {producto.codigo}")
        self._menu[producto.codigo] = producto

    def obtener_producto(self, codigo: str) -> Producto:
        if codigo not in self._menu:
            raise ValueError(f"Producto '{codigo}' no encontrado")
        return self._menu[codigo]

    def listar_menu(self) -> list[Producto]:
        return list(self._menu.values())

    def registrar_cliente(self, nombre: str, telefono: str) -> Cliente:
        if telefono in self._clientes:
            return self._clientes[telefono]
        cliente = Cliente(nombre, telefono)
        self._clientes[telefono] = cliente
        return cliente

    def generar_numero_pedido(self) -> int:
        num = self._contador_pedidos
        self._contador_pedidos += 1
        return num

    def registrar_pedido(self, pedido: Pedido):
        self._pedidos.append(pedido)

    def buscar_pedido(self, numero: int) -> Pedido:
        for p in self._pedidos:
            if p.numero_pedido == numero:
                return p
        raise ValueError(f"Pedido #{numero} no encontrado")

    def listar_pedidos(self) -> list[Pedido]:
        return list(self._pedidos)

    def total_recaudado(self) -> float:
        return round(sum(p.pago.monto for p in self._pedidos if p.pago is not None), 2)

    def cargar_datos_iniciales(self):
        p1 = Plato("P1", "Pique Macho", 65.0, "Carne, salchicha, papa y huevo")
        p2 = Plato("P2", "Silpancho Cochabambino", 45.0, "Carne apanada con arroz, papa y huevo")
        p3 = Plato("P3", "Chicharrón de Cerdo", 70.0, "Con mote y chuño")
        b1 = Bebida("B1", "Jarra de Chicha Morada", 20.0, "Fría")
        b2 = Bebida("B2", "Refresco de Mocochinchi", 10.0, "Fría")
        c1 = Combo("C1", "Combo Valluno", [p2, b2])  # (45 + 10) * 0.90 = 49.50

        for item in (p1, p2, p3, b1, b2, c1):
            self.registrar_producto(item)