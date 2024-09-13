from flask import Flask
from routes import bp
import logging
from generate_preview_image import generate_preview_image

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Add a secret key for session management
logging.basicConfig(level=logging.DEBUG)

# Generate the preview image when the server starts
generate_preview_image()

# Register the blueprint
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
