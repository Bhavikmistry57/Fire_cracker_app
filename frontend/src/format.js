export function rupees(amount) {
  return `₹${Number(amount).toLocaleString("en-IN")}`;
}

const CART_KEY = "firecracker-cart";

export function loadCart() {
  try {
    const raw = localStorage.getItem(CART_KEY);
    const parsed = raw ? JSON.parse(raw) : {};
    if (!parsed || typeof parsed !== "object") return {};
    const cart = {};
    for (const [id, qty] of Object.entries(parsed)) {
      const quantity = Number(qty);
      if (Number.isInteger(quantity) && quantity > 0 && quantity <= 99) {
        cart[id] = quantity;
      }
    }
    return cart;
  } catch {
    return {};
  }
}

export function saveCart(cart) {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
}
