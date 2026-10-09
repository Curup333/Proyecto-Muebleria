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
