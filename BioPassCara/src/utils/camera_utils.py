import cv2
import numpy as np
import os


class CameraUtils:
    # Cargamos el detector de rostros pre-entrenado
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    @staticmethod
    def detectar_rostro(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rostros = CameraUtils.face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(rostros) == 1:
            x, y, w, h = rostros[0]
            # Retorna el recorte de la cara y las coordenadas
            return gray[y:y + h, x:x + w], (x, y, w, h)
        return None, None

    @staticmethod
    def convertir_a_bytes(imagen_cv2):
        # Codifica la imagen a formato .jpg en memoria y luego a bytes
        is_success, buffer = cv2.imencode(".jpg", imagen_cv2)
        if is_success:
            return buffer.tobytes()
        return None

    @staticmethod
    def entrenar_y_predecir(lista_usuarios, cara_actual):
        """
        Recibe lista de tuplas (id, nombre, cara_bytes) de la BD.
        Entrena el modelo 'lazy' y predice la cara actual.
        """
        if not lista_usuarios:
            return "Sin usuarios"

        rostros_entrenamiento = []
        ids = []
        mapa_nombres = {}

        for user_id, nombre, cara_blob in lista_usuarios:
            # Convertir bytes (memoryview/buffer) de vuelta a numpy array
            nparr = np.frombuffer(cara_blob, np.uint8)
            rostro_img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

            if rostro_img is not None:
                rostros_entrenamiento.append(rostro_img)
                ids.append(user_id)
                mapa_nombres[user_id] = nombre

        # Entrenar (Tarda milisegundos si son pocos usuarios)
        CameraUtils.recognizer.train(rostros_entrenamiento, np.array(ids))

        # Predecir
        id_predicho, confianza = CameraUtils.recognizer.predict(cara_actual)

        # Confianza baja es mejor (0 es match perfecto). < 100 suele ser aceptable en LBPH.
        if confianza < 100:
            return f"{mapa_nombres.get(id_predicho)} ({round(100 - confianza)}%)"
        else:
            return "Desconocido"