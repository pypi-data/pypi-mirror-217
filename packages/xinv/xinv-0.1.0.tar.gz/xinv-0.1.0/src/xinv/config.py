from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping

import pydantic

from xinv.exceptions import ConfigError
from xinv.models import Company, InvoiceConfig, Item, Summary, Taxrate, Total


def get_default_config_path() -> str:
    return str(Path.home() / ".inv.json")


def get_sample_config() -> InvoiceConfig:
    return InvoiceConfig(
        place_of_issue="Warsaw",
        date_of_issue="2023-05-31",
        date_of_sale="2023-05-31",
        seller=Company(
            name="Seller Ltd",
            vat_id="PL1234567890",
            address1="al. Jerozolimskie 65/79",
            address2="00-697 Warsaw",
        ),
        buyer=Company(
            name="Buyer GmbH",
            vat_id="DE0987654321",
            address1="Pariser-Platz 1",
            address2="10117 Berlin",
        ),
        invoice_number="01/05/2023",
        items=[
            Item(
                description="Blue Jeans",
                unit="1 pcs.",
                quantity=1,
                unit_net_price=Decimal("100.59"),
                total_net_price=Decimal("100.59"),
                vat_rate="reverse charge",
                vat_amount=Decimal("0"),
                total_gross_price=Decimal("100.59"),
            ),
        ],
        taxrate=Taxrate(
            total_net_price=Decimal("100.59"),
            vat_rate="reverse charge",
            vat_amount=Decimal("0"),
            total_gross_price=Decimal("100.59"),
        ),
        summary=Summary(
            method_of_payment="transfer",
            account_number="PL61109010140000071219812874",
        ),
        currency="EUR",
        total=Total(
            total_net_price=Decimal("100.59"),
            vat_amount=Decimal("0"),
            total_gross_price=Decimal("100.59"),
            amount_in_words="one hundred 59/100 EUR",
        ),
    )


def load_config(config_data: Mapping[str, Any]) -> InvoiceConfig:
    try:
        return InvoiceConfig(**config_data)
    except pydantic.ValidationError as exc:
        raise ConfigError(exc.errors())
