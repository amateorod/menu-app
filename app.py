import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Obtener lista de archivos Excel en el mismo directorio
diet_files = [f for f in os.listdir() if f.endswith('.xlsx') and f != 'app.py']

# Crear diccionario: nombre en mayúsculas (sin extensión) -> nombre del archivo
diet_options = {os.path.splitext(f)[0].upper(): f for f in diet_files}

st.title("Adaptador de Menús según Dietas")

uploaded_file = st.file_uploader("Sube el menú en Excel", type=["xlsx", "xls"])
dieta_seleccionada = st.selectbox("Selecciona el tipo de dieta", list(diet_options.keys()))

if uploaded_file and dieta_seleccionada:
    try:
        df_menu = pd.read_excel(uploaded_file, sheet_name=None)
        file_dieta = diet_options[dieta_seleccionada]
        df_dieta = pd.read_excel(file_dieta)

        # Aplicar sustituciones a cada hoja
        for hoja in df_menu:
            df_menu[hoja].replace(dict(zip(df_dieta.iloc[:, 0], df_dieta.iloc[:, 1])), inplace=True)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for hoja, datos in df_menu.items():
                datos.to_excel(writer, sheet_name=hoja, index=False)
        output.seek(0)

        st.success("Archivo modificado correctamente.")
        st.download_button(
            label="Descargar menú corregido",
            data=output,
            file_name="menu_corregido.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")

