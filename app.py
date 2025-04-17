import streamlit as st
import pandas as pd
import os
import fitz  # PyMuPDF
import io
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from PyPDF2 import PdfReader

# Función para extraer texto del PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# Función para cargar base de datos de sustituciones
def load_substitution_database(file):
    try:
        df = pd.read_excel(file)
        if "PLATOS" not in df.columns:
            return None, "La base de datos no contiene la columna 'PLATOS'."
        return df, None
    except Exception as e:
        return None, f"Error al cargar la base de datos: {e}"

# Función para sustituir alimentos en el menú
def replace_ingredients_in_excel(original_excel, substitutions_df):
    try:
        workbook = load_workbook(filename=original_excel)
        if "Menu sin Recomendación" not in workbook.sheetnames:
            return None, "La hoja 'Menu sin Recomendación' no se encuentra en el archivo."

        sheet = workbook["Menu sin Recomendación"]
        platos_dict = dict(zip(substitutions_df["PLATOS"], substitutions_df["VEGANO"]))

        fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

        for row in sheet.iter_rows():
            for cell in row:
                if cell.value in platos_dict:
                    cell.value = platos_dict[cell.value]
                    cell.fill = fill

        # Guardar en memoria
        output = io.BytesIO()
        workbook.save(output)
        output.seek(0)
        return output, None
    except Exception as e:
        return None, str(e)

# Interfaz Streamlit
st.title("Adaptador de menús PDF a dieta vegana")

uploaded_pdf = st.file_uploader("Sube el menú en PDF", type=["pdf"])
substitution_file = st.file_uploader("Sube la base de datos de sustituciones (Excel)", type=["xlsx"])

if uploaded_pdf and substitution_file:
    with st.spinner("Procesando PDF..."):
        try:
            text = extract_text_from_pdf(uploaded_pdf)
            with open("temp_text.txt", "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            st.error(f"Error al extraer texto del PDF: {e}")

    with st.spinner("Cargando base de datos..."):
        substitutions_df, error = load_substitution_database(substitution_file)
        if error:
            st.error(error)
        else:
            uploaded_excel = st.file_uploader("Sube el menú original en Excel para modificarlo", type=["xlsx"])
            if uploaded_excel:
                with st.spinner("Aplicando sustituciones..."):
                    modified_excel, error = replace_ingredients_in_excel(uploaded_excel, substitutions_df)
                    if error:
                        st.error(error)
                    else:
                        st.success("Sustituciones aplicadas correctamente.")
                        st.download_button(
                            label="Descargar Excel corregido",
                            data=modified_excel,
                            file_name="menu_corregido.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
