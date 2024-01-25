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
        recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(options)
        return recognizer

    def get_gesture_prediction(self, base64):
        """
        Get a gesture prediction from an image.
        Returns a dictionary with the result or None if no gesture is recognized.
        """
        try:
            # Decodificar la cadena base64
            # frame = cv2.imdecode(image_base64, cv2.IMREAD_COLOR)
            # Agregar una impresión para verificar el tamaño de la imagen
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=base64)
            results = self.recognizer.recognize(mp_image)
            if results.gestures:
                return {"result": results.gestures[0][0].category_name}
            else:
                return None
        except Exception as e:
            print(f"Error: {str(e)}")
            raise ValueError(f"Error al procesar la imagen y obtener la predicción: {str(e)}")