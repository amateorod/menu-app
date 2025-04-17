
# 🥗 Adaptador de Menús con Base de Datos en Word

Esta aplicación permite adaptar automáticamente un menú en Excel a distintos tipos de dieta (como vegana, ovolacteovegetariana, etc.) usando una tabla contenida en un archivo Word como base de sustituciones.

---

## 🚀 ¿Cómo funciona?

1. **Sube el archivo de menú en Excel**, que debe contener una hoja llamada exactamente:  
   `Menu sin Recomendación`
2. **Sube el archivo Word (.docx)** que contiene la tabla de sustituciones.  
   La tabla debe tener columnas como `PLATOS`, `VEGANO`, `OVOLACTEOVEGETARIANO`, etc.
3. **Selecciona el tipo de dieta** a aplicar.
4. **Descarga el archivo Excel corregido**, con los cambios aplicados y manteniendo el formato original.

---

## 📁 Estructura esperada

### 🔹 Excel del menú
- Hoja llamada `Menu sin Recomendación`
- Contiene los platos base que serán modificados según la dieta

### 🔹 Word con la base de datos
- Una tabla con:
  - Columna `PLATOS` (alimentos base)
  - Otras columnas con los tipos de dieta (`VEGANO`, `OVOLACTEOVEGETARIANO`, etc.)

Ejemplo:

| PLATOS                     | VEGANO           | OVOLACTEOVEGETARIANO  |
|---------------------------|------------------|------------------------|
| Arroz con huevo           | Arroz con tomate | Arroz con huevo        |
| Croquetas de jamón        | Filete vegetal   | Croquetas de verduras  |

---

## ✅ Requisitos

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

Contenido mínimo del `requirements.txt`:

```
streamlit
pandas
openpyxl
python-docx
```

---

## 🧠 Flujo completo

1. Subes tu menú Excel (con la hoja `"Menu sin Recomendación"`).
2. Subes tu base de sustituciones en formato Word (.docx).
3. Seleccionas la dieta deseada.
4. Obtienes un menú corregido en Excel con el mismo formato visual original.

---

## 👩‍🍳 Ideal para...

- Dietistas-nutricionistas
- Restauración colectiva
- Menús escolares o institucionales

---

Desarrollado con ❤️ para facilitar el trabajo de adaptación alimentaria.
