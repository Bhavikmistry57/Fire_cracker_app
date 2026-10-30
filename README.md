# Firecracker Shop

A small catalog and cart. The customer checks out with a name, WhatsApp number, and delivery address. The app saves the order, prices it on the server, and opens WhatsApp with the bill ready to send to the seller. Payment is arranged in that chat.

## Local

Backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Edit `SELLER_WHATSAPP` in `backend/.env`. Use country code plus number, with no plus sign, for example `9198xxxxxxx`.

Frontend, in another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://127.0.0.1:5173. The Vite dev server proxies `/api` to the backend.

Change the catalog in `backend/app/seed.py`. Restart the backend. New product slugs are inserted. Slugs that already exist are left as they are.

Orders are stored in SQLite at `DATABASE_PATH` (default `backend/data/shop.db` when you run from `backend/`).

## Railway

The repo is one service. The Docker image builds the React app and FastAPI serves it.

1. Push this project to GitHub.
2. On [railway.com](https://railway.com), create a project from that repo. Railway reads `railway.toml` and builds the `Dockerfile`.
3. Add variables:
   - `SELLER_WHATSAPP` = your number with country code, no `+`
   - `DATABASE_PATH` = `/data/shop.db`
4. Add a volume mounted at `/data` so orders survive restarts.
5. Generate a public domain. Open it and place a test order.

Railway’s Free plan includes $1 of usage credit each month (new accounts also get $5 for the first 30 days). This app is a single small process plus a SQLite file so it can fit that credit. If usage passes the credit, Railway pauses the service until the next month.

There is no card payment and no WhatsApp Business API. The customer taps **Send order on WhatsApp**, then presses Send in WhatsApp. The seller replies in that chat to collect payment.
