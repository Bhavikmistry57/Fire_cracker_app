import { rupees } from "../format";

export default function Cart({ lines, total, onSetQty, onCheckout, onBack }) {
  return (
    <section className="panel">
      <button type="button" className="text-button" onClick={onBack}>
        Back to catalog
      </button>
      <h2>Your cart</h2>
      {lines.length === 0 ? (
        <p className="empty">Your cart is empty. Add something from the catalog.</p>
      ) : (
        <>
          <ul className="line-list">
            {lines.map((line) => (
              <li key={line.product.id}>
                <div>
                  <strong>{line.product.name}</strong>
                  <span>
                    {rupees(line.product.price)}
                    {line.product.unit && ` / ${line.product.unit}`}
                  </span>
                </div>
                <div className="line-actions">
                  <div className="stepper" aria-label={`Quantity for ${line.product.name}`}>
                    <button type="button" onClick={() => onSetQty(line.product.id, line.qty - 1)} aria-label="Decrease quantity">
                      −
                    </button>
                    <span>{line.qty}</span>
                    <button
                      type="button"
                      onClick={() => onSetQty(line.product.id, line.qty + 1)}
                      disabled={line.qty >= 99}
                      aria-label="Increase quantity"
                    >
                      +
                    </button>
                  </div>
                  <span className="line-total">{rupees(line.lineTotal)}</span>
                  <button type="button" className="text-button" onClick={() => onSetQty(line.product.id, 0)}>
                    Remove
                  </button>
                </div>
              </li>
            ))}
          </ul>
          <div className="total-row">
            <span>Total</span>
            <strong>{rupees(total)}</strong>
          </div>
          <button type="button" className="button wide" onClick={onCheckout}>
            Checkout
          </button>
        </>
      )}
    </section>
  );
}
