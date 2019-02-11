from mock import patch
import unittest
from shutil import rmtree
from os import path, listdir, unlink, makedirs
from collections import Counter

from helpers.screens_manager import ScreensManager


class ScreensManagerTests(unittest.TestCase):

    def setUp(self):
        self.project_dir = path.abspath(path.join(path.dirname(__file__), '..'))
        self.screens_dir = path.abspath(path.join(self.project_dir, 'screens'))
        self.used_dir = path.abspath(path.join(self.screens_dir, 'used'))
        makedirs(self.used_dir)
        self.used_screens_file = path.abspath(path.join(path.dirname(path.realpath(__file__)), 'used_screens.txt'))
        self.sc = ScreensManager(self.screens_dir)

    def tearDown(self):
        rmtree(self.screens_dir)
        try:
            unlink(self.used_screens_file)
        except FileNotFoundError:
            pass

    def create_num_files(self, directory, num_files):
        for num in range(num_files):
            with open(path.join(directory, str(num) + '.txt'), 'w'):
                pass

    @patch('builtins.open')
    def test_make_screens_list_opens_specified_dir(self, file_open):
        test_file_dir = path.abspath(path.join(self.project_dir, 'test.txt'))
        self.sc.make_screens_list(test_file_dir)
        file_open.assert_called_with(test_file_dir, 'a')

    def test_list_consists_of_files_in_used_dir(self):
        self.create_num_files(self.used_dir, 3)
        self.sc.make_screens_list(self.used_screens_file)
        actual = []
        with open(self.used_screens_file, 'r') as used_screens:
            lines = [l.strip() for l in used_screens.readlines()]
            for image_name in lines:
                actual.append(image_name)
        self.assertEqual(Counter(['0.txt', '1.txt', '2.txt']), Counter(actual))

    def test_screens_dir_syncs_with_list(self):
        with open(self.used_screens_file, 'a') as used_screens:
            for num in range(3):
                used_screens.write(str(num) + '.txt\n')
        self.create_num_files(self.screens_dir, 3)
        self.sc.update_screens_dir(self.used_screens_file)
        actual = []
        for used_screen in listdir(self.used_dir):
            actual.append(used_screen)
        self.assertEqual(Counter(['0.txt', '1.txt', '2.txt']), Counter(actual))

    def test_can_get_random_image(self):
        self.create_num_files(self.screens_dir, 3)
        with open(self.used_screens_file, 'w'):
            pass
        actual = self.sc.get_random_image()
        possible_images = [self.screens_dir + '/0.txt', self.screens_dir + '/1.txt', self.screens_dir + '/2.txt']
        self.assertTrue(actual in possible_images)
