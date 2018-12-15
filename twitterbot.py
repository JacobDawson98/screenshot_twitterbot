import tweepy
from dotenv import load_dotenv
from os import path, environ, rename
from screen_picker.screenpicker import get_random_image_dir

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
new_image_dir = path.abspath(
        path.join(
            path.dirname(__file__),
            'public',
            'screens',
            'used',
            image_dir.rsplit('/', 1)[-1]))
rename(image_dir, new_image_dir)
