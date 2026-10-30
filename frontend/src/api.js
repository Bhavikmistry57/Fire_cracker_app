async function readError(response) {
  const body = await response.json().catch(() => ({}));
  if (typeof body.detail === "string" && body.detail) return body.detail;
  return "Something went wrong. Please try again.";
}

export async function fetchProducts() {
  const response = await fetch("/api/products");
  if (!response.ok) throw new Error(await readError(response));
  return response.json();
}

export async function placeOrder(payload) {
  const response = await fetch("/api/orders", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error(await readError(response));
  return response.json();
}
