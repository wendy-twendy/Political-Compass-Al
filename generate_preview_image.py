from PIL import Image, ImageDraw, ImageFont
import os

def generate_preview_image():
    # Create a new image with a white background
    img = Image.new('RGB', (800, 800), color='white')
    draw = ImageDraw.Draw(img)

    # Draw the axes
    draw.line((400, 0, 400, 800), fill='black', width=2)
    draw.line((0, 400, 800, 400), fill='black', width=2)

    # Add quadrants with colors
    quadrants = [
        {"name": "Authoritarian Left", "bbox": (0, 0, 400, 400), "color": "#ff7575"},
        {"name": "Authoritarian Right", "bbox": (400, 0, 800, 400), "color": "#42aaff"},
        {"name": "Libertarian Left", "bbox": (0, 400, 400, 800), "color": "#9aed97"},
        {"name": "Libertarian Right", "bbox": (400, 400, 800, 800), "color": "#c09aec"}
    ]

    for quadrant in quadrants:
        draw.rectangle(quadrant["bbox"], fill=quadrant["color"])

    # Re-draw the axes on top of the quadrants
    draw.line((400, 0, 400, 800), fill='black', width=2)
    draw.line((0, 400, 800, 400), fill='black', width=2)

    # Add labels
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    draw.text((350, 20), "Authoritarian", fill='black', font=font)
    draw.text((350, 750), "Libertarian", fill='black', font=font)
    draw.text((20, 380), "Left", fill='black', font=font)
    draw.text((700, 380), "Right", fill='black', font=font)

    # Add title
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    draw.text((200, 50), "Political Compass Quiz", fill='black', font=title_font)

    # Ensure the static/images directory exists
    os.makedirs('static/images', exist_ok=True)

    # Save the image
    img.save('static/images/political_compass_preview.png')

if __name__ == "__main__":
    generate_preview_image()
