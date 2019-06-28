from random import randint
from mock import patch
import unittest

from helpers.download_screens import ScreensDownloader


class TestScreensDownloader(unittest.TestCase):

    def setUp(self):
        self.base_url = 'https://s3.amazonaws.com/images.springfieldspringfield.co.uk/screencaps/futurama/season'
        self.sd = ScreensDownloader()

    @patch('helpers.screen.urlretrieve')
    @patch('helpers.download_screens.ScreensDownloader.download_episode')
    def test_download_season_calls_correct_amount_num_episodes(self, download_episode, urlretrieve):
        season = randint(1, max(self.sd.num_episodes.keys()))
        self.sd.download_season(season)
        self.assertEqual(self.sd.num_episodes[season], download_episode.call_count)

    @patch('helpers.screen.urlretrieve')
    def test_do_not_use_unavailable_season(self, urlretrieve):
        with self.assertRaises(KeyError):
            self.sd.download_season(max(self.sd.num_episodes.keys()) + randint(1, 100))

    @patch('helpers.download_screens.ScreensDownloader.download_season')
    @patch('helpers.screen.urlretrieve')
    def test_download_all_episodes_calls_all_seasons(self, urlretrieve, download_season):
        self.sd.download_all_episodes()
        self.assertEqual(max(self.sd.num_episodes.keys()), download_season.call_count)

    @patch('helpers.screen.urlretrieve')
    def test_download_all_episodes_downloads_all_episodes(self, urlretrieve):
        self.sd.download_all_episodes()
        self.assertEqual(sum(self.sd.num_episodes.values()) * (self.sd.frames_per_episode - 1), urlretrieve.call_count)
