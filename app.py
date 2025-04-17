import streamlit as st
import pandas as pd
import openpyxl
from io import BytesIO

# Diccionario de sustituciones
sustituciones = {
    "Salchichas frescas": "Pechuga de pavo al horno",
    "Croquetas de jamón": "Filete de aguja en su jugo",
    "Ensalada césar (lechuga, pollo, queso y salsa césar)": "Ensalada variada con pollo",
    "Olleta alicantina": "legumbres (no lentejas)",
    "Pizza margarita": "pizza sin gluten",
    "Albóndigas con salsa": "Albóndigas sin gluten",
    "Buñuelos de bacalao": "Buñuelos sin gluten (maicena)",
    "Lomo adobado": "Lomo fresco"
}

st.set_page_config(page_title="Adaptador de menús", layout="wide")
st.title("🍽️ Adaptador de menús con IA (sin gluten y otras sustituciones)")

archivo = st.file_uploader("Sube el archivo Excel del menú", type=["xlsx"])

if archivo:
    # Cargar el archivo Excel en memoria
    libro = pd.ExcelFile(archivo)
    hojas = libro.sheet_names
    hoja_seleccionada = st.selectbox("Selecciona la hoja a modificar:", hojas)

    df = pd.read_excel(archivo, sheet_name=hoja_seleccionada, dtype=str)
    df = df.fillna("")  # Evita errores con celdas vacías

    # Aplicar sustituciones
    for original, nuevo in sustituciones.items():
        df = df.applymap(lambda x: x.replace(original, nuevo) if isinstance(x, str) else x)

    st.success("Sustituciones aplicadas correctamente ✅")

    st.dataframe(df)

    # Botón para descargar archivo corregido
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=hoja_seleccionada, index=False)
    output.seek(0)

    st.download_button(
        label="📥 Descargar Excel corregido",
        data=output,
        file_name="menu_corregido.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )




