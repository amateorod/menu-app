
import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.title("Adaptador automático de menús según tipo de dieta")

def cargar_diccionarios():
    diet_files = [f for f in os.listdir() if f.endswith(".xlsx") and f != "app.py"]
    if not diet_files:
        st.error("No se encontraron archivos .xlsx para las dietas. Asegúrate de subirlos al mismo nivel que app.py.")
        st.stop()

    dietas = {os.path.splitext(f)[0].upper(): f for f in diet_files}
    return dietas

def aplicar_sustituciones(df_original, df_sustituciones):
    sustituciones = dict(zip(df_sustituciones.iloc[:, 0], df_sustituciones.iloc[:, 1]))
    df_modificado = df_original.replace(sustituciones)
    return df_modificado

def main():
    dietas = cargar_diccionarios()
    dieta_seleccionada = st.selectbox("Selecciona el tipo de dieta", list(dietas.keys()))

    archivo_menu = st.file_uploader("Sube el archivo Excel del menú", type=["xlsx"])
    if archivo_menu and dieta_seleccionada:
        try:
            df_menu = pd.read_excel(archivo_menu)
            archivo_sustituciones = dietas[dieta_seleccionada]
            df_sustituciones = pd.read_excel(archivo_sustituciones, sheet_name=dieta_seleccionada.capitalize())

            df_modificado = aplicar_sustituciones(df_menu, df_sustituciones)

            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_modificado.to_excel(writer, index=False, sheet_name='Menú adaptado')

            output.seek(0)
            st.download_button(
                label="Descargar menú adaptado",
                data=output,
                file_name="menu_adaptado.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")

if __name__ == "__main__":
    main()
