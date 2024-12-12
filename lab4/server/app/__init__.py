from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from server.config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import routers
        app.register_blueprint(routers.bp)

        # Імпортуємо schema тут, після ініціалізації db
        from server.app.graphql_schema import schema
        from flask_graphql import GraphQLView

        # Реєструємо GraphQL endpoint
        app.add_url_rule(
            '/graphql',
            view_func=GraphQLView.as_view(
                'graphql',
                schema=schema,
                graphiql=True
            )
        )

    return app
