
import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.title("Adaptador de menús según dieta")

# Diccionario actualizado con archivos y hojas
hojas_archivos = {
    "Vegana": ("OVOLACTEOVEGETARIANA Y VEGANA.xlsx", "Vegana"),
    "Ovolactovegetariana": ("OVOLACTEOVEGETARIANA Y VEGANA.xlsx", "Ovolactovegetariana"),
    "Sin frutos secos": ("SIN FRUTOS SECOS Y LEGUMBRES.xlsx", "Sin frutos secos"),
    "Sin legumbres": ("SIN FRUTOS SECOS Y LEGUMBRES.xlsx", "Sin legumbres"),
    "Celiaco": ("SIN LACTOSA Y CELIACO.xlsx", "Celiaco"),
    "Sin lactosa": ("SIN LACTOSA Y CELIACO.xlsx", "Sin lactosa")
}

# Selección de tipo de dieta
tipo_dieta = st.selectbox("Selecciona el tipo de dieta", list(hojas_archivos.keys()))

archivo_usuario = st.file_uploader("Sube el archivo Excel del menú", type=["xlsx"])

if archivo_usuario and tipo_dieta:
    try:
        df_usuario = pd.read_excel(archivo_usuario)

        archivo_base, hoja_base = hojas_archivos[tipo_dieta]
        ruta_archivo = os.path.join("data", archivo_base)
        df_base = pd.read_excel(ruta_archivo, sheet_name=hoja_base)

        # Diccionario de sustituciones a partir del Excel
        sustituciones = dict(zip(df_base["original"], df_base["sustituto"]))

        df_corregido = df_usuario.replace(sustituciones, regex=True)

        # Descargar el archivo corregido
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_corregido.to_excel(writer, index=False, sheet_name="Menú corregido")
        output.seek(0)

        st.success("Archivo procesado correctamente.")
        st.download_button(
            label="Descargar menú corregido",
            data=output,
            file_name="menu_corregido.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
