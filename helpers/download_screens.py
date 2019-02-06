from fire import Fire
from os import path
from urllib.request import urlretrieve
from datetime import datetime


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
        self.num_downloaded = 0

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
        episode = 1
        while episode <= self.num_episodes[season]:
            print('Episode: ', episode)
            self.download_episode(season, episode)
            episode += 1

    def download_episode(self, season, episode):
        print('Episode: ', episode)
        for frame in range(1, 292):
            screens_dir = path.abspath(path.join(
                path.dirname(__file__),
                '..',
                'public',
                'screens', '{}_{}_{}.jpg'.format(season, episode, frame)))
            try:
                url = self.get_download_url(season, episode, frame)
                urlretrieve(url, screens_dir)
                self.num_downloaded += 1
            except Exception as e:
                print(e)
                print('Couldn\'t download from: {}'.format(url))

    def download_all_episodes(self):
        time_initial = int(datetime.now().strftime('%s'))
        season = 1
        while season <= 7:
            self.download_season(season)
            season += 1
        time_final = (int(datetime.now().strftime(('%s'))) - time_initial) / 60
        if time_final > 60:
            print('Total time it took to download {} screenshots was {} hours'.format(
                self.num_downloaded, time_final/60))
        else:
            print('Total time it took to download {} screenshots was {} minutes'.format(
                self.num_downloaded, time_final))


if __name__ == '__main__':
    Fire(ScreensDownloader)
