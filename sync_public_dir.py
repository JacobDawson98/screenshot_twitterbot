from os import path, listdir, rename


screens_dir = path.abspath(path.join(path.dirname(__file__), 'public', 'screens'))
used_dir = path.abspath(path.join(screens_dir, 'used'))
used_screens_file = 'used_screens.txt'


def create_used_screens_list():
    with open(used_screens_file, 'a') as used_screens:
        for f in listdir(used_dir):
            if path.isfile(path.join(used_dir, f)):
                used_screens.write(f + '\n')


def update_screens_dir(used_screens_list):
    with open(used_screens_file, 'a') as used_screens:
        lines = [l.strip() for l in used_screens.readlines()]
        for image_name in lines:
            image_dir = path.join(screens_dir, image_name)
            if path.isfile(image_dir):
                new_image_dir = path.abspath(
                        path.join(
                            path.dirname(__file__),
                            'public',
                            'screens',
                            'used',
                            image_dir.rsplit('/', 1)[-1]))
                rename(image_dir, new_image_dir)


create_used_screens_list()
