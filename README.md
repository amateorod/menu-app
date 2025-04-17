
# 🥗 Adaptador de Menús por Dietas (línea por línea)

Esta aplicación permite adaptar automáticamente un menú en Excel, modificando solo los platos indicados en una base de datos que viene en un archivo Word. Detecta y reemplaza **línea por línea** dentro de cada celda del menú.

---

## 🚀 ¿Qué hace?

- Carga un menú en Excel que contenga una hoja llamada exactamente **Menu sin Recomendación**.
- Usa un archivo Word (.docx) que tenga una tabla con:
  - Columna `PLATOS` (platos originales)
  - Columnas con nombres de dietas (`VEGANO`, `OVOLACTEOVEGETARIANO`, etc.)
- Aplica sustituciones **solo a las líneas que coinciden exactamente**.
- Conserva el formato y devuelve un archivo Excel corregido.

---

## 📂 Estructura esperada

### 🟢 Excel del menú:
- Hoja obligatoria: `Menu sin Recomendación`
- Celdas con varios platos separados por salto de línea (`\n`), por ejemplo:

```
Sopa de pescado
Pizza margarita
Fruta de temporada
```

### 🟣 Word con la base de datos:
| PLATOS            | VEGANO            | OVOLACTEOVEGETARIANO   |
|-------------------|-------------------|-------------------------|
| Sopa de pescado   | Sopa de verduras  | Sopa de arroz           |
| Pizza margarita   | Pizza vegetal     | Pizza 4 quesos          |

---

## 📦 Requisitos

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

Contenido del `requirements.txt`:

```
streamlit
pandas
openpyxl
python-docx
```

---

## ▶️ Uso

1. Inicia la app:

```bash
streamlit run app.py
```

2. Sube tu Excel con el menú y el Word con las sustituciones.
3. Selecciona la dieta que quieres aplicar.
4. Descarga el menú corregido con todos los cambios aplicados **línea por línea**.

---

## 👩‍🍳 Ideal para...

- Menús escolares
- Restauración colectiva
- Centros sanitarios y dietistas

---

Desarrollado con ❤️ para una nutrición más accesible y automatizada.
