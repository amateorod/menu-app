import streamlit as st
from openpyxl import load_workbook
import tempfile
import io
import re

st.set_page_config(page_title="🥦 Adaptador de Menús con IA")

st.title("🥦 Adaptador de Menús con IA (sin gluten, manteniendo formato)")
st.write("Sube tu menú en Excel. Reemplazamos alimentos concretos (como lentejas o pasta ECO) manteniendo el resto del texto y el diseño original.")

uploaded_file = st.file_uploader("📤 Sube tu menú en formato Excel", type=["xlsx"])

# Reemplazos personalizados
REEMPLAZOS = {
    r"\blentejas\b": "legumbres (no lenteja)",
    r"\bpasta eco\b": "pasta sin gluten",
    r"\bpasta\b": "pasta sin gluten",
    r"\bpan\b": "pan sin gluten",
    r"\bgalleta\b": "galleta sin gluten"
}

def adaptar_valor(valor):
    if valor is None:
        return valor
    texto = str(valor)
    for patron, reemplazo in REEMPLAZOS.items():
        texto = re.sub(patron, reemplazo, texto, flags=re.IGNORECASE)
    return texto

if uploaded_file:
    try:
        # Guardar archivo subido en una ruta temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        wb = load_workbook(tmp_path)
        sheetnames = wb.sheetnames
        sheet_to_edit = st.selectbox("📄 Elige la hoja que quieres adaptar", sheetnames)
        ws = wb[sheet_to_edit]

        st.write("📋 Vista previa original:")
        preview = [[cell.value for cell in row] for row in ws.iter_rows(min_row=1, max_row=10)]
        st.dataframe(preview)

        # Reemplazar palabras en celdas de texto
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str):
                    cell.value = adaptar_valor(cell.value)

        # Guardar archivo modificado
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        st.success("✅ Menú adaptado sin gluten, manteniendo el formato original")

        st.download_button(
            label="📥 Descargar menú adaptado",
            data=output,
            file_name="menu_adaptado_sin_gluten.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")


