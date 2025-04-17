# Menu App - Adaptador de Menús

Esta aplicación permite adaptar automáticamente un menú en formato Excel según diferentes tipos de dieta (vegana, sin lactosa, sin gluten, etc.).

## ¿Cómo funciona?

1. Sube un archivo Excel con tu menú original.
2. Selecciona el tipo de dieta en el desplegable.
3. El menú se modificará automáticamente según las sustituciones definidas en los archivos `.xlsx`.
4. Descarga el nuevo menú corregido manteniendo el formato original.

## Instrucciones

- Coloca todos los archivos `.xlsx` de las dietas en la misma carpeta que `app.py`.
- Los archivos deben tener dos columnas: la primera con los alimentos originales y la segunda con los alimentos sustitutos.
- Asegúrate de que los nombres de los archivos están en mayúsculas para que coincidan con el desplegable.

## Requisitos

- Python 3.8+
- Streamlit
- pandas
- openpyxl

Instala las dependencias con:

```bash
pip install -r requirements.txt
