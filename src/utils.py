##Constants & FILEPATHS
import logging
import os
import random

from PIL import Image, ImageDraw

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__)) ## src
ROOT_PATH = os.path.dirname(CURRENT_PATH)
LOG_PATH = os.path.join(ROOT_PATH, 'logs')


def generate_random_image(filepath=LOG_PATH):
    """
    Generate a random image with a random number displayed on it.

    Args:
        filepath (str, optional): Path where the image will be saved. Defaults to None.
    """
    # Set default path if not provided
    if filepath is None:
        filepath = os.path.join('logs', 'random.png')

    try:
        # Create image
        width, height = 256, 256
        random_value = random.randint(0, 255)

        # Create white image
        img = Image.new('RGB', (width, height), color='white')
        d = ImageDraw.Draw(img)

        # Add text with better positioning
        text = f"Random Value: {random_value}"
        text_bbox = d.textbbox((0, 0), text)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2

        # Draw centered text
        d.text((x, y), text, fill=(0, 0, 0))



        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        filepath = os.path.join(LOG_PATH, 'random.png')
        # Save image
        img.save(filepath)
        print(f"Image saved to: {filepath}")

    except Exception as e:
        print(f"Error generating image: {str(e)}")

## Lets test the normal logger instead of the zenml one
def generate_logger(logpath=LOG_PATH):
    os.makedirs(logpath,exist_ok=True)
    logger = logging.getLogger(__name__)
    print(logpath)
    filename= 'test-logger.log'
    filepath = os.path.join(logpath, filename)
    logging.basicConfig(filename=filepath, encoding='utf-8', level=logging.DEBUG)
    print(filepath)
    logger.info("Hi")
    logger.warning("Whatsasasdasd")
