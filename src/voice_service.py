import speech_recognition as sr
import time

class VoiceService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone() 

    def escuchar_y_transcribir(self):
        """Actúa como fachada, oculta la complejidad de la captura de audio """
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("Escuchando...")
                start_time = time.time()
                audio = self.recognizer.listen(source, timeout=5)
                latencia = f"{round(time.time() - start_time, 2)}s"

            texto = self.recognizer.recognize_google(audio, language="es-ES")
            confianza = 0.95 
            
            return {"status": "OK", "texto": texto.lower(), "confianza": confianza, "latencia": latencia}
        except sr.UnknownValueError:
            return {"status": "ERROR", "motivo": "no_entendido"}
        except sr.RequestError:
            return {"status": "ERROR", "motivo": "error_red"}
        except Exception as e:
            return {"status": "ERROR", "motivo": str(e)}