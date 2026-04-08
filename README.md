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

6. Run the service: `python run.py`

7.  Test API:
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

