import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from src.usuario_dao import UsuarioDAO
from src.utils.camera_utils import CameraUtils


class BioPassApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BioPass - Control de Acceso DAO")

        # Variables
        self.cap = cv2.VideoCapture(0)
        self.nombre_var = tk.StringVar()

        # UI
        self.label_video = tk.Label(root)
        self.label_video.pack()

        frame_controls = tk.Frame(root)
        frame_controls.pack(pady=10)

        tk.Label(frame_controls, text="Nombre:").pack(side=tk.LEFT)
        tk.Entry(frame_controls, textvariable=self.nombre_var).pack(side=tk.LEFT, padx=5)

        tk.Button(frame_controls, text="Registrar", command=self.registrar_usuario).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_controls, text="Login (Biométrico)", command=self.login_usuario).pack(side=tk.LEFT, padx=5)

        self.actualizar_video()

    def actualizar_video(self):
        ret, frame = self.cap.read()
        if ret:
            # Dibujar rectángulo si hay cara
            cara_gris, coords = CameraUtils.detectar_rostro(frame)
            if coords:
                x, y, w, h = coords
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Mostrar en Tkinter
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label_video.imgtk = imgtk
            self.label_video.configure(image=imgtk)

        self.root.after(10, self.actualizar_video)

    def registrar_usuario(self):
        nombre = self.nombre_var.get()
        if not nombre:
            messagebox.showwarning("Error", "Escribe un nombre")
            return

        ret, frame = self.cap.read()
        if ret:
            cara_gris, coords = CameraUtils.detectar_rostro(frame)
            if cara_gris is not None:
                # 1. Convertir imágenes a bytes para BLOB
                foto_bytes = CameraUtils.convertir_a_bytes(frame)
                cara_bytes = CameraUtils.convertir_a_bytes(cara_gris)

                # 2. Llamar al DAO (El DAO se encarga de la BD)
                UsuarioDAO.registrar_usuario(nombre, foto_bytes, cara_bytes)
                messagebox.showinfo("Éxito", f"Usuario {nombre} registrado")
            else:
                messagebox.showerror("Error", "No se detecta rostro claro")

    def login_usuario(self):
        # 1. Capturar cara actual
        ret, frame = self.cap.read()
        if ret:
            cara_gris, coords = CameraUtils.detectar_rostro(frame)
            if cara_gris is not None:
                # 2. Obtener usuarios de la BD (Bytes)
                usuarios = UsuarioDAO.obtener_todos()

                # 3. Entrenar y predecir en tiempo real
                resultado = CameraUtils.entrenar_y_predecir(usuarios, cara_gris)
                messagebox.showinfo("Resultado Login", f"Usuario detectado: {resultado}")
            else:
                messagebox.showerror("Error", "Acércate a la cámara")


if __name__ == "__main__":
    root = tk.Tk()
    app = BioPassApp(root)
    root.mainloop()