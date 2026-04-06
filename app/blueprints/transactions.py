from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.utils.decorators import role_required
from app.services.transaction_service import (
    create_transaction, get_transactions, update_transaction, delete_transaction
)

txn_bp = Blueprint("transactions", __name__)

def to_dict(t):
    return {
        "id": t.id, "amount": t.amount, "type": t.type.value,
        "category": t.category, "date": str(t.date), "notes": t.notes
    }

@txn_bp.route("/", methods=["POST"])
@role_required("analyst", "admin")
def create():
    data = request.get_json()
    if not all(k in data for k in ["amount", "type", "category", "date"]):
        return jsonify({"error": "Missing required fields"}), 400
    if data["amount"] <= 0:
        return jsonify({"error": "Amount must be positive"}), 400
    txn = create_transaction(int(get_jwt_identity()), data)
    return jsonify(to_dict(txn)), 201

@txn_bp.route("/", methods=["GET"])
@role_required("viewer", "analyst", "admin")
def list_all():
    from app.extensions import db
    from app.models.user import User
    filters = {k: request.args.get(k) for k in ["type", "category", "start_date", "end_date"]}
    user = db.session.get(User, int(get_jwt_identity()))
    txns = get_transactions(int(get_jwt_identity()), filters, user.role.value)
    return jsonify([to_dict(t) for t in txns]), 200

@txn_bp.route("/<int:txn_id>", methods=["PUT"])
@role_required("admin")
def update(txn_id):
    txn = update_transaction(txn_id, request.get_json())
    return jsonify(to_dict(txn)), 200

@txn_bp.route("/<int:txn_id>", methods=["DELETE"])
@role_required("admin")
def delete(txn_id):
    delete_transaction(txn_id)
    return jsonify({"message": "Deleted"}), 200