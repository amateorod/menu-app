
import streamlit as st
import pandas as pd
import os
import tempfile
from openpyxl import load_workbook
from io import BytesIO

# Cargar todas las tablas de sustituciones desde archivos Excel
@st.cache_data
def load_substitution_data():
    files = {
        "Ovolactovegetariana y Vegano": "OVOLACTEOVEGETARIANA Y VEGANA.xlsx",
        "Sin lactosa y Celiaco": "SIN LACTOSA Y CELIACO.xlsx",
        "Sin frutos secos y Legumbres": "SIN FRUTOS SECOS Y LEGUMBRES.xlsx"
    }
    substitutions = {}

    for label, filename in files.items():
        path = os.path.join("data", filename)
        if os.path.exists(path):
            df = pd.read_excel(path, sheet_name="Worksheet")
            for column in df.columns[1:]:
                substitutions[column] = dict(zip(df[df.columns[0]], df[column]))
    
    return substitutions

# Aplicar sustituciones a una hoja
def apply_substitutions(sheet_df, substitutions):
    def substitute_cell(cell_value):
        if isinstance(cell_value, str):
            return substitutions.get(cell_value.strip(), cell_value)
        return cell_value

    return sheet_df.applymap(substitute_cell)

# Interfaz de Streamlit
st.title("Adaptador de menús según dieta")

st.markdown("Sube un menú en Excel y selecciona el tipo de dieta para realizar los cambios necesarios.")

uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if uploaded_file:
    wb = load_workbook(uploaded_file)
    sheet_names = wb.sheetnames
    selected_sheet = st.selectbox("Selecciona la hoja del menú", sheet_names)

    substitutions = load_substitution_data()
    selected_diet = st.selectbox("Selecciona el tipo de dieta", list(substitutions.keys()))

    if st.button("Aplicar cambios"):
        df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
        modified_df = apply_substitutions(df, substitutions[selected_diet])

        # Escribir el resultado en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_original = pd.read_excel(uploaded_file, sheet_name=None)
            for sheet, content in df_original.items():
                if sheet == selected_sheet:
                    modified_df.to_excel(writer, sheet_name=sheet, index=False)
                else:
                    content.to_excel(writer, sheet_name=sheet, index=False)
            writer.save()
        output.seek(0)

        st.success("Menú corregido. Puedes descargarlo abajo.")
        st.download_button(label="📥 Descargar Excel corregido",
                           data=output,
                           file_name="menu_corregido.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
