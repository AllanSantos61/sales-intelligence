"""Build public static dashboard data from synthetic transactions."""
from pathlib import Path
import json
import pandas as pd
from src.etl import transform
from src.generate_data import generate

ROOT = Path(__file__).resolve().parents[1]
def build():
    df = transform(pd.DataFrame(generate()))
    df["month"] = df["order_date"].dt.strftime("%Y-%m")
    done = df[df["status"] == "completed"]
    monthly = done.groupby("month", as_index=False).agg(
        revenue=("recognized_revenue", "sum"),
        profit=("recognized_profit", "sum"),
        orders=("order_id", "count"))
    sellers = done.groupby("seller", as_index=False).agg(
        revenue=("recognized_revenue", "sum"), orders=("order_id", "count"))
    products = done.groupby("product", as_index=False).agg(
        revenue=("recognized_revenue", "sum"), profit=("recognized_profit", "sum"))
    customers = done.groupby("customer_id", as_index=False).agg(
        revenue=("recognized_revenue", "sum"), orders=("order_id", "count"))
    payload = {
        "meta": {"synthetic": True, "seed": 42, "orders": len(df), "completed": len(done)},
        "kpis": {"revenue": round(float(done["recognized_revenue"].sum()), 2),
                 "profit": round(float(done["recognized_profit"].sum()), 2),
                 "orders": len(done),
                 "average_order": round(float(done["recognized_revenue"].mean()), 2),
                 "margin_pct": round(100*float(done["recognized_profit"].sum())/float(done["recognized_revenue"].sum()), 2)},
        "monthly": monthly.to_dict(orient="records"),
        "sellers": sellers.sort_values("revenue", ascending=False).to_dict(orient="records"),
        "products": products.sort_values("revenue", ascending=False).to_dict(orient="records"),
        "customers": customers.sort_values("revenue", ascending=False).to_dict(orient="records"),
    }
    out = ROOT / "docs/dashboard/data.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Dashboard data generated: {out}")
    return payload

if __name__ == "__main__":
    build()
