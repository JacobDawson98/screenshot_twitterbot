from os import path
from urllib.request import urlretrieve


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
public_dir = path.abspath(path.join(path.dirname(__file__), 'public'))
base_url = 'https://s3.amazonaws.com/images.springfieldspringfield.co.uk/screencaps/futurama/'
while season < 8:
    while episode <= num_episodes[season]:
        for index in range(1, 292):
            if episode > 9:
                url = base_url + 'season{}/s0{}e{}/s0{}e{}_{}.jpg'.format(
                        season, season, episode, season, episode, index)
            else:
                url = base_url + 'season{}/s0{}e0{}/s0{}e0{}_{}.jpg'.format(
                        season, season, episode, season, episode, index)
            screens_dir = path.abspath(path.join(public_dir, 'screens', '{}_{}_{}.jpg'.format(season, episode, index)))
            try:
                urlretrieve(url, screens_dir)
            except Exception as e:
                print(e)
                print('failed on {}'.format(url))
        episode += 1
    season += 1
