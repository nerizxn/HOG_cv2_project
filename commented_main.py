import numpy
import cv2
from paho.mqtt.publish import single

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
key = -1
detected = 0
print('Программа для охраны частной территории.')

while key == -1:
    isRead, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    boxes, weights = hog.detectMultiScale(image, winStride=(8, 8))
    boxes = numpy.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    if len(boxes) != 0:
        detected += 1
    if detected == 1:
        single('security/main',
               payload='На территории постороний человек',
               hostname='mqtt.pi40.ru',
               port=1883,
               client_id='main_pc',
               auth={'username':'security','password':'T3HIBn'})
        detected = 2
    for (x_1, y_1, x_2, y_2) in boxes:
        cv2.rectangle(image, (x_1, y_1), (x_2, y_2), (255, 255, 255), 2)
    cv2.imshow('window', image)
    key = cv2.waitKey(20)
cap.release()
print(f'\n{detected} раз(а) был зафиксирован подозрительный объект.')
