import streamlit as st
import tempfile
import os
import subprocess
import re
from openpyxl import load_workbook

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

def convertir_a_pdf_con_libreoffice(archivo_excel, carpeta_salida):
    try:
        subprocess.run([
            "soffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", carpeta_salida,
            archivo_excel
        ], check=True)
        return True
    except Exception as e:
        st.error(f"Error al convertir a PDF con LibreOffice: {e}")
        return False

st.title("🍽️ Adaptador de Menús + PDF con LibreOffice")

uploaded_file = st.file_uploader("📤 Sube tu archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    with tempfile.TemporaryDirectory() as tmpdir:
        original_excel_path = os.path.join(tmpdir, "original.xlsx")
        with open(original_excel_path, "wb") as f:
            f.write(uploaded_file.read())

        wb = load_workbook(original_excel_path)
        hoja_nombres = wb.sheetnames
        hoja_seleccionada = st.selectbox("📄 Elige la hoja del menú", hoja_nombres)
        ws = wb[hoja_seleccionada]

        for fila in ws.iter_rows():
            for celda in fila:
                if isinstance(celda.value, str):
                    celda.value = adaptar_valor(celda.value)

        modificado_path = os.path.join(tmpdir, "menu_modificado.xlsx")
        wb.save(modificado_path)

        pdf_convertido = convertir_a_pdf_con_libreoffice(modificado_path, tmpdir)

        with open(modificado_path, "rb") as f:
            st.download_button("📥 Descargar Excel corregido", f, file_name="menu_adaptado.xlsx")

        if pdf_convertido:
            pdf_path = os.path.join(tmpdir, "menu_modificado.pdf")
            with open(pdf_path, "rb") as f:
                st.download_button("📄 Descargar PDF (con formato)", f, file_name="menu_adaptado.pdf")




