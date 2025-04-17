
# App de Adaptación Automática de Menús

Esta app de Streamlit permite adaptar automáticamente menús en formato Excel según diferentes tipos de dieta (vegana, sin lactosa, sin gluten, etc.), sustituyendo ingredientes según una tabla predefinida.

## ¿Cómo funciona?

1. **Selecciona el tipo de dieta** en el desplegable.
2. **Sube un archivo Excel** con el menú original.
3. La app aplicará automáticamente las sustituciones.
4. **Descarga el archivo Excel modificado.**

## 📁 Archivos necesarios

- Archivos `.xlsx` con los nombres en MAYÚSCULAS (por ejemplo, `VEGANA.xlsx`, `SIN GLUTEN.xlsx`).
- Cada archivo debe contener una hoja con el mismo nombre que el archivo (por ejemplo, `VEGANA` como nombre de hoja dentro de `VEGANA.xlsx`).

## 🛠 Requisitos

- Python 3.8+
- Streamlit
- Pandas
- XlsxWriter

## 🚀 Ejecutar localmente

```bash
streamlit run app.py
```
