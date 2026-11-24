from productos import Producto, Plato, Bebida, Combo
from pagos import Pago, Efectivo, Qr, Tarjeta
from clientes import Cliente
from pedidos import Pedido, Local, Llevar, Delivery
from restaurante import Restaurante


def ejecutar_pruebas():
    # 1. Abstracción: no se pueden instanciar clases abstractas
    for clase_abs, args in [(Producto, ("X", "X", 10)), (Pedido, (1, Cliente("A", "1"))), (Pago, (10,))]:
        try:
            clase_abs(*args)
            assert False, f"{clase_abs.__name__} no debería instanciarse"
        except TypeError:
            pass

    # 2. Combo con 10% de descuento y combo anidado
    pique = Plato("P1", "Pique Macho", 60.0)
    chicha = Bebida("B1", "Chicha", 20.0)
    combo1 = Combo("C1", "Combo 1", [pique, chicha])  # (60+20)*0.90 = 72.0
    assert combo1.calcular_precio() == 72.0

    combo_mega = Combo("C2", "Combo Mega", [combo1, chicha])  # (72+20)*0.90 = 82.80
    assert combo_mega.calcular_precio() == 82.80

    # 3. Protección contra combo autorreferenciado
    try:
        combo1.agregar_producto(combo1)
        assert False
    except ValueError:
        pass

    # 4. Delivery: mínimo Bs 40
    cli = Cliente("Maria Nava", "70000001")
    deliv_bajo = Delivery(1, cli, "Av. Blanco Galindo km 5")
    deliv_bajo.agregar_item(chicha, 1)  # Bs 20 < 40
    try:
        deliv_bajo.calcular_total()
        assert False
    except ValueError:
        pass

    # 5. Delivery: envases (Bs 2 c/u) + envío (Bs 15 si subtotal < 150)
    deliv_normal = Delivery(2, cli, "Plaza 14 de Septiembre")
    deliv_normal.agregar_item(pique, 2)  # subtotal = 120, envases = 4, envío = 15 -> 139
    assert deliv_normal.calcular_total() == 139.0

    # 6. Delivery: envío gratis si subtotal >= 150
    deliv_gratis = Delivery(3, cli, "Av. América")
    deliv_gratis.agregar_item(pique, 2)  # 120
    deliv_gratis.agregar_item(Bebida("B2", "Refresco", 30.0), 1)  # 30 -> subtotal = 150
    # 3 unidades * 2 envase = 6, envío = 0 -> 156
    assert deliv_gratis.calcular_total() == 156.0

    # 7. Delivery: rechaza Tarjeta y acepta QR / Efectivo
    try:
        deliv_gratis.registrar_pago(Tarjeta(156.0, "1234"))
        assert False
    except ValueError:
        pass
    deliv_gratis.registrar_pago(Qr(156.0, "QR-9988"))
    assert deliv_gratis.pago is not None

    # 8. Encapsulación: no permite modificar ítems después de pagar
    try:
        deliv_gratis.agregar_item(chicha, 1)
        assert False
    except ValueError:
        pass

    # 9. Pedido Local sin envases y pago en Efectivo con cambio
    local = Local(4, cli, 5)
    local.agregar_item(pique, 1)  # 60.0
    assert local.calcular_total() == 60.0
    pago_ef = Efectivo(60.0, 100.0)
    local.registrar_pago(pago_ef)
    assert pago_ef.calcular_cambio() == 40.0

    # 10. Gestor Restaurante
    rest = Restaurante()
    rest.cargar_datos_iniciales()
    rest.registrar_pedido(local)
    assert rest.total_recaudado() == 60.0

    print("Todas las pruebas de Variante A pasaron correctamente (10/10).")


if __name__ == "__main__":
    ejecutar_pruebas()