from os import path
from urllib.request import urlretrieve
from datetime import datetime


def get_download_url(season, episode, frame):
    """
    Assumes valid season, episode, and frame number. Returns formatted url
    for downloading a specific image
    """
    base_url = 'https://s3.amazonaws.com/images.springfieldspringfield.co.uk/screencaps/futurama/'
    if episode > 9:
        extension = 'season{0}/s0{0}e{1}/s0{0}e{1}_{2}.jpg'.format(season, episode, frame)
    else:
        extension = 'season{0}/s0{0}e0{1}/s0{0}e0{1}_{2}.jpg'.format(season, episode, frame)
    return base_url + extension


if __name__ == '__main__':
    # Used for interesting print statement after all screenshots are downloaded
    time_initial = int(datetime.now().strftime('%s'))
    num_downloaded = 0

    num_episodes = {
            1: 9,
            2: 20,
            3: 15,
            4: 12,
            5: 16,
            6: 26,
            7: 26
        }
    episode = season = 1
    while season <= 7:
        print('Downloading season ' + str(season))
        while episode <= num_episodes[season]:
            print('Episode: ' + str(episode))
            for frame in range(1, 292):
                screens_dir = path.abspath(path.join(
                    path.dirname(__file__),
                    '..',
                    'public',
                    'screens', '{}_{}_{}.jpg'.format(season, episode, frame)))
                try:
                    url = get_download_url(season, episode, frame)
                    urlretrieve(url, screens_dir)
                    num_downloaded += 1
                except Exception as e:
                    print(e)
                    print('Couldn\'t download from: {}'.format(url))
            episode += 1
        episode = 1  # start from episode one in the next season
        season += 1
    time_final = (int(datetime.now().strftime(('%s'))) - time_initial) / 60
    if time_final > 60:
        print('Total time it took to download {} screenshots was {} hours'.format(num_downloaded, time_final/60))
    else:
        print('Total time it took to download {} screenshots was {} minutes'.format(num_downloaded, time_final))
