create table total_orders (delivered_at datetime) as
SELECT delivered_at
from
(
    SELECT delivered_at FROM orders
    UNION ALL
    SELECT delivered_at FROM orders2
) T1
GROUP BY delivered_at