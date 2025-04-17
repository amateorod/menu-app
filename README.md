# 🧠 Menu-App: Adaptador automático de menús para dietas especiales

Esta aplicación web permite subir un menú en **formato PDF**, detectar la tabla de alimentos y **adaptarla automáticamente** a diferentes tipos de dietas utilizando una base de datos propia de sustituciones. El resultado se descarga como un archivo **Excel corregido**.

## ✅ Funcionalidades

- ✅ Subida de archivos PDF con menús.
- ✅ Detección automática de la tabla del menú.
- ✅ Adaptación a dietas especiales (vegana, sin gluten, sin lactosa, sin huevo, etc.).
- ✅ Reemplazo inteligente de platos según una base de datos.
- ✅ Descarga del menú corregido en formato Excel (.xlsx).

## 🧩 Tipos de dieta soportados

- VEGANA
- OVOLACTEOVEGETARIANA
- CELIACO
- SIN LACTOSA
- SIN HUEVO
- SIN FRUTOS SECOS
- SIN LEGUMBRES
- SIN CERDO

## 🗂️ Organización de archivos

Asegúrate de tener los archivos `.xlsx` de sustituciones dietéticas guardados en la **misma carpeta que `app.py`**. Cada archivo debe tener una columna llamada `PLATOS` (en mayúsculas) y las demás columnas deben tener los nombres de las dietas en mayúsculas.

Ejemplo de columnas válidas:

```
PLATOS | VEGANA | CELIACO | SIN HUEVO | ...
```

## 📦 Requisitos

Instala las dependencias necesarias con:

```bash
pip install -r requirements.txt
```

Contenido del `requirements.txt`:

```
streamlit
pandas
openpyxl
PyMuPDF
tabula-py
```

> 💡 `tabula-py` requiere Java instalado en el sistema. Alternativamente puedes usar `pdfplumber` si prefieres evitar Java.

## 🚀 Ejecutar la app

Lanza la aplicación con:

```bash
streamlit run app.py
```

## 📝 Autoría

Creado por [amateorod](https://github.com/amateorod), con ayuda de inteligencia artificial para automatizar procesos en restauración colectiva.
