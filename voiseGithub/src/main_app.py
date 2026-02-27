import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from src.auth_dao import AuthDAO
from src.voice_service import VoiceService

class VoiceAuditApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VoiceAudit Login")
        self.root.geometry("400x500")
        
        self.dao = AuthDAO()
        self.voice_service = VoiceService()
        self.frase_temporal = None 

        tk.Label(root, text="Usuario:").pack(pady=5)
        self.entry_username = tk.Entry(root)
        self.entry_username.pack(pady=5)

        tk.Button(root, text="1. Capturar Voz para Registro", command=self.capturar_registro).pack(pady=10)
        
        self.lbl_confirmacion = tk.Label(root, text="Frase reconocida: -", fg="blue")
        self.lbl_confirmacion.pack(pady=5)
        
        tk.Button(root, text="2. Confirmar y Guardar Registro", command=self.confirmar_registro).pack(pady=5)
        
        tk.Label(root, text="-"*40).pack(pady=10)
        
        tk.Button(root, text="Login por Voz", command=self.login).pack(pady=10)
        tk.Button(root, text="Auditoría Crítica", command=self.mostrar_auditoria).pack(pady=10)

        self.txt_auditoria = tk.Text(root, height=10, width=45)
        self.txt_auditoria.pack(pady=10)

    def capturar_registro(self):
        username = self.entry_username.get().strip()
        if not username:
            messagebox.showwarning("Aviso", "Introduce un usuario primero.")
            return

        resultado = self.voice_service.escuchar_y_transcribir()
        if resultado["status"] == "OK":
            self.frase_temporal = resultado["texto"]
            self.lbl_confirmacion.config(text=f"Frase reconocida: '{self.frase_temporal}'")
        else:
            self.dao.registrar_error_tecnico(username, resultado["motivo"])
            messagebox.showerror("Error", "No se pudo entender el audio.")

    def confirmar_registro(self):
        username = self.entry_username.get().strip()
        if not username or not self.frase_temporal:
            messagebox.showwarning("Aviso", "Debes capturar la voz primero.")
            return
            
        if self.dao.registrar_usuario(username, self.frase_temporal):
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.frase_temporal = None
            self.lbl_confirmacion.config(text="Frase reconocida: -")
        else:
            messagebox.showerror("Error", "El usuario ya existe o hubo un problema.")

    def login(self):
        username = self.entry_username.get().strip()
        user_data = self.dao.obtener_usuario(username)
        
        if not user_data:
            messagebox.showerror("Error", "Usuario no encontrado.")
            return

        user_id, passphrase_correcta, intentos, bloqueado_hasta = user_data

        if bloqueado_hasta and bloqueado_hasta > datetime.now():
            messagebox.showerror("Bloqueado", f"Usuario bloqueado hasta {bloqueado_hasta.strftime('%H:%M:%S')}")
            return

        resultado = self.voice_service.escuchar_y_transcribir()
        
        if resultado["status"] == "OK":
            frase_dicha = resultado["texto"]
            if frase_dicha == passphrase_correcta:
                self.dao.registrar_acceso_exitoso(user_id, resultado["confianza"], resultado["latencia"])
                messagebox.showinfo("Acceso Permitido", f"Bienvenido {username}")
            else:
                restantes = self.dao.registrar_intento_fallido(user_id, frase_dicha, intentos) 
                if restantes == 0:
                    messagebox.showerror("Acceso Denegado", "Usuario bloqueado por demasiados intentos.") 
                else:
                    messagebox.showwarning("Acceso Denegado", f"Frase incorrecta. Intentos restantes: {restantes}")
        else:
            self.dao.registrar_error_tecnico(username, resultado["motivo"])
            messagebox.showerror("Error de Audio", "No te he entendido.")

    def mostrar_auditoria(self):
        self.txt_auditoria.delete(1.0, tk.END)
        registros = self.dao.obtener_auditoria_critica()
        if not registros:
            self.txt_auditoria.insert(tk.END, "No hay registros críticos.")
            return
            
        for idx, (user, status) in enumerate(registros, 1):
            self.txt_auditoria.insert(tk.END, f"{idx}. Usuario: {user} | Estado: {status}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAuditApp(root)
    root.mainloop()