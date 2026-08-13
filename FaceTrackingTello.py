# Importa-se tudo que está em utlis.py
from utlis import *
import cv2
w,h = 360, 240
myDrone = initializeTello()
while True:
    img = telloGetFrame(myDrone, w, h)
    img = findFace(img)
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
    break