import numpy
import cv2
from paho.mqtt.publish import single

# 6-7 - инициализируем детектор человека
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
# берем изображение с камеры
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
key = -1  # переменная, отвечающая за закрытие окна при нажатии на клавишу
detected = 0  # переменная, которая считает сколько кадров было с человеком
print('Программа для охраны частной территории.')

while key == -1:
    isRead, image = cap.read()  # берет изображение
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # переводит в оттенки серого для быстрого распознования
    boxes, weights = hog.detectMultiScale(image, winStride=(8, 8))  # распознает человека
    boxes = numpy.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])  # определяет границы рамки человека
    if len(boxes) != 0:
        detected += 1  # считает количество кадров, где был человек
    if detected == 1:  # на первое определение человека срабатывает отправка сообщения на сервер
        single('security/main',
               payload='На территории постороний человек',
               hostname='mqtt.pi40.ru',
               port=1883,
               client_id='main_pc',
               auth={'username':'security','password':'T3HIBn'})
        detected = 2  # сделано для того, чтобы сообщение отправилось только один раз
    for (x_1, y_1, x_2, y_2) in boxes:
        cv2.rectangle(image, (x_1, y_1), (x_2, y_2), (255, 255, 255), 2)  # рисует рамку вокруг человека
    cv2.imshow('window', image)  # показывает окно
    key = cv2.waitKey(20)  # проверяет нажатие кнопки
cap.release()
print(f'\n{detected} раз(а) был зафиксирован подозрительный объект.')
