import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk, messagebox

URL_BCE = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"

class ConversorDivisasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Divisas")
        self.root.geometry("450x480")
        self.root.configure(bg="#F0F4F8")
        self.root.resizable(False, False)

        self.tasas = {}
        self.fecha_actualizacion = "---"

        self.cargar_datos_xml()
        self.crear_interfaz()

    def cargar_datos_xml(self):
        try:
            response = requests.get(URL_BCE)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                cubo_datos = None
                for cube in root.iter():
                    if 'time' in cube.attrib:
                        self.fecha_actualizacion = cube.attrib['time']
                        cubo_datos = cube
                        break
                
                if cubo_datos is not None:
                    self.tasas['EUR'] = 1.0
                    for child in cubo_datos:
                        if 'currency' in child.attrib and 'rate' in child.attrib:
                            self.tasas[child.attrib['currency']] = float(child.attrib['rate'])
            else:
                messagebox.showerror("Error", "No se pudo conectar con el BCE.")
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {e}")

    def crear_interfaz(self):
        estilo_fuente = ("Helvetica", 11)
        estilo_titulo = ("Helvetica", 18, "bold")
        
        titulo = tk.Label(self.root, text="Cambio de Divisas", font=estilo_titulo, bg="#F0F4F8", fg="#2C3E50")
        titulo.pack(pady=(30, 5))

        lbl_fecha = tk.Label(self.root, text=f"Datos oficiales del BCE: {self.fecha_actualizacion}", font=("Helvetica", 9), bg="#F0F4F8", fg="#7F8C8D")
        lbl_fecha.pack(pady=(0, 20))

        frame_main = tk.Frame(self.root, bg="#FFFFFF", bd=1, relief="solid")
        frame_main.pack(padx=40, pady=10, fill="both", expand=True)

        tk.Label(frame_main, text="Importe:", font=estilo_fuente, bg="#FFFFFF").grid(row=0, column=0, padx=20, pady=20, sticky="w")
        self.entry_cantidad = tk.Entry(frame_main, font=estilo_fuente, width=15, justify="center", bg="#ECF0F1")
        self.entry_cantidad.grid(row=0, column=1, padx=20, pady=20)

        lista_monedas = sorted(self.tasas.keys())

        tk.Label(frame_main, text="De:", font=estilo_fuente, bg="#FFFFFF").grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.combo_origen = ttk.Combobox(frame_main, values=lista_monedas, state="readonly", font=estilo_fuente, width=12)
        self.combo_origen.set("EUR")
        self.combo_origen.grid(row=1, column=1, padx=20, pady=10)

        tk.Label(frame_main, text="A:", font=estilo_fuente, bg="#FFFFFF").grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.combo_destino = ttk.Combobox(frame_main, values=lista_monedas, state="readonly", font=estilo_fuente, width=12)
        self.combo_destino.set("USD")
        self.combo_destino.grid(row=2, column=1, padx=20, pady=10)

        btn_convertir = tk.Button(self.root, text="CONVERTIR AHORA", command=self.convertir, font=("Helvetica", 11, "bold"), bg="#3498DB", fg="white", activebackground="#2980B9", activeforeground="white", relief="flat", cursor="hand2")
        btn_convertir.pack(pady=25, ipadx=30, ipady=8)

        self.lbl_resultado = tk.Label(self.root, text="", font=("Helvetica", 20, "bold"), bg="#F0F4F8", fg="#27AE60")
        self.lbl_resultado.pack(pady=5)

    def convertir(self):
        try:
            cantidad = float(self.entry_cantidad.get())
            moneda_origen = self.combo_origen.get()
            moneda_destino = self.combo_destino.get()

            if moneda_origen not in self.tasas or moneda_destino not in self.tasas:
                return

            tasa_origen = self.tasas[moneda_origen]
            tasa_destino = self.tasas[moneda_destino]

            resultado = (cantidad / tasa_origen) * tasa_destino

            self.lbl_resultado.config(text=f"{resultado:.2f} {moneda_destino}")

        except ValueError:
            messagebox.showwarning("Atención", "Introduce solo números válidos.")
        except Exception:
            messagebox.showerror("Error", "Error inesperado en el cálculo.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConversorDivisasApp(root)
    root.mainloop()