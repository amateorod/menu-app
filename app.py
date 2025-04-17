import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Diccionario para asociar cada tipo de dieta con su archivo Excel de sustituciones
dieta_archivos = {
    "Sin gluten": "SIN LACTOSA Y CELIACO.xlsx",
    "Sin lactosa": "SIN LACTOSA Y CELIACO.xlsx",
    "Vegana": "OVOLACTEOVEGETARIANA Y VEGANA.xlsx",
    "Ovolactovegetariana": "OVOLACTEOVEGETARIANA Y VEGANA.xlsx",
    "Sin frutos secos": "SIN FRUTOS SECOS Y LEGUMBRES.xlsx",
    "Sin legumbres": "SIN FRUTOS SECOS Y LEGUMBRES.xlsx"
}

st.title("Adaptador de menús según dieta")

# Selección del tipo de dieta
dieta = st.selectbox("Selecciona el tipo de dieta a aplicar:", list(dieta_archivos.keys()))

# Subida del archivo Excel a modificar
archivo_menu = st.file_uploader("Sube el menú en Excel", type=["xlsx", "xls"])

if archivo_menu:
    df_menu = pd.read_excel(archivo_menu, sheet_name=None)

    # Cargar archivo de sustituciones
    archivo_sustituciones = dieta_archivos[dieta]
    if not os.path.exists(archivo_sustituciones):
        st.error(f"No se encontró el archivo de sustituciones: {archivo_sustituciones}")
    else:
        df_sustituciones = pd.read_excel(archivo_sustituciones)

        # Aplicar cambios a todas las hojas del menú
        hojas_modificadas = {}
        for nombre_hoja, hoja_df in df_menu.items():
            hoja_modificada = hoja_df.copy()
            for index, row in df_sustituciones.iterrows():
                original = str(row.get("Original")).strip().lower()
                nuevo = str(row.get(dieta)).strip()
                if original and nuevo and original != "nan" and nuevo != "nan":
                    hoja_modificada = hoja_modificada.applymap(
                        lambda x: str(x).replace(row["Original"], nuevo) if isinstance(x, str) and row["Original"] in x else x
                    )
            hojas_modificadas[nombre_hoja] = hoja_modificada

        # Guardar resultado en Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for hoja, contenido in hojas_modificadas.items():
                contenido.to_excel(writer, sheet_name=hoja, index=False)
        output.seek(0)

        st.success("Menú adaptado correctamente.")
        st.download_button(
            label="📥 Descargar menú adaptado en Excel",
            data=output,
            file_name="menu_adaptado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

