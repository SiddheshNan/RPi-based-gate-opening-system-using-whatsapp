import json
import numpy
import os
import shutil
import string
import sys
import time

from cv2 import cv2

haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'  #All the faces data will be present this folder
sub_data = sys.argv[1]    #This will creater folders in datasets with the face of people, so change it's name everytime for the new person.

def start_training(count):
    (width, height) = (130, 100)  # defining the size of images

    face_cascade = cv2.CascadeClassifier(haar_file)
    webcam = cv2.VideoCapture(0)  # '0' is use for my webcam, if you've any other camera attached use '1' like this
    # The program loops until it has 30 images of the face.
    cv2.namedWindow('Image')
    cv2.resizeWindow('Image', 720, 480)
    #count = 0
    while True:
        (_, im) = webcam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            cv2.imwrite('%s/%s.png' % (path, count), face_resize)
        count += 1

        cv2.putText(im, 'Wait 15 sec, then press ESC', (25, 25), cv2.FONT_HERSHEY_SIMPLEX , 0.77, (0, 0, 255) , 2, cv2.LINE_AA)
        cv2.imshow('Image', im)
        key = cv2.waitKey(150)
        if key == 27:
            webcam.release()
            cv2.destroyWindow('Image')
            cv2.destroyAllWindows()
            cv2.waitKey(0)
            break


path = os.path.join(datasets, sub_data)

if not os.path.isdir(path):
    os.mkdir(path)
    start_training(0)

else:
    num = []
    for file in os.listdir(path):
        if file.endswith(".png"):
            num.append(int(file.split(".")[0]))
    start_training(max(num)+1)
