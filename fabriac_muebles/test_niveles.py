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
