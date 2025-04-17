import streamlit as st
import pandas as pd
import os
from io import BytesIO
import openpyxl

st.title("Adaptador Automático de Menús por Dietas")

# Cargar todos los archivos Excel que estén en el mismo directorio que app.py
def cargar_bases_de_datos():
    archivos = [f for f in os.listdir() if f.endswith('.xlsx') and f != 'Sin título 1 (documento reparado).xlsx']
    bases = {}
    for archivo in archivos:
        try:
            df = pd.read_excel(archivo)
            columnas = df.columns.str.upper()
            df.columns = columnas  # Asegura mayúsculas
            if 'PLATOS' in columnas:
                for col in columnas:
                    if col != 'PLATOS':
                        bases[col] = df.set_index('PLATOS')[col].dropna().to_dict()
        except Exception as e:
            st.warning(f"No se pudo cargar {archivo}: {e}")
    return bases

bases_sustituciones = cargar_bases_de_datos()

# Mostrar opciones de dieta en mayúsculas
opciones_dietas = sorted(bases_sustituciones.keys())
dieta_seleccionada = st.selectbox("Selecciona una dieta:", opciones_dietas)

archivo_subido = st.file_uploader("Sube el archivo Excel del menú", type=["xlsx"])

if archivo_subido and dieta_seleccionada:
    try:
        libro = openpyxl.load_workbook(archivo_subido)
        if "MENU SIN RECOMENDACIÓN" not in libro.sheetnames:
            st.error("No se encuentra la hoja 'MENU SIN RECOMENDACIÓN'.")
        else:
            hoja = libro["MENU SIN RECOMENDACIÓN"]
            base_sustitucion = bases_sustituciones[dieta_seleccionada]

            for fila in hoja.iter_rows():
                for celda in fila:
                    if celda.value and isinstance(celda.value, str):
                        valor = celda.value.strip().upper()
                        for no_permitido, permitido in base_sustitucion.items():
                            if no_permitido.strip().upper() in valor:
                                celda.value = valor.replace(no_permitido.strip().upper(), permitido.strip().upper())

            buffer = BytesIO()
            libro.save(buffer)
            buffer.seek(0)

            st.success("Archivo corregido con éxito. Descárgalo abajo:")
            st.download_button("📥 Descargar menú corregido", buffer, file_name="menu_corregido.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
