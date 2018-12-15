from os import path
from urllib.request import urlretrieve


episode = 1
public_dir = path.abspath(path.join(path.dirname(__file__), 'public'))
while episode < 10:
    for index in range(1, 292):
        url = 'https://s3.amazonaws.com/images.springfieldspringfield.co.uk/screencaps/futurama/season1/s01e0{}/s01e0{}_{}.jpg\n'.format(episode, episode, index)
        screens_dir = path.abspath(path.join(public_dir, 'screens', '{}_{}_{}.jpg'.format(1, episode, index)))
        try:
            urlretrieve(url, screens_dir)
        except Exception as e:
            print(e)
            print('failed on {}'.format(url))
    episode += 1
