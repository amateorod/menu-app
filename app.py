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

# Interfaz Streamlit
st.set_page_config(page_title="Adaptador de menús", layout="wide")
st.title("🍽️ Adaptador de menús por tipo de dieta")

archivo = st.file_uploader("📁 Sube tu archivo Excel de menú", type=["xlsx"])

if archivo:
    try:
        wb = load_workbook(filename=archivo)
        hojas = wb.sheetnames

        hoja_nombre = st.selectbox("📄 Selecciona la hoja del menú a modificar:", hojas)

        tipo_dieta = st.selectbox(
            "⚙️ Selecciona el tipo de adaptación que deseas aplicar:",
            list(sustituciones_dietas.keys())
        )

        if st.button("🔁 Aplicar adaptación"):
            hoja = wb[hoja_nombre]
            sustituciones = sustituciones_dietas[tipo_dieta]

            cambios = 0
            for fila in hoja.iter_rows():
                for celda in fila:
                    if celda.value and isinstance(celda.value, str):
                        for original, nuevo in sustituciones.items():
                            if original in celda.value:
                                celda.value = celda.value.replace(original, nuevo)
                                cambios += 1

            output = BytesIO()
            wb.save(output)
            output.seek(0)

            st.success(f"✅ Adaptación '{tipo_dieta}' aplicada. Se han realizado {cambios} cambios.")
            st.download_button(
                label="📥 Descargar Excel adaptado",
                data=output,
                file_name=f"menu_adaptado_{tipo_dieta.lower().replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")

