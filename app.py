import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Título de la app
st.title("Adaptador de menús según tipo de dieta")

# Subida del archivo Excel
uploaded_file = st.file_uploader("Sube tu archivo Excel con el menú", type=["xlsx"])

# Leer archivos de sustitución en la carpeta "data"
def cargar_diccionarios():
    diccionarios = {}
    for archivo in os.listdir("data"):
        if archivo.endswith(".xlsx"):
            nombre_dieta = os.path.splitext(archivo)[0].upper()  # Nombre del archivo como nombre de dieta (MAYÚSCULAS)
            df = pd.read_excel(os.path.join("data", archivo))
            diccionario = dict(zip(df["Original"], df["Sustituto"]))
            diccionarios[nombre_dieta] = diccionario
    return diccionarios

diccionarios_dietas = cargar_diccionarios()
dietas_disponibles = list(diccionarios_dietas.keys())

# Selección del tipo de dieta
dieta_seleccionada = st.selectbox("Selecciona el tipo de dieta", dietas_disponibles)

# Procesar archivo
if uploaded_file and dieta_seleccionada:
    hoja = st.text_input("Nombre de la hoja a modificar", value="MENÚ SIN RECOMENDACIÓN")
    df = pd.read_excel(uploaded_file, sheet_name=hoja)

    sustituciones = diccionarios_dietas[dieta_seleccionada]

    df_modificado = df.applymap(lambda x: sustituciones.get(x, x) if isinstance(x, str) else x)

    # Descargar Excel modificado
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_modificado.to_excel(writer, index=False, sheet_name=hoja)
    st.success("Menú adaptado correctamente")

    st.download_button(
        label="Descargar archivo corregido",
        data=output.getvalue(),
        file_name=f"menu_adaptado_{dieta_seleccionada}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

