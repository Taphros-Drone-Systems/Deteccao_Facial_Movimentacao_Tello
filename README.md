# Movimentação baseada em detecção facial de DJI Tello Drones
## 1. Bibliotecas
````
opencv-python
djitellopy
````
## 2. Script principal: FaceTrackingTello.py
Importa-se tudo que está em utlis.py:
````
from utlis import *
import cv2
````
É necessário importar as imagens do Tello.

## 3. Script que irá conter funções de suporte: utlis.py
Importam-se as bibliotecas necessárias:
````
from djitellopy import Tello
import cv2
````

Criamos uma função para inicializar e nos comunicarmos com o Tello:
````
def initializeTello():
  # Dê um nome ao seu Tello e associe-o ao objeto "Tello":
  myDrone = Tello()
````
