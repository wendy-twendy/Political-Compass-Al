from flask import Flask
from routes import bp

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Add a secret key for session management

# Register the blueprint
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
