from fire import Fire

from .screen import Screen


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

    def download_season(self, season):
        print('Downloading season:', season)
        for episode in range(self.num_episodes[season]):
            self.download_episode(season, episode)

    def download_episode(self, season, episode):
        print('Episode: ', episode)
        for frame in range(1, self.frames_per_episode):
            screen_to_download = Screen(season, episode, frame)
            screen_to_download.download()

    def download_all_episodes(self):
        for season in range(1, max(self.num_episodes.keys()) + 1):
            self.download_season(season)


if __name__ == '__main__':
    Fire(ScreensDownloader)
