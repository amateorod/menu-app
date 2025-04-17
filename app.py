import streamlit as st
from openpyxl import load_workbook
import tempfile
import io
import re

st.set_page_config(page_title="🍽️ Adaptador de Menús Avanzado")

st.title("🍽️ Adaptador de Menús (sustituciones avanzadas)")
st.write("Sube tu menú en Excel (.xlsx). Esta app cambiará alimentos concretos por otros manteniendo el formato del archivo.")

uploaded_file = st.file_uploader("📤 Sube tu archivo Excel", type=["xlsx"])

# Diccionario de sustituciones exactas (en minúsculas)
REEMPLAZOS = {
    "salchichas frescas": "Pechuga de pavo al horno",
    "croquetas de jamón": "Filete de aguja en su jugo",
    "ensalada césar (lechuga, pollo, queso y salsa césar)": "Ensalada variada con pollo",
    "olleta alicantina": "Legumbres (no lentejas)",
    "pizza margarita": "Pizza sin gluten",
    "albóndigas con salsa": "Albóndigas sin gluten",
    "buñuelos de bacalao": "Buñuelos sin gluten (maicena)",
    "lomo adobado": "Lomo fresco",
}

def adaptar_valor(valor):
    if valor is None or not isinstance(valor, str):
        return valor

    texto_modificado = valor

    for buscar, reemplazo in REEMPLAZOS.items():
        patron = re.compile(re.escape(buscar), re.IGNORECASE)
        texto_modificado = patron.sub(reemplazo, texto_modificado)

    return texto_modificado

if uploaded_file:
    try:
        # Guardar archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        # Cargar libro de Excel
        wb = load_workbook(tmp_path)
        hojas = wb.sheetnames
        hoja_seleccionada = st.selectbox("📄 Selecciona la hoja que quieres adaptar", hojas)
        ws = wb[hoja_seleccionada]

        # Vista previa antes
        st.write("🔍 Vista previa antes de aplicar los cambios:")
        vista_previa = [[cell.value for cell in row] for row in ws.iter_rows(min_row=1, max_row=10)]
        st.dataframe(vista_previa)

        # Aplicar sustituciones
        for fila in ws.iter_rows():
            for celda in fila:
                if isinstance(celda.value, str):
                    celda.value = adaptar_valor(celda.value)

        # Guardar archivo modificado en memoria
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        st.success("✅ Menú adaptado con éxito.")

        st.download_button(
            label="📥 Descargar Excel adaptado",
            data=output,
            file_name="menu_adaptado_sustituciones.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st




