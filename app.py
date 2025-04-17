import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Adaptador de Menús", layout="centered")

st.title("🍽️ Adaptador de Menús según tipo de dieta")

uploaded_file = st.file_uploader("Sube el archivo Excel del menú", type=["xlsx"])
tipo_dieta = st.selectbox(
    "Selecciona el tipo de dieta",
    ("VEGANO", "OVOLACTOVEGETARIANO", "SIN LACTOSA", "CELIACO", "SIN HUEVO", "SIN FRUTOS SECOS", "SIN LEGUMBRES")
)

if uploaded_file:
    try:
        # Cargar el menú original
        menu_df = pd.read_excel(uploaded_file, engine="openpyxl")

        # Cargar todas las bases de datos de sustitución
        bd_archivos = [f for f in os.listdir() if f.endswith(".xlsx") and tipo_dieta in f.upper()]
        if not bd_archivos:
            st.error(f"No se encontró una base de datos que incluya '{tipo_dieta}' en su nombre.")
        else:
            bd_path = bd_archivos[0]
            bd_df = pd.read_excel(bd_path, engine="openpyxl")

            # Buscar la columna 'platos' y la de la dieta elegida
            if "platos" not in bd_df.columns or tipo_dieta not in bd_df.columns:
                st.error("La base de datos no contiene las columnas necesarias ('platos' y la dieta seleccionada).")
            else:
                # Crear un diccionario de sustituciones
                sustituciones = dict(zip(bd_df["platos"], bd_df[tipo_dieta]))

                # Aplicar las sustituciones en todo el DataFrame del menú
                menu_modificado = menu_df.replace(sustituciones, regex=False)

                # Descargar Excel
                output = BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    menu_modificado.to_excel(writer, index=False, sheet_name="Menú adaptado")
                output.seek(0)

                st.success("Menú adaptado correctamente. Puedes descargarlo a continuación:")
                st.download_button(
                    label="📥 Descargar Excel adaptado",
                    data=output,
                    file_name="menu_adaptado.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")

