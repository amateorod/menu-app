import streamlit as st
from openpyxl import load_workbook
import tempfile
import io

st.set_page_config(page_title="🥦 Adaptador de Menús con IA")

st.title("🥦 Adaptador de Menús con IA (con formato original)")
st.write("Sube un archivo Excel con tu menú y lo adaptaremos sin gluten, manteniendo el diseño original.")

uploaded_file = st.file_uploader("📤 Sube tu menú en formato Excel", type=["xlsx"])

def adaptar_valor(valor):
    if valor is None:
        return valor
    texto = str(valor).lower()
    if "lenteja" in texto:
        return "legumbres (no lenteja)"
    if "pasta" in texto and "sin gluten" not in texto:
        return "pasta sin gluten"
    if "pan" in texto and "sin gluten" not in texto:
        return "pan sin gluten"
    if "galleta" in texto and "sin gluten" not in texto:
        return "galleta sin gluten"
    return valor

if uploaded_file:
    try:
        # Cargar el archivo Excel en memoria temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        wb = load_workbook(tmp_path)
        sheetnames = wb.sheetnames
        sheet_to_edit = st.selectbox("📄 Elige la hoja que quieres adaptar", sheetnames)
        ws = wb[sheet_to_edit]

        # Mostrar valores originales (hasta 10 filas)
        st.write("📋 Vista previa original:")
        original_preview = [[cell.value for cell in row] for row in ws.iter_rows(min_row=1, max_row=10)]
        st.dataframe(original_preview)

        # Adaptar celdas
        for row in ws.iter_rows():
            for cell in row:
                if cell.data_type == 's':  # Solo cambiar celdas con texto
                    cell.value = adaptar_valor(cell.value)

        # Guardar a memoria
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        st.success("✅ Menú adaptado con éxito (sin gluten, sin perder formato)")

        st.download_button(
            label="📥 Descargar menú adaptado",
            data=output,
            file_name="menu_adaptado_sin_gluten.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")

