# Acta de Consultas - Restaurante Sabor Valluno (Variante A)

**Estudiante:** Nava Nina Maria del Carmen  
**Variante:** A  

| Fecha | Pregunta o tema consultado al docente | Respuesta / Aclaración del docente |
| :--- | :--- | :--- |
| 17/11/2026 | Cómo modelar `lista_productos` dentro de la clase `Combo` para que soporte platos, bebidas y otros combos. | Aclaró que `Combo` hereda de `Producto` y guarda una lista de objetos de tipo `Producto`, lo que permite incluir tanto productos simples como otros combos. |
| 17/11/2026 | Consulta realizada en aula sobre la Regla 9 (retraso en delivery). | El ingeniero indicó en clase que se omita la implementación de la Regla 9. |
| 17/11/2026 | Cómo se maneja el pago en `Delivery` respecto a la clase padre `Pedido`. | Aclaró que el atributo `pago` se hereda desde `Pedido`, pero en `Delivery` se restringe para aceptar únicamente efectivo o QR (sin tarjeta). |