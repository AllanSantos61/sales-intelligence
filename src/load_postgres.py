"""Load cleaned synthetic CSV to PostgreSQL via DATABASE_URL.

Usage:
    DATABASE_URL=postgresql://... python -m src.load_postgres
Requires: pip install 'psycopg[binary]>=3,<4'
No credentials are stored in the repository.
"""
import os
from pathlib import Path
import pandas as pd
from src.etl import transform

ROOT = Path(__file__).resolve().parents[1]

def load(connection, frame):
    """Idempotent transactional load, with dimension upserts and fact upserts."""
    df = transform(frame)
    with connection.transaction():
        with connection.cursor() as cur:
            cur.execute((ROOT / "sql/01_schema.sql").read_text(encoding="utf-8"))
            customers = sorted(set(df["customer_id"]))
            products = sorted(set(df["product"]))
            sellers = sorted(set(df["seller"]))
            for customer in customers:
                cur.execute("INSERT INTO dim_customer(customer_id) VALUES (%s) ON CONFLICT DO NOTHING", (customer,))
            for product in products:
                cur.execute("INSERT INTO dim_product(product_name) VALUES (%s) ON CONFLICT DO NOTHING", (product,))
            for seller in sellers:
                cur.execute("INSERT INTO dim_seller(seller_name) VALUES (%s) ON CONFLICT DO NOTHING", (seller,))
            cur.execute("SELECT product_name, product_id FROM dim_product")
            product_ids = dict(cur.fetchall())
            cur.execute("SELECT seller_name, seller_id FROM dim_seller")
            seller_ids = dict(cur.fetchall())
            for row in df.itertuples(index=False):
                cur.execute("""
                    INSERT INTO fact_sales(order_id,order_date,customer_id,product_id,seller_id,
                        quantity,unit_price,discount_pct,unit_cost,status)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (order_id) DO UPDATE SET
                        order_date=EXCLUDED.order_date, customer_id=EXCLUDED.customer_id,
                        product_id=EXCLUDED.product_id, seller_id=EXCLUDED.seller_id,
                        quantity=EXCLUDED.quantity, unit_price=EXCLUDED.unit_price,
                        discount_pct=EXCLUDED.discount_pct, unit_cost=EXCLUDED.unit_cost,
                        status=EXCLUDED.status
                """, (row.order_id,row.order_date.date(),row.customer_id,
                      product_ids[row.product],seller_ids[row.seller],int(row.quantity),
                      float(row.unit_price),float(row.discount_pct),float(row.unit_cost),row.status))
    return len(df)

def main():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise SystemExit("DATABASE_URL not configured. Nothing loaded.")
    import psycopg
    path = ROOT / "data/sales_synthetic.csv"
    if not path.exists():
        raise SystemExit("Generate synthetic data first: python -m src.generate_data")
    with psycopg.connect(url) as connection:
        count = load(connection, pd.read_csv(path))
    print(f"Upserted {count} synthetic orders")

if __name__ == "__main__":
    main()
