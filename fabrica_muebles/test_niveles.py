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
