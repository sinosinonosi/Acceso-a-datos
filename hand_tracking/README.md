# 🖐️🔊 Control de Volumen con Detección de Manos

Esta aplicación en Python permite controlar el volumen del sistema operativo (Windows) mediante gestos de la mano captados por la webcam. El proyecto implementa la arquitectura MVC (Modelo-Vista-Controlador) y el patrón DAO para el acceso a datos.

## 🚀 Características Principales

* **Detección en tiempo real:** Utiliza OpenCV y MediaPipe para detectar 21 puntos clave de la mano.
* **Control de audio:** Mapea la distancia entre el dedo pulgar y el índice para ajustar el volumen del sistema usando la librería `pycaw`.
* **Gesto intencional:** El cambio de volumen *solo* se aplica si el dedo meñique está bajado, evitando cambios accidentales.
* **Persistencia de datos:** Registra el inicio, fin y duración de cada sesión de uso, así como los eventos de cambio de volumen (volumen anterior, nuevo y distancia de los dedos) en una base de datos NoSQL alojada en MongoDB Atlas.
* **Indicador visual:** Muestra en pantalla una barra de volumen, el porcentaje actual, los FPS y el estado de la conexión a la base de datos (`DB: OK` o `DB: --`).

## ⚠️ Requisito Importante: Versión de Python

Para garantizar el correcto funcionamiento del módulo de visión por computadora, **es estrictamente necesario utilizar Python 3.11** (o 3.10). 
La librería `mediapipe` en su versión compatible con este código (`0.10.14`) presenta problemas de importación (errores de la API `solutions`) en versiones más recientes como Python 3.13.

## ⚙️ Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en tu entorno local:

1.  **Clonar el repositorio:**
    Descarga o clona este proyecto en tu equipo.

2.  **Crear un entorno virtual:**
    Abre una terminal en la raíz del proyecto y crea un entorno virtual forzando la versión 3.11 de Python:
    ```bash
    py -3.11 -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instalar las dependencias:**
    Instala las librerías necesarias utilizando el archivo de requisitos:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno:**
    Crea un archivo llamado `.env` en la raíz del proyecto para almacenar de forma segura las credenciales de MongoDB. Añade el siguiente contenido, reemplazando la URI por la de tu clúster de Atlas:
    ```env
    MONGODB_URI=mongodb+srv://<usuario>:<contraseña>@<tu_cluster>.mongodb.net/?retryWrites=true&w=majority
    DATABASE_NAME=hand_tracking_db
    ```

## 🎮 Cómo usar la aplicación

1.  Asegúrate de tener el entorno virtual activado (`venv`).
2.  Ejecuta el archivo principal:
    ```bash
    python main.py
    ```
3.  Levanta la mano frente a la webcam. Verás el esqueleto dibujado.
4.  **Para cambiar el volumen:** Baja el dedo meñique. El indicador central se pondrá verde. Junta o separa el pulgar y el índice para ajustar el volumen.
5.  **Para salir y guardar:** Presiona la tecla `q` en tu teclado. Esto cerrará la ventana y actualizará la duración total de la sesión en MongoDB.