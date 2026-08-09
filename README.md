# Movimentação baseada em detecção facial de DJI Tello Drones
## 1. Bibliotecas
````
opencv-python
djitellopy
````

## 2. Script que irá conter funções de suporte: utlis.py
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

  # Conecte-se ao drone
  myDrone.connect()

  # Estabeleça todas as velocidades iguais a zero: frente/trás, esquerda/direita, para cima/para baixo e yaw.
  # Controlaremos apenas o yaw.
  myDrone.for_back_velocity = 0
  myDrone.left_right_velocity = 0
  myDrone.up_down_velocity = 0
  myDrone.yaw_velocity = 0

  #Temos também a velocidade geral do drone:
  myDrone.speed = 0

  # Vamos mostrar a carga da bateria
  print(myDrone.get_battery())

  # Vamos solicitar que streamings antigos que podem não ter sido desligados anteriormente sejam desligados agora:
  myDrone.streamoff()

  # Iniciamos um novo streaming de vídeo
  myDrone.streamon()

  # Retorne nosso objeto:
  return myDrone 
````

## 3. Script principal: FaceTrackingTello.py
````
# Importa-se tudo que está em utlis.py
from utlis import *
import cv2

# Chamamos a função initializeTello dentro de myDrone
myDrone = initializeTello()

````
É necessário importar as imagens do Tello.
