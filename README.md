# Order Service

A Flask service that ingests ecommerce orders from a mock API and serves them via REST API.

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Set Flask app (required for migrations):
   Windows:
   `set FLASK_APP=run.py`
   Linux/Mac:
   `export FLASK_APP=run.py`
4. Initialize database: `flask db init && flask db migrate && flask db upgrade`
5. Run the service: `python run.py`
6.  Test API:
   - Windows PowerShell: `iwr -Uri "http://localhost:5000/api/orders?email=demo1@example.com" -UseBasicParsing`
   - Linux/Mac: `curl "http://localhost:5000/api/orders?email=demo1@example.com"`


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
`iwr -Uri "http://localhost:5000/api/customer/test@example.com"`
`curl "http://localhost:5000/api/customer/test@example.com"`

# Get customer orders(email, phone)
`iwr -Uri "http://localhost:5000/api/orders?email=test@example.com"`
`curl"http://localhost:5000/api/orders?email=test@example.com"`

`iwr -Uri  "http://localhost:5000/api/orders?phone=1234567890"`
`curl "http://localhost:5000/api/orders?phone=1234567890"`

