import pdfkit
from jinja2 import Environment, PackageLoader

from xinv.filters import localize_decimal
from xinv.models import InvoiceConfig

env = Environment(loader=PackageLoader("xinv", "assets"))
env.filters["localize_decimal"] = localize_decimal


def render_invoice(config: InvoiceConfig, output_path: str) -> None:
    template = env.get_template("template.html")
    html_string = template.render(**config.dict())

    pdfkit.from_string(
        html_string,
        output_path,
        {
            "enable-local-file-access": True,
            "footer-right": "[page] / [topage]",
        },
    )
