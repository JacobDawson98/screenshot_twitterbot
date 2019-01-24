import tweepy
from dotenv import load_dotenv
from os import path, environ, rename

from helpers.screens_manager import ScreensManager


if __name__ == '__main__':
    load_dotenv(path.abspath(path.join(path.dirname(__file__), '.env')))
    auth = tweepy.OAuthHandler(environ.get('API_KEY'), environ.get('API_SECRET'))
    auth.set_access_token(environ.get('OAUTH_TOKEN'), environ.get('OATUH_TOKEN_SECRET'))

    sm = ScreensManager()
    image_dir = sm.get_random_image()
    tweepy.API(auth).update_with_media(image_dir)
    image_name = image_dir.rsplit('/', 1)[-1]
    new_image_dir = path.abspath(
            path.join(
                path.dirname(__file__),
                'public',
                'screens',
                'used',
                image_name))
    rename(image_dir, new_image_dir)

    if path.isfile(path.join(path.dirname(__file__), environ.get('USED_SCREENS_FILE'))):
        with open(environ.get('USED_SCREENS_FILE'), 'a') as used_screens:
            used_screens.write(image_name + '\n')
    else:
        sm.make_screens_list()
