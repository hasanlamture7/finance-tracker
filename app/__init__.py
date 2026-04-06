from flask import Flask
from .config import Config
from .extensions import db, jwt, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    from .blueprints.auth import auth_bp
    from .blueprints.transactions import txn_bp
    from .blueprints.analytics import analytics_bp

    app.register_blueprint(auth_bp,      url_prefix="/auth")
    app.register_blueprint(txn_bp,       url_prefix="/transactions")
    app.register_blueprint(analytics_bp, url_prefix="/analytics")

    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Not found"}, 404

    @app.errorhandler(403)
    def forbidden(e):
        return {"error": "Forbidden"}, 403

    with app.app_context():
        db.create_all()

    return app