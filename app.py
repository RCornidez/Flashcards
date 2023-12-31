from flask import Flask
from flask_cors import CORS
from controllers.flashcardController import flashcard_blueprint
from databaseContext import get_db, get_collection
import os


def create_app():
    app = Flask(__name__, template_folder='views')
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Determine the configuration to use based on an environment variable
    config_type = os.getenv('FLASK_ENV', 'development')  # Defaults to 'development' if not set

    if config_type == 'development':
        app.config.from_object('config.DevelopmentConfig')
    elif config_type == 'testing':
        app.config.from_object('config.TestingConfig')
    elif config_type == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        # Default to development if unknown config_type
        app.config.from_object('config.DevelopmentConfig')

    # Initialize database context
    db = get_db(app.config["MONGO_URI"], app.config["DB_NAME"])
    app.config['db'] = db  # Store db in app config for access in routes

    # Register blueprints
    app.register_blueprint(flashcard_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'])
