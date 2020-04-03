# Falta corroborar el correcto funcionamiento de los metodos
# Tambien falta implementar LSH

import numpy as np
import cv2 as cv
import os.path

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
        detector = cv.xfeatures2d.StarDetector_create()
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
    kp1, desc1 = detector.detectAndCompute(img1, None)
    kp2, desc2 = detector.detectAndCompute(img2, None)

    if matchMethod == '1':
        if int(detectMethod) <= 3:
            #matcher = cv.DescriptorMatcher_BRUTEFORCE_L1
            matcher = cv.BFMatcher(cv.NORM_L2, crossCheck=False)
        else:
            #matcher = cv.DescriptorMatcher_BRUTEFORCE_HAMMING
            matcher = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=False)
    elif matchMethod == '2':
        if int(detectMethod) <= 3:
            matcher = cv.DescriptorMatcher_FLANNBASED
        else:
            # TO DO: FLANNBASED LSH
            matcher = cv.DescriptorMatcher_FLANNBASED
    else:
        return
    matches = matcher.knnMatch(desc1, desc2, k=2, mask=None)

    # Filtering out matches
    good_matches = []
    for m, n in matches:
        if m.distance < t * n.distance:
            good_matches.append(m)

    # Sort them in the order of their distance.
    #good_matches = sorted(matches, key=lambda x: x.distance)

    #Draw matches
    img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1], 3), dtype= np.uint8 )
    cv.drawMatches(img1, kp1, img2, kp2, good_matches, img_matches,
                   flags = cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)


    #img3 = cv.drawMatches(img1, kp1, img2, kp2, matches[:10], None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    # Show image with detected matches
    #plt.imshow(img3), plt.show()
    cv.imshow('Emparejamientos de Rasgos', img_matches)

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
      'Descriptores binarios:\n (4)BRIEF\n(5)BRISK\n(6)ORB\n(7)AKAZE\n')
detectMethod = input('Seleccione el metodo: ')

# Selecciion del metodo de emparejamiento
print('Metodos de emparejamiento:\n (1) Fuerza Bruta\n (2) FLANN\n')
matchMethod = input('Seleccione el metodo: ')

# Crea una ventana y muetra la imagen
cv.namedWindow('Emparejamiento de Rasgos', cv.WINDOW_NORMAL)

matching(0.7)

# Ciclo que espera un evento
while (1):
    # Espera la tecla ESC para salir del ciclo
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break

# Destruye la ventana antes de terminar la ejecucion
cv.destroyAllWindows()
