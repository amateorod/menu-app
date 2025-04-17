import streamlit as st
import pandas as pd
import os
import fitz  # PyMuPDF
import tempfile
import tabula
from io import BytesIO

# Función para extraer tablas de PDF y convertirlas a DataFrame
def pdf_to_dataframe(pdf_path):
    try:
        dfs = tabula.read_pdf(pdf_path, pages='all', multiple_tables=False)
        if dfs:
            return dfs[0]
        else:
            return None
    except Exception as e:
        st.error(f"Error al extraer la tabla del PDF: {e}")
        return None

# Cargar bases de datos de sustituciones
def cargar_bases_de_datos():
    bases = {}
    for file in os.listdir():
        if file.endswith('.xlsx') and file != "menu_corregido.xlsx":
            df = pd.read_excel(file)
            if 'PLATOS' in df.columns:
                df.columns = [col.upper() for col in df.columns]
                bases[file.replace(".xlsx", "").upper()] = df
    return bases

# Función para aplicar las sustituciones
def aplicar_sustituciones(df_menu, df_sustituciones, tipo_dieta):
    df_menu_corr = df_menu.copy()
    sustituciones = dict(zip(df_sustituciones['PLATOS'].str.upper(), df_sustituciones[tipo_dieta].str.upper()))
    for i, row in df_menu.iterrows():
        for col in df_menu.columns:
            celda = str(row[col]).upper()
            for original, reemplazo in sustituciones.items():
                if original in celda:
                    celda = celda.replace(original, reemplazo)
            df_menu_corr.at[i, col] = celda
    return df_menu_corr

st.title("🧠 App de adaptación dietética automática desde PDF")

archivo_pdf = st.file_uploader("Sube un archivo PDF con el menú", type=["pdf"])
tipo_dieta = st.selectbox("Selecciona el tipo de dieta", ["VEGANA", "OVOLACTEOVEGETARIANA", "CELIACO", "SIN LACTOSA", "SIN HUEVO", "SIN FRUTOS SECOS", "SIN LEGUMBRES", "SIN CERDO"])

if archivo_pdf:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(archivo_pdf.read())
        ruta_pdf = tmp_file.name

    st.success("PDF subido correctamente. Procesando...")

    df_menu = pdf_to_dataframe(ruta_pdf)

    if df_menu is not None:
        bases = cargar_bases_de_datos()
        base_encontrada = None

        for nombre, base in bases.items():
            if tipo_dieta in base.columns:
                base_encontrada = base
                break

        if base_encontrada is not None:
            df_corregido = aplicar_sustituciones(df_menu, base_encontrada, tipo_dieta)

            # Descargar Excel corregido
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_corregido.to_excel(writer, index=False, sheet_name="Menú Corregido")
            st.download_button("📥 Descargar menú corregido (Excel)", output.getvalue(), file_name="menu_corregido.xlsx")
        else:
            st.error("No se encontró una base de datos compatible con la dieta seleccionada.")
    else:
        st.error("No se pudo extraer una tabla del PDF.")


