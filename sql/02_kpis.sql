-- Revenue and gross profit exclude cancelled orders.
WITH sales AS (
  SELECT f.*,
    quantity * unit_price * (1 - discount_pct) AS net_revenue,
    quantity * unit_cost AS total_cost
  FROM fact_sales f
)
SELECT
  DATE_TRUNC('month', order_date)::date AS month,
  COUNT(*) FILTER (WHERE status='completed') AS orders,
  ROUND(SUM(net_revenue) FILTER (WHERE status='completed'), 2) AS revenue,
  ROUND(SUM(net_revenue - total_cost) FILTER (WHERE status='completed'), 2) AS gross_profit,
  ROUND(
    SUM(net_revenue) FILTER (WHERE status='completed')
    / NULLIF(COUNT(*) FILTER (WHERE status='completed'), 0), 2
  ) AS average_order_value
FROM sales
GROUP BY 1
ORDER BY 1;

-- Revenue by seller
SELECT s.seller_name,
  COUNT(*) AS completed_orders,
  ROUND(SUM(f.quantity*f.unit_price*(1-f.discount_pct)), 2) AS revenue
FROM fact_sales f
JOIN dim_seller s ON s.seller_id=f.seller_id
WHERE f.status='completed'
GROUP BY s.seller_name
ORDER BY revenue DESC;
