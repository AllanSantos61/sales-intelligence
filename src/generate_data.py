"""Deterministic synthetic commercial dataset. No personal or client data."""
from pathlib import Path
import csv
import random
from datetime import date, timedelta

BASE = Path(__file__).resolve().parents[1]
CUSTOMERS = ["Aurora Labs", "Vértice Digital", "Prisma Store", "Horizonte Tech",
             "Nexo Serviços", "Orion Comércio", "Lume Solutions", "Nova Era"]
PRODUCTS = [("Software", 1200, 0.35), ("Consultoria", 2400, 0.24),
            ("Treinamento", 600, 0.18), ("Suporte", 450, 0.30)]
SELLERS = ["Marina", "Rafael", "Camila", "Bruno"]

def generate(n=600, seed=42):
    rng = random.Random(seed)
    start = date(2025, 1, 1)
    records = []
    for i in range(1, n + 1):
        category, price, cost_ratio = rng.choice(PRODUCTS)
        quantity = rng.randint(1, 6)
        discount = rng.choice([0, 0, 0.05, 0.10, 0.15])
        unit_price = round(price * rng.uniform(0.9, 1.1), 2)
        records.append({
            "order_id": i,
            "order_date": (start + timedelta(days=rng.randrange(730))).isoformat(),
            "customer_id": f"C{rng.randrange(1, len(CUSTOMERS)+1):03d}",
            "customer_name": "",  # intentionally excluded from fact table
            "product": category,
            "seller": rng.choice(SELLERS),
            "quantity": quantity,
            "unit_price": unit_price,
            "discount_pct": discount,
            "unit_cost": round(unit_price * (1 - cost_ratio), 2),
            "status": rng.choices(["completed", "cancelled"], weights=[94, 6])[0],
        })
    return records

def main():
    folder = BASE / "data"
    folder.mkdir(exist_ok=True)
    records = generate()
    path = folder / "sales_synthetic.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print(f"Generated {len(records)} synthetic orders: {path}")

if __name__ == "__main__":
    main()
