import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Adaptador de Menús", layout="centered")

st.title("🥗 Adaptador de Menús según Dietas")

st.markdown("Sube un archivo PDF o Excel con el menú, selecciona la dieta a aplicar y descarga el resultado adaptado.")

uploaded_file = st.file_uploader("📤 Sube el menú en formato Excel", type=["xlsx"])

# Detectar archivos Excel que contienen sustituciones
db_files = [f for f in os.listdir() if f.endswith(".xlsx") and f != "Sin título 1 (documento reparado).xlsx"]
dietas_disponibles = set()

for f in db_files:
    df = pd.read_excel(f, sheet_name=0)
    for col in df.columns:
        if col != "PLATOS":
            dietas_disponibles.add(col.upper())

dietas_ordenadas = sorted(list(dietas_disponibles))
dieta_seleccionada = st.selectbox("🔄 Selecciona el tipo de dieta", options=dietas_ordenadas)

if uploaded_file and dieta_seleccionada:
    menu_df = pd.read_excel(uploaded_file, sheet_name=None)
    hoja_menu = list(menu_df.keys())[0]
    menu = menu_df[hoja_menu]

    reemplazos = {}

    # Buscar archivo de base de datos que tenga la columna con la dieta seleccionada
    db_df = None
    for f in db_files:
        df = pd.read_excel(f)
        columnas = [c.upper() for c in df.columns]
        if "PLATOS" in columnas and dieta_seleccionada.upper() in columnas:
            df.columns = columnas  # asegurarse de que todas estén en mayúsculas
            db_df = df
            break

    if db_df is not None:
        reemplazos = dict(zip(db_df["PLATOS"], db_df[dieta_seleccionada.upper()]))

        # Hacer una copia del DataFrame original
        menu_modificado = menu.copy()

        for col in menu.columns:
            menu_modificado[col] = menu[col].replace(reemplazos)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            menu_modificado.to_excel(writer, index=False, sheet_name=hoja_menu)
        output.seek(0)

        st.download_button(
            label="📥 Descargar menú adaptado",
            data=output,
            file_name="menu_adaptado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("No se encontró una base de datos que contenga la dieta seleccionada.")

