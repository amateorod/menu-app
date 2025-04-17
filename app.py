import streamlit as st
from openpyxl import load_workbook
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
st.title("🍽️ Adaptador de menús con formato original")

archivo = st.file_uploader("📁 Sube el archivo Excel del menú", type=["xlsx"])

if archivo:
    wb = load_workbook(filename=archivo)

    # Mostrar lista de hojas disponibles para elegir
    nombre_hoja = st.selectbox("📄 Elige la hoja del menú a modificar", wb.sheetnames)

    if st.button("🔁 Aplicar sustituciones"):
        hoja = wb[nombre_hoja]

        # Recorrer celdas y aplicar cambios
        for fila in hoja.iter_rows():
            for celda in fila:
                if celda.value and isinstance(celda.value, str):
                    for original, nuevo in sustituciones.items():
                        if original in celda.value:
                            celda.value = celda.value.replace(original, nuevo)

        # Guardar cambios a memoria
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        st.success("✅ Sustituciones aplicadas manteniendo el formato.")
        st.download_button(
            label="📥 Descargar Excel corregido",
            data=output,
            file_name="menu_corregido_formato.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
