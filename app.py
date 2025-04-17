import streamlit as st
import pandas as pd
from io import BytesIO
from openpyxl import load_workbook
import docx

st.set_page_config(page_title="Adaptador de Menús línea por línea", layout="centered")
st.title("🥗 Adaptador de Menús por Dieta (desde Word, línea por línea)")

# Función para extraer la tabla del Word como DataFrame
def cargar_tabla_docx(docx_file):
    doc = docx.Document(docx_file)
    for table in doc.tables:
        data = []
        for row in table.rows:
            data.append([cell.text.strip() for cell in row.cells])
        df = pd.DataFrame(data[1:], columns=data[0])
        return df
    return None

# Subir archivos
menu_excel = st.file_uploader("📤 Sube el menú en Excel (hoja 'Menu sin Recomendación')", type=["xlsx"])
base_docx = st.file_uploader("📄 Sube el archivo Word con la base de sustituciones", type=["docx"])

if menu_excel and base_docx:
    try:
        df_base = cargar_tabla_docx(base_docx)
        columnas_dietas = [col for col in df_base.columns if col.upper() != "PLATOS"]
        dieta = st.selectbox("🩺 Selecciona la dieta a aplicar", columnas_dietas)
    except Exception as e:
        st.error(f"❌ Error al procesar el Word: {e}")
        st.stop()

    if st.button("Aplicar cambios"):
        try:
            wb = load_workbook(menu_excel)
            if "Menu sin Recomendación" not in wb.sheetnames:
                st.error("❌ No se encuentra la hoja 'Menu sin Recomendación'.")
                st.stop()

            ws = wb["Menu sin Recomendación"]

            # Crear diccionario limpio con sustituciones
            sustituciones = {
                str(k).strip(): str(v).strip()
                for k, v in zip(df_base["PLATOS"], df_base[dieta])
                if pd.notna(k) and pd.notna(v) and str(v).strip() != ""
            }

            cambios = 0
            for fila in ws.iter_rows():
                for celda in fila:
                    if celda.value and isinstance(celda.value, str):
                        lineas = celda.value.strip().split("\n")
                        nuevas_lineas = []
                        for linea in lineas:
                            linea_limpia = linea.strip()
                            if linea_limpia in sustituciones:
                                nuevas_lineas.append(sustituciones[linea_limpia])
                                cambios += 1
                            else:
                                nuevas_lineas.append(linea)
                        celda.value = "\n".join(nuevas_lineas)

            if cambios == 0:
                st.warning("⚠️ No se encontraron platos para sustituir.")
            else:
                output = BytesIO()
                wb.save(output)
                output.seek(0)
                st.success(f"✅ Sustituciones aplicadas: {cambios}")
                st.download_button(
                    label="📥 Descargar menú corregido",
                    data=output,
                    file_name="menu_corregido.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        except Exception as e:
            st.error(f"❌ Error aplicando sustituciones: {e}")



