-- Count total customers
select count(*) from customers;

-- Count total products
select count(*) from products;

-- Count total orders
select count(*) from orders;

-- Count total payments
select count(*) from payments;

-- Count orders by status
select status, count(*) from orders group by status; 

-- Count payments by status
select status, count(*) from payments group by status;

-- Get total revenue from completed orders
select sum(total_amount) from orders where status='completed';

-- Get average order value
select avg(total_amount) as average_total_value from orders;

-- Get minimum and maximum order amount
select min(total_amount) as min, max(total_amount) as max from orders;

-- Get total orders per customer
select o.customer_id, c.name, count(*) as total_orders
from orders o join customers c 
on o.customer_id = c.id
group by o.customer_id, c.name
order by customer_id;

-- Get customers with more than 2 orders
select o.customer_id, c.name, count(*) as total_orders
from orders o join customers c 
on o.customer_id = c.id
group by o.customer_id, c.name
having count(*) > 2 order by customer_id;

-- Get total spend per customer
select o.customer_id, c.name, sum(total_amount) as total_spend
from orders o join customers c 
on o.customer_id = c.id
group by o.customer_id, c.name order by customer_id;

-- Get customers with total spend greater than 10000
select o.customer_id, c.name, sum(total_amount) as total_spend
from orders o join customers c 
on o.customer_id = c.id
group by o.customer_id, c.name 
having sum(total_amount) > 10000
order by customer_id;

-- Get number of items in each order
select order_id, count(*) as items_in_order from order_items group by order_id order by order_id;

-- Get orders having more than 5 items
select order_id, count(*) as items_in_order from order_items group by order_id having count(*) > 5 order by order_id;

-- Get total quantity sold per product
select oi.product_id, p.name, sum(quantity) as items_sold 
from order_items oi join products p 
on oi.product_id=p.id 
group by oi.product_id, p.name 
order by product_id;

-- Get top 10 selling products by quantity
select oi.product_id, p.name, sum(quantity) as items_sold 
from order_items oi join products p 
on oi.product_id=p.id 
group by oi.product_id, p.name 
order by items_sold desc
limit 10;

-- Get top 10 products by revenue
select oi.product_id, p.name, sum(subtotal) as product_revenue
from order_items oi join products p 
on oi.product_id=p.id 
group by oi.product_id, p.name 
order by product_revenue desc
limit 10;

-- Get products ordered more than 5 times
select oi.product_id, p.name, count(*) as number_of_times_ordered
from order_items oi join products p 
on oi.product_id=p.id 
group by oi.product_id, p.name
having count(*) > 5
order by oi.product_id;

-- Get failed payment count
select count(*) from payments where status='failed';

-- Get failed payment rate percentage

-- Get paid amount total by payment status
select status, round(sum(amount)::numeric,2) from payments group by status;

-- Get average payment amount by payment status
select status, round(avg(amount)::numeric,2) from payments group by status;

-- Get monthly order count
select date_trunc('month', created_at) as month,
 count(*) as orders_count
 from orders group by date_trunc('month', created_at)
 order by month;

-- Get monthly revenue from completed orders
select date_trunc('month', created_at) as month, round(sum(total_amount)::numeric,2) as monthly_revenue
from orders
where status='completed'
group by date_trunc('month', created_at)
order by month;

-- Find orders where total_amount does not match sum of order_items subtotal
select order_id, total_amount as actual_total, expected_total
from orders o join 
(select order_id, round(sum(subtotal)::numeric,2) as expected_total from order_items group by order_id) as x
on o.id=x.order_id
where total_amount <> expected_total
order by o.id;

-- Find duplicate payments for same order
select order_id, count(*) as payment_count
from payments
group by order_id
having count(*) > 1;

-- Find duplicate product lines within same order
select order_id, product_id, count(*)
from order_items
group by order_id, product_id
having count(*) > 1;

-- Find customers with no orders count
select count(*)
from customers c left join orders o
on c.id=o.customer_id
where o.customer_id is null;

-- Find products never ordered count
select count(*)
from products p left join order_items oi
on p.id=oi.product_id
where oi.product_id is null;