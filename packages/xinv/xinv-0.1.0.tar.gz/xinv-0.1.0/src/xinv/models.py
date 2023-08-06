from datetime import date
from typing import Sequence

from pydantic import BaseModel, ConstrainedDecimal, condecimal

Money: ConstrainedDecimal = condecimal(decimal_places=2)


class Company(BaseModel):
    name: str
    vat_id: str
    address1: str
    address2: str


class Item(BaseModel):
    description: str
    unit: str
    quantity: int
    unit_net_price: Money
    total_net_price: Money
    vat_rate: str
    vat_amount: Money
    total_gross_price: Money


class Taxrate(BaseModel):
    total_net_price: Money
    vat_rate: str
    vat_amount: Money
    total_gross_price: Money


class Total(BaseModel):
    total_net_price: Money
    vat_amount: Money
    total_gross_price: Money
    amount_in_words: str


class Summary(BaseModel):
    method_of_payment: str
    account_number: str


class InvoiceConfig(BaseModel):
    place_of_issue: str
    date_of_issue: date
    date_of_sale: date
    seller: Company
    buyer: Company
    invoice_number: str
    items: Sequence[Item]
    taxrate: Taxrate
    total: Total
    summary: Summary
    currency: str
