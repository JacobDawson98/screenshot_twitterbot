from contextlib import contextmanager
from mock import patch
from io import StringIO
import sys
import unittest
import urllib

from helpers.download_screens import ScreensDownloader


class TestScreensDownloader(unittest.TestCase):

    def setUp(self):
        self.base_url = 'https://s3.amazonaws.com/images.springfieldspringfield.co.uk/screencaps/futurama/season'
        self.sd = ScreensDownloader()

    @contextmanager
    def captured_output(self):
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    def test_get_episode_with_single_digits(self):
        expected = self.base_url + '1/s01e01/s01e01_1.jpg'
        self.assertEqual(expected, self.sd.get_download_url(1, 1, 1))

    def test_get_episode_with_double_digits(self):
        expected = self.base_url + '2/s02e16/s02e16_74.jpg'
        self.assertEqual(expected, self.sd.get_download_url(2, 16, 74))

    @patch('helpers.download_screens.ScreensDownloader.get_download_url')
    @patch('helpers.download_screens.urlretrieve')
    def test_download_episodes_calls_for_all_frames(self, urlretrieve, get_download_url):
        urlretrieve.return_value = 'oi'
        self.sd.download_episode(1, 1)
        self.assertEqual(291, urlretrieve.call_count)
        self.assertEqual(291, get_download_url.call_count)

    @patch('helpers.download_screens.urlretrieve')
    def test_download_episodes_handles_exception(self, urlretrieve):
        urlretrieve.side_effect = urllib.error.HTTPError
        with self.captured_output() as (out, err):
            self.sd.download_episode(1, 1)
        output = out.getvalue().strip().splitlines()
        self.assertEqual('Couldn\'t download from: {}'.format(self.sd.get_download_url(1, 1, 291)),
                         output[len(output) - 1])
