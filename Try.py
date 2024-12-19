from PIL import Image, ImageTk 


def load_image(file_path, width, height):
    """Load and resize an image."""
    image = Image.open(file_path)  # Open the image
    image = image.resize((width, height))  # Resize to specified dimensions
    return image.save(file_path) 


load_image(file_path = "pause_button.png", width=16, height=16)