-- Get all customers sorted by name ascending

select * from customers order by NAME asc;

-- Get all customers

select count(*) from customers;

-- Get only customer names

select name from customers;

-- Get customers with id greater than 2

select * from customers where id > 2;

-- Get customers whose name starts with 'A'

select * from customers where name like 'A%';

-- Get first 3 customers
select * from customers limit 3;

-- Get next 3 customers using offset (pagination)
select * from customers offset 3 limit 3;

-- Get orders with status 'completed'
select * from orders where status = 'completed';

-- Get orders with total amount greater than 100
select * from orders where total_amount > 100;

-- Get all orders sorted by total amount highest first
select * from orders order by total_amount desc;

-- Get latest 5 orders
select * from orders order by created_at desc limit 5;

-- Get all products with price between 50 and 200
select * from products where price between 50 and 200 order by price;

-- Get all order items where quantity is greater than or equal to 2
select * from order_items where quantity >=2;