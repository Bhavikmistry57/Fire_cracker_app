import os
import re
from urllib.parse import quote

from dotenv import load_dotenv

load_dotenv()


def seller_number() -> str | None:
    raw = os.environ.get("SELLER_WHATSAPP", "")
    digits = re.sub(r"\D", "", raw)
    if 11 <= len(digits) <= 15:
        return digits
    return None


def order_message(order_id: int, customer_name: str, whatsapp: str, address: str, items: list[dict], total: int) -> str:
    lines = [
        f"New order #{order_id}",
        f"Name: {customer_name}",
        f"WhatsApp: {whatsapp}",
        f"Address: {address}",
        "",
        "Items:",
    ]
    for item in items:
        lines.append(
            f"- {item['name']} x {item['quantity']} = ₹{item['line_total']}"
        )
    lines.append("")
    lines.append(f"Total: ₹{total}")
    lines.append("Please share payment details on WhatsApp.")
    return "\n".join(lines)


def whatsapp_url(message: str) -> str | None:
    number = seller_number()
    if not number:
        return None
    return f"https://wa.me/{number}?text={quote(message)}"
