import cv2
import mediapipe as mp

class GestureRecognitionService:
    def __init__(self, model_path):
        self.recognizer = self._initialize_recognizer(model_path)

    def _initialize_recognizer(self, model_path):
        options = mp.tasks.vision.GestureRecognizerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=model_path),
            running_mode=mp.tasks.vision.RunningMode.IMAGE
        )
        return mp.tasks.vision.GestureRecognizer.create_from_options(options)

    def get_gesture_prediction(self, image_base64):
        """
        Get a gesture prediction from an image.
        Returns a dictionary with the result or None if no gesture is recognized.
        """
        try:
            frame = cv2.imdecode(image_base64, cv2.IMREAD_COLOR)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            results = self.recognizer.recognize(mp_image)
            if results.gestures:
                return {"result": results.gestures[0][0].category_name}
            else:
                return None
        except Exception as e:
            raise ValueError(f"Error al procesar la imagen y obtener la predicción: {str(e)}")