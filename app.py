import streamlit as st
import pandas as pd
import openpyxl
from openpyxl.styles import NamedStyle
import os
from io import BytesIO

st.title("Adaptador automático de menús según dieta")

# Paso 1: Selección de tipo de dieta
dieta = st.selectbox(
    "Selecciona el tipo de dieta",
    ["VEGANA", "OVOLACTEOVEGETARIANA", "CELIACO", "SIN LACTOSA", "SIN FRUTOS SECOS", "SIN LEGUMBRES"]
)

# Paso 2: Subida del archivo Excel del menú
menu_file = st.file_uploader("Sube el archivo Excel con el menú (debe tener una hoja llamada 'Menu sin Recomendación')", type=["xlsx"])

if menu_file:
    try:
        # Cargar el Excel del menú con formato
        original_wb = openpyxl.load_workbook(menu_file)
        if "Menu sin Recomendación" not in original_wb.sheetnames:
            st.error("No se encuentra la hoja 'Menu sin Recomendación' en el archivo subido.")
        else:
            menu_ws = original_wb["Menu sin Recomendación"]

            # Convertir la hoja en DataFrame
            data = menu_ws.values
            headers = next(data)
            df_menu = pd.DataFrame(data, columns=headers)

            # Buscar la base de datos de sustituciones correspondiente
            archivos = os.listdir()
            archivo_dieta = None
            for archivo in archivos:
                if archivo.endswith(".xlsx") and dieta in archivo.upper():
                    archivo_dieta = archivo
                    break

            if not archivo_dieta:
                st.error(f"No se encontró una base de datos que contenga la dieta: {dieta}")
            else:
                # Cargar el archivo de sustituciones
                df_sustituciones = pd.read_excel(archivo_dieta)
                if "PLATOS" not in df_sustituciones.columns or dieta not in df_sustituciones.columns:
                    st.error(f"El archivo de sustituciones no contiene las columnas necesarias: 'PLATOS' y '{dieta}'")
                else:
                    # Crear diccionario de sustitución
                    sustituciones = dict(zip(df_sustituciones["PLATOS"], df_sustituciones[dieta]))

                    # Aplicar sustituciones a todo el DataFrame
                    df_corregido = df_menu.replace(sustituciones)

                    # Escribir los datos corregidos en la misma hoja (manteniendo el formato)
                    for row_idx, row in enumerate(df_corregido.itertuples(index=False), start=2):  # Empieza en la fila 2 (asumiendo encabezado en 1)
                        for col_idx, value in enumerate(row, start=1):
                            cell = menu_ws.cell(row=row_idx, column=col_idx)
                            cell.value = value

                    # Guardar el archivo en memoria y permitir descarga
                    output = BytesIO()
                    original_wb.save(output)
                    output.seek(0)

                    st.success("Archivo corregido con éxito.")
                    st.download_button("Descargar menú corregido", output, file_name="menu_corregido.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
