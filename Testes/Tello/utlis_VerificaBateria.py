from djitellopy import Tello
import cv2
import numpy as np
import time

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

  # Sobe 70 cm
  myDrone.takeoff()
  time.sleep(2)
  myDrone.move_up(70)
  time.sleep(3)

  # Retorne nosso objeto:
  return myDrone 

# Os parâmetros da função são myDrone, o comprimento da imagem e sua altura
def telloGetFrame(myDrone, w=360, h=240):
  # Definimos a leitura dos frames da imagem
  myFrame = myDrone.get_frame_read()
  myFrame = myFrame.frame

  # Podemos redefinir o tamanho da imagem
  img = cv2.resize(myFrame, (w,h))

  #Retornamos a imagem
  return img

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

def trackFace(myDrone, info, w, pid, pError):
  # Nosso ponto de referência será a metade da largura da imagem, portando o erro é a diferença e      entre o cx detectado e o centro da imagem
  error = info[0][0] - w//2

  # Equação do PID para velocidade: kp*error + kD*(error-pError)
  speed = pid[0]*error + pid[1]*(error-pError)

  # Precisamos garantir que a velocidade não exceda limites determinados. Para isso, podemos           utilizar a função clip do numpy
  speed = int(np.clip(speed, -100, 100))

  # Visualizando as velocidades
  print(speed)

  # Checagem de se o centro da detecção existe
  if info[0][0] != 0:

    # Enviamos a velocidade corrigida pelo PID ao yaw
    myDrone.yaw_velocity = speed

  # Se não, zeramos as velocidades e os erros
  else:
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    error = 0

  # Agora precisamos enviar as velocidades ao Tello, pois apenas setamos elas
  if myDrone.send_rc_control:
    myDrone.send_rc_control(myDrone.left_right_velocity,
                            myDrone.for_back_velocity,
                            myDrone.up_down_velocity,
                            myDrone.yaw_velocity)

  # Precisamos retornar o erro encontrado, quando ele existe, porque será usado para a próxima         detecção
  return error
