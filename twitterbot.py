import tweepy
from dotenv import load_dotenv
from os import path, environ, rename, getcwd

from helpers.screens_manager import ScreensManager


if __name__ == '__main__':
    load_dotenv(path.abspath(path.join(getcwd(), '.env')))
    API_KEY = environ.get('API_KEY')
    API_SECRET = environ.get('API_SECRET')
    OAUTH_TOKEN = environ.get('OAUTH_TOKEN')
    OAUTH_TOKEN_SECRET = environ.get('OAUTH_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    api = tweepy.API(auth)

    sc = ScreensManager()
    image_dir = sc.get_random_image()
    api.update_with_media(image_dir)
    image_name = image_dir.rsplit('/', 1)[-1]
    new_image_dir = path.abspath(
            path.join(
                path.dirname(__file__),
                'public',
                'screens',
                'used',
                image_name))
    rename(image_dir, new_image_dir)

    if path.isfile(path.join(getcwd(), environ.get('USED_SCREENS_FILE'))):
        with open(environ.get('USED_SCREENS_FILE'), 'a') as used_screens:
            used_screens.write(image_name + '\n')
    else:
        sc.make_screens_list()
