from os import path, environ, rename
from requests import post

import tweepy
from dotenv import load_dotenv

from helpers.screens_manager import ScreensManager


if __name__ == '__main__':
    load_dotenv(path.abspath(path.join(path.dirname(__file__), '.env')))
    auth = tweepy.OAuthHandler(environ.get('API_KEY'), environ.get('API_SECRET'))
    auth.set_access_token(environ.get('OAUTH_TOKEN'), environ.get('OAUTH_TOKEN_SECRET'))

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

    pastebin_dev_key = environ.get('PASTEBIN_KEY')
    pastebin_user_key = environ.get('PASTEBIN_USER_KEY')
    if pastebin_dev_key and pastebin_user_key:
        pastebin_url = 'https://pastebin.com/api/api_post.php'
        data = {'api_dev_key': pastebin_dev_key, 'api_user_key': pastebin_user_key,
                'api_option': 'paste', 'api_paste_name': 'used_screens.txt',
                'api_paste_expire_date ': 'N'}
        with open(environ.get('USED_SCREENS_FILE'), 'r') as used_screens:
            data.update({'api_paste_code': used_screens.read()})
        post(pastebin_url, data=data)
