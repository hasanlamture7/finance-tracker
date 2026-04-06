from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity
from app.utils.decorators import role_required
from app.services.analytics_service import get_summary, get_category_breakdown, get_monthly_totals

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/summary", methods=["GET"])
@role_required("viewer", "analyst", "admin")
def summary():
    return jsonify(get_summary(int(get_jwt_identity()))), 200

@analytics_bp.route("/by-category", methods=["GET"])
@role_required("analyst", "admin")
def by_category():
    return jsonify(get_category_breakdown(int(get_jwt_identity()))), 200

@analytics_bp.route("/monthly", methods=["GET"])
@role_required("analyst", "admin")
def monthly():
    return jsonify(get_monthly_totals(int(get_jwt_identity()))), 200