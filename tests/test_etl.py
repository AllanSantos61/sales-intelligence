import pandas as pd
import pytest
from src.generate_data import generate
from src.etl import transform

def frame():
    return pd.DataFrame(generate(n=20, seed=7))

def test_deterministic_generation():
    assert generate(10, 42) == generate(10, 42)

def test_revenue_and_cost():
    df = frame()
    result = transform(df)
    row = result.iloc[0]
    assert row["net_revenue"] == round(row["quantity"] * row["unit_price"] * (1 - row["discount_pct"]), 2)
    assert row["gross_profit"] == round(row["net_revenue"] - row["total_cost"], 2)

def test_cancelled_orders_not_recognized():
    df = frame()
    df.loc[0, "status"] = "cancelled"
    out = transform(df)
    assert out.iloc[0]["recognized_revenue"] == 0
    assert out.iloc[0]["recognized_profit"] == 0

def test_duplicate_id_rejected():
    df = frame()
    df.loc[1, "order_id"] = df.loc[0, "order_id"]
    with pytest.raises(ValueError, match="unique"):
        transform(df)

def test_invalid_discount_rejected():
    df = frame()
    df.loc[0, "discount_pct"] = 1.5
    with pytest.raises(ValueError, match="discount_pct"):
        transform(df)
