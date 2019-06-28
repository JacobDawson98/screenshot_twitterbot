import unittest
from os import pardir, environ
from os.path import abspath, join, dirname
from mock import patch

from helpers.screen import Screen


environ_return_value = {
    'API_KEY': 'key',
    'API_SECRET': 'secret',
    'OAUTH_TOKEN': 'token',
    'OAUTH_TOKEN_SECRET': 'token secret'
}


class TestScreen(unittest.TestCase):

    def setUp(self):
        self.season = 1
        self.episode = 2
        self.frame = 3
        self.instance = Screen(self.season, self.episode, self.frame)
        self.screens_dir = abspath(join(dirname(__file__), pardir, 'public', 'screens'))
        self.environ = environ_return_value

    def test_name_is_set_on_creation(self):
        self.assertEqual('{}_{}_{}'.format(self.season, self.episode, self.frame), self.instance.name)

    def test_tweeted_is_set_to_false_on_initialization(self):
        self.assertEqual(False, self.instance.tweeted)

    def test_dir_is_set_to_non_used_dir_on_initialization(self):
        self.assertEqual(self.screens_dir, self.instance.screens_dir)
        self.assertEqual(
            join(
                self.instance.screens_dir,
                self.instance.name
            ), self.instance.dir)

    def test_to_string_method(self):
        self.assertEqual('{}.jpg {}'.format(self.instance.name, self.instance.dir), self.instance.__str__())

    @patch('helpers.screen.rename')
    def test_move_to_used_dir_moves_screen_to_used_dir(self, rename):
        non_used_dir = self.instance.dir
        self.instance.move_to_used_dir()
        rename.assert_called_with(non_used_dir, join(self.screens_dir, 'used', self.instance.name))

    @patch('helpers.screen.Screen.move_to_used_dir')
    def test_marking_screen_as_tweeted_sets_tweeted_to_true(self, move_to_used_dir):
        self.assertFalse(self.instance.tweeted)
        self.instance.mark_as_tweeted()
        self.assertTrue(self.instance.tweeted)
        move_to_used_dir.assert_called_once()

    @patch('helpers.screen.tweepy.OAuthHandler')
    @patch.dict(environ, environ_return_value)
    def test_get_tweepy_auth_creates_auth(self, OAuthHandler):
        self.instance._get_tweepy_auth()
        OAuthHandler.assert_called_with(environ_return_value['API_KEY'], environ_return_value['API_SECRET'])

    @patch('helpers.screen.tweepy.OAuthHandler.set_access_token')
    @patch.dict(environ, environ_return_value)
    def test_get_tweepy_auth_sets_access_token(self, set_access_token):
        self.instance._get_tweepy_auth()
        set_access_token.assert_called_with(
            environ_return_value['OAUTH_TOKEN'],
            environ_return_value['OAUTH_TOKEN_SECRET']
        )

    @patch.dict(environ, environ_return_value)
    def test_get_tweepy_auth_returns_auth(self):
        instance = self.instance._get_tweepy_auth()
        self.assertEqual(environ_return_value['API_KEY'], instance.consumer_key.decode('utf-8'))
        self.assertEqual(environ_return_value['API_SECRET'], instance.consumer_secret.decode('utf-8'))
        self.assertEqual(environ_return_value['OAUTH_TOKEN'], instance.access_token)
        self.assertEqual(environ_return_value['OAUTH_TOKEN_SECRET'], instance.access_token_secret)

    @patch('helpers.screen.Screen._get_tweepy_auth')
    @patch('helpers.screen.Screen.mark_as_tweeted')
    @patch('helpers.screen.tweepy.API')
    def test_tweet_gets_tweepy_auth_and_moves_screen_dir(self, _get_tweepy_auth, mark_as_tweeted, tweepy_api):
        self.instance.tweet()
        _get_tweepy_auth.assert_called_once()
        mark_as_tweeted.assert_called_once()
        tweepy_api.assert_called_once()

    def test_get_download_url_returns_correct_url_for_single_digit_episode(self):
        actual = self.instance._get_download_url()
        base_url = 'https://s3.amazonaws.com/images.springfieldspringfield.co.uk/screencaps/futurama/'
        expected = base_url + 'season{0}/s0{0}e0{1}/s0{0}e0{1}_{2}.jpg'.format(self.season, self.episode, self.frame)
        self.assertEqual(expected, actual)

    def test_get_download_url_returns_correct_url_for_two_digit_episode(self):
        season = 1
        episode = 10
        frame = 2
        instance = Screen(season, episode, frame)
        actual = instance._get_download_url()
        base_url = 'https://s3.amazonaws.com/images.springfieldspringfield.co.uk/screencaps/futurama/'
        expected = base_url + 'season{0}/s0{0}e{1}/s0{0}e{1}_{2}.jpg'.format(season, episode, frame)
        self.assertEqual(expected, actual)

    @patch('helpers.screen.urlretrieve')
    def test_download_calls_urlretrieve_on_download_url_and_instance_dir(self, urlretrieve):
        self.instance.download()
        urlretrieve.assert_called_with(self.instance._get_download_url(), self.instance.dir)
