create table total_orders as
SELECT *
from
(
    SELECT * FROM orders
    UNION ALL
    SELECT * FROM orders2
) T1
GROUP BY id;

drop table orders;
drop table orders2;

rename table total_orders to orders;

create table total_order_statuses as
SELECT *
from
(
    SELECT * FROM order_statuses
    UNION ALL
    SELECT * FROM order_statuses2
) T1
GROUP BY id;

drop table order_statuses;
drop table order_statuses2;
rename table total_order_statuses to order_statuses;


create table total_drivers as
SELECT *
from
(
    SELECT * FROM drivers
    UNION ALL
    SELECT * FROM drivers2
) T1
GROUP BY id;

drop table drivers;
drop table drivers2;
rename table total_drivers to drivers;



