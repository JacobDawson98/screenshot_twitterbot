from random import randint
import cv2
from os import path


def frame_cap():
    public_dir = path.abspath(path.join(path.dirname(__file__), '..', 'public'))
    vidcap = cv2.VideoCapture(path.abspath(path.join(public_dir, 'videos', 'babys_first_script.mp4')))
    num_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    rand_frame = randint(0, num_frames)
    while rand_frame % 24 != 0:
        rand_frame = randint(0, num_frames)
    cap_successful = False
    while not cap_successful:
        cap_successful, image = vidcap.read()
    image_dir = path.abspath(path.join(public_dir, 'screens', 'frame{}.jpg'.format(rand_frame)))
    cv2.imwrite(image_dir, image)
    return image_dir
