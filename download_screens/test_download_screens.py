import unittest
from .download_screens import get_download_url


class TestGetDownloadUrl(unittest.TestCase):

    def test_get_episode_with_single_digits(self):
        expected = 'https://s3.amazonaws.com/images.springfieldspringfield.co.uk/screencaps/futurama/season1/s01e01/s01e01_1.jpg'
        self.assertEqual(expected, get_download_url(1, 1, 1))

    def test_get_episode_with_double_digits(self):
        expected = 'https://s3.amazonaws.com/images.springfieldspringfield.co.uk/screencaps/futurama/season2/s02e16/s02e16_74.jpg'
        self.assertEqual(expected, get_download_url(2, 16, 74))
