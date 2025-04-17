import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="🥦 Adaptador de Menús con IA")

st.title("🥦 Adaptador de Menús con IA")
st.write("Sube tu archivo Excel y genera una versión adaptada sin gluten para niños.")

# Subida del archivo
uploaded_file = st.file_uploader("📤 Sube tu menú en formato Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Leer el Excel
    try:
        xl = pd.ExcelFile(uploaded_file)
        sheet_names = xl.sheet_names
        sheet = st.selectbox("📄 Selecciona la hoja a adaptar", sheet_names)
        df = xl.parse(sheet)

        st.write("📋 Vista previa del menú original:")
        st.dataframe(df)

        # Procesamiento
        df_modificado = df.copy()

        def adaptar_celda(celda):
            if pd.isna(celda):
                return celda
            texto = str(celda).lower()
            if "lenteja" in texto:
                return "legumbres (no lenteja)"
            if "pasta" in texto and "sin gluten" not in texto:
                return "pasta sin gluten"
            if "pan" in texto and "sin gluten" not in texto:
                return "pan sin gluten"
            if "galleta" in texto and "sin gluten" not in texto:
                return "galleta sin gluten"
            return celda

        df_modificado = df_modificado.applymap(adaptar_celda)

        st.write("✅ Menú adaptado sin gluten:")
        st.dataframe(df_modificado)

        # Preparar descarga
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_modificado.to_excel(writer, index=False, sheet_name="Menú sin gluten")
        output.seek(0)

        st.download_button(
            label="📥 Descargar menú adaptado",
            data=output,
            file_name="menu_sin_gluten.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error al leer el archivo: {e}")
