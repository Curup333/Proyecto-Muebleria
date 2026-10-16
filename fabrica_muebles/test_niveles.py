import pytest

from creacion_orden import create_product, order_product


# Nivel 1: producto repetido en la orden

def test_nivel1_repetido_supera_stock():
    valery = create_product("valery", 3700, 10)
    with pytest.raises(ValueError, match="No hay stock suficiente de valery."):
        order_product([(valery, 6), (valery, 6)])


def test_nivel1_repetido_dentro_del_stock():
    valery = create_product("valery", 3700, 10)
    order_product([(valery, 5), (valery, 5)])


# Nivel 2: descontar el stock al confirmar

def test_nivel2_orden_valida_descuenta_stock():
    valery = create_product("valery", 3700, 10)
    order_product([(valery, 2)])
    assert valery["stock"] == 8


def test_nivel2_linea_mala_no_cambia_nada():
    valery = create_product("valery", 3700, 10)
    teresa = create_product("teresa", 130, 30)
    order_product([(valery, 2)])
    with pytest.raises(ValueError, match="No hay stock suficiente de teresa."):
        order_product([(valery, 3), (teresa, 999)])
    assert valery["stock"] == 8
    assert teresa["stock"] == 30


# Nivel 3: separar el calculo de la impresion

from decimal import Decimal

from creacion_orden import customer_data, order_summary


def test_nivel3_orden_de_ejemplo_vip():
    from creacion_orden import order_totals
    valery = create_product("valery", 3700, 10)
    teresa = create_product("teresa", 130, 30)
    lines = order_product([(valery, 2), (teresa, 6)])
    totals = order_totals(customer_data("angel", True), lines)
    assert totals == {
        "subtotal": Decimal("8180.00"),
        "discount": Decimal("818.00"),
        "total": Decimal("7362.00"),
    }


def test_nivel3_resumen_imprime_el_mismo_total(capsys):
    valery = create_product("valery", 3700, 10)
    teresa = create_product("teresa", 130, 30)
    lines = order_product([(valery, 2), (teresa, 6)])
    order_summary(customer_data("angel", True), lines)
    out = capsys.readouterr().out
    assert "TOTAL: $7362.00" in out
    assert out.count("valery - ") == 1
    assert "cantidad solicitada: 2, subtotal: $7400.00" in out


# Nivel 4: cancelar una orden

def test_nivel4_cancelar_devuelve_stock():
    from creacion_orden import create_order, cancel_order
    valery = create_product("valery", 3700, 10)
    order = create_order([(valery, 2)])
    assert order["status"] == "confirmada"
    assert valery["stock"] == 8
    cancel_order(order)
    assert order["status"] == "cancelada"
    assert valery["stock"] == 10


def test_nivel4_no_se_cancela_dos_veces():
    from creacion_orden import create_order, cancel_order
    valery = create_product("valery", 3700, 10)
    order = create_order([(valery, 2)])
    cancel_order(order)
    with pytest.raises(ValueError, match="La orden ya esta cancelada."):
        cancel_order(order)
    assert valery["stock"] == 10


# Nivel 5: productos con el mismo nombre y ordenes vacias

def test_nivel5_mismo_nombre_stock_separado():
    from creacion_orden import create_order
    silla_a = create_product("silla", 100, 5)
    silla_b = create_product("silla", 100, 5)
    order = create_order([(silla_a, 4), (silla_b, 4)])
    assert order["status"] == "confirmada"
    assert silla_a["stock"] == 1
    assert silla_b["stock"] == 1


def test_nivel5_orden_vacia_se_rechaza():
    from creacion_orden import create_order
    with pytest.raises(ValueError, match="La orden no tiene productos."):
        create_order([])


# Nivel 6: numeros que no son enteros de verdad

def test_nivel6_bool_no_es_numero():
    from creacion_orden import create_order
    with pytest.raises(ValueError, match="El stock tiene que ser un numero entero."):
        create_product("mesa", 500, True)
    valery = create_product("valery", 3700, 10)
    with pytest.raises(ValueError, match="La cantidad tiene que ser un numero entero."):
        create_order([(valery, True)])
    assert valery["stock"] == 10


def test_nivel6_decimal_con_decimales_se_rechaza():
    from creacion_orden import create_order
    with pytest.raises(ValueError, match="El stock tiene que ser un numero entero."):
        create_product("mesa", 500, Decimal("2.5"))
    valery = create_product("valery", 3700, 10)
    with pytest.raises(ValueError, match="La cantidad tiene que ser un numero entero."):
        create_order([(valery, Decimal("2.5"))])
    assert valery["stock"] == 10


# Nivel 7: cancelar un producto de la orden

def test_nivel7_cancelar_un_producto():
    from creacion_orden import create_order, cancel_line
    valery = create_product("valery", 3700, 10)
    teresa = create_product("teresa", 130, 30)
    order = create_order([(valery, 2), (valery, 1), (teresa, 6)])
    assert valery["stock"] == 7

    cancel_line(order, valery["id"])
    assert valery["stock"] == 10
    assert teresa["stock"] == 24
    assert len(order["lines"]) == 1
    assert order["status"] == "confirmada"

    cancel_line(order, teresa["id"])
    assert teresa["stock"] == 30
    assert len(order["lines"]) == 0
    assert order["status"] == "cancelada"


def test_nivel7_errores_no_cambian_nada():
    from creacion_orden import create_order, cancel_order, cancel_line
    valery = create_product("valery", 3700, 10)
    harp = create_product("harp", 1600, 20)
    order = create_order([(valery, 2)])
    with pytest.raises(ValueError, match="El producto no esta en la orden."):
        cancel_line(order, harp["id"])
    assert valery["stock"] == 8
    assert len(order["lines"]) == 1

    cancel_order(order)
    with pytest.raises(ValueError, match="La orden ya esta cancelada."):
        cancel_line(order, valery["id"])
    assert valery["stock"] == 10
