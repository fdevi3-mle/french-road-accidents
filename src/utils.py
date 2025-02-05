##Constants & FILEPATHS
import logging
import os
import random

from PIL.Image import Image
from PIL.ImageDraw import ImageDraw

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__)) ## src
ROOT_PATH = os.path.dirname(CURRENT_PATH)
LOG_PATH = os.path.join(ROOT_PATH, 'logs')



def generate_random_image(filepath=LOG_PATH):
    width, height = 256, 256
    random_value = random.randint(0, 255)

    img = Image.new('RGB', (width, height), color='white')
    d = ImageDraw.Draw(img)
    d.text((10, 10), f"Random Value: {random_value}", fill=(0, 0, 0))
    filename = 'random.png'
    filepath = os.path.join(LOG_PATH, filename)
    img.save(filepath)
    print(filepath)

    return random_value, filepath


## Lets test the normal logger instead of the zenml one
def generate_logger(logpath=LOG_PATH):
    os.makedirs(logpath,exist_ok=True)
    logger = logging.getLogger(__name__)
    print(logpath)
    filename= 'test-logger.abc'
    filepath = os.path.join(logpath, filename)
    logging.basicConfig(filename=filepath, encoding='utf-8', level=logging.DEBUG)
    print(filepath)
    logger.info("Hi")
    logger.warning("Whatsasasdasd")
