"""Validated ETL for synthetic sales data."""
from pathlib import Path
import pandas as pd

REQUIRED = {"order_id", "order_date", "customer_id", "product", "seller",
            "quantity", "unit_price", "discount_pct", "unit_cost", "status"}

def transform(df: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    out = df.copy()
    if out["order_id"].isna().any() or out["order_id"].duplicated().any():
        raise ValueError("order_id must be unique and non-null")
    out["order_date"] = pd.to_datetime(out["order_date"], errors="raise")
    numeric = ["quantity", "unit_price", "discount_pct", "unit_cost"]
    for column in numeric:
        out[column] = pd.to_numeric(out[column], errors="raise")
    if (out["quantity"] <= 0).any() or (out[["unit_price", "unit_cost"]] < 0).any().any():
        raise ValueError("Invalid quantity, price or cost")
    if (~out["discount_pct"].between(0, 1)).any():
        raise ValueError("discount_pct must be between 0 and 1")
    if (~out["status"].isin(["completed", "cancelled"])).any():
        raise ValueError("Unknown order status")
    out["gross_revenue"] = (out["quantity"] * out["unit_price"]).round(2)
    out["net_revenue"] = (out["gross_revenue"] * (1 - out["discount_pct"])).round(2)
    out["total_cost"] = (out["quantity"] * out["unit_cost"]).round(2)
    out["gross_profit"] = (out["net_revenue"] - out["total_cost"]).round(2)
    # Cancelled orders are retained for operational analysis but excluded from sales KPIs.
    out["recognized_revenue"] = out["net_revenue"].where(out["status"] == "completed", 0)
    out["recognized_profit"] = out["gross_profit"].where(out["status"] == "completed", 0)
    return out

def run(source: Path, destination: Path):
    cleaned = transform(pd.read_csv(source))
    destination.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(destination, index=False, date_format="%Y-%m-%d")
    print(f"Processed {len(cleaned)} rows to {destination}")

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    run(root / "data/sales_synthetic.csv", root / "data/sales_clean.csv")
