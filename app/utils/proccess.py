import cv2
import base64
import numpy as np
import math
from PIL import Image
from io import BytesIO
import os

# PARA EL RECONOCIMEINTO DE LAS MANOS
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier 

Classifier = Classifier("./model/keras_model.h5", "./model/labels.txt")

detector = HandDetector(maxHands=1)
offset = 20
imgSize = 300

labels = ["A", "I"]

# Decodificar la imagen base64 y convertirla a una imagen PIL
# pil_image = Image.open(BytesIO(image_bytes))
# Convertir la imagen PIL a una matriz de NumPy
# frame_capture = np.array(pil_image)
# output_directory = '/img'
# os.makedirs(output_directory, exist_ok=True)
# pil_image = Image.fromarray(frame)
# pil_image.save(os.path.join(output_directory, 'nueva1.jpeg'))

def process_image_from_base64(image_base64):
    image_bytes = base64.b64decode(image_base64)
    np_array = np.frombuffer(image_bytes, dtype=np.uint8)
    return np_array

def get_prediction(image):

    # Decodifica el arreglo de NumPy a una imagen
    frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
    hands, frame = detector.findHands(frame)

    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']
        frameWhite = np.ones((imgSize, imgSize, 3), np.uint8)*255
        frameCapture = frame[y-offset:y + h + offset, x - offset:x + w + offset]

        if frameWhite is not None and frameWhite.any():
            frameShape = frameWhite.shape
            aspectRatio = h / w
            
            if(aspectRatio > 1):
                k = imgSize/h
                wCal = math.ceil(k*w)
                imgResize = cv2.resize(frameWhite, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize-wCal) / 2)
                frameWhite[: , wGap:wCal+wGap, :] = imgResize
                # frameWhite[0: imgResizeShape[0], 0: imgResizeShape[1]] = imgResize
                prediction, index = Classifier.getPrediction(frameWhite, draw=False)
                print(prediction, index)
                print(labels[index])
            else:
                k = imgSize / w
                hCal = math.ceil(k*h)
                imgResize = cv2.resize(frameWhite, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize-hCal) / 2)
                frameWhite[hGap:hCal + hGap , :] = imgResize
                prediction, index = Classifier.getPrediction(frameWhite, draw=False)
                print(prediction, index)
                print(labels[index])
