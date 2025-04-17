import streamlit as st
from openpyxl import load_workbook
import tempfile
import io
import re

st.set_page_config(page_title="🥗 Adaptador de Menús - Sin Gluten y Personalizado")

st.title("🥗 Adaptador de Menús (sin gluten, mantiene diseño original)")
st.write("Sube un archivo Excel con el menú y haremos las sustituciones necesarias manteniendo el formato del archivo.")

uploaded_file = st.file_uploader("📤 Sube tu menú en formato Excel", type=["xlsx"])

# Diccionario de sustituciones
REEMPLAZOS = {
    r"\bsalchichas frescas\b": "pechuga de pavo al horno",
    r"\bcroquetas\b": "filete de aguja en su jugo",
    r"\bensalada césar\b": "ensalada variada con pollo",
    r"\bolleta alicantina\b": "legumbres (no lentejas)",
    r"\bpizza\b": "pizza sin gluten",
    r"\balbóndigas\b": "albóndigas sin gluten",
    r"\bbuñuelos\b": "buñuelos sin gluten (maicena)",
    r"\blomo adobado\b": "lomo fresco",
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

        # Aplicar reemplazos
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str):
                    cell.value = adaptar_valor(cell.value)

        # Guardar a memoria
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        st.success("✅ Menú adaptado con éxito")

        st.download_button(
            label="📥 Descargar menú adaptado",
            data=output,
            file_name="menu_adaptado_personalizado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")



