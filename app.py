import streamlit as st
import pandas as pd
import os
import difflib
from io import BytesIO
from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook

def load_substitution_db(diet_type):
    # Recorremos todos los archivos .xlsx del directorio actual
    for file in os.listdir():
        if file.endswith(".xlsx"):
            df = pd.read_excel(file)
            if 'PLATOS' in df.columns and diet_type in df.columns:
                return df.set_index('PLATOS')[diet_type].dropna().to_dict()
    return None

def substitute_foods(input_excel, substitutions):
    # Cargar el archivo original conservando el formato
    wb = load_workbook(input_excel)
    if "Menu sin Recomendación" not in wb.sheetnames:
        st.error("No se encontró la hoja 'Menu sin Recomendación' en el archivo.")
        return None

    ws = wb["Menu sin Recomendación"]

    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str):
                closest_match = difflib.get_close_matches(cell.value, substitutions.keys(), n=1, cutoff=0.9)
                if closest_match:
                    original = closest_match[0]
                    replacement = substitutions[original]
                    cell.value = replacement

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output

st.title("Adaptador de Menús según Dietas")

uploaded_file = st.file_uploader("Sube tu archivo Excel de menú", type=["xlsx"])

# Mostrar opciones de dietas detectadas automáticamente
diet_options = []
for file in os.listdir():
    if file.endswith(".xlsx"):
        df = pd.read_excel(file)
        if 'PLATOS' in df.columns:
            for col in df.columns[1:]:
                if col.upper() not in diet_options:
                    diet_options.append(col.upper())

diet_type = st.selectbox("Selecciona el tipo de dieta", sorted(diet_options))

if uploaded_file and diet_type:
    substitutions = load_substitution_db(diet_type.upper())
    if substitutions:
        output = substitute_foods(uploaded_file, substitutions)
        if output:
            st.success("Archivo procesado correctamente.")
            st.download_button(
                label="Descargar Excel corregido",
                data=output,
                file_name="menu_corregido.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.error("No se encontró una base de datos válida con ese tipo de dieta.")
