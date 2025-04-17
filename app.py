import streamlit as st
from openpyxl import load_workbook
import tempfile
import io

st.set_page_config(page_title="🍽️ Adaptador de Menús Avanzado")

st.title("🍽️ Adaptador de Menús (sustituciones personalizadas)")
st.write("Sube tu archivo Excel con el menú. Cambiamos alimentos concretos por otros manteniendo el formato original.")

uploaded_file = st.file_uploader("📤 Sube tu archivo Excel", type=["xlsx"])

# Diccionario de sustituciones en minúsculas
REEMPLAZOS = {
    "salchichas frescas": "pechuga de pavo al horno",
    "croquetas": "filete de aguja en su jugo",
    "ensalada césar": "ensalada variada con pollo",
    "olleta alicantina": "legumbres (no lentejas)",
    "pizza": "pizza sin gluten",
    "albóndigas": "albóndigas sin gluten",
    "buñuelos": "buñuelos sin gluten (maicena)",
    "lomo adobado": "lomo fresco",
}

def adaptar_valor(valor):
    if valor is None:
        return valor
    original = str(valor)
    modificado = original
    texto_buscado = original.lower()
    for buscar, reemplazo in REEMPLAZOS.items():
        if buscar in texto_buscado:
            # Sustituimos conservando el formato original
            indices = texto_buscado.find(buscar)
            if indices != -1:
                modificado = modificado[:indices] + reemplazo + modificado[indices + len(buscar):]
                # Actualizamos texto_buscado para siguientes búsquedas
                texto_buscado = modificado.lower()
    return modificado

if uploaded_file:
    try:
        # Guardar archivo temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        # Cargar Excel
        wb = load_workbook(tmp_path)
        sheetnames = wb.sheetnames
        sheet_to_edit = st.selectbox("📄 Elige la hoja que quieres adaptar", sheetnames)
        ws = wb[sheet_to_edit]

        st.write("📋 Vista previa antes de cambios:")
        preview = [[cell.value for cell in row] for row in ws.iter_rows(min_row=1, max_row=10)]
        st.dataframe(preview)

        # Aplicar cambios
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str):
                    cell.value = adaptar_valor(cell.value)

        # Guardar Excel modificado en memoria
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        st.success("✅ Sustituciones realizadas correctamente.")

        st.download_button(
            label="📥 Descargar Excel adaptado",
            data=output,
            file_name="menu_adaptado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")




