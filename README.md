# Order + Payment Simulation API (QA Project)

## Goal
Build and test a backend system that simulates order creation and payment processing, focusing on API validation, database consistency, and backend QA practices.

## Scope
The system will include:

- Customers -> who is buying
- Products -> what is being sold
- Orders -> what customer order
- Order_items
- Payments -> how order was paid

Relationsips:

1 customer -> Many orders
1 order -> Many order items
2 product -> Can appear on many orders_items
1 order -> 1 payment

Core flow:
1. Create customer
2. Create product
3. Create order
4. Process payment
5. Update order status

## Out of Scope

- Authentication / login
- UI / frontend
- Real payment gateway
- Complex business rules

## QA Focus

- API testing (positive and negative cases)
- Request/response validation
- Database validation using SQL
- Data integrity checks between API and DB
- Basic performance testing using JMeter
- CI execution using GitHub Actions

## Tech Stack

- FastAPI
- PostgreSQL
- Docker Compose
- Pytest
- JMeter
- GitHub Actions

## Data Model

### Customers
Stores customer details.

### Products
Stores product catalog details.

### Orders
Stores order header details such as customer, status, and total amount.

### Order Items
Stores products linked to an order, including quantity and item price.

### Payments
Stores payment details linked to an order, including amount and payment status.