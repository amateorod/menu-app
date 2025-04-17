import streamlit as st
import pandas as pd
import os
from io import BytesIO
from openpyxl import load_workbook
import docx

st.set_page_config(page_title="Adaptador de Menús Word→Excel", layout="centered")
st.title("🍽️ Adaptador de Menús con base en Word")

# Función para extraer tabla del Word y convertirla en DataFrame
def cargar_tabla_docx(docx_file):
    doc = docx.Document(docx_file)
    data = []
    for table in doc.tables:
        for i, row in enumerate(table.rows):
            row_data = [cell.text.strip() for cell in row.cells]
            data.append(row_data)
    df = pd.DataFrame(data[1:], columns=data[0])
    return df

# Subida del archivo de menú
menu_excel = st.file_uploader("📤 Sube el archivo Excel del menú (hoja 'Menu sin Recomendación')", type=["xlsx"])

# Subida del archivo Word con la base de sustituciones
base_word = st.file_uploader("📄 Sube la base de datos de sustituciones (.docx)", type=["docx"])

if menu_excel and base_word:
    # Cargar base desde Word
    try:
        df_base = cargar_tabla_docx(base_word)
        columnas = [col.upper() for col in df_base.columns if col.upper() != "PLATOS"]
        dieta = st.selectbox("🩺 Selecciona la dieta a aplicar", columnas)
    except Exception as e:
        st.error(f"❌ Error al procesar el documento Word: {e}")
        st.stop()

    if st.button("Aplicar cambios"):
        try:
            wb = load_workbook(menu_excel)
            if "Menu sin Recomendación" not in wb.sheetnames:
                st.error("❌ La hoja 'Menu sin Recomendación' no se encuentra en el Excel.")
                st.stop()

            ws = wb["Menu sin Recomendación"]

            # Crear diccionario de sustituciones
            sustituciones = dict(zip(df_base["PLATOS"], df_base[dieta]))

            # Aplicar sustituciones manteniendo formato
            for fila in ws.iter_rows():
                for celda in fila:
                    if celda.value and isinstance(celda.value, str):
                        if celda.value.strip() in sustituciones and sustituciones[celda.value.strip()] != "":
                            celda.value = sustituciones[celda.value.strip()]

            output = BytesIO()
            wb.save(output)
            output.seek(0)

            st.success("✅ Cambios aplicados correctamente.")
            st.download_button(
                label="📥 Descargar menú corregido",
                data=output,
                file_name="menu_corregido.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"❌ Error al aplicar cambios: {e}")

