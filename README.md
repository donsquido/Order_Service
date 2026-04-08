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

## API Endpoints

- `POST /api/ingest-orders` - Fetch and store orders from external API
- `GET /api/customer/{email|phone}` - Get customer orders (404 if not found)
- `GET /api/health` - Health check

### Additional Endpoint (Query आधारित)
- `GET /api/orders?email=<email>`  
- `GET /api/orders?phone=<phone>`  
Fetch orders using query parameters (as per assignment requirement)

---

## Example Usage

```bash
# Ingest orders
iwr -Uri "http://localhost:5000/api/ingest-orders" -Method POST


# Get customer orders (path param)
iwr -Uri "http://localhost:5000/api/customer/test@example.com"

# Get customer orders (query param - recommended)
iwr -Uri "http://localhost:5000/api/orders?email=test@example.com"

iwr -Uri  "http://localhost:5000/api/orders?phone=1234567890"
