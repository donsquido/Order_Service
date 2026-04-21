# Order Service

A Flask-based backend service that fetches ecommerce orders from an external API, stores them in a normalized SQLite database, and exposes REST APIs to query customer orders.

---

##  Features

* Fetch orders from external API and store in DB
* Normalized database schema (Customer, Order, OrderItem)
* Idempotent ingestion (prevents duplicate orders)
* Query orders by email or phone
* Proper error handling and logging
* Basic unit tests included

---

##  Tech Stack

* Python + Flask
* SQLite (lightweight DB for local/demo use)
* SQLAlchemy (ORM)
* Flask-Migrate (DB migrations)

---

##  Setup

1. Clone the repository:

```
git clone https://github.com/donsquido/Order_Service.git
cd Order_Service
```

2. Create virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Run database migrations:

```
set FLASK_APP=run.py
flask db upgrade
```

5. (Optional) Seed demo data:

```
python seed.py
```

6. Start the server:

```
python run.py
```

---

##  API Endpoints

### Health Check

```
GET /api/health
```

### Ingest Orders (External API → DB)

```
POST /api/ingest-orders
```

### Get Customer Orders (Query Param)

```
GET /api/orders?email=<email>
GET /api/orders?phone=<phone>
```

---

##  Example Usage (Recommended: curl)

### 1. Ingest Orders

```
curl.exe -X POST http://localhost:5000/api/ingest-orders
```

Expected:

```
{"status":"success","processed":1}
```

---

### 2. Idempotency Check (Run Again)

```
curl.exe -X POST http://localhost:5000/api/ingest-orders
```

Expected:

```
{"status":"success","processed":0}
```

Ensures duplicate orders are not inserted.

---

### 3. Fetch Orders (Success Case)

```
curl.exe "http://localhost:5000/api/orders?email=thomas@avantcha.com"
```

---

### 4. Customer Not Found

```
curl.exe "http://localhost:5000/api/orders?email=wrong@example.com"
```

Expected:

```
{"error":"Customer not found"}
```

---

### 5. Missing Query Parameter

```
curl.exe http://localhost:5000/api/orders
```

Expected:

```
{"error":"Email or phone is required"}
```

---

##  Design Decisions

* **SQLite**: Used for simplicity and easy local setup (as per assignment scope)
* **SQLAlchemy ORM**: Cleaner DB interactions and maintainability
* **Normalized Schema**:

  * Customer → Orders → OrderItems
  * Avoids data duplication
* **Idempotency**:

  * Prevents duplicate order insertion using unique `order_id`
* **Retry Logic**:

  * Handles temporary API failures with retries

---

##  Running Tests

Run all unit tests:

```
python -m unittest discover tests
```

Verbose mode:

```
python -m unittest discover tests -v
```

Expected:

```
Ran X tests
OK
```

---

## Notes

* External API used:
  https://mocki.io/v1/32fbc0ab-7bfe-40fa-96c3-d1cadedb5d2a

* Some fields (like customer name) may default to `"Unknown"` if not provided by API.

