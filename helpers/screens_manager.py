from fire import Fire
from os import path, listdir, rename, environ


class ScreensManager(object):

    def __init__(self, screens_dir):
        # load_dotenv()
        self.screens_dir = screens_dir
        # if not screens_dir:
        #     self.screens_dir = path.abspath(path.join(path.dirname(__file__), pardir, 'public', 'screens'))
        self.used_dir = path.abspath(path.join(self.screens_dir, 'used'))
        self.project_dir = path.abspath(path.join(path.dirname(__file__), '..'))
        # if environ.get('USED_SCREENS_FILE'):
        #     self.default_file = path.abspath(path.join(self.project_dir, environ.get('USED_SCREENS_FILE')))
        self.used_screens = path.abspath(path.join(self.project_dir, environ.get('USED_SCREENS_FILE')))

    def make_screens_list(self):
        with open(self.used_screens, 'a') as used_screens:
            for f in listdir(self.used_dir):
                if path.isfile(path.join(self.used_dir, f)):
                    used_screens.write(f + '\n')

    def update_screens_dir(self):
        with open(self.used_screens) as used_screens:
            lines = [l.strip() for l in used_screens.readlines()]
            for image_name in lines:
                image_dir = path.join(self.screens_dir, image_name)
                if path.isfile(image_dir):
                    new_image_dir = path.abspath(path.join(self.used_dir, image_dir.rsplit('/', 1)[-1]))
                    rename(image_dir, new_image_dir)

    # def get_random_image_dir(self):
    #     random_file = choice([f for f in listdir(self.screens_dir) if path.isfile(path.join(self.screens_dir, f))])
    #     return path.abspath(path.join(self.screens_dir, random_file))

    # def get_new_used_location(self, image_name):
    #     return self.used_dir + '/' + image_name


if __name__ == '__main__':
    Fire(ScreensManager)
