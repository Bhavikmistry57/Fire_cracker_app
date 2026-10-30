"""Catalog products. Add each product's image URL in the image_url field."""

import re

PRODUCTS = [
    {"name": "Butterfly", "price": 150, "image_url": "/images/butterfly.jpg"},
    {"name": "Kothi small", "price": 120, "image_url": "/images/kothi small.jpg"},
    {"name": "Hira kothi", "price": 200, "image_url": "/images/hira kothi.jpg"},
    {"name": "Chakedi", "price": 160, "image_url": "/images/Chakedi.jpg"},
    {"name": "Chakedi Giant", "price": 270, "image_url": "/images/chakedi Gaint.jpg"},
    {"name": "Dragon fight", "price": 60, "image_url": "/images/dragon fight.jpg"},
    {"name": "M Kothi 12 PC", "price": 420, "image_url": "/images/M kothi 12 PC.jpg"},
    {"name": "M kothi 5 PC", "price": 350, "image_url": "/images/M kothi 5 PC.jpg"},
    {"name": "Green & red Fulzadi 10 BOX", "price": 220, "image_url": "/images/red&green fulzadi.jpg"},
    {"name": "Big Green & Red Fulzadi 10 BOX", "price": 500, "image_url": "/images/big red&green fulzadi.jpg"},
    {"name": "Jai bharat Fulzadi 10 BOX", "price": 100, "image_url": "/images/Jai bharat Fulzadi.jpg"},
    {"name": "Kothi big", "price": 180, "image_url": "/images/kothi big.jpg"},
    {"name": "Rocket 1 shot", "price": 110, "image_url": "/images/Rocket 1 shot.jpg"},
    {"name": "Big Taj Tetta", "price": 1100, "image_url": "/images/Big Taj Tetta.jpg"},
    {"name": "Rocket 3 shot", "price": 250, "image_url": "/images/Rocket 3 shot.jpg"},
    {"name": "Small Taj Tetta", "price": 750, "image_url": "/images/small Taj Tetta.jpg"},
    {"name": "Rocket 2 shot", "price": 200, "image_url": "/images/Rocket 2 shot.jpg"},
    {"name": "Chakli bomb", "price": 400, "image_url": "/images/Chakli bomb.jpg"},
    {"name": "Dori small", "price": 50, "image_url": "/images/dori small.jpg"},
    {"name": "Dori big", "price": 120, "image_url": "/images/dori big.jpg"},
    {"name": "Sapoliya", "price": 60, "image_url": "/images/sapoliya.jpg"},
    {"name": "Pop-pop box", "price": 300, "image_url": "/images/pop pop.jpg"},
    {"name": "Amazing Roll", "price": 300, "image_url": "/images/amazing roll.jpg"},
    {"name": "Bidi bomb", "price": 180, "image_url": "/images/bidi bomb.jpg"},
    {"name": "2 shot bomb", "price": 80, "image_url": "/images/2 shot bomb.jpg"},
    {"name": "12 sky shot", "price": 350, "image_url": "/images/12 sky shot.jpg"},
    {"name": "555", "price": 100, "image_url": "/images/555 Bomb.jpg"},
    {"name": "Mirchi", "price": 120, "image_url": "/images/mirchi bomb.jpg"},
    {"name": "Hand rocket", "price": 400, "image_url": "/images/hand rocket.jpg"},
    {"name": "Sutli gold", "price": 150, "image_url": "/images/Sutli gold.jpg"},
    {"name": "Sutli BB", "price": 230, "image_url": "/images/sutli bb.jpg"},
    {"name": "Sutli VIP", "price": 240, "image_url": "/images/sutli vip.jpg"},
    {"name": "Peacock jumbo", "price": 600, "image_url": "/images/peacock jumbo.jpg"},
    {"name": "Peacock small", "price": 450, "image_url": "/images/peacock small.jpg"},
    {"name": "Combo offer 1", "description": "BUTTERFLY - 1 BOX, KOTHI SMALL - 2 BOX, POP POP - 10 BOXES, CHAKEDI ROCK ON ROLL - 1 BOX, DRAGON FIGHT - 1 BOX, GREEN RED TARAMANDL - 10 BOXES, BHARAT TARAMANDAL - 10 BOXES, DORI SMALL - 1 BOX, SAPOLIYA - 1 BOX, BIDI BOMB - 1 BOX", "price": 999, "image_url": "/images/combo-product.jpg"},
    {"name": "Combo offer 2", "description": "VIP SUTLI BOMB - 2 BOXES, 555 BOMB - 2 BOXES, PREMIUM AMAZING CHAKRI - 1 BOX, VIP MIRCHI 2 BOXES, 2 SHOT BOMB - 2 BOXES, MATLA KOTHI 12 PCS, BIG TAJ BOMB 5 PCS, CHAKLI BOMB 2 PCS", "price": 1499, "image_url": "/images/combo_offer 2.jpg"}
]

LEGACY_STARTER_SLUGS = (
    "gold-sparklers",
    "color-sparklers",
    "bijili",
    "ground-chakkar",
    "flower-pots",
    "pencil-rockets",
    "lakshmi",
    "anar",
    "chorsa",
    "gift-box",
)


def _product_data(item: dict) -> dict:
    slug = re.sub(r"[^a-z0-9]+", "-", item["name"].casefold()).strip("-")
    return {
        "slug": slug,
        "name": item["name"],
        "description": item.get("description", ""),
        "price": item["price"],
        "unit": "",
        "image_url": item.get("image_url") or None,
    }


def seed_products(db) -> None:
    from app.models import Product

    db.query(Product).filter(Product.slug.in_(LEGACY_STARTER_SLUGS)).delete(
        synchronize_session=False
    )
    db.flush()
    products_by_slug = {product.slug: product for product in db.query(Product).all()}
    for item in PRODUCTS:
        data = _product_data(item)
        product = products_by_slug.get(data["slug"])
        if product is None:
            db.add(Product(**data))
            continue

        product.name = data["name"]
        product.description = data["description"]
        product.price = data["price"]
        product.unit = data["unit"]
        if "image_url" in item:
            product.image_url = data["image_url"]

    db.commit()
