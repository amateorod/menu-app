
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Adaptador automático de menús", layout="centered")

st.title("Adaptador automático de menús según tipo de dieta")

# Cargar archivos Excel disponibles (en el mismo directorio que app.py)
import os
archivos_excel = [f for f in os.listdir() if f.endswith(".xlsx")]

# Detectar dietas según columnas dentro de los archivos
def detectar_dietas(archivos):
    dietas = set()
    for archivo in archivos:
        try:
            df = pd.read_excel(archivo)
            for col in df.columns[2:]:  # Saltamos SEMANAS y PLATOS
                dietas.add(col.upper())
        except Exception as e:
            print(f"No se pudo leer {archivo}: {e}")
    return sorted(list(dietas))

dietas_disponibles = detectar_dietas(archivos_excel)

dieta_seleccionada = st.selectbox("Selecciona el tipo de dieta", dietas_disponibles)

archivo_menu = st.file_uploader("Sube el archivo Excel del menú", type=["xlsx"])

if archivo_menu and dieta_seleccionada:
    try:
        df_menu = pd.read_excel(archivo_menu)
        if dieta_seleccionada not in df_menu.columns.str.upper():
            st.error(f"No se encontró la columna '{dieta_seleccionada}' en el archivo.")
        else:
            # Encontrar la columna real (con mayúsculas y minúsculas exactas)
            columna_real = [col for col in df_menu.columns if col.upper() == dieta_seleccionada][0]
            df_corregido = df_menu.copy()
            df_corregido["PLATOS"] = df_corregido[columna_real]

            # Exportar a Excel
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df_corregido.to_excel(writer, index=False, sheet_name="Menú corregido")
            output.seek(0)

            st.download_button("Descargar menú corregido", output, file_name="menu_corregido.xlsx")
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
