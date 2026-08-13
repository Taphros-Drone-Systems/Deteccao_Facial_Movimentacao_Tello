from djitellopy import Tello
import cv2

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
  
  # A partir daqui vamos para a função _findFaces_ para adicionar a variável _info_