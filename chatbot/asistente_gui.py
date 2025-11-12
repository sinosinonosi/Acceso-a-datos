import tkinter as tk
from tkinter import scrolledtext, messagebox
import google.generativeai as genai
import os
from dotenv import load_dotenv

def cargar_api_key():
    load_dotenv()
    api_key = os.getenv('API_KEY')
    if not api_key:
        messagebox.showerror("Error de Configuración",
                             "No se encontró la 'API_KEY' en el archivo .env.\n"
                             "Por favor, crea un archivo .env y añade tu clave.")
        return None
    return api_key

def cargar_contexto(archivo="servicios.txt"):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        messagebox.showwarning("Archivo Faltante",
                               f"No se encontró el archivo '{archivo}'.\n"
                               "El asistente podría no tener contexto.")
        return "No hay información de servicios disponible."
    except Exception as e:
        messagebox.showerror("Error de Archivo", f"Error al leer {archivo}: {e}")
        return ""

def generar_respuesta_ia(pregunta, modelo, contexto):
    prompt_completo = f"""
    **Contexto de la Peluquería:**
    ---
    {contexto}
    ---
    
    **Instrucción:** Eres un asistente virtual amable y profesional 
    de la "Peluquería Brillo Estelar". Tu única tarea es responder 
    preguntas de clientes basándote *exclusivamente* en el contexto 
    proporcionado (servicios, precios, horarios).

    - Si la pregunta se puede responder con el contexto, hazlo.
    - Si la pregunta no está relacionada o no se puede responder 
      con el contexto, indícalo amablemente (ej. "Esa información 
      no está disponible en nuestros registros, pero puedo ayudarte 
      con nuestros servicios y horarios.").
    - No inventes información.

    **Pregunta del Usuario:**
    {pregunta}
    
    **Asistente:**
    """

    try:
        response = modelo.generate_content(prompt_completo)
        
        if response.parts:
            return response.text
        else:
            return "Lo siento, no puedo generar una respuesta para esa consulta."

    except Exception as e:
        print(f"Error en la API de Gemini: {e}")
        return f"Error al contactar la API. Por favor, revisa la consola."

def al_enviar_click(modelo, contexto):
    pregunta = entrada_pregunta.get("1.0", tk.END).strip()
    if not pregunta:
        return

    actualizar_chat("Tú", pregunta, "user_tag")
    entrada_pregunta.delete("1.0", tk.END)

    boton_enviar.config(text="Pensando...", state=tk.DISABLED)
    ventana.update_idletasks() 

    respuesta = generar_respuesta_ia(pregunta, modelo, contexto)
    
    actualizar_chat("Asistente", respuesta, "assistant_tag")
    boton_enviar.config(text="Enviar", state=tk.NORMAL)

def actualizar_chat(usuario, mensaje, tag):
    area_chat.config(state=tk.NORMAL)
    area_chat.insert(tk.END, f"{usuario}: {mensaje}\n\n", tag)
    area_chat.config(state=tk.DISABLED)
    area_chat.see(tk.END)

API_KEY_GEMINI = cargar_api_key()
CONTEXTO_PELUQUERIA = cargar_contexto("servicios.txt")
MODELO_IA = None

if API_KEY_GEMINI:
    try:
        genai.configure(api_key=API_KEY_GEMINI)
        MODELO_IA = genai.GenerativeModel('gemini-2.5-flash') 
    except Exception as e:
        messagebox.showerror("Error de API", f"No se pudo configurar Gemini: {e}")
        API_KEY_GEMINI = None

ventana = tk.Tk()
ventana.title("Asistente de Peluquería IA")
ventana.geometry("550x650")
ventana.configure(bg="#F0F0F0")

frame_principal = tk.Frame(ventana, bg="#F0F0F0")
frame_principal.pack(expand=True, fill=tk.BOTH, padx=15, pady=15)

etiqueta_titulo = tk.Label(frame_principal, 
                           text="Bienvenido al Asistente de Peluquería",
                           font=("Arial", 16, "bold"), 
                           bg="#F0F0F0")
etiqueta_titulo.pack(side=tk.TOP, pady=(0, 10))

frame_entrada = tk.Frame(frame_principal, bg="#F0F0F0")
frame_entrada.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

area_chat = scrolledtext.ScrolledText(frame_principal, 
                                      wrap=tk.WORD, 
                                      state=tk.DISABLED, 
                                      font=("Arial", 11),
                                      bg="#FFFFFF",
                                      border=0)
area_chat.pack(expand=True, fill=tk.BOTH, pady=5)

area_chat.tag_config("user_tag", foreground="#004080", font=("Arial", 11, "bold"))
area_chat.tag_config("assistant_tag", foreground="#006400")

entrada_pregunta = tk.Text(frame_entrada, 
                           height=2, 
                           font=("Arial", 10), 
                           wrap=tk.WORD,
                           border=1, 
                           relief=tk.SOLID)
entrada_pregunta.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

boton_enviar = tk.Button(frame_entrada, 
                         text="Enviar", 
                         font=("Arial", 10, "bold"), 
                         bg="#007BFF", 
                         fg="white",
                         width=10,
                         relief=tk.FLAT,
                         command=lambda: al_enviar_click(MODELO_IA, CONTEXTO_PELUQUERIA))
boton_enviar.pack(side=tk.RIGHT)

if not API_KEY_GEMINI or not MODELO_IA:
    boton_enviar.config(text="Error", state=tk.DISABLED)
    if not API_KEY_GEMINI:
        actualizar_chat("Sistema", "Error: API Key no configurada.", "assistant_tag")
    else:
        actualizar_chat("Sistema", "Error: No se pudo iniciar el modelo de IA.", "assistant_tag")

ventana.mainloop()