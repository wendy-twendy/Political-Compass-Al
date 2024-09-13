from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Add a secret key for session management

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/{}'.format(
    os.environ['PGUSER'],
    os.environ['PGPASSWORD'],
    os.environ['PGHOST'],
    os.environ['PGPORT'],
    os.environ['PGDATABASE']
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()

def create_app():
    from routes import bp
    app.register_blueprint(bp)
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000, debug=True)
