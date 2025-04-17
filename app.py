import streamlit as st
import pandas as pd
from io import BytesIO
import os

# Mapeo de las dietas con sus archivos correspondientes
DIET_FILES = {
    "Celiaco": "CELIACO.xlsx",
    "Sin lactosa": "SIN LACTOSA.xlsx",
    "Sin frutos secos": "SIN FRUTOS SECOS.xlsx",
    "Sin legumbres": "SIN LEGUMBRES.xlsx",
    "Vegana": "VEGANA.xlsx",
    "Ovolactovegetariana": "OVOLACTEOVEGETARIANA.xlsx"
}

def cargar_sustituciones(tipo_dieta):
    archivo = DIET_FILES.get(tipo_dieta)
    if not archivo:
        return {}
    
    ruta = os.path.join("data", archivo)
    df = pd.read_excel(ruta)
    
    sustituciones = {}
    for _, fila in df.iterrows():
        original = str(fila[0]).strip()
        reemplazo = str(fila[1]).strip()
        if original and reemplazo:
            sustituciones[original.lower()] = reemplazo
    
    return sustituciones

def aplicar_sustituciones(df, sustituciones):
    df_copiado = df.copy()
    for col in df.columns:
        df_copiado[col] = df[col].apply(lambda x: reemplazar_texto(str(x), sustituciones))
    return df_copiado

def reemplazar_texto(texto, sustituciones):
    texto_lower = texto.lower()
    for original, reemplazo in sustituciones.items():
        if original in texto_lower:
            texto_lower = texto_lower.replace(original, reemplazo.lower())
    return texto_lower

def convertir_a_excel(df_original, nombre_hoja):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_original.to_excel(writer, sheet_name=nombre_hoja, index=False, header=False)
    output.seek(0)
    return output

# Interfaz de Streamlit
st.title("Adaptador automático de menús según dieta")

archivo_subido = st.file_uploader("Sube el archivo Excel del menú", type=["xlsx"])

if archivo_subido:
    tipo_dieta = st.selectbox("Selecciona el tipo de dieta", list(DIET_FILES.keys()))

    if st.button("Aplicar cambios"):
        try:
            original = pd.read_excel(archivo_subido, sheet_name=None)

            hoja = list(original.keys())[0]  # Selecciona la primera hoja
            df = original[hoja]
            sustituciones = cargar_sustituciones(tipo_dieta)
            df_modificado = aplicar_sustituciones(df, sustituciones)

            excel_corregido = convertir_a_excel(df_modificado, hoja)

            st.success("Cambios aplicados correctamente.")
            st.download_button(
                label="Descargar menú corregido",
                data=excel_corregido,
                file_name=f"menu_{tipo_dieta.lower()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")


