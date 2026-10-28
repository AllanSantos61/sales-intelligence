-- PostgreSQL demonstration schema; all records are synthetic.
CREATE TABLE IF NOT EXISTS dim_customer (
  customer_id VARCHAR(8) PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS dim_product (
  product_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  product_name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS dim_seller (
  seller_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  seller_name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS fact_sales (
  order_id BIGINT PRIMARY KEY,
  order_date DATE NOT NULL,
  customer_id VARCHAR(8) NOT NULL REFERENCES dim_customer(customer_id),
  product_id BIGINT NOT NULL REFERENCES dim_product(product_id),
  seller_id BIGINT NOT NULL REFERENCES dim_seller(seller_id),
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  unit_price NUMERIC(14,2) NOT NULL CHECK (unit_price >= 0),
  discount_pct NUMERIC(5,4) NOT NULL CHECK (discount_pct BETWEEN 0 AND 1),
  unit_cost NUMERIC(14,2) NOT NULL CHECK (unit_cost >= 0),
  status TEXT NOT NULL CHECK (status IN ('completed','cancelled'))
);
CREATE INDEX IF NOT EXISTS idx_fact_sales_date ON fact_sales(order_date);
CREATE INDEX IF NOT EXISTS idx_fact_sales_customer ON fact_sales(customer_id);
