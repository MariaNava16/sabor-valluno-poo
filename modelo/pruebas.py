from productos import Plato, Bebida, Combo
from clientes import Cliente
from pedidos import Local, Llevar, Delivery
from pagos import Efectivo, Qr, Tarjeta
from restaurante import Restaurante


def ejecutar_pruebas():
    dias_todos = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    silpancho = Plato("Silpancho", 35.0, dias_todos)
    pique = Plato("Pique Macho", 55.0, dias_todos)
    chicharron = Plato("Chicharrón", 60.0, ["domingo"])
    mocochinchi_vaso = Bebida("Mocochinchi Vaso", 6.0, "vaso")
    mocochinchi_jarra = Bebida("Mocochinchi Jarra", 6.0, "jarra")

    # Prueba 1: Bebida en jarra cuesta 3 veces el vaso
    assert mocochinchi_jarra.calcular_precio() == 18.0

    # Prueba 2: Caso de referencia Variante A (Combo con 10% descuento + Delivery Quillacollo Bs 15)
    combo_ref = Combo("Combo Valluno", [silpancho, mocochinchi_vaso])
    assert combo_ref.calcular_precio() == 36.90

    cliente1 = Cliente("Carlos Mamani", "71234567")
    pedido_deliv = Delivery(1, cliente1, "Quillacollo", "lunes")
    pedido_deliv.agregar_producto(combo_ref, 2)
    assert pedido_deliv.calcular_total() == 88.80

    # Prueba 3: Combo dentro de otro combo (recursividad y conteo de platos)
    combo_grande = Combo("Combo Familiar", [pique, combo_ref, mocochinchi_jarra])
    # (55 + 36.90 + 18) = 109.90 -> 10% desc = 10.99 -> 98.91
    assert combo_grande.calcular_precio() == 98.91
    assert combo_grande.contar_platos() == 2

    # Prueba 4: Pedido Para Llevar cobra Bs 2 por cada plato (incluso dentro de combos)
    pedido_llevar = Llevar(2, cliente1, "lunes")
    pedido_llevar.agregar_producto(combo_grande, 1)
    assert pedido_llevar.n_envases == 2
    assert pedido_llevar.calcular_cargos() == 4.0

    # Prueba 5: Envío gratis en Cercado desde Bs 150 (Variante A)
    pedido_cercado = Delivery(3, cliente1, "Cercado", "lunes")
    pedido_cercado.agregar_producto(pique, 3)  # 55 * 3 = 165 >= 150
    assert pedido_cercado.calcular_cargos() == 0.0
    assert pedido_cercado.calcular_total() == 165.0

    # Prueba 6: Pedido mínimo de delivery Bs 40 en Variante A lanza error si es menor
    pedido_minimo = Delivery(4, cliente1, "Cercado", "lunes")
    pedido_minimo.agregar_producto(silpancho, 1)  # 35 < 40
    error_minimo = False
    try:
        pedido_minimo.calcular_cargos()
    except ValueError:
        error_minimo = True
    assert error_minimo is True

    # Prueba 7: Chicharrón solo se vende los domingos (Variante A)
    assert chicharron.esta_disponible("domingo") is True
    assert chicharron.esta_disponible("lunes") is False

    # Prueba 8: Pagos (Efectivo calcula cambio, Delivery rechaza Tarjeta)
    pago_ef = Efectivo(88.80, 100.0)
    assert pago_ef.calcular_cambio() == 11.20

    error_tarjeta = False
    try:
        pedido_deliv.asignar_pago(Tarjeta(88.80))
    except ValueError:
        error_tarjeta = True
    assert error_tarjeta is True

    # Prueba 9: Mesa en Local no permite dos pedidos abiertos al mismo tiempo
    rest = Restaurante()
    p_local1 = Local(5, cliente1, 4, "lunes")
    p_local1.agregar_producto(silpancho, 1)
    rest.registrar_pedido(p_local1)

    p_local2 = Local(6, cliente1, 4, "lunes")
    p_local2.agregar_producto(pique, 1)
    error_mesa = False
    try:
        rest.registrar_pedido(p_local2)
    except ValueError:
        error_mesa = True
    assert error_mesa is True

    print("Todas las pruebas pasaron correctamente.")


if __name__ == "__main__":
    ejecutar_pruebas()