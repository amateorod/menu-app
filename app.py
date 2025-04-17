import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import tabula
import tempfile
import os
from io import BytesIO

# Título
st.title("Adaptador automático de menús según tipo de dieta")

# Opciones de dieta
opciones_dieta = ["VEGANO", "OVOLACTEOVEGETARIANO", "SIN LACTOSA", "CELIACO", "SIN LACTOSA Y CELIACO"]
dieta_seleccionada = st.selectbox("Selecciona el tipo de dieta", opciones_dieta)

# Subida de archivos
archivo_menu = st.file_uploader("Sube el archivo del menú (Excel o PDF)", type=["xlsx", "pdf"])

# Subida de base de datos de sustituciones
archivo_bd = st.file_uploader("Sube la base de datos de sustituciones", type=["xlsx"])

def extraer_tabla_pdf(pdf_path):
    try:
        tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
        if tables and len(tables) > 0:
            df = pd.concat(tables, ignore_index=True)
            st.success("Tabla extraída correctamente del PDF.")
            return df
        else:
            st.error("No se pudo extraer una tabla del PDF.")
            return None
    except Exception as e:
        st.error(f"Error al extraer la tabla del PDF: {e}")
        return None

def aplicar_sustituciones(df_menu, df_bd, columna_dieta):
    df_bd.columns = df_bd.columns.str.upper()
    columna_dieta = columna_dieta.upper()

    if "PLATOS" not in df_bd.columns or columna_dieta not in df_bd.columns:
        st.error("La base de datos no contiene las columnas necesarias ('PLATOS' y la dieta seleccionada).")
        return None

    dicc_sustituciones = dict(zip(df_bd["PLATOS"].astype(str).str.upper(), df_bd[columna_dieta].astype(str)))
    
    df_menu_sustituido = df_menu.applymap(lambda x: dicc_sustituciones.get(str(x).upper(), x))
    return df_menu_sustituido

# Procesamiento
if archivo_menu and archivo_bd:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(archivo_menu.name)[1]) as tmp:
        tmp.write(archivo_menu.read())
        tmp_path = tmp.name

    if archivo_menu.name.endswith(".pdf"):
        df_menu = extraer_tabla_pdf(tmp_path)
    else:
        df_menu = pd.read_excel(tmp_path)

    if df_menu is not None:
        df_bd = pd.read_excel(archivo_bd)
        df_resultado = aplicar_sustituciones(df_menu, df_bd, dieta_seleccionada)

        if df_resultado is not None:
            st.success("Menú adaptado correctamente.")
            buffer = BytesIO()
            df_resultado.to_excel(buffer, index=False)
            buffer.seek(0)
            st.download_button(
                label="📥 Descargar Excel corregido",
                data=buffer,
                file_name="menu_corregido.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

