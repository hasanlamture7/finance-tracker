from datetime import datetime
from app.extensions import db
from app.models.transaction import Transaction

def create_transaction(user_id, data):
    txn = Transaction(
        user_id  = user_id,
        amount   = data["amount"],
        type     = data["type"],
        category = data["category"],
        date     = datetime.strptime(data["date"], "%Y-%m-%d").date(),
        notes    = data.get("notes", "")
    )
    db.session.add(txn)
    db.session.commit()
    return txn

def get_transactions(user_id, filters, role):
    q = Transaction.query
    if filters.get("type"):
        q = q.filter_by(type=filters["type"])
    if filters.get("category"):
        q = q.filter_by(category=filters["category"])
    if filters.get("start_date"):
        q = q.filter(Transaction.date >= filters["start_date"])
    if filters.get("end_date"):
        q = q.filter(Transaction.date <= filters["end_date"])
    return q.order_by(Transaction.date.desc()).all()

def update_transaction(txn_id, data):
    txn = Transaction.query.get_or_404(txn_id)
    for field in ["amount", "type", "category", "notes"]:
        if field in data:
            setattr(txn, field, data[field])
    if "date" in data:
        txn.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    db.session.commit()
    return txn

def delete_transaction(txn_id):
    txn = Transaction.query.get_or_404(txn_id)
    db.session.delete(txn)
    db.session.commit()