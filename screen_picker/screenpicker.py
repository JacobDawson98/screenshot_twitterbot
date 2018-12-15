from random import randint
import cv2

vidcap = cv2.VideoCapture('babys_first_script.mp4')
num_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
rand_frame = randint(0, num_frames)
while rand_frame % 24 != 0:
    rand_frame = randint(0, num_frames)
success,image = vidcap.read()
cv2.imwrite("frame%d.jpg" % rand_frame, image)
print('Read a new frame: ', success)
print(rand_frame)
