-- Get customer name with their order id and order status
select c.name as cusomtomer_name, o.id as order_id , o.status as order_status
from customers c join orders o
on c.id = o.customer_id;

-- Get all orders with customer name sorted by latest order first
select o.id as order_id, c.name as customer_name, o.created_at as order_created_at
from orders o join customers c
on o.customer_id = c.id
order by o.created_at desc;

-- Get customers who have placed at least one order
select distinct customers.id, customers.name 
from customers join orders 
on customers.id = orders.customer_id
order by customers.id;

-- Get customers with no orders
select c.id, c.name 
from customers c left join orders o 
on c.id = o.customer_id where o.customer_id is null;

-- Get each order with its ordered products
select o.id, o.customer_id, oi.product_id, o.status, o.total_amount
from orders o join order_items oi
on o.id=oi.order_id 
order by o.id;

-- Get each order with product name, quantity, price, and subtotal
SELECT o.id as order_id, p.name as product_name, oi.quantity, p.price, oi.subtotal
from orders o join order_items oi
on o.id = oi.order_id
join products p
on oi.product_id = p.id;

-- Get orders with payment status and payment amount
select o.id, p.status as payment_status, p.amount as amount
from orders o join payments p
on o.id=p.order_id
order by o.id;

-- Get full chain data: customer name, order id, product name, quantity, payment id
SELECT c.name, o.id as order_id, p.name as product_name, oi.quantity as quantity, pay.id as payment_id
from customers c join orders o
on c.id=o.customer_id
join order_items oi
on o.id=oi.order_id
join products p
on oi.product_id = p.id
left join payments pay
on o.id=pay.order_id;

-- Get all completed orders with paid payment
select o.id as order_id, o.status as order_status, o.total_amount as amout_to_pay, p.amount as paid_amount, p.status as paid_status
from orders o join payments p
on o.id=p.order_id
where o.status='completed' and p.status='paid'
order by o.id;

-- Get all pending orders with pending payment
select o.id as order_id, o.status as order_status, o.total_amount as amout_to_pay, p.amount as pending_amount, p.status as paid_status
from orders o join payments p
on o.id=p.order_id
where o.status='pending' and p.status='pending'
order by o.id;

-- Get all cancelled orders with no payment
select o.id as order_id, o.status as order_status, o.total_amount as amout_to_pay, p.amount as paid_amount, p.status as paid_status
from orders o left join payments p
on o.id=p.order_id
where o.status='cancelled' and p.order_id is null
order by o.id;

-- Get orders where payment exists but customer details also shown
select o.id, o.status,c.name
from orders o join payments p
on o.id=p.order_id
join customers c
on o.customer_id=c.id
order by o.id;

-- Get number of items in each order
select o.id, count(oi.id)
from orders o join order_items oi
on o.id=oi.order_id
group by o.id
order by o.id;

-- Get orders having more than 5 items
select o.id, o.status, count(oi.id) as ordered_items_count
from orders o join order_items oi
on o.id=oi.order_id
group by o.id, o.status
having count(oi.id) > 5
order by o.id;


-- Get customers and total number of orders placed
select c.id, c.name, count(o.id) as total_orders
from customers c left join orders o
on c.id = o.customer_id
group by c.id, c.name;

-- Get latest order for each customer
select c.id as customer_id, c.name as customer_name, o.id as order_id, o.created_at as order_creation_date
from customers c 
join orders o
on c.id = o.customer_id
join (select customer_id, max(created_at) as latest_orders 
from orders group by customer_id) latest
on o.customer_id = latest.customer_id
and o.created_at = latest.latest_orders
order by c.id;

select customer_id, customer_name, order_id, order_created_at
FROM(
SELECT 
        c.id AS customer_id,
        c.name AS customer_name,
        o.id AS order_id,
        o.created_at AS order_created_at,
        ROW_NUMBER() OVER (
            PARTITION BY c.id 
            ORDER BY o.created_at DESC
        ) AS rn
    FROM customers c
    JOIN orders o
    ON c.id = o.customer_id) x
    where rn=1 order by customer_id;

-- Get products that were never ordered
select p.id,p.name 
from products p left join order_items oi
on p.id=oi.product_id
where oi.product_id is null;

-- Get orders that contain more than one different product
select o.id, count(distinct oi.product_id)
from orders o join order_items oi
on o.id=oi.order_id
group by o.id
having count(distinct oi.product_id)>1;

-- Get orders where payment amount matches total_amount
select o.id, o.total_amount, p.amount
from orders o join payments p
on o.id=p.order_id
where o.total_amount = p.amount
order by o.id;

-- Get orders where payment amount does not match total_amount
select o.id, o.total_amount, p.amount
from orders o join payments p
on o.id=p.order_id
where o.total_amount <> p.amount;