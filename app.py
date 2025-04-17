import streamlit as st
from openpyxl import load_workbook
from io import BytesIO

# Diccionarios de sustituciones por tipo de dieta
sustituciones_dietas = {
    "Sin gluten": {
        "Pizza margarita": "Pizza sin gluten",
        "Albóndigas con salsa": "Albóndigas sin gluten",
        "Buñuelos de bacalao": "Buñuelos sin gluten (maicena)",
        "Pan": "Pan sin gluten",
        "Pasta": "Pasta sin gluten"
    },
    "Sin lactosa": {
        "Queso": "Queso sin lactosa",
        "Yogur": "Yogur vegetal",
        "Leche": "Bebida vegetal",
        "Flan": "Postre vegetal"
    },
    "Sin huevo": {
        "Tortilla": "Tortilla sin huevo (vegana)",
        "Mayonesa": "Mayonesa vegana",
        "Bizcocho": "Bizcocho sin huevo"
    },
    "Sin cerdo": {
        "Jamón": "Pechuga de pavo",
        "Lomo adobado": "Lomo fresco",
        "Salchichas frescas": "Pechuga de pollo"
    }
}

st.set_page_config(page_title="Adaptador de menús", layout="wide")
st.title("🍽️ Adaptador de menús por tipo de dieta")

archivo = st.file_uploader("📁 Sube el archivo Excel del menú", type=["xlsx"])

if archivo:
    wb = load_workbook(filename=archivo)

    # Selección de hoja
    hoja_nombre = st.selectbox("📄 Elige la hoja del menú", wb.sheetnames)

    # Selección de adaptación dietética
    tipo_dieta = st.selectbox("🍽️ Elige el tipo de adaptación dietética", list(sustituciones_dietas.keys()))

    if st.button("🔁 Aplicar adaptación"):
        hoja = wb[hoja_nombre]
        sustituciones = sustituciones_dietas[tipo_dieta]

        for fila in hoja.iter_rows():
            for celda in fila:
                if celda.value and isinstance(celda.value, str):
                    for original, nuevo in sustituciones.items():
                        if original in celda.value:
                            celda.value = celda.value.replace(original, nuevo)

        output = BytesIO()
        wb.save(output)
        output.seek(0)

        st.success(f"✅ Menú adaptado a: {tipo_dieta}")
        st.download_button(
            label="📥 Descargar Excel adaptado",
            data=output,
            file_name=f"menu_adaptado_{tipo_dieta.lower().replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

