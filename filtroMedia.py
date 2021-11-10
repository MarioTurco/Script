from math import  floor, ceil
from PIL.Image import new
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import time

from numpy.lib.type_check import imag

image_name = 'roma.jpg'
def filtroMediaOpenCV(img, kernel_size):
    kernel = np.ones((kernel_size, kernel_size), np.float32)/(kernel_size**2)
    dst = cv.filter2D(img, -1, kernel)
    return dst

def thresholding(image, threshold):
    new_image = image.copy()
    if len(new_image.shape) == 3:
        new_image = cv.cvtColor(new_image, cv.COLOR_BGR2GRAY)
    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            if(new_image[i][j] > threshold):
                new_image[i][j] = 255
            else:
                new_image[i][j] = 0
    return new_image

def filtroMediaMio(image, kernel_size):
    start = time.time()
    new_image = image.copy()
    if(len(image.shape) == 3): #se l'immagine non è in scala di grigi convertila
        new_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    a = floor((kernel_size - 1)/2)
    b = floor((kernel_size - 1)/2)
    new_pixel = 0
    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            for r in range (-a, a):
                for s in range(-b, b):
                    if( i+r < 0 or j+s <0 or i+r > image.shape[0]-1 or j+s > image.shape[1]-1):
                        pass
                    else:
                        new_pixel +=  (new_image[i+r][j+s])
            new_image[i][j] = new_pixel * (1/kernel_size**2)
            new_pixel = 0
    end = time.time()
    elapsed = round(end-start, 10)
    print("Tempo impiegato senza slicing: ", elapsed)
    return new_image

def localEnhancement(image, level, E):
    new_image = image.copy()
    if(len(image.shape) == 3): #se l'immagine non è in scala di grigi convertila
        new_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            if new_image[i][j] <= level:
                new_image[i][j] = (new_image[i][j]+1)*E
    return new_image

def filtroMediaSlicing(image, kernel_size):
    '''Filtro media implementato tramite slicing'''
    start = time.time()
    new_image = image.copy()
    if(len(image.shape) == 3): #se l'immagine non è in scala di grigi convertila
        new_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    a = floor((kernel_size - 1)/2)
    b = floor((kernel_size - 1)/2)

    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            new_image[i][j] = np.sum(new_image[i-a:i+a+1, j-b:j+b+1]) * (1/(kernel_size**2))
    end = time.time()
    elapsed = round(end-start, 10)
    print("Tempo impiegato con Slicing: ", elapsed)
    return new_image

def filtroMedianaSlicingMulti(image, kernel_size):
    '''Filtro media implementato tramite slicing'''
    start = time.time()
    new_image = image.copy()
    a = floor((kernel_size - 1)/2)
    b = floor((kernel_size - 1)/2)
    for d in range(0,image.shape[2]):
        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                new_image[i][j][d] = np.median(new_image[i-a:i+a+1, j-b:j+b+1,d]) 
    end = time.time()
    elapsed = round(end-start, 10)
    print("Tempo impiegato con Slicing: ", elapsed)
    return new_image



def calcHist(image):
    histogram = [0]*256
    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            if histogram[image[i][j]] == None:
                histogram[image[i][j]] = 1
            else:
                histogram[image[i][j]] += 1
    return histogram

#TODO correggere
def filtroMedianaHuang(image, filter_size):
    '''Applica filtro mediana all'immagine (in bianco e nero) con la tecnica di Huang con complessita O(n)'''
    start = time.time()
    new_image = image.copy()
    histogram = calcHist(image)
    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            for k in range(ceil(-filter_size/2), ceil(filter_size/2)):
                if(i+k>=image.shape[0] or j+filter_size>=image.shape[1] or j-filter_size-1>=image.shape[1]):
                    pass
                else:
                    histogram[image[i+k][j-filter_size-1]]-=1
                    histogram[image[i+k][j+filter_size]]+=1
            
            new_image[i][j] = np.median(histogram)
    end = time.time()
    print("Tempo impiegato filtro mediana: ", round(end-start, 10))   
    return new_image

def gaussianNoise(image, sigma=1):
    '''Restituisce una copia dell'immagine con rumore gaussiano 
    
       image = immagine
       sigma = deviazione standard [Default=1]
    '''
    new_image = image.copy()
    for i in range(0, image.shape[2]):
        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                new_image[i][j] = np.random.normal(image[i][j], sigma)
    return new_image

def roberts_cross(image, threshold):
    '''Restituisce una copia dell'immagine con il filtro di Roberts'''
    new_image = cv.cvtColor(image.copy(), cv.COLOR_BGR2GRAY)
    new_image = cv.GaussianBlur(new_image, (3,3), 0)
    kernel1 = np.array([[1, 0], [0, -1]])
    kernel2 = np.array([[0, 1], [-1, 0]])
    I_x = cv.filter2D(new_image, -1, kernel1)
    I_y = cv.filter2D(new_image, -1, kernel2)
    magnitude = np.sqrt(I_x**2 + I_y**2)
    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            if(magnitude[i][j] > threshold):
                new_image[i][j] = 255
            else:
                new_image[i][j] = 0
    return new_image



threshold = 50
enchancement = 3.5
level = 25
image = cv.imread(image_name)
#gray_im = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
new_image = roberts_cross(image, 10)
plt.subplot(121), plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB)),plt.title('Original') #OpenCv usa BRG invece che RBG, quindi bisogna invertire il colore
plt.subplot(122), plt.imshow(cv.cvtColor(new_image, cv.COLOR_BGR2RGB)), plt.title('Rumore')
#plt.subplot(223), plt.imshow(new_image_2, cmap='gray'), plt.title('Filtro Mediana 2')
#plt.subplot(224), plt.imshow(new_image_3, cmap='gray'), plt.title('Filtro Mediana 3')

plt.show()
# plt.subplot(221), plt.imshow(gray_im, cmap='gray'), plt.title('Gray')
# plt.subplot(222), plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB)),plt.title('Original') #OpenCv usa BRG invece che RBG, quindi bisogna invertire il colore
# plt.subplot(223), plt.imshow(filtroMediaMio(gray_im, kernel_size), cmap='gray'), plt.title('Filtro Media Senza Slice ' +   str(kernel_size) +"x" + str(kernel_size))
# plt.subplot(224), plt.imshow(filtroMediaSlicing(gray_im, kernel_size), cmap='gray'), plt.title('Filtro Media Slice ' +   str(kernel_size) +"x" + str(kernel_size))
# plt.show()
