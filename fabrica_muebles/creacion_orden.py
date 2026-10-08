from decimal import Decimal, ROUND_HALF_UP, DecimalException


def _validar(condicion: bool, mensaje: str) -> None:
    if not condicion:
        raise ValueError(mensaje)


def create_product(name, price, stock=0, active=True) -> dict:
    _validar(isinstance(active, bool), "Active tiene que ser True o False.")
    _validar(isinstance(name, str), "El nombre tiene que ser un texto.")
    clean_name = name.strip().lower()
    _validar(clean_name, "El nombre no puede estar vacio.")
    _validar(not isinstance(stock, float) or stock.is_integer(), "El stock tiene que ser un numero entero.")

    try:
        price_dec = Decimal(str(price)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        stock_int = int(stock)
    except (ValueError, TypeError, DecimalException):
        raise ValueError("El precio y el stock tienen que ser numeros validos.") from None

    _validar(price_dec.is_finite(), "El precio tiene que ser un numero valido.")
    _validar(price_dec > 0, "El precio tiene que ser mayor que cero.")
    _validar(stock_int >= 0, "El stock no puede ser negativo.")

    return {
        "name": clean_name,
        "price": price_dec,
        "stock": stock_int,
        "active": active,
    }


def validate_stock(product, amount) -> tuple[int, bool]:
    _validar(product["active"], "El producto no esta activo.")
    _validar(not isinstance(amount, float) or amount.is_integer(), "La cantidad tiene que ser un numero entero.")

    try:
        amount_int = int(amount)
    except (ValueError, TypeError):
        raise ValueError("La cantidad tiene que ser un numero valido.") from None

    _validar(amount_int > 0, "La cantidad tiene que ser mayor que cero.")
    stock_available = product["stock"] >= amount_int

    return amount_int, stock_available


def customer_data(user_name, vip=False) -> dict:
    _validar(isinstance(vip, bool), "VIP tiene que ser True o False.")
    _validar(isinstance(user_name, str), "El nombre tiene que ser texto.")

    clean_user_name = user_name.strip().lower()
    _validar(clean_user_name, "El nombre no puede estar vacio.")

    return {
        "name": clean_user_name,
        "vip": vip,
    }


def order_product(items) -> list[dict]:
    order_lines = []

    for product, amount in items:
        amount_int, available = validate_stock(product, amount)
        _validar(available, f"No hay stock suficiente de {product['name']}.")
        order_lines.append({"product": product, "amount": amount_int})

    return order_lines


def order_summary(user_data: dict, order_lines: list) -> None:
    print("=" * 10, "RESUMEN DE ORDEN", "=" * 10)

    print(f"Usuario: {user_data['name']}")
    print(f"VIP?: {user_data['vip']}")

    print("ITEMS")
    for line in order_lines:
        product = line["product"]
        amount = line["amount"]
        print(f"{product['name']} - precio: {product['price']}, cantidad solicitada: {amount}")

    print("-" * 30)


if __name__ == "__main__":
    try:
        valery = create_product("valery", 3700, 10)
        teresa = create_product("teresa", 130, 30)
        harp = create_product("harp", 1600, 20)

        lines = order_product([(valery, 2), (teresa, 6)])
        user1 = customer_data("angel", True)

        order_summary(user1, lines)

    except ValueError as e:
        print(f"Error: {e}")
    