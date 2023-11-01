import cv2
import base64
import numpy as np
import math
from PIL import Image
from io import BytesIO
import os
import mediapipe as mp
from mediapipe.tasks import python


model_path = "./model/sign_language_recognizer_25-04-2023.task"
BaseOptions = python.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode


def print_result(result: GestureRecognizerResult, output_image: mp.Image):
    try:
        print('gesture recognition result: {}'.format(result.gestures[0][0].category_name))
    except:
        print(f"Error al obtener la categoría clasificada: {str(result)}")
        return None

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE)

recognizer = GestureRecognizer.create_from_options(options)

def process_image_from_base64(image_base64):
    try:
        # Verifica que la cadena comience con "data:image/"
        if not image_base64.startswith("data:image/"):
            raise ValueError("No es una URL de datos válida")
        # Extrae el tipo de contenido
        content_type = image_base64.split(";")[0].replace("data:image/", "")
        # Verifica que el tipo de contenido sea compatible
        if content_type not in ["jpeg", "jpg", "png"]:
            raise ValueError(f"Tipo de contenido no compatible: {content_type}")
        # Elimina los encabezados "data:image/<tipo_de_contenido>;base64,"
        base64_data = image_base64.split(",")[1]
        # Decodifica la cadena base64 y devuelve los bytes
        image_bytes = base64.b64decode(base64_data)
        image_np = np.frombuffer(image_bytes, dtype=np.uint8)
        return image_np
    except Exception as e:
        print(f"Error al obtener los bytes de la imagen: {str(e)}")
        return None

def get_prediction(image):
    # Decodifica el arreglo de NumPy a una imagen
    frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    results = recognizer.recognize(mp_image)
    print_result(results, mp_image)
    if results.gestures:
        return {"Resultado": results.gestures[0][0].category_name}
    return None