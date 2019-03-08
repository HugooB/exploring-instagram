import requests
import json
import os
import cv2
import numpy as np
from sklearn.cluster import KMeans

def open_image(path):
    return cv2.imread(path, cv2.IMREAD_UNCHANGED)

def has_faces(image):
    # Load classifiers
    face_cascade = cv2.CascadeClassifier('C:/Program Files (x86)/Python36-32/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('C:/Program Files (x86)/Python36-32/Lib/site-packages/cv2/data/haarcascade_eye.xml')

    # Convert image to gray scale and detect faces
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, 1.3, 5)
    return (len(faces))

def get_main_color(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
    clt = KMeans(n_clusters=1) #cluster number
    clt.fit(img)
    main_color = clt.cluster_centers_[0]
    return int(main_color[0]), int(main_color[1]), int(main_color[2])

# Famous building

def start(path):
    # Open the image
    image = open_image(path)

    # Get the dimensions of the image
    dimensions = image.shape

    # Get the number of faces
    num_of_faces = has_faces(image)

    # Get the main color of the image
    r, g, b = get_main_color(image)
    print(r,g,b)

if __name__ == '__main__':
    print("Started!")
    start("D:/Hugo/Documents/GitHub/exploring-instagram/temp/1846855971559590614_642497121.jpg")
