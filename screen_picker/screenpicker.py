from random import randint
import cv2
from os import path

def frame_cap():
    #video_directory = '../public/video'
    base_dir = path.dirname(__file__)
    videos_dir = path.abspath(path.join(base_dir, '..', 'public', 'videos', 'babys_first_script.mp4'))
    print(videos_dir)
    vidcap = cv2.VideoCapture(videos_dir)
    num_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    rand_frame = randint(0, num_frames)
    while rand_frame % 24 != 0:
        rand_frame = randint(0, num_frames)
    success,image = vidcap.read()
    screens_path = path.abspath(path.join(base_dir, '..', 'public', 'screens'))
    print('bigfoot')
    cv2.imwrite(path.join(screens_path, "frame%d.jpg" % rand_frame), image)
    print('Read a new frame: ', success)
    print(rand_frame)

frame_cap()
