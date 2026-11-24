from productos import Plato, Bebida, Combo
from pagos import Efectivo, Qr, Tarjeta
from clientes import Cliente
from pedidos import Local, Llevar, Delivery
from restaurante import Restaurante


def cargar_datos_iniciales(rest):
    dias_todos = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    silpancho = Plato("Silpancho", 35.0, dias_todos)
    pique = Plato("Pique Macho", 55.0, dias_todos)
    chicharron = Plato("Chicharrón", 60.0, ["domingo"])
    sopa_mani = Plato("Sopa de Maní", 20.0, ["lunes", "miercoles", "viernes", "domingo"])

    mocochinchi_vaso = Bebida("Mocochinchi Vaso", 6.0, "vaso")
    mocochinchi_jarra = Bebida("Mocochinchi Jarra", 6.0, "jarra")
    gaseosa = Bebida("Gaseosa 2L", 14.0, "vaso")

    combo_valluno = Combo("Combo Valluno", [silpancho, mocochinchi_vaso])
    combo_familiar = Combo("Combo Familiar", [pique, combo_valluno, mocochinchi_jarra])

    productos_base = [
        silpancho, pique, chicharron, sopa_mani,
        mocochinchi_vaso, mocochinchi_jarra, gaseosa,
        combo_valluno, combo_familiar
    ]
    for item in productos_base:
        rest.registrar_producto(item)

    rest.registrar_cliente(Cliente("Juan Pérez", "71234567"))
    rest.registrar_cliente(Cliente("María Gómez", "68901234"))


def mostrar_menu_consola():
    print("\n" + "=" * 45)
    print("   RESTAURANTE SABOR VALLUNO (VARIANTE A)")
    print("=" * 45)
    print("1. Ver menú disponible por día")
    print("2. Registrar nuevo producto (Plato/Bebida/Combo)")
    print("3. Registrar nuevo cliente")
    print("4. Crear nuevo pedido (Local/Llevar/Delivery)")
    print("5. Agregar o quitar producto de un pedido")
    print("6. Cambiar estado de un pedido")
    print("7. Registrar pago de un pedido")
    print("8. Ver reporte de ventas del día")
    print("0. Salir")


def mostrar_detalle_pedido(pedido):
    print(f"\n--- Detalle del Pedido #{pedido.numero_pedido} ({type(pedido).__name__}) ---")
    print(f"Cliente: {pedido.cliente.nombre} | Día: {pedido.dia.capitalize()} | Estado: {pedido.estado}")
    for item in pedido.items:
        p = item.producto
        print(f"  - {p.cantidad} x {p.nombre}: Bs {item.subtotal_item():.2f}")
    print(f"Subtotal: Bs {pedido.calcular_subtotal():.2f}")
    print(f"Cargos:   Bs {pedido.calcular_cargos():.2f}")
    print(f"TOTAL:    Bs {pedido.calcular_total():.2f}")


def main():
    rest = Restaurante()
    cargar_datos_iniciales(rest)
    contador_pedidos = 1

    while True:
        mostrar_menu_consola()
        opcion = input("Elige una opción: ").strip()

        try:
            if opcion == "1":
                dia = input("Ingresa el día de la semana (ej. lunes, domingo): ").strip()
                disponibles = rest.listar_menu_dia(dia)
                print(f"\n--- Menú disponible el {dia.capitalize()} ---")
                for idx, p in enumerate(disponibles, 1):
                    print(f"{idx}. {p.nombre} ({type(p).__name__}) - Bs {p.calcular_precio():.2f}")

            elif opcion == "2":
                tipo = input("Tipo (plato / bebida / combo): ").strip().lower()
                nombre = input("Nombre: ").strip()
                if tipo == "plato":
                    precio = float(input("Precio (Bs): "))
                    dias = input("Días disponibles separados por coma (ej. lunes,domingo): ").split(",")
                    rest.registrar_producto(Plato(nombre, precio, dias))
                elif tipo == "bebida":
                    precio = float(input("Precio del vaso (Bs): "))
                    presentacion = input("Presentación (vaso / jarra): ").strip().lower()
                    rest.registrar_producto(Bebida(nombre, precio, presentacion))
                elif tipo == "combo":
                    print("Productos actuales en el menú:")
                    for i, p in enumerate(rest.menu, 1):
                        print(f"  {i}. {p.nombre} (Bs {p.calcular_precio():.2f})")
                    indices = input("Números de productos para el combo separados por coma (mínimo 2): ").split(",")
                    seleccionados = []
                    for i in indices:
                        seleccionados.append(rest.menu[int(i.strip()) - 1])
                    rest.registrar_producto(Combo(nombre, seleccionados))
                else:
                    print("Tipo no reconocido.")
                    continue
                print("Producto registrado con éxito.")

            elif opcion == "3":
                nombre = input("Nombre del cliente: ").strip()
                telefono = input("Teléfono (8 dígitos, inicia en 6 o 7): ").strip()
                rest.registrar_cliente(Cliente(nombre, telefono))
                print("Cliente registrado con éxito.")

            elif opcion == "4":
                print("\nClientes registrados:")
                for i, c in enumerate(rest.clientes, 1):
                    print(f"  {i}. {c.nombre} (Tel: {c.telefono})")
                idx_cliente = int(input("Selecciona el número de cliente: ")) - 1
                cliente = rest.clientes[idx_cliente]

                dia = input("Día del pedido (ej. lunes, domingo): ").strip().lower()
                modalidad = input("Tipo de pedido (local / llevar / delivery): ").strip().lower()

                if modalidad == "local":
                    mesa = int(input("Número de mesa (1 al 15): "))
                    pedido = Local(contador_pedidos, cliente, mesa, dia)
                elif modalidad == "llevar":
                    pedido = Llevar(contador_pedidos, cliente, dia)
                elif modalidad == "delivery":
                    zona = input("Zona (Cercado / Quillacollo / Sacaba / Vinto): ").strip()
                    pedido = Delivery(contador_pedidos, cliente, zona, dia)
                else:
                    print("Modalidad inválida.")
                    continue

                disponibles = rest.listar_menu_dia(dia)
                while True:
                    print(f"\nMenú disponible ({dia}):")
                    for i, p in enumerate(disponibles, 1):
                        print(f"  {i}. {p.nombre} - Bs {p.calcular_precio():.2f}")
                    sel = input("Número de producto a agregar (o 'fin' para terminar): ").strip().lower()
                    if sel == "fin":
                        break
                    prod = disponibles[int(sel) - 1]
                    cant = int(input("Cantidad (1 a 20): "))
                    pedido.agregar_producto(prod, cant)
                    print(f"Agregado: {cant} x {prod.nombre}")

                rest.registrar_pedido(pedido)
                mostrar_detalle_pedido(pedido)
                contador_pedidos += 1

            elif opcion == "5":
                num = int(input("Número de pedido: "))
                pedido = rest.buscar_pedido(num)
                mostrar_detalle_pedido(pedido)
                accion = input("¿Deseas (agregar) o (quitar) un producto?: ").strip().lower()
                if accion == "agregar":
                    disponibles = rest.listar_menu_dia(pedido.dia)
                    for i, p in enumerate(disponibles, 1):
                        print(f"  {i}. {p.nombre} - Bs {p.calcular_precio():.2f}")
                    sel = int(input("Número de producto: ")) - 1
                    cant = int(input("Cantidad (1 a 20): "))
                    pedido.agregar_producto(disponibles[sel], cant)
                    print("Producto agregado.")
                elif accion == "quitar":
                    nombre_prod = input("Nombre exacto del producto a quitar: ").strip()
                    pedido.quitar_producto(nombre_prod)
                    print("Producto quitado.")
                else:
                    print("Acción no válida.")
                mostrar_detalle_pedido(pedido)

            elif opcion == "6":
                num = int(input("Número de pedido: "))
                pedido = rest.buscar_pedido(num)
                print(f"Estado actual del pedido #{num}: {pedido.estado}")
                nuevo = input("Nuevo estado (EN_PREPARACION / LISTO / ENTREGADO / CANCELADO): ").strip()
                pedido.cambiar_estado(nuevo)
                print(f"Estado actualizado a {pedido.estado}.")

            elif opcion == "7":
                num = int(input("Número de pedido a pagar: "))
                pedido = rest.buscar_pedido(num)
                total = pedido.calcular_total()
                print(f"Total del pedido #{num}: Bs {total:.2f}")
                metodo = input("Método de pago (efectivo / qr / tarjeta): ").strip().lower()

                if metodo == "efectivo":
                    recibido = float(input("Monto recibido (Bs): "))
                    pago = Efectivo(total, recibido)
                    rest.registrar_pago_pedido(num, pago)
                    print(f"Pago registrado. Cambio a devolver: Bs {pago.calcular_cambio():.2f}")
                elif metodo == "qr":
                    codigo = input("Código de transacción (10 dígitos): ").strip()
                    pago = Qr(total, codigo)
                    rest.registrar_pago_pedido(num, pago)
                    print("Pago por QR registrado con éxito.")
                elif metodo == "tarjeta":
                    pago = Tarjeta(total)
                    rest.registrar_pago_pedido(num, pago)
                    print(
                        f"Pago con tarjeta registrado. Comisión (3%): Bs {pago.calcular_comision():.2f} | "
                        f"Total cobrado: Bs {pago.calcular_total_con_comision():.2f}"
                    )
                else:
                    print("Método de pago inválido.")

            elif opcion == "8":
                dia = input("Día para el reporte (ej. lunes, domingo): ").strip()
                rep = rest.reporte_ventas_dia(dia)
                print(f"\n--- Reporte de Ventas ({rep['dia'].capitalize()}) ---")
                print(f"Pedidos pagados: {rep['cantidad_pedidos']}")
                print(f"Total recaudado: Bs {rep['total_recaudado']:.2f}")
                print("Ventas por tipo de pedido:")
                for tipo_ped, monto in rep["por_tipo"].items():
                    print(f"  - {tipo_ped}: Bs {monto:.2f}")
                print("Top 3 productos más vendidos:")
                if len(rep["top_3"]) == 0:
                    print("  (Sin ventas registradas)")
                else:
                    for nombre_prod, cant in rep["top_3"]:
                        print(f"  - {nombre_prod}: {cant} unidades")

            elif opcion == "0":
                print("Saliendo del sistema Sabor Valluno...")
                break

            else:
                print("Opción no válida.")

        except Exception as e:
            print(f"\n[ERROR]: {e}")


if __name__ == "__main__":
    main()