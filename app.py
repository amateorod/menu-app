import streamlit as st
import pandas as pd
from io import BytesIO
from openpyxl import load_workbook
import docx

st.set_page_config(page_title="Adaptador Word→Excel", layout="centered")
st.title("🥗 Adaptador de Menús usando Word como base de datos")

# Función para extraer la tabla del documento Word y convertirla en DataFrame
def cargar_tabla_docx(docx_file):
    doc = docx.Document(docx_file)
    for table in doc.tables:
        data = []
        for row in table.rows:
            data.append([cell.text.strip() for cell in row.cells])
        df = pd.DataFrame(data[1:], columns=data[0])
        return df
    return None

# Subida del menú Excel
menu_excel = st.file_uploader("📤 Sube el archivo Excel del menú (hoja 'Menu sin Recomendación')", type=["xlsx"])

# Subida del documento Word con las sustituciones
base_docx = st.file_uploader("📄 Sube el archivo Word con la base de datos de sustituciones", type=["docx"])

if menu_excel and base_docx:
    try:
        df_base = cargar_tabla_docx(base_docx)
        columnas_dietas = [col for col in df_base.columns if col.upper() != "PLATOS"]
        dieta = st.selectbox("🩺 Selecciona la dieta", columnas_dietas)
    except Exception as e:
        st.error(f"❌ Error al procesar el archivo Word: {e}")
        st.stop()

    if st.button("Aplicar cambios"):
        try:
            wb = load_workbook(menu_excel)
            if "Menu sin Recomendación" not in wb.sheetnames:
                st.error("❌ No se encontró la hoja 'Menu sin Recomendación'.")
                st.stop()

            ws = wb["Menu sin Recomendación"]

            sustituciones = dict(zip(df_base["PLATOS"], df_base[dieta]))

            for fila in ws.iter_rows():
                for celda in fila:
                    if celda.value and isinstance(celda.value, str):
                        plato = celda.value.strip()
                        if plato in sustituciones and sustituciones[plato] != "":
                            celda.value = sustituciones[plato]

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
            st.error(f"❌ Error durante el proceso: {e}")


