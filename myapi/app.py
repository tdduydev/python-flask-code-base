from flask import Flask
from myapi import news, user, auth, role, tag, category, tagnews, categorynews, tinhthanh, quanhuyen, xaphuong
from myapi import manage
from myapi.extensions import apispec
from myapi.extensions import db
from myapi.extensions import jwt
from myapi.extensions import migrate
from flask_cors import CORS
from flask_seeder import FlaskSeeder




def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("myapi")
    CORS(app)
    app.config.from_object("myapi.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    configure_cli(app)
    configure_apispec(app)
    register_blueprints(app)

    db.init_app(app)

    return app


def configure_extensions(app):
    """Configure flask extensions"""
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    seeder = FlaskSeeder()
    seeder.init_app(app, db)


def configure_cli(app):
    """Configure Flask 2.0's cli for easy entity management"""
    app.cli.add_command(manage.init)


def configure_apispec(app):
    """Configure APISpec for swagger support"""
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    """Register all blueprints for application"""
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(role.views.blueprint)
    app.register_blueprint(news.views.blueprint)
    app.register_blueprint(tag.views.blueprint)
    app.register_blueprint(tagnews.views.blueprint)
    app.register_blueprint(category.views.blueprint)
    app.register_blueprint(categorynews.views.blueprint)
    app.register_blueprint(tinhthanh.views.blueprint)
    app.register_blueprint(quanhuyen.views.blueprint)
    app.register_blueprint(xaphuong.views.blueprint)


    
