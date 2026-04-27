-- Find orders where total_amount does not match sum of order_items subtotal
select o.id, o.total_amount,x.calculated_amount
from orders o 
join (
	select oi.order_id, round(sum(subtotal)::numeric, 2) as calculated_amount
	from order_items oi
	group by oi.order_id
	order by oi.order_id) x
on o.id = x.order_id
WHERE o.total_amount <> x.calculated_amount
order by o.id;

-- Find completed orders without paid payment
select o.id, o.status, p.status
from orders o left join payments p
on o.id = p.order_id
where o.status='completed' and (p.status<>'paid' or p.status is null);

-- Find pending orders with paid payment
select o.id, o.status, p.status
from orders o join payments p
on o.id = p.order_id
where o.status='pending' and p.status='paid';

-- Find orphan order_items
select o.id as parent_order_id, oi.id as child_parent_id
from order_items oi left join orders o
on o.id=oi.order_id
where o.id is null;

-- Find duplicate payments for same order
select order_id, count(order_id)
from payments
group by order_id
having count(order_id)>1;