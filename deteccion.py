import numpy as np
import cv2 as cv
import os.path
#from matplotlib import pyplot as plt

# Define variables globales
input_img = np.zeros((480, 640, 3), np.uint8)
metodo = '1'


# Funcion que se ejecuta al mover la barra de deslizamiento
def detectar(x):
    t = cv.getTrackbarPos('Threshold', 'Deteccion de Rasgos')

    # Crea un objeto de acuerdo al metodo seleccionado
    # y llama a la funcion para detectar los rasgos
    if metodo == '1':
        gftt = cv.GFTTDetector_create(0, 0.01, t, 3)
        kp = gftt.detect(input_img, None)
    elif metodo == '2':
        # Crea un objeto tipo FAST
        fast = cv.FastFeatureDetector_create(t)
        # Detecta los rasgos
        kp = fast.detect(input_img, None)
    elif metodo == '3':
        # Crea un objeto tipo AGAST
        agast = cv.AgastFeatureDetector_create(t)
        # Detecta los rasgos
        kp = agast.detect(input_img, None)

    #Los siguientes metodos aun deben ser corroborados
    elif metodo == '4':
        #Crea un objeto tipo star(?)
        star = cv.xfeatures2d.StarDetector_create(t)
        #Detecta los rasgos
        kp = star.detect(input_img, None)
    elif metodo == '5':
        #Crea un objeto tipo ORB
        orb = cv.ORB_create(t)
        #Detecta los ragos
        kp = orb.detect(input_img, None)
    #AKAZE Crashes
    elif metodo == '6':
        akaze = cv.AKAZE_create(t)
        kp = akaze.detect(input_img, None)
    elif metodo == '7':
        brisk = cv.BRISK_create(t)
        kp = brisk.detect(input_img, None)
     #KAZE image doesnt seem to update
    elif metodo == '8':
        kaze = cv.KAZE_create(t)
        kp = kaze.detect(input_img, None)

    #SIFT_y SURF son versiones no gratuitas
    #parece haber un problema al acceder a ellas en PyCharm, el IDE que yo uso.
    elif metodo == '9':
        sift = cv.xfeatures2d.SIFT_create(t)
        kp = sift.detect(cv.cvtColor(input_img, cv.COLOR_BGR2GRAY), None)
    elif metodo == '10':
        surf = cv.xfeatures2d.SURF_create(t)
        kp = surf.detect(cv.cvtColor(input_img, cv.COLOR_BGR2GRAY), None)

    else:
        return

    # Dibuja los rasgos detectados sobre la imagen original
    output_img = cv.drawKeypoints(input_img, kp, None, color=(255, 0, 0))
    cv.imshow('Deteccion de Rasgos', output_img)


# Abre la imagen definida por el usuario
archivo = input('Nombre de la imagen a procesar: ')
while not os.path.isfile(archivo):
    archivo = input('No se encontro el archivo.\nVuelve a teclear el nombre: ')
    pass
input_img = cv.imread(archivo, 0)

# Permite al usuario seleccionar el metodo de deteccion de rasgos
print('\nMetodos de Deteccion de Rasgos:\n(1)GFTT\n(2)FAST\n(3)AGAST\n(4)BRIEF\n(5)ORB\n'
      '(6)AKAZE\n(7)BRISK\n(8)KAZE\n(9)SIFT\n(10)SURF\n')
metodo = input('Selecciona el metodo: ')

# Crea una ventana y muetra la imagen
cv.namedWindow('Deteccion de Rasgos', cv.WINDOW_NORMAL)
cv.createTrackbar('Threshold', 'Deteccion de Rasgos', 10, 100, detectar)
cv.imshow('Deteccion de Rasgos', input_img)

# Ciclo que espera un evento
while (1):
    # Espera la tecla ESC para salir del ciclo
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break

# Destruye la ventana antes de terminar la ejecucion
cv.destroyAllWindows()