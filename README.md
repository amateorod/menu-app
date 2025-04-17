# 🥗 Adaptador de Menús según Dietas

Esta aplicación permite adaptar automáticamente menús escolares o de restauración colectiva a diferentes tipos de dietas especiales (vegana, sin gluten, sin lactosa, etc.).

## 🚀 ¿Qué hace esta app?

- ✅ Sube un menú en formato `.xlsx`
- ✅ Selecciona el tipo de dieta (ej. VEGANA, CELIACO, SIN LACTOSA…)
- ✅ El sistema reemplaza automáticamente los platos que no cumplen con la dieta usando las bases de datos
- ✅ Descarga el nuevo menú ya corregido, manteniendo el formato original

## 🧠 ¿Cómo funciona?

1. **Menú Base**: Subes un archivo Excel que contiene un menú.
2. **Base de datos**: Internamente, la app compara los alimentos de ese menú con una columna base llamada `PLATOS`, y sustituye por lo indicado en la columna correspondiente a la dieta seleccionada.
3. **Resultado**: Se genera un nuevo archivo Excel adaptado, manteniendo el estilo original.

## 📁 Estructura esperada

- Los archivos de base de datos deben ser archivos `.xlsx` que contengan:
  - Una columna llamada `PLATOS` (con mayúsculas) → representa los alimentos originales.
  - Otras columnas con el nombre de la dieta (`VEGANA`, `CELIACO`, `SIN LACTOSA`, etc.), también en mayúsculas.

### Ejemplo:

| PLATOS                      | VEGANA              | CELIACO          |
|----------------------------|---------------------|------------------|
| Arroz a la cubana con huevo| Arroz con tomate    | Arroz a la cubana|
| Lentejas con chorizo       | Lentejas con tofu   | Lentejas naturales|

## 📦 Instalación (local)

1. Clona este repositorio
2. Instala las dependencias:

```bash
pip install -r requirements.txt
