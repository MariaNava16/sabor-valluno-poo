from restaurante import Restaurante
from pedidos import Local, Llevar, Delivery
from pagos import Efectivo, Qr, Tarjeta


def mostrar_menu_principal():
    print("\n=== RESTAURANTE SABOR VALLUNO (VARIANTE A) ===")
    print("1. Ver menú de productos")
    print("2. Crear nuevo pedido")
    print("3. Agregar/quitar productos a pedido pendiente")
    print("4. Registrar pago de pedido")
    print("5. Cambiar estado de pedido")
    print("6. Ver listado de pedidos y recaudación")
    print("7. Cambiar disponibilidad de producto")
    print("0. Salir")


def ejecutar():
    restaurante = Restaurante()
    restaurante.cargar_datos_iniciales()

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                for prod in restaurante.listar_menu():
                    print(" ", prod)

            elif opcion == "2":
                nombre = input("Nombre del cliente: ")
                telefono = input("Teléfono: ")
                cliente = restaurante.registrar_cliente(nombre, telefono)
                tipo = input("Tipo (1=Local, 2=Llevar, 3=Delivery): ").strip()
                num = restaurante.generar_numero_pedido()

                if tipo == "1":
                    mesa = int(input("Número de mesa: "))
                    pedido = Local(num, cliente, mesa)
                elif tipo == "2":
                    pedido = Llevar(num, cliente)
                elif tipo == "3":
                    direccion = input("Dirección de entrega: ")
                    zona = input("Zona: ")
                    pedido = Delivery(num, cliente, direccion, zona)
                else:
                    print("Tipo inválido.")
                    continue

                restaurante.registrar_pedido(pedido)
                print(f"Pedido #{num} creado para {cliente.nombre}.")

            elif opcion == "3":
                num = int(input("Número de pedido: "))
                pedido = restaurante.buscar_pedido(num)
                accion = input("(A)gregar o (Q)uitar: ").strip().upper()
                cod = input("Código del producto: ").strip().upper()
                if accion == "A":
                    cant = int(input("Cantidad: "))
                    prod = restaurante.obtener_producto(cod)
                    pedido.agregar_item(prod, cant)
                    print(f"Agregado. Total actual: Bs {pedido.calcular_total():.2f}")
                elif accion == "Q":
                    pedido.quitar_item(cod)
                    print("Producto quitado del pedido.")

            elif opcion == "4":
                num = int(input("Número de pedido: "))
                pedido = restaurante.buscar_pedido(num)
                total = pedido.calcular_total()
                print(f"Total a pagar: Bs {total:.2f}")
                metodo = input("Método (1=Efectivo, 2=QR, 3=Tarjeta): ").strip()
                if metodo == "1":
                    recibido = float(input("Monto recibido: "))
                    pago = Efectivo(total, recibido)
                    pedido.registrar_pago(pago)
                    print(f"Pago confirmado. Cambio: Bs {pago.calcular_cambio():.2f}")
                elif metodo == "2":
                    ref = input("Código de transferencia QR: ")
                    pago = Qr(total, ref)
                    pedido.registrar_pago(pago)
                    print("Pago QR confirmado.")
                elif metodo == "3":
                    digitos = input("Últimos 4 dígitos de la tarjeta: ")
                    pago = Tarjeta(total, digitos)
                    pedido.registrar_pago(pago)
                    print("Pago con tarjeta confirmado.")

            elif opcion == "5":
                num = int(input("Número de pedido: "))
                pedido = restaurante.buscar_pedido(num)
                print("Estados:", ", ".join(pedido.ESTADOS_VALIDOS))
                estado = input("Nuevo estado: ").strip()
                pedido.cambiar_estado(estado)
                print(f"Estado actualizado a {pedido.estado}.")

            elif opcion == "6":
                for p in restaurante.listar_pedidos():
                    pagado = f"Pagado (Bs {p.pago.monto:.2f})" if p.pago else "Sin pago"
                    print(f"Pedido #{p.numero_pedido} | {p.cliente.nombre} | {p.__class__.__name__} | {p.estado} | {pagado}")
                print(f"Total recaudado: Bs {restaurante.total_recaudado():.2f}")

            elif opcion == "7":
                cod = input("Código del producto: ").strip().upper()
                prod = restaurante.obtener_producto(cod)
                prod.disponible = not prod.disponible
                print(f"{prod.nombre} ahora está: {'Disponible' if prod.disponible else 'Agotado'}")

            elif opcion == "0":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida.")

        except ValueError as e:
            print(f"[Error]: {e}")


if __name__ == "__main__":
    ejecutar()