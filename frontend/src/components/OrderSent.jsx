import { rupees } from "../format";

export default function OrderSent({ order, onNew }) {
  return (
    <section className="panel">
      <p className="eyebrow">Order #{order.id} saved</p>
      <h2>Send this to the seller</h2>
      <p className="lede">
        Tap the button so WhatsApp opens with the bill filled in. You still need to press Send in WhatsApp. The seller will reply there for payment.
      </p>
      <ul className="summary">
        {order.items.map((item) => (
          <li key={item.product_id}>
            <span>
              {item.name} × {item.quantity}
            </span>
            <span>{rupees(item.line_total)}</span>
          </li>
        ))}
      </ul>
      <div className="total-row">
        <span>Total</span>
        <strong>{rupees(order.total)}</strong>
      </div>
      <dl className="details">
        <div>
          <dt>Name</dt>
          <dd>{order.customer_name}</dd>
        </div>
        <div>
          <dt>WhatsApp</dt>
          <dd>{order.whatsapp}</dd>
        </div>
        <div>
          <dt>Address</dt>
          <dd>{order.address}</dd>
        </div>
      </dl>
      {order.whatsapp_url ? (
        <a className="button wide" href={order.whatsapp_url} target="_blank" rel="noreferrer">
          Send order on WhatsApp
        </a>
      ) : (
        <p className="form-error">
          The order is saved, but the seller WhatsApp number is not configured yet. Set SELLER_WHATSAPP and open this order again.
        </p>
      )}
      <button type="button" className="text-button center" onClick={onNew}>
        Start a new order
      </button>
    </section>
  );
}
