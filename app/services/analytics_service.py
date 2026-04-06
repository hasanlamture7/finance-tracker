from sqlalchemy import func
from app.extensions import db
from app.models.transaction import Transaction, TypeEnum

def get_summary(user_id):
    def total(ttype):
        result = db.session.query(func.sum(Transaction.amount))\
            .filter_by(user_id=user_id, type=ttype).scalar()
        return round(result or 0.0, 2)
    income   = total(TypeEnum.income)
    expenses = total(TypeEnum.expense)
    return {"total_income": income, "total_expenses": expenses, "balance": round(income - expenses, 2)}

def get_category_breakdown(user_id):
    rows = db.session.query(
        Transaction.category, Transaction.type,
        func.sum(Transaction.amount).label("total")
    ).filter_by(user_id=user_id).group_by(Transaction.category, Transaction.type).all()
    return [{"category": r.category, "type": r.type.value, "total": round(r.total, 2)} for r in rows]

def get_monthly_totals(user_id):
    rows = db.session.query(
        func.strftime("%Y-%m", Transaction.date).label("month"),
        Transaction.type,
        func.sum(Transaction.amount).label("total")
    ).filter_by(user_id=user_id).group_by("month", Transaction.type).order_by("month").all()
    return [{"month": r.month, "type": r.type.value, "total": round(r.total, 2)} for r in rows]