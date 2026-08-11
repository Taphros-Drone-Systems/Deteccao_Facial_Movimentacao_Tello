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

Definimos uma função que recebe as imagens captadas pela câmera do Tello:

````
# Os parâmetros da função são myDrone, o comprimento da imagem e sua altura
def telloGetFrame(myDrone, w=360, h=240):
  # Definimos a leitura dos frames da imagem
  myFrame = myDrone.get_frame_read()
  myFrame = myFrame.frame

  # Podemos redefinir o tamanho da imagem
  img = cv2.resize(myFrame, (w,h))

  #Retornamos a imagem
  return img
````

Para realizar a detecção facial, vamos utilizar o Método Viola Jones, que usa um arquivo _hard cascade_ para detectar faces. Então, precisamos colocar o arquivo _haarcascade_frontalface_default.xml_ em nosso diretório. Este arquivo está presente no topo desta página para _download_.

## 3. Script principal: FaceTrackingTello.py

````
# Importa-se tudo que está em utlis.py
from utlis import *
import cv2

# Dimensões da imagem
w,h = 360, 240

# Chamamos a função initializeTello dentro de myDrone
myDrone = initializeTello()

# Conecte-se ao Tello via Wifi e execute o script para checar a conexão

# Loop de recepção de frames que darão origem ao vídeo :
while True:
  # Chamada da função que recebe os frames
  img = telloGetFrame(myDrone, w, h)

  # Visualização da imagem na tela. O primeiro parâmetro é o nome da janela que irá abrir
  cv2.imshow('Image', img)
...
````

É necessário importar as imagens do Tello.
