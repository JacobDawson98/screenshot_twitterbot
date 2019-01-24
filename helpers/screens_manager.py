from fire import Fire
from dotenv import load_dotenv
from os import path, listdir, rename, environ, pardir
from random import choice


class ScreensManager(object):

    def __init__(self, screens_dir=None):
        load_dotenv(path.abspath(path.join(path.dirname(__file__), '.env')))
        self.screens_dir = screens_dir
        if not screens_dir:
            self.screens_dir = path.abspath(path.join(path.dirname(__file__), pardir, 'public', 'screens'))
        self.used_dir = path.abspath(path.join(self.screens_dir, 'used'))
        self.default_file = environ.get('USED_SCREENS_FILE')

    def make_screens_list(self, used_screens_file=None):
        with open(used_screens_file if used_screens_file else self.default_file, 'a') as used_screens:
            for f in listdir(self.used_dir):
                if path.isfile(path.join(self.used_dir, f)):
                    used_screens.write(f + '\n')

    def update_screens_dir(self, used_screens_file=None, screens_dir=None):
        with open(used_screens_file if used_screens_file else self.default_file) as used_screens:
            lines = [l.strip() for l in used_screens.readlines()]
            for image_name in lines:
                image_dir = path.join(self.screens_dir, image_name)
                if path.isfile(image_dir):
                    new_image_dir = path.abspath(path.join(self.used_dir, image_dir.rsplit('/', 1)[-1]))
                    rename(image_dir, new_image_dir)

    def get_random_image(self):
        random_file = choice([f for f in listdir(self.screens_dir) if path.isfile(path.join(self.screens_dir, f))])
        return path.abspath(path.join(self.screens_dir, random_file))


if __name__ == '__main__':
    Fire(ScreensManager)
