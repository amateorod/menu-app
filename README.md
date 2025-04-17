# 🥗 Adaptador Automático de Menús según Tipo de Dieta

Esta aplicación permite adaptar automáticamente un menú en formato Excel (`.xlsx`) a diferentes tipos de dieta, como VEGANA, SIN GLUTEN, SIN LACTOSA, etc., realizando las sustituciones necesarias de forma automática.

---

## 📂 ¿Qué necesita la app para funcionar?

1. **Un archivo Excel con el menú a modificar**, cargado por el usuario a través de la app.
2. **Una base de datos de sustituciones**, también en formato Excel, ya incluida en la carpeta del proyecto (por ejemplo: `VEGANA.xlsx`, `SIN LACTOSA Y CELIACO.xlsx`, etc.).

---

## 📄 Formato de las bases de datos

Cada archivo de base de datos debe tener una sola hoja y cumplir con estas condiciones:

- Una columna llamada **PLATOS** (en mayúsculas), que contiene los alimentos del menú "basal" (los que se podrían necesitar sustituir).
- Una o más columnas con nombres de tipos de dietas (también en **mayúsculas**), como: `VEGANA`, `SIN GLUTEN`, `OVOLACTEOVEGETARIANA`, etc.
- Cada fila representa un alimento del menú original, y en cada columna de dieta se indica el alimento alternativo correspondiente (o puede quedar en blanco si no hay sustitución).

### 🧠 Ejemplo de una base de datos:

| PLATOS         | VEGANA         | SIN GLUTEN      | SIN LACTOSA     |
|----------------|----------------|-----------------|-----------------|
| LECHE ENTERA   | BEBIDA DE SOJA | LECHE SIN GLUTEN| BEBIDA DE AVENA |
| HUEVOS FRITOS  | TOFU REVUELTO  | HUEVOS FRITOS   | HUEVOS FRITOS   |
| PAN            | PAN VEGANO     | PAN SIN GLUTEN  | PAN VEGANO      |

---

## 🧪 ¿Cómo funciona?

1. El usuario elige el tipo de dieta deseada en un desplegable.
2. Sube su archivo de menú en Excel (con los platos que quiere adaptar).
3. La aplicación:
   - Carga la base de datos de sustituciones correspondiente (por ejemplo, `VEGANA.xlsx`).
   - Busca la columna `PLATOS` como referencia.
   - Sustituye automáticamente los alimentos del menú por sus equivalentes en la dieta elegida, **solo si hay un reemplazo disponible**.
4. El resultado es un archivo Excel corregido, que el usuario puede descargar.

---

## 🚀 ¿Cómo ejecutar la app?

1. Asegúrate de tener instalado Python y las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
