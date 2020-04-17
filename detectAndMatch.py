import numpy as np
import cv2 as cv
import os.path

# Funcion de deteccion
# Se ejecuta al mover la barra de deslizamiento
def detectar(x):
    t = cv.getTrackbarPos('Threshold', 'Deteccion de Rasgos')

    # Crea un objeto de acuerdo al metodo seleccionado
    # y llama a la funcion para detectar los rasgos
    if metodo == '1':
        # Crea un objeto "Good Features to Track"
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
    elif metodo == '4':
        #Crea un objeto tipo star(?) / BRIEF
        star = cv.xfeatures2d.StarDetector_create(t)
        #Detecta los rasgos
        kp = star.detect(input_img, None)
    elif metodo == '5':
        #Crea un objeto tipo ORB
        orb = cv.ORB_create(t)
        #Detecta los ragos
        kp = orb.detect(input_img, None)
    elif metodo == '6':
        # Crea un objeto tipo AKAZE, la funcion requiere valores mas bajos de t
        akaze = cv.AKAZE_create(threshold=0.001*t)
        kp = akaze.detect(input_img, None)
        print(t)
    elif metodo == '7':
        # Crea un objeto tipo BRISK
        brisk = cv.BRISK_create(t)
        kp = brisk.detect(input_img, None)
    elif metodo == '8':
        # Crea un objeto tipo KAZE, la funcion requiere valores mas bajos de t
        kaze = cv.KAZE_create(threshold=0.001*t)
        kp = kaze.detect(input_img, None)
    elif metodo == '9':
        # Crea un objeto tipo SIFT
        sift = cv.xfeatures2d.SIFT_create(t)
        kp = sift.detect(input_img, None)
    elif metodo == '10':
        # Crea un objeto tipo SURF
        surf = cv.xfeatures2d.SURF_create(t)
        kp = surf.detect(input_img, None)

    else:
        return

    # Dibuja los rasgos detectados sobre la imagen original
    output_img = cv.drawKeypoints(input_img, kp, None, color=(255, 0, 0))
    cv.imshow('Deteccion de Rasgos', output_img)

#Funcion de emparejamiento
def matching(t):
    # SIFT
    if detectMethod == '1':
        detector = cv.xfeatures2d.SIFT_create()
    # SURF
    elif detectMethod == '2':
        detector = cv.xfeatures2d.SURF_create()
    # KAZE
    elif detectMethod == '3':
        detector = cv.KAZE_create()
    # BRIEF
    elif detectMethod == '4':
        # Se crea un detector "star" para keypoints
        # y un detector "brief" para descriptores
        star = cv.xfeatures2d.StarDetector_create()
        detector = cv.xfeatures2d.BriefDescriptorExtractor_create()
    # BRISK
    elif detectMethod == '5':
        detector = cv.BRISK_create()
    # ORB
    elif detectMethod == '6':
        detector = cv.ORB_create()
    # AKAZE
    elif detectMethod == '7':
        detector = cv.AKAZE_create()
    else:
        return

    # Si se emplea BRIEF, se realizan las operaciones de deteccion
    # y computacion por separado, pues BRIEF no posee metodo .detectAndCompute
    if detectMethod != '4':
        # Si no se usa BRIEF
        kp1, desc1 = detector.detectAndCompute(img1, None)
        kp2, desc2 = detector.detectAndCompute(img2, None)
    else:
        # Si se usa BRIEF:
        # Se detectan los rasgos con star
        kp1 = star.detect(img1, None)
        kp2 = star.detect(img1, None)
        #Se obtienen los descriptores con BRIEF
        kp1, desc1 = detector.compute(img1, kp1)
        kp2, desc2 = detector.compute(img2, kp2)

    # Si se usa emparejamiento por fuerza bruta
    if matchMethod == '1':
        # Si se usa un descriptor con punto flotante, se usa distancia entre
        # descriptores de norma L2
        if int(detectMethod) <= 3:
            matcher = cv.BFMatcher(cv.NORM_L2, crossCheck=False)
        # Si se usa un descriptor binario, se usa distancia de hamming
        else:
            matcher = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=False)

    # Si se usa emparejamiento por FLANN
    elif matchMethod == '2':
        # Si se usa descriptor de punto flotante, se usan KD-trees con 5 arboles
        if int(detectMethod) <= 3:
            FLANN_INDEX_KDTREE = 0
            index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            search_params = dict(checks=50)
            matcher = cv.FlannBasedMatcher(index_params, search_params)

        # Si se usa un descriptor binario, se usa LSH
        else:
            FLANN_INDEX_LSH = 6
            index_params = dict(algorithm=FLANN_INDEX_LSH, table_number=6,
                                key_size=12, multi_probe_level=1)
            search_params = dict(checks=50)
            matcher = cv.FlannBasedMatcher(index_params, search_params)
    else:
        return
    # Deteccion de los k vecinos mas cercanos
    matches = matcher.knnMatch(desc1, desc2, k=2, mask=None)

    # Filtrado de emparejamientos
    good_matches = []
    for m, n in matches:
        if m.distance < t * n.distance:
            good_matches.append(m)


    # Se dibujan los emparejamientos en la imagen por medio de drawMatches
    img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1], 3), dtype= np.uint8 )
    cv.drawMatches(img1, kp1, img2, kp2, good_matches, img_matches,
                   flags = cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    cv.imshow('Emparejamiento de Rasgos', img_matches)

# Solicita al usuario la seleccion de un modo de funcionamiento
print('Este programa permite realizar las siguientes tareas:'
      '\n(1) Deteccion de rasgos\n(2) Emparejamiento de rasgos\n')
modo = input('Ingrese la tarea a realizar: ')

while (modo != '1' and modo != '2'):
    print('Entrada no valida.\n')
    modo = input('¿Que tarea desea realizar?\n')
    pass

# Deteccion de rasgos
if modo =='1':
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

# Emparejamiento de rasgos
elif modo == '2':
    # Entrada de imagen de referencia
    archivo = input('Nombre de la imagen de referencia: \n')
    while not os.path.isfile(archivo):
        archivo = input('No se encontro el archivo.\nVuelve a teclear el nombre: ')
        pass
    img1 = cv.imread(archivo, 0)

    # Entrada de imagen a emparejar
    archivo = input('Nombre de la imagen a emparejar: ')
    while not os.path.isfile(archivo):
        archivo = input('No se encontro el archivo.\nVuelve a teclear el nombre: ')
        pass
    img2 = cv.imread(archivo, 0)

    # Seleccion del metodo de deteccion de rasgos
    print('\nMetodos de Deteccion de Rasgos\nDescriptores de punto flotante:\n'
          '(1)SIFT\n(2)SURF\n(3)KAZE\n'
          'Descriptores binarios:\n(4)BRIEF\n(5)BRISK\n(6)ORB\n(7)AKAZE\n')
    detectMethod = input('Seleccione el metodo: ')

    # Selecciion del metodo de emparejamiento
    print('Metodos de emparejamiento:\n (1) Fuerza Bruta\n (2) FLANN\n')
    matchMethod = input('Seleccione el metodo: ')

    # Se llama a la funcion matching con un threshold default de 0.7
    matching(0.7)

    # Ciclo que espera un evento
    while (1):
        # Espera la tecla ESC para salir del ciclo
        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break
else:
    print('\nSi este mensaje es mostrado al usuario, algo no funciono correctamente.\n')

# Destruye la ventana antes de terminar la ejecucion
cv.destroyAllWindows()
