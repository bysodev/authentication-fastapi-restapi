# STEP 1: Import the necessary modules.
import cv2
import base64
import numpy as np

def process_image_from_base64(base64_image):
    try:
        # Remove metadata if present
        if "base64," in base64_image:
            base64_image = base64_image.split("base64,")[1]
        # Decode the base64 image
        image_data = base64.b64decode(base64_image)
        # Convert the image data to a numpy array
        image_data = np.frombuffer(image_data, dtype=np.uint8)
        # Load the image from the numpy array
        image = cv2.imdecode(image_data, cv2.IMREAD_UNCHANGED)
        return image
    except Exception as e:
        print(f"Error al obtener los bytes de la imagen: {str(e)}")
        return None
    
def normalize(image):
    return image / 255.0

def resize(image, width=446, height=446):
    return cv2.resize(image, (width, height))

def subtract_background(image):
    fgbg = cv2.createBackgroundSubtractorMOG2()
    fgmask = fgbg.apply(image)
    return fgmask

def improve_lighting(image_np):
    # Check if the image is already grayscale
    if image_np.ndim == 2 or image_np.shape[2] == 1:
        gray = image_np
    else:
        # Convert the image to grayscale
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    # Apply histogram equalization
    equalized = cv2.equalizeHist(gray)
    # Convert back to BGR
    improved = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
    return improved

def segment_hand(image):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Define range for skin color in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    # Threshold the HSV image to get only skin colors
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(image, image, mask=mask)
    return res

def flip_horizontal(image):
    return cv2.flip(image, 1)
