import unittest
from helpers.download_screens import get_download_url


class TestGetDownloadUrl(unittest.TestCase):

    def setUp(self):
        self.base_url = 'https://s3.amazonaws.com/images.springfieldspringfield.co.uk/screencaps/futurama/season'

    def test_get_episode_with_single_digits(self):
        expected = self.base_url + '1/s01e01/s01e01_1.jpg'
        self.assertEqual(expected, get_download_url(1, 1, 1))

    def test_get_episode_with_double_digits(self):
        expected = self.base_url + '2/s02e16/s02e16_74.jpg'
        self.assertEqual(expected, get_download_url(2, 16, 74))
