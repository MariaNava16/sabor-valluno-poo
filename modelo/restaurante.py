from productos import Producto
from clientes import Cliente
from pedidos import Pedido, Local, Llevar, Delivery
from pagos import Pago


class Restaurante:
    def __init__(self):
        self.__menu = []
        self.__clientes = []
        self.__pedidos = []

    @property
    def menu(self):
        return list(self.__menu)

    @property
    def clientes(self):
        return list(self.__clientes)

    @property
    def pedidos(self):
        return list(self.__pedidos)

    def registrar_producto(self, producto):
        for p in self.__menu:
            if p.nombre.lower() == producto.nombre.lower():
                raise ValueError("El producto ya está registrado en el menú.")
        self.__menu.append(producto)

    def registrar_cliente(self, cliente):
        for c in self.__clientes:
            if c.telefono == cliente.telefono:
                raise ValueError("Ya existe un cliente con ese teléfono.")
        self.__clientes.append(cliente)

    def registrar_pedido(self, pedido):
        if isinstance(pedido, Local):
            for p in self.__pedidos:
                if (
                    isinstance(p, Local)
                    and p.n_mesa == pedido.n_mesa
                    and p.estado not in ["ENTREGADO", "CANCELADO"]
                ):
                    raise ValueError("Esa mesa ya tiene un pedido abierto.")
        pedido.registrar_pedido()
        self.__pedidos.append(pedido)

    def listar_menu_dia(self, dia):
        disponibles = []
        for p in self.__menu:
            if p.esta_disponible(dia):
                disponibles.append(p)
        return disponibles

    def registrar_pago_pedido(self, numero_pedido, pago):
        pedido = self.buscar_pedido(numero_pedido)
        pedido.asignar_pago(pago)

    def buscar_pedido(self, numero_pedido):
        for p in self.__pedidos:
            if p.numero_pedido == numero_pedido:
                return p
        raise ValueError("No existe ese número de pedido.")

    def reporte_ventas_dia(self, dia):
        dia_norm = dia.strip().lower()
        total_recaudado = 0.0
        cantidad_pedidos = 0
        por_tipo = {"Local": 0.0, "Llevar": 0.0, "Delivery": 0.0}
        conteo_productos = {}

        for p in self.__pedidos:
            if p.dia == dia_norm and p.estado != "CANCELADO" and p.pago is not None:
                cantidad_pedidos += 1
                total_pedido = p.calcular_total()
                total_recaudado += total_pedido

                tipo_nombre = type(p).__name__
                if tipo_nombre in por_tipo:
                    por_tipo[tipo_nombre] = round(por_tipo[tipo_nombre] + total_pedido, 2)

                for item in p.items:
                    nombre_prod = item.producto.nombre
                    if nombre_prod not in conteo_productos:
                        conteo_productos[nombre_prod] = 0
                    conteo_productos[nombre_prod] += item.producto.cantidad

        lista_ordenar = []
        for nombre_prod, cant in conteo_productos.items():
            lista_ordenar.append((cant, nombre_prod))
        lista_ordenar.sort(reverse=True)

        top_3 = []
        for cant, nombre_prod in lista_ordenar[:3]:
            top_3.append((nombre_prod, cant))

        return {
            "dia": dia_norm,
            "cantidad_pedidos": cantidad_pedidos,
            "total_recaudado": round(total_recaudado, 2),
            "por_tipo": por_tipo,
            "top_3": top_3,
        }