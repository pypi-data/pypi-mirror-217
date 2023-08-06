import locale
from decimal import Decimal


def localize_decimal(value: Decimal) -> str:
    return locale.format_string("%.2f", value)
