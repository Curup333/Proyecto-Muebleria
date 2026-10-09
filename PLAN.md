# Plan: fábrica de muebles

**Modo:** reto. El usuario escribe todo el código. Claude escribe los niveles y las pruebas finales, y ayuda solo cuando se lo piden.

**Meta:** aprender a escribir reglas de negocio de una orden que nunca dejan datos inválidos.

**Meta final:** `python3 -m pytest` → todo en verde (niveles 1 a 3).

## Nivel 1: Producto repetido en la orden
Hoy: stock=10, orden `[(valery, 6), (valery, 6)]` → se acepta (pide 12).
Construir: si un producto aparece varias veces, la orden revisa el stock contra la suma de sus cantidades.
Prueba final: `python3 -m pytest -k nivel1` → 2 passed
- `[(valery, 6), (valery, 6)]` con stock 10 → `ValueError("No hay stock suficiente de valery.")`
- `[(valery, 5), (valery, 5)]` con stock 10 → se acepta

## Nivel 2: Descontar el stock al confirmar
Construir: si toda la orden es válida, restar el stock. Si una línea falla, no cambia nada.
Prueba final: valery.stock 10 → orden de 2 → 8. Orden con una línea mala → sigue en 8.

## Nivel 3: Separar el cálculo de la impresión
Construir: una función que devuelve subtotal, descuento y total. `order_summary` solo imprime.
Prueba final: la orden de ejemplo da total `Decimal("7362.00")`.
