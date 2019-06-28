from os import path, rename, environ, pardir
from dotenv import load_dotenv
from urllib.request import urlretrieve

import tweepy


class Screen(object):

    def __init__(self, season, episode, frame):
        self.screens_dir = path.abspath(path.join(
            path.dirname(__file__),
            pardir,
            'public',
            'screens'
        ))
        self.season = season
        self.episode = episode
        self.frame = frame
        self.name = '{}_{}_{}'.format(season, episode, frame)
        self.tweeted = False
        self.dir = path.abspath(path.join(self.screens_dir, self.name))

    def __str__(self):
        return '{}.jpg {}'.format(self.name, self.dir)

    def tweet(self):
        auth = self._get_tweepy_auth()
        twitter = tweepy.API(auth)
        twitter.update_with_media(self.dir)
        self.mark_as_tweeted()

    def _get_tweepy_auth(self):
        load_dotenv()
        auth = tweepy.OAuthHandler(environ.get('API_KEY'), environ.get('API_SECRET'))
        auth.set_access_token(environ.get('OAUTH_TOKEN'), environ.get('OAUTH_TOKEN_SECRET'))
        return auth

    def mark_as_tweeted(self):
        self.tweeted = True
        self.move_to_used_dir()

    def move_to_used_dir(self):
        old_dir = self.dir
        self.dir = path.abspath(path.join(self.screens_dir, 'used', self.name))
        rename(old_dir, self.dir)

    def download(self):
        image_source = self._get_download_url()
        try:
            urlretrieve(image_source, self.dir)
        except Exception as e:
            print(e)
            print('Couldn\'t download screen: {}'.format(self))

    def _get_download_url(self):
        base_url = 'https://s3.amazonaws.com/images.springfieldspringfield.co.uk/screencaps/futurama/'
        if self._episode_is_two_digit_num():
            return self._get_two_digit_episode_url(base_url)
        return self._get_one_digit_episode_url(base_url)

    def _episode_is_two_digit_num(self):
        if self.episode > 9:
            return True
        return False

    def _get_two_digit_episode_url(self, base_url):
        return base_url + 'season{0}/s0{0}e{1}/s0{0}e{1}_{2}.jpg'.format(self.season, self.episode, self.frame)

    def _get_one_digit_episode_url(self, base_url):
        return base_url + 'season{0}/s0{0}e0{1}/s0{0}e0{1}_{2}.jpg'.format(self.season, self.episode, self.frame)
