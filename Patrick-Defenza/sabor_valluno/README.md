# Sistema de Gestión de Pedidos – Restaurante "Sabor Valluno" (Variante A)

Proyecto de Programación Orientada a Objetos desarrollado en Python para la gestión de menú, pedidos, pagos y recaudación del restaurante **Sabor Valluno**.

## Integrante / Autor
* **Estudiante:** Patrick Quiroz (`Pathquiroz`)
* **Variante asignada:** Variante A

## Estructura del Proyecto
* `productos.py`: Jerarquía abstracta `Producto` con subclases `Plato`, `Bebida` y `Combo` (descuento del 10 % y soporte para combos anidados).
* `pedidos.py`: Jerarquía abstracta `Pedido` con subclases `Local`, `Llevar` y `Delivery` (envases a Bs 2, monto mínimo Bs 40 y envío gratis desde Bs 150).
* `pagos.py`: Jerarquía abstracta `Pago` con subclases `Efectivo`, `Qr` y `Tarjeta` (restricción polimórfica de tarjeta en Delivery).
* `clientes.py`: Clase `Cliente` con validación de datos.
* `restaurante.py`: Clase gestora que centraliza el menú, clientes, pedidos y reportes.
* `main.py`: Interfaz de consola con las 7 opciones operativas.
* `pruebas.py`: Suite de 10 pruebas unitarias automatizadas con `assert`.
* `docs/`: Diagrama de clases (`diagrama_v1.jpeg`), acta de consultas y bitácora de uso de IA.

## Ejecución
```bash
python pruebas.py
python main.py