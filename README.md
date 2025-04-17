
# 🥗 Adaptador de Menús con Base de Datos en Word

Esta aplicación permite adaptar automáticamente un menú en Excel a distintos tipos de dieta (como vegana, ovolacteovegetariana, etc.) usando una tabla contenida en un archivo Word como base de sustituciones.

---

## 🚀 ¿Cómo funciona?

1. **Sube el archivo de menú en Excel**, que debe contener una hoja llamada exactamente:  
   `Menu sin Recomendación`  
2. **Sube el archivo Word (.docx)** que contiene la tabla de sustituciones.  
   La tabla debe tener al menos dos columnas:
   - `PLATOS`: contiene los platos originales del menú.
   - Una o más columnas con los nombres de dietas (`VEGANO`, `OVOLACTEOVEGETARIANO`, etc.).
3. **Selecciona la dieta** que quieres aplicar desde el desplegable.
4. La app reemplazará cada alimento que se encuentre en la columna `PLATOS` por su equivalente en la columna correspondiente a la dieta seleccionada.
5. **Descarga el menú corregido** manteniendo el formato original del Excel.

---

## 🗂 Estructura esperada

### 🔹 Excel del menú
- Hoja llamada `Menu sin Recomendación`
- Contiene los platos base que serán modificados

### 🔹 Word con la base de datos
- Una tabla con:
  - Columna `PLATOS` (alimentos base)
  - Columnas con los tipos de dieta (`VEGANO`, `OVOLACTEOVEGETARIANO`, etc.)

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

Contenido sugerido del `requirements.txt`:

```
streamlit
pandas
openpyxl
python-docx
```

---

## 🧠 Flujo completo

1. Subes el Excel con la hoja `Menu sin Recomendación`.
2. Subes el Word con la tabla de sustituciones.
3. Seleccionas el tipo de dieta.
4. El sistema aplica los cambios según la columna correspondiente.
5. Descargas el Excel corregido.

---

## 👩‍🍳 Ideal para...

- Dietistas-nutricionistas
- Restauración colectiva
- Menús escolares, sanitarios o institucionales

---

Desarrollado con ❤️ para facilitar el trabajo de adaptación alimentaria.
