from random import choice
from os import path, listdir


def get_random_image_dir():
    screens_dir = path.abspath(path.join(path.dirname(__file__), '..', 'public', 'screens'))
    random_file = choice([f for f in listdir(screens_dir) if path.isfile(path.join(screens_dir, f))])
    return path.abspath(path.join(screens_dir, random_file))
