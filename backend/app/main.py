import json
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db, init_db
from app.models import Order, Product
from app.schemas import OrderCreate, OrderItemOut, OrderOut, ProductOut
from app.whatsapp import order_message, whatsapp_url


def _static_dir() -> Path | None:
    configured = os.environ.get("STATIC_DIR")
    if configured:
        path = Path(configured)
    else:
        path = Path(__file__).resolve().parents[2] / "frontend" / "dist"
    if path.is_dir() and (path / "index.html").is_file():
        return path
    return None


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Firecracker Shop", lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_error(_request: Request, exc: RequestValidationError):
    messages = []
    for err in exc.errors():
        loc = [part for part in err.get("loc", ()) if part != "body"]
        field = str(loc[-1]) if loc else "request"
        msg = err.get("msg", "Invalid value")
        if msg.startswith("Value error, "):
            msg = msg[len("Value error, ") :]
        messages.append(f"{field}: {msg}")
    return JSONResponse(status_code=422, content={"detail": "; ".join(messages)})


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/products", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).order_by(Product.id).all()


def _line_items(db: Session, payload: OrderCreate) -> list[dict]:
    merged: dict[int, int] = {}
    for item in payload.items:
        merged[item.product_id] = merged.get(item.product_id, 0) + item.quantity

    products = db.query(Product).filter(Product.id.in_(merged.keys())).all()
    by_id = {product.id: product for product in products}
    missing = [str(product_id) for product_id in merged if product_id not in by_id]
    if missing:
        raise HTTPException(status_code=400, detail="One or more products are no longer in the catalog")

    lines = []
    for product_id, quantity in merged.items():
        if quantity > 99:
            raise HTTPException(status_code=400, detail="Quantity cannot be more than 99")
        product = by_id[product_id]
        lines.append(
            {
                "product_id": product.id,
                "name": product.name,
                "unit": product.unit,
                "quantity": quantity,
                "unit_price": product.price,
                "line_total": product.price * quantity,
            }
        )
    return lines


def _order_out(order: Order) -> OrderOut:
    items = [OrderItemOut(**item) for item in json.loads(order.items_json)]
    message = order_message(
        order.id,
        order.customer_name,
        order.whatsapp,
        order.address,
        [item.model_dump() for item in items],
        order.total,
    )
    return OrderOut(
        id=order.id,
        customer_name=order.customer_name,
        whatsapp=order.whatsapp,
        address=order.address,
        items=items,
        total=order.total,
        created_at=order.created_at,
        message=message,
        whatsapp_url=whatsapp_url(message),
    )


@app.post("/api/orders", response_model=OrderOut)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    lines = _line_items(db, payload)
    total = sum(line["line_total"] for line in lines)
    order = Order(
        customer_name=payload.customer_name,
        whatsapp=payload.whatsapp,
        address=payload.address,
        items_json=json.dumps(lines),
        total=total,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return _order_out(order)


@app.get("/api/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return _order_out(order)


static_dir = _static_dir()
if static_dir is not None:

    @app.get("/", include_in_schema=False)
    def spa_index():
        return FileResponse(static_dir / "index.html")

    @app.get("/{full_path:path}", include_in_schema=False)
    def spa_files(full_path: str):
        if full_path.startswith("api/") or full_path == "api":
            raise HTTPException(status_code=404, detail="Not found")
        root = static_dir.resolve()
        candidate = (static_dir / full_path).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            raise HTTPException(status_code=404, detail="Not found") from None
        if candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(static_dir / "index.html")
