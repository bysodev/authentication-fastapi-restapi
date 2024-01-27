import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import io

from app.utils.proccess import flip_horizontal

class GestureRecognitionService:
    def __init__(self, model_path):
        self.recognizer = self._initialize_recognizer(model_path)

    def _initialize_recognizer(self, model_path):
        options = mp.tasks.vision.GestureRecognizerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=model_path),
            running_mode=mp.tasks.vision.RunningMode.IMAGE
        )
        recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(options)
        return recognizer   

    def get_gesture_prediction(self, image_np):
        """
        Get a gesture prediction from an image.
        Returns a dictionary with the result or None if no gesture is recognized.
        """
        try:
            # Initialize MediaPipe Hands.
            mp_hands = mp.solutions.hands
            hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
            # Convert the image from BGR to RGB
            mp_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB) 
            # Process the image and detect hands.
            # Convert the image from BGR to RGB
            results = hands.process(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
            # Print handedness and draw hand landmarks on the image.
            if not results.multi_hand_landmarks:
                return None
            for handedness in results.multi_handedness:
                if handedness.classification[0].label == "Left":
                    image_np = flip_horizontal(image_np)
            # Convert the image from BGR to RGB
            mp_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
            # Create an mp.Image object from the numpy array
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=mp_image)
            results = self.recognizer.recognize(mp_image)
            # Close MediaPipe Hands.
            hands.close()
            if results.gestures:
                print(results.gestures[0][0].category_name)
                return {"result": results.gestures[0][0].category_name}
            else:
                return None  
                      
        except Exception as e:
            print(f"Error: {str(e)}")
            raise ValueError(f"Error al procesar la imagen y obtener la predicción: {str(e)}")