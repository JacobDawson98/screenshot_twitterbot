from fire import Fire
from os import path
from urllib.request import urlretrieve


class ScreensDownloader(object):

    def __init__(self):
        self.num_episodes = {
                1: 9,
                2: 20,
                3: 15,
                4: 12,
                5: 16,
                6: 26,
                7: 26
        }
        self.frames_per_episode = 292

    def get_download_url(self, season, episode, frame):
        """
        Assumes valid season, episode, and frame number. Returns formatted url
        for downloading a specific image
        """
        base_url = 'https://s3.amazonaws.com/images.springfieldspringfield.co.uk/screencaps/futurama/'
        if episode > 9:
            return base_url + 'season{0}/s0{0}e{1}/s0{0}e{1}_{2}.jpg'.format(season, episode, frame)
        return base_url + 'season{0}/s0{0}e0{1}/s0{0}e0{1}_{2}.jpg'.format(season, episode, frame)

    def download_season(self, season):
        print('Downloading season:', season)
        for episode in range(self.num_episodes[season]):
            self.download_episode(season, episode)

    def download_episode(self, season, episode):
        print('Episode: ', episode)
        for frame in range(1, self.frames_per_episode):
            screens_dir = path.abspath(path.join(
                path.dirname(__file__),
                '..',
                'public',
                'screens', '{}_{}_{}.jpg'.format(season, episode, frame)))
            try:
                url = self.get_download_url(season, episode, frame)
                urlretrieve(url, screens_dir)
            except Exception as e:
                print(e)
                print('Couldn\'t download from: {}'.format(url))

    def download_all_episodes(self):
        for season in range(1, max(self.num_episodes.keys()) + 1):
            self.download_season(season)


if __name__ == '__main__':
    Fire(ScreensDownloader)
