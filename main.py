from app import create_app
from generate_preview_image import generate_preview_image

app = create_app()

# Generate the preview image when the server starts
generate_preview_image()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
