import { useEffect, useMemo, useState } from "react";
import { fetchProducts, placeOrder } from "./api";
import { loadCart, saveCart } from "./format";
import Catalog from "./components/Catalog";
import Cart from "./components/Cart";
import Checkout from "./components/Checkout";
import OrderSent from "./components/OrderSent";

export default function App() {
  const [view, setView] = useState("catalog");
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState(loadCart);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [order, setOrder] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");

  useEffect(() => {
    let cancelled = false;
    fetchProducts()
      .then((data) => {
        if (!cancelled) setProducts(data);
      })
      .catch((error) => {
        if (!cancelled) setLoadError(error.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const productById = useMemo(() => {
    const map = new Map();
    for (const product of products) map.set(product.id, product);
    return map;
  }, [products]);

  useEffect(() => {
    saveCart(cart);
  }, [cart]);

  useEffect(() => {
    if (loading || loadError || products.length === 0) return;
    setCart((current) => {
      const next = {};
      let changed = false;
      for (const [id, qty] of Object.entries(current)) {
        if (productById.has(Number(id))) next[id] = qty;
        else changed = true;
      }
      return changed ? next : current;
    });
  }, [loading, loadError, products.length, productById]);

  const lines = useMemo(() => {
    return Object.entries(cart)
      .map(([id, qty]) => {
        const product = productById.get(Number(id));
        if (!product) return null;
        return { product, qty, lineTotal: product.price * qty };
      })
      .filter(Boolean);
  }, [cart, productById]);

  const total = lines.reduce((sum, line) => sum + line.lineTotal, 0);
  const count = lines.length
    ? lines.reduce((sum, line) => sum + line.qty, 0)
    : Object.values(cart).reduce((sum, qty) => sum + qty, 0);

  function setQty(productId, qty) {
    setCart((current) => {
      const next = { ...current };
      const key = String(productId);
      if (qty <= 0) delete next[key];
      else next[key] = Math.min(99, qty);
      return next;
    });
  }

  async function submitOrder(payload) {
    setSubmitting(true);
    setSubmitError("");
    try {
      const saved = await placeOrder(payload);
      setOrder(saved);
      setCart({});
      setView("sent");
    } catch (error) {
      setSubmitError(error.message);
    } finally {
      setSubmitting(false);
    }
  }

  function startOver() {
    setOrder(null);
    setSubmitError("");
    setView("catalog");
  }

  return (
    <div className="page">
      <header className="topbar">
        <button type="button" className="brand" onClick={() => setView("catalog")}>
          <span className="mark" aria-hidden="true" />
          Firecracker Shop
        </button>
        {view !== "sent" && (
          <button type="button" className="cart-link" onClick={() => setView("cart")}>
            Cart
            <span>{count}</span>
          </button>
        )}
      </header>
      <main>
        {loading && <p className="empty">Loading the catalog…</p>}
        {!loading && loadError && <p className="form-error">{loadError}</p>}
        {!loading && !loadError && view === "catalog" && (
          <Catalog products={products} cart={cart} onSetQty={setQty} />
        )}
        {!loading && !loadError && view === "cart" && (
          <Cart lines={lines} total={total} onSetQty={setQty} onCheckout={() => setView("checkout")} onBack={() => setView("catalog")} />
        )}
        {!loading && !loadError && view === "checkout" && (
          <Checkout
            lines={lines}
            total={total}
            onSubmit={submitOrder}
            submitting={submitting}
            error={submitError}
            onBack={() => setView("cart")}
          />
        )}
        {view === "sent" && order && <OrderSent order={order} onNew={startOver} />}
      </main>
      <footer>Payment is collected by the seller on WhatsApp.</footer>
    </div>
  );
}
