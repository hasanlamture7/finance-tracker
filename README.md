# Finance Tracker API

A Python Flask-based finance tracking system that allows users to manage and analyze their financial records. The system supports role-based access control, transaction management, and analytics.

---

## Tech Stack

- **Framework:** Flask
- **Database:** SQLite (via Flask-SQLAlchemy)
- **Authentication:** JWT (Flask-JWT-Extended)
- **Password Hashing:** Bcrypt (Flask-Bcrypt)
- **Language:** Python 3

---

## Project Structure

```
finance_tracker/
├── app/
│   ├── __init__.py          # App factory (create_app)
│   ├── config.py            # Configuration settings
│   ├── extensions.py        # db, jwt, bcrypt instances
│   ├── models/
│   │   ├── user.py          # User model with roles
│   │   └── transaction.py   # Transaction model
│   ├── blueprints/
│   │   ├── auth.py          # Register and login routes
│   │   ├── transactions.py  # Transaction CRUD routes
│   │   └── analytics.py     # Analytics and summary routes
│   ├── services/
│   │   ├── transaction_service.py   # Transaction business logic
│   │   └── analytics_service.py     # Analytics business logic
│   └── utils/
│       └── decorators.py    # Role-based access decorator
├── run.py                   # Entry point
├── .env                     # Environment variables
└── requirements.txt
```

---

## Setup Instructions

### 1. Clone or download the project

```bash
cd finance_tracker
```

### 2. Create and activate a virtual environment

```bash
# Create
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the .env file

Create a `.env` file in the root folder with the following:

```
DATABASE_URL=sqlite:///finance.db
JWT_SECRET_KEY=******
```

### 5. Run the server

```bash
python run.py
```

The server will start at `http://127.0.0.1:5000`

---

## Roles

| Role     | Permissions                                              |
|----------|----------------------------------------------------------|
| viewer   | View transactions and summary                            |
| analyst  | View transactions, filters, and detailed analytics       |
| admin    | Full access — create, update, delete transactions        |

---

## API Endpoints

### Auth

| Method | Endpoint         | Description        | Auth Required |
|--------|------------------|--------------------|---------------|
| POST   | /auth/register   | Register a user    | No            |
| POST   | /auth/login      | Login and get JWT  | No            |

### Transactions

| Method | Endpoint                  | Description               | Roles Allowed         |
|--------|---------------------------|---------------------------|-----------------------|
| POST   | /transactions/            | Create a transaction      | analyst, admin        |
| GET    | /transactions/            | List all transactions     | viewer, analyst, admin|
| PUT    | /transactions/<id>        | Update a transaction      | admin                 |
| DELETE | /transactions/<id>        | Delete a transaction      | admin                 |

#### Filter transactions using query params:
```
GET /transactions/?type=income
GET /transactions/?category=salary
GET /transactions/?start_date=2026-01-01&end_date=2026-04-30
```

### Analytics

| Method | Endpoint                  | Description                    | Roles Allowed         |
|--------|---------------------------|--------------------------------|-----------------------|
| GET    | /analytics/summary        | Total income, expenses, balance| viewer, analyst, admin|
| GET    | /analytics/by-category    | Breakdown by category          | analyst, admin        |
| GET    | /analytics/monthly        | Monthly income and expenses    | analyst, admin        |

---

## Testing the API

Use [Postman](https://www.postman.com/downloads/) to test the endpoints.

### Step 1 — Register an admin user

**POST** `http://127.0.0.1:5000/auth/register`

```json
{
  "email": "admin@test.com",
  "password": "pass123",
  "role": "admin"
}
```

### Step 2 — Login to get a token

**POST** `http://127.0.0.1:5000/auth/login`

```json
{
  "email": "admin@test.com",
  "password": "pass123"
}
```

Copy the token from the response.

### Step 3 — Add the token to requests

In Postman, go to the **Authorization** tab, select **Bearer Token**, and paste your token.

### Step 4 — Create a transaction

**POST** `http://127.0.0.1:5000/transactions/`

```json
{
  "amount": 5000,
  "type": "income",
  "category": "salary",
  "date": "2026-04-01",
  "notes": "April salary"
}
```

### Step 5 — Get all transactions

**GET** `http://127.0.0.1:5000/transactions/`

### Step 6 — Get analytics summary

**GET** `http://127.0.0.1:5000/analytics/summary`

Response:
```json
{
  "total_income": 5000.0,
  "total_expenses": 200.0,
  "balance": 4800.0
}
```

---

## Role Testing

### Register a viewer

**POST** `http://127.0.0.1:5000/auth/register`

```json
{
  "email": "viewer@test.com",
  "password": "pass123",
  "role": "viewer"
}
```

### Viewer tries to create a transaction — blocked

**POST** `http://127.0.0.1:5000/transactions/` with viewer token

```json
{
  "error": "Access denied"
}
```

### Viewer views transactions — allowed

**GET** `http://127.0.0.1:5000/transactions/` with viewer token — returns all transactions.

---

## Assumptions

- Each transaction belongs to the user who created it.
- All roles can view all transactions (shared finance system).
- Only admin can update or delete transactions.
- Analyst and admin can create transactions and access detailed analytics.
- Viewer can only view transactions and the summary.
- JWT tokens are valid for 24 hours.
- No multi-currency support — all amounts are in a single currency.
- SQLite is used for simplicity. Can be swapped for PostgreSQL by changing `DATABASE_URL` in `.env`.

---

## Error Responses

| Status Code | Meaning                        |
|-------------|--------------------------------|
| 400         | Missing or invalid input       |
| 401         | Missing or expired token       |
| 403         | Access denied (wrong role)     |
| 404         | Resource not found             |
| 409         | Email already exists           |

---

## Sample Data

To quickly populate the database with sample data, register an admin and create a few transactions using the endpoints above, or add a seed script to `run.py`.
