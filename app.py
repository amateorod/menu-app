import streamlit as st
import pandas as pd
import os
from io import BytesIO
import openpyxl

# Diccionario con las rutas de los CSV por tipo de dieta
csv_rutas = {
    "Normal": "platos_normal.csv",
    "Sin carne": "platos_sin_carne.csv",
    "Sin pescado": "platos_sin_pescado.csv",
    "Ovolacteovegetariana": "platos_ovolacteovegetariana.csv",
    "Vegana": "platos_vegana.csv",
    "Sin huevo": "platos_sin_huevo.csv",
    "Sin legumbres": "platos_sin_legumbres.csv",
    "Celíaco": "platos_celíaco.csv",
    "Sin lactosa": "platos_sin_lactosa.csv"
}

st.title("Adaptador de menús dietéticos")
st.write("Sube tu archivo Excel y selecciona el tipo de dieta para adaptar el menú automáticamente.")

dieta = st.selectbox("Selecciona el tipo de dieta:", list(csv_rutas.keys()))
archivo_excel = st.file_uploader("Sube el archivo Excel (.xlsx)", type=["xlsx"])

if archivo_excel and dieta:
    try:
        # Cargar sustituciones de la dieta elegida
        sustituciones = pd.read_csv(csv_rutas[dieta])["Platos"].tolist()

        # Cargar Excel manteniendo formato
        libro = openpyxl.load_workbook(archivo_excel)
        hojas = libro.sheetnames
        hoja_seleccionada = st.selectbox("Selecciona la hoja que quieres adaptar:", hojas)

        hoja = libro[hoja_seleccionada]

        # Reemplazar cada plato en cada celda
        for fila in hoja.iter_rows():
            for celda in fila:
                if celda.value and isinstance(celda.value, str):
                    for plato in sustituciones:
                        if plato.lower() in celda.value.lower():
                            celda.value = celda.value.lower().replace(plato.lower(), f"[ADAPTADO] {plato}")

        # Guardar resultado en memoria
        salida = BytesIO()
        libro.save(salida)
        salida.seek(0)

        st.success("¡Menú adaptado correctamente!")
        st.download_button("📥 Descargar Excel adaptado", data=salida, file_name="menu_adaptado.xlsx")

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")

