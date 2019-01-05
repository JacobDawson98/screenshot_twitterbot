import tweepy
from dotenv import load_dotenv
from os import path, environ, rename, listdir
from random import choice

from sync_screens import create_used_screens_list


def get_random_image_dir():
    screens_dir = path.abspath(path.join(path.dirname(__file__), 'public', 'screens'))
    random_file = choice([f for f in listdir(screens_dir) if path.isfile(path.join(screens_dir, f))])
    return path.abspath(path.join(screens_dir, random_file))


def _append_used_screen(image_name):
    with open('used_screens.txt', 'a') as used_screens:
        used_screens.write(image_name + '\n')


load_dotenv(path.abspath(path.join(path.dirname(__file__), '.env')))
API_KEY = environ.get('API_KEY')
API_SECRET = environ.get('API_SECRET')
OAUTH_TOKEN = environ.get('OAUTH_TOKEN')
OAUTH_TOKEN_SECRET = environ.get('OAUTH_TOKEN_SECRET')

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth)

image_dir = get_random_image_dir()
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

try:
    _append_used_screen(image_name)
except FileNotFoundError:
    create_used_screens_list()
    _append_used_screen(image_name)
