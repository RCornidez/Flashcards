# config.py

class Config:
    """Base configuration."""
    # Common configurations (e.g., logging)

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    MONGO_URI = "mongodb://localhost:27017/dev_db"
    DB_NAME = "dev_db"

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    MONGO_URI = "mongodb://localhost:27017/test_db"
    DB_NAME = "test_db"

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    MONGO_URI = "mongodb://localhost:27017/prod_db" 
    DB_NAME = "prod_db"
