import requests
from bs4 import BeautifulSoup
import pandas as pd

print("Iniciando el scraping de 'Fake Python Job Site'...")

url = "https://realpython.github.io/fake-jobs/"
pagina = requests.get(url)

soup = BeautifulSoup(pagina.content, "html.parser")

results_container = soup.find("div", id="ResultsContainer")

job_elements = results_container.find_all("div", class_="card-content")

puestos = []
compañias = []
ubicaciones = []

for job in job_elements:
    puesto = job.find("h2", class_="title").text.strip()
    compañia = job.find("h3", class_="company").text.strip()
    ubicacion = job.find("p", class_="location").text.strip()
    
    puestos.append(puesto)
    compañias.append(compañia)
    ubicaciones.append(ubicacion)

print(f"Se encontraron {len(puestos)} ofertas de trabajo.")

df = pd.DataFrame({
    "Puesto": puestos,
    "Compañia": compañias,
    "Ubicacion": ubicaciones
})

df.to_csv("ofertas_trabajo.csv", index=False)

print("Datos guardados exitosamente en 'ofertas_trabajo.csv'.")