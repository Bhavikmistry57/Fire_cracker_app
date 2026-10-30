import { rupees } from "../format";

export default function Catalog({ products, cart, onSetQty }) {
  if (products.length === 0) {
    return <p className="empty">The catalog is empty right now.</p>;
  }

  return (
    <section className="catalog">
      <p className="lede">
        Pick what you want. Payment happens later on WhatsApp with the seller.
      </p>
      <ul className="product-grid">
        {products.map((product) => {
          const qty = cart[product.id] || 0;
          return (
            <li key={product.id} className="product-card">
              {product.image_url && (
                <img className="product-image" src={product.image_url} alt={product.name} loading="lazy" />
              )}
              <div className="product-copy">
                <h2>{product.name}</h2>
                {product.description && <p>{product.description}</p>}
                {product.unit && <span className="unit">Sold as {product.unit}</span>}
              </div>
              <div className="product-buy">
                <strong>{rupees(product.price)}</strong>
                {qty === 0 ? (
                  <button type="button" className="button" onClick={() => onSetQty(product.id, 1)}>
                    Add
                  </button>
                ) : (
                  <div className="stepper" aria-label={`Quantity for ${product.name}`}>
                    <button type="button" onClick={() => onSetQty(product.id, qty - 1)} aria-label="Decrease quantity">
                      −
                    </button>
                    <span>{qty}</span>
                    <button
                      type="button"
                      onClick={() => onSetQty(product.id, qty + 1)}
                      disabled={qty >= 99}
                      aria-label="Increase quantity"
                    >
                      +
                    </button>
                  </div>
                )}
              </div>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
