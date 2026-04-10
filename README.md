# Order Service

A Flask service that ingests ecommerce orders from a mock API and serves them via REST API.

## Setup
1. Clone the repo:
   git clone https://github.com/donsquido/Order_Service.git
   cd Order_Service

2. Create and activate virtual environment:
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate # Linux/Mac
  
3. Install dependencies: `pip install -r requirements.txt`

4. Set Flask app (required for migrations):
   Windows:
   `set FLASK_APP=run.py`
   Linux/Mac:
   `export FLASK_APP=run.py`

5. Initialize database:  
   Run the following command to apply existing migrations and create tables:  
   `flask db upgrade`  

   OR  

   If you want to make changes to the models (e.g., add new fields or tables) then run:  
   `flask db init`      # only once, if migrations folder does not exist  
   `flask db migrate`   # generates migration scripts based on model changes  
   `flask db upgrade`   # apply the new migrations  

---

## Database Access and Verification

The application uses a SQLite database (`order.db`) located in the `instance/` folder.  
You can directly open and inspect this file using any SQLite viewer (e.g., DB Browser for SQLite).

### Option A: View Database via SQLite CLI

If you don’t want to run Python code in the terminal to check data, you can directly inspect the database file after seeding:

1. Run migrations and seed data:
   ```bash
   ```flask db upgrade```
   ```python seed.py```

   Navigate to the instance folder:

   ```cd instance```
   Open the database using SQLite CLI (make sure SQLite is installed on your system):

  ``` sqlite3 order.db```

  Inside SQLite prompt, you can run commands like:

  sql
  .tables
  SELECT * FROM customer;
  SELECT * FROM "order";
  SELECT * FROM order_item;
OR

flask shell
Then run:

from app.models import Customer, Order, OrderItem
for c in Customer.query.all():
    print(c.id, c.name)

for o in Order.query.all():
    print(o.id, o.customer_id, o.total_amount)

for i in OrderItem.query.all():
    print(i.id, i.order_id, i.product_name, i.quantity)
# This will display the database data accordingly just for overview



6. Run the service: `python run.py`

7.  Test API:
   - Windows PowerShell: `iwr -Uri "http://localhost:5000/api/orders?email=demo1@example.com" -UseBasicParsing`
   - Linux/Mac: `curl "http://localhost:5000/api/orders?email=demo1@example.com"`

## Running Tests

This project includes basic unit tests for order creation, retry logic, idempotency, and error logging.

To run all tests:

``` For Windows:
python -m unittest discover tests 

Expected output:
Success and failure cases for order creation.
Retry logic.
Idempotency and Error Logging stub.
``` 

All tests should complete with OK.
## API Endpoints

- `POST /api/ingest-orders` - Fetch and store orders from external API
- `GET /api/customer/{email|phone}` - Get customer orders (404 if not found)
- `GET /api/health` - Health check

---

## Example Commands

---For Windows use `"iwr -Uri"` & For Linux/Mac use `"curl"`
# Ingest orders
`iwr -Uri "http://localhost:5000/api/ingest-orders"`
`curl "http://localhost:5000/api/ingest-orders"`

# Get customer orders (path param)
`iwr -Uri "http://localhost:5000/api/customer/demo1@example.com"`
`curl "http://localhost:5000/api/customer/demo1@example.com"`

# Get customer orders(email, phone)
`iwr -Uri "http://localhost:5000/api/orders?email=demo2@example.com"`
`curl"http://localhost:5000/api/orders?email=demo2@example.com"`

`iwr -Uri  "http://localhost:5000/api/orders?phone=1111111111"`
`curl "http://localhost:5000/api/orders?phone=1111111111"`

