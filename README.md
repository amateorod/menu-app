
# 🥗 App de Adaptación de Menús por Dieta

Esta aplicación permite adaptar automáticamente menús en formato Excel según diferentes tipos de dietas (vegana, sin lactosa, celíaco, etc.). Los menús se suben como archivos Excel y la app reemplaza automáticamente los alimentos no permitidos por otros compatibles según las bases de datos cargadas.

---

## 🚀 ¿Cómo funciona?

1. **Sube tu archivo de menú en Excel** (`.xlsx`) con una hoja llamada exactamente:  
   **`Menu sin Recomendación`** *(sin tilde)*  
   Este será el menú base que se modificará.

2. **Selecciona el tipo de dieta** en el desplegable.

3. **Descarga el archivo corregido** en Excel manteniendo el formato original.

---

## 🗂 Estructura esperada

### 🔹 Archivo de menú original (`.xlsx`)
- Debe contener una hoja llamada: `Menu sin Recomendación`
- En ella debe haber alimentos a sustituir (por ejemplo: `Arroz a la cubana con huevo`)

### 🔹 Archivos de base de datos dietética (`.xlsx`)
- Deben estar en la misma carpeta que `app.py`
- Deben tener una columna llamada **`PLATOS`** (en mayúscula), que contiene los alimentos base a sustituir.
- Cada otra columna representa un tipo de dieta. Ejemplo:

| PLATOS                        | VEGANO               | CELIACO              |
|------------------------------|----------------------|----------------------|
| Arroz a la cubana con huevo  | Arroz con tomate     | Arroz blanco         |
| Macarrones con queso         | Macarrones con soja  | Macarrones sin gluten|

---

## 📦 Requisitos (requirements.txt)

Aquí un ejemplo de dependencias necesarias:

```txt
streamlit
pandas
openpyxl
```

---

## 💡 Notas importantes

- El sistema busca coincidencias de texto exactas o muy parecidas (utiliza detección inteligente con `difflib`).
- Los nombres de las dietas deben coincidir con las columnas de las bases de datos y estar en **MAYÚSCULAS**.
- No se necesita una columna llamada "BASAL", se usa directamente la columna `PLATOS`.

---

## 🧠 Ejemplo de flujo

1. Sube `menu_original.xlsx` que contiene una hoja `Menu sin Recomendación`.
2. Sube bases de datos como `OVOLACTEOVEGETARIANA Y VEGANA.xlsx` que contiene columnas `PLATOS`, `VEGANO`, etc.
3. Selecciona `VEGANO` en el desplegable.
4. El sistema cambiará automáticamente los alimentos no veganos por los definidos como veganos.
5. Descarga el archivo Excel con el menú corregido.

---

## 🧑‍💻 Autoría

Desarrollado con ❤️ para facilitar la adaptación de menús en restauración colectiva.
