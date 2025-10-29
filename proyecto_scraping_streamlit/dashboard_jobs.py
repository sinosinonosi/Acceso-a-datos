import streamlit as st
import pandas as pd
from collections import Counter

try:
    df = pd.read_csv("ofertas_trabajo.csv")
except FileNotFoundError:
    st.error("Error: No se encontró el archivo 'ofertas_trabajo.csv'.")
    st.info("Por favor, ejecuta primero el script 'scrape_jobs.py' para generar los datos.")
    st.stop()

st.set_page_config(
    page_title="Dashboard de Empleos",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Dashboard de Ofertas de Trabajo")
st.write("Análisis interactivo de las ofertas extraídas de 'Fake Python Job Site'.")

st.sidebar.header("Filtros Interactivos")

filtro_puesto = st.sidebar.text_input(
    "Buscar por Puesto (ej: 'Python', 'Developer'):"
)
filtro_ubicacion = st.sidebar.text_input(
    "Buscar por Ubicación (ej: 'Port', 'AE'):"
)

df_filtrado = df.copy()

if filtro_puesto:
    df_filtrado = df_filtrado[
        df_filtrado["Puesto"].str.contains(filtro_puesto, case=False, na=False)
    ]

if filtro_ubicacion:
    df_filtrado = df_filtrado[
        df_filtrado["Ubicacion"].str.contains(filtro_ubicacion, case=False, na=False)
    ]

st.markdown("---")
kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric(
    label="Total Ofertas Encontradas",
    value=len(df_filtrado)
)
kpi2.metric(
    label="Compañías Únicas",
    value=df_filtrado["Compañia"].nunique()
)
kpi3.metric(
    label="Ubicaciones Únicas",
    value=df_filtrado["Ubicacion"].nunique()
)

st.subheader(f"Mostrando {len(df_filtrado)} ofertas de trabajo")
st.dataframe(df_filtrado, height=350, use_container_width=True)

st.markdown("---")
st.subheader("Análisis de Palabras Clave en Puestos")

if df_filtrado.empty:
    st.warning("No hay datos para mostrar en los gráficos.")
else:
    keywords = [
        'Python', 'Developer', 'Engineer', 'Senior', 
        'Entry-Level', 'Programmer', 'Data', 'Software'
    ]
    
    texto_titulos = " ".join(df_filtrado["Puesto"].str.lower())
    conteo_palabras = Counter(texto_titulos.split())
    
    conteo_final = {
        keyword: conteo_palabras.get(keyword.lower(), 0) 
        for keyword in keywords
    }
    
    df_keywords = pd.DataFrame.from_dict(
        conteo_final, 
        orient="index", 
        columns=["Conteo"]
    )
    df_keywords = df_keywords.sort_values("Conteo", ascending=False)
    
    st.bar_chart(df_keywords)