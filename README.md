# Movimentação baseada em detecção facial de DJI Tello Drones

## 1. Bibliotecas

````
opencv-python
djitellopy
````

## 2. _Script_ que irá conter funções de suporte: _utlis.py_

Importam-se as bibliotecas necessárias:

````
from djitellopy import Tello
import cv2
import numpy as np
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

Para realizar a detecção facial, vamos utilizar o Método Viola Jones, que usa um arquivo _Hard Cascade_ para detectar faces. Então, precisamos colocar o arquivo _haarcascade_frontalface_default.xml_ em nosso diretório. Este arquivo está presente no topo desta página para _download_. Adicione a seguinte função ao nosso _utlis.py_ :

````
def findFace(img):
  # Defina a variável que recebe o modelo _Cascade_
  faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

  # Passamos a imagem para o domínio dos tons de cinza
  imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # Encontramos os rostos no frame
  # Os parâmetros de _MultiScale_ são o _scale factor_ e o número mínimo de _neighbors_
  faces = faceCascade.detectMultiScale(imgGray, 1.2, 4)

  # Lista com os centros das faces detectadas, para evitar detecção das múltiplas faces detectadas
  myFaceListC = []

  # Lista com as áreas das _bound boxes_
  myFaceListArea = []

  # Encontre as faces e desenhe as caixas delimitadoras
  # Os parâmetros de cv2.rectangle são: imagem, ponto inicial, ponto final, cor em BGR, em espessura da linha
  for (x,y,w,h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Determine a área e os centros das imagens detectadas
    cx = x + w//2
    cy = y + h//2
    area = w*h
    
    # Adicionamos as áreas e os centros às suas listas
    myFaceListArea.append(area)
    myFaceListC.append([cx, cy])

  # Se existe alguma área na lista de áreas
  if len(myFaceListArea) != 0:

    # Armazena-se o índice do elemento de maior área da lista 
    i = myFaceListArea.index(max(myFaceListArea))
    
    # Retorne a imagem com o maior centro e a maior área das listas
    return img, [myFaceListC[i], myFaceListArea[i]]
  
  # Do contrário, retorne a imagem com valores nulos
  else:
    return img, [[0,0], 0]
  
  # A partir daqui vamos para a função findFaces em FacetrackingTello.py para adicionar a variável "info"
````
A ideia é que se houver mais de um rosto, não queremos detectar todas elas. Deste modo, o rosto mais próximo é aquele que deve ser detectado.

Agora, vamos implementar o PID para suavizar a grande latência dos dados recebidos.

````
def trackFace(myDrone, info, w, pid, pError):
  # Nosso ponto de referência será a metade da largura da imagem, portando o erro é a diferença e      entre o cx detectado e o centro da imagem
  error = info[0][0] - w//2

  # Equação do PID para velocidade: kp*error + kD*(error-pError)
  speed = pid[0]*error + pid[1]*(error-pError)

  # Precisamos garantir que a velocidade não exceda limites determinados. Para isso, podemos           utilizar a função clip do numpy
  speed = np.clip(speed, -100, 100)

  # Checagem de se o centro da detecção existe
  if info[0][0] != 0:

    # Enviamos a velocidade corrigida pelo PID ao yaw
    myDrone.yaw_velocity = speed

  Se não, zeramos as velocidades e os erros
  else:
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    error = 0
````


## 3. _Script_ principal: _FaceTrackingTello.py_

````
# Importa-se tudo que está em utlis.py
from utlis import *
import cv2

# Dimensões da imagem
w,h = 360, 240

# Parâmetros kp, kD e kI do PID
pid = [0.5, 0.5, 0]

# Chamamos a função initializeTello dentro de myDrone
myDrone = initializeTello()

# Conecte-se ao Tello via Wifi e execute o script para checar a conexão

# Loop de recepção de frames que darão origem ao vídeo :

while True:

  # Chamada da função que recebe os frames
  img = telloGetFrame(myDrone, w, h)

  # Chamada da função que detecta as faces
  img, info = findFace(img)

  # Valor x do nosso ponto central (cx) , assim podemos observá-lo e ver como ele se comporta
  print(info[0][0])

  # Visualização da imagem na tela. O primeiro parâmetro é o nome da janela que irá abrir
  cv2.imshow('Image', img)

  # A tecla Q é usada para cessar a missão
  if cv2.waitKey(1) & 0xFF == ord('q'):
    myDrone.land()
    break
````

É necessário importar as imagens do Tello.
