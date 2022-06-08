import cv2
import imutils
import numpy
import os
from imutils.video import FPS
from imutils.video import WebcamVideoStream
from datetime import datetime
from mailgun import mail
import pin_control
import whatsapp

EMAIL = ""

whatsapp.thing.setCallback(whatsapp.handleResponse)
whatsapp.thing.daemon = True
whatsapp.thing.start()


def run():
    COUNT_TRIES = 60
    nam = ''
    count = 20

    cv2.namedWindow('Image')

    while True:
        im = webcam.read()
        im = imutils.resize(im, width=400)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            # Try to recognize the face
            prediction = model.predict(face_resize)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)

            if count >= 0 and count < COUNT_TRIES:
                if prediction[1] < 72:

                    nam = names[prediction[0]]
                    count += 1

                    cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 3)
                    cv2.putText(im, '%s - %.0f' % (names[prediction[0]], prediction[1]), (x - 10, y - 10),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

                    print('Face recognized: ' + str(names[prediction[0]]) + ' - ' + str(
                        prediction[1]) + '%' + ' | attempt: ' + str(count))
                else:
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    print('Face not recognized | attempt:', count)
                    cv2.putText(im, 'not recognized', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                    count -= 1
            elif count >= COUNT_TRIES:
                cv2.imwrite('face_img.jpg', im)
                print("Face Successfully Recognized:", nam, '| Opening Gate & Sending Email.. | ', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                pin_control.open_gate()
                fps.stop()
                mail(EMAIL, "Alert", "Face of " + nam + " Recognized at: " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
                cv2.waitKey(6000)
                pin_control.close_date()
                return
            elif count < 0:
                cv2.imwrite('face_img.jpg', im)
                print("Failed to recognize the face.. Sending email.. | ", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                fps.stop()
                mail(EMAIL, "Alert", "Failed to recognize the face at: " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
                cv2.waitKey(6000)
                return

        cv2.imshow('Image', im)
        key = cv2.waitKey(10)
        if key == 27:
            fps.stop()
            break
        fps.update()


haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'

print('Training...')
# Create a list of images and a list of corresponding names
(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id += 1
(width, height) = (130, 100)

# Create a Numpy array from the two lists above
(images, labels) = [numpy.array(lis) for lis in [images, labels]]

model = cv2.face.LBPHFaceRecognizer_create()
model.train(images, labels)

face_cascade = cv2.CascadeClassifier(haar_file)
webcam = WebcamVideoStream(src=0).start()
fps = FPS().start()

while True:
    run()
