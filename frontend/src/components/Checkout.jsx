import { useState } from "react";
import { rupees } from "../format";

export default function Checkout({ lines, total, onSubmit, submitting, error, onBack }) {
  const [name, setName] = useState("");
  const [whatsapp, setWhatsapp] = useState("");
  const [address, setAddress] = useState("");
  const [localError, setLocalError] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    const customerName = name.trim();
    const phone = whatsapp.replace(/\D/g, "");
    const delivery = address.trim();
    if (customerName.length < 2) {
      setLocalError("Enter your name.");
      return;
    }
    const normalized = phone.length === 12 && phone.startsWith("91") ? phone.slice(2) : phone.replace(/^0/, "");
    if (!/^[6-9]\d{9}$/.test(normalized)) {
      setLocalError("Enter a 10-digit WhatsApp mobile number.");
      return;
    }
    if (delivery.length < 10) {
      setLocalError("Enter a delivery address of at least 10 characters.");
      return;
    }
    setLocalError("");
    onSubmit({
      customer_name: customerName,
      whatsapp: normalized,
      address: delivery,
      items: lines.map((line) => ({ product_id: line.product.id, quantity: line.qty })),
    });
  }

  return (
    <section className="panel">
      <button type="button" className="text-button" onClick={onBack}>
        Back to cart
      </button>
      <h2>Delivery details</h2>
      <p className="lede">
        We do not take payment here. After you confirm, WhatsApp opens with this order ready to send to the seller.
      </p>
      <ul className="summary">
        {lines.map((line) => (
          <li key={line.product.id}>
            <span>
              {line.product.name} × {line.qty}
            </span>
            <span>{rupees(line.lineTotal)}</span>
          </li>
        ))}
      </ul>
      <div className="total-row">
        <span>Total</span>
        <strong>{rupees(total)}</strong>
      </div>
      <form onSubmit={handleSubmit} className="checkout-form">
        <label>
          Your name
          <input value={name} onChange={(event) => setName(event.target.value)} autoComplete="name" required />
        </label>
        <label>
          WhatsApp mobile number
          <input
            value={whatsapp}
            onChange={(event) => setWhatsapp(event.target.value)}
            inputMode="numeric"
            autoComplete="tel"
            placeholder="10-digit mobile"
            required
          />
        </label>
        <label>
          Delivery address
          <textarea
            value={address}
            onChange={(event) => setAddress(event.target.value)}
            rows={4}
            autoComplete="street-address"
            required
          />
        </label>
        {(localError || error) && <p className="form-error">{localError || error}</p>}
        <button type="submit" className="button wide" disabled={submitting || lines.length === 0}>
          {submitting ? "Saving order…" : "Confirm order"}
        </button>
      </form>
    </section>
  );
}
