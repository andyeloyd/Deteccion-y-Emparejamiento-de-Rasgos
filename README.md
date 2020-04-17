# Deteccion-y-Emparejamiento-de-Rasgos
Tarea de Programacion 1

Se desarrollo un algoritmo para la deteccion y emparejamiento de imagenes en Python, utilizando el IDE PyCharm. Tal algoritmo tiene la
capacidad para detectar los keypoints en una imagen segun el tipo de detector o de realizar un emparejamiento entre 2 imagenes segun el tipo detector y el metodo de emparejamiento.

Los metodos disponibles para deteccion son:

• Good Features to Track

• FAST

• BRIEF

• ORB

• AGAST

• AKAZE

• BRISK

• KAZE

• SIFT

• SURF


Para emparejamiento se dispone de los siguientes detectores:

• SIFT

• SURF

• KAZE

• BRIEF

• BRISK

• ORB

• AKAZE

Los metodos de emparejamiento incluidos en el algoritmo son:

• Fuerza bruta (basado en L2 para descriptores de punto flotante y basado en hamming para descriptores binarios)

• FLANN (KD-Trees con 5 arboles para descriptores de punto flotante y LSH para descriptores binarios)


El algoritmo tiene el siguiente funcionamiento:

-Se solicita al usuario el tipo de tarea a realizar (deteccion o emparejamiento de rasgos)

-Se solicita la o las imagenes de entrada (solo una para deteccion, 2 para emparejamiento)


Si se realiza deteccion:

-Se pide al usuario el tipo de detector a usar

-Se llama a la funcion de deteccion (con slider para variacion del parametro de threshold)

-Se crean un objeto del tipo de detector seleccionado

-Se extraen los keypoints de la imagen segun el detector

-Se dibujan los keypoints en la imagen


Si se realiza emparejamiento:

-Se pide al usuario el tipo de descriptores a usar y el metodo de emparejamiento

-Se llama a la funcion de emparajamiento

-Se crea un objeto del tipo de descriptor/detector seleccionado

-Se extraen los keypoints y descriptores de las imagenes segun el descriptor/detector

-Se crea un objeto matcher segun el tipo de emparejamiento seleccionado

-Se detectan los k vecinos mas cercanos en los descriptores segun el objeto matcher

-Se filtran los emparejamientos debiles

-Se dibuja los emparejamientos en el par de imagenes


Observaciones

Ya que los metodos SURF y SIFT de OpenCV no son gratuitos deben instalarse ciertas bibliotecas especificas para poder utilizarse.
Sin embargo, se presentaron problemas de compatibilidad en el IDE en el cual este algoritmo fue desarrollado, PyCharm. Es por
ello que se opto por intalar la version 3.4.2.16 de OpenCV, la cual si incluye estos metodos sin restriccion alguna.

Conclusiones

Se obtuvo un algoritmo capaz de realizar tanto deteccion como emparejamiento de rasgos en imagenes, a partir de los metodos
solicitados por el usuario. En el caso de deteccion se presenta un slider para variar los parametros. Se obtuvo una buena respuesta
por el programa, congruente con lo esperado teoricamente. 




Documentacion

GFTT    https://docs.opencv.org/3.4/df/d21/classcv_1_1GFTTDetector.html , https://docs.opencv.org/master/d4/d8c/tutorial_py_shi_tomasi.html

FAST    https://docs.opencv.org/master/df/d0c/tutorial_py_fast.html

AGAST   https://docs.opencv.org/3.4/d7/d19/classcv_1_1AgastFeatureDetector.html

BRIEF   https://docs.opencv.org/master/dc/d7d/tutorial_py_brief.html

ORB     https://docs.opencv.org/3.4/db/d95/classcv_1_1ORB.html, https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_orb/py_orb.html

AKAZE   https://docs.opencv.org/3.4/d8/d30/classcv_1_1AKAZE.html

BRISK   https://docs.opencv.org/3.4/de/dbf/classcv_1_1BRISK.html

KAZE    https://docs.opencv.org/3.4/d3/d61/classcv_1_1KAZE.html

SIFT    https://docs.opencv.org/trunk/da/df5/tutorial_py_sift_intro.html

SURF    https://docs.opencv.org/3.4/d5/df7/classcv_1_1xfeatures2d_1_1SURF.html




Emparejamiento: https://docs.opencv.org/master/dc/dc3/tutorial_py_matcher.html

Emparejamiento: https://docs.opencv.org/3.4/db/d39/classcv_1_1DescriptorMatcher.html

FLANN: https://docs.opencv.org/3.4/dc/de2/classcv_1_1FlannBasedMatcher.html

Teoría LSH: https://en.wikipedia.org/wiki/Locality-sensitive_hashing


