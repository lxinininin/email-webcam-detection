# pip install opencv-python
import cv2
import time

video = cv2.VideoCapture(0)  # 0 means using the main camera
time.sleep(1)

while True:
    check, frame = video.read()
    cv2.imshow("My video", frame)

    # this creates key object basically
    key = cv2.waitKey(1)
    # if user press the q key, we will break the video
    if key == ord("q"):
        break

video.release()