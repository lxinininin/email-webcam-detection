# pip install opencv-python
import cv2
import time
import glob
from emailing import send_email

video = cv2.VideoCapture(0)  # 0 means using the main camera
time.sleep(1)

first_frame = None
status_list = []
count = 1

while True:
    status = 0
    check, frame = video.read()

    # convert frame to gray frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray_frame_gau will be the grayscale image gray_frame
    # after applying the Gaussian blur with the specified kernel size.
    # This operation is often used to reduce noise and detail in images.
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    # compare the difference between two frames
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # 60 is the threshold value.
    # Pixels with intensity values greater than or equal to 60 will be set to the maximum value (255 in this case),
    # while pixels with intensity values below 60 will be set to 0.
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # detect contours
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # if it is a small object, which means it is perhaps a fake object (maybe is a light difference and so on)
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        # this will draw the rectangle around the original frame
        # (x, y) is the coordinate of left-up corner, (x+w, y+h) is the coordinate of right-down corner
        # (o, 255, 0) is the color of the rectangle, which is pure green
        # 3 is the width
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1

            # store the image
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)  # get the middle image
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]  # last 2 elements

    # the object just exit from the frame
    if status_list[0] == 1 and status_list[1] == 0:
        send_email()

    cv2.imshow("My video", frame)

    # this creates key object basically
    key = cv2.waitKey(1)
    # if user press the q key, we will break the video
    if key == ord("q"):
        break

video.release()