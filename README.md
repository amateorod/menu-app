# Menu Adaptation App

Esta aplicación permite adaptar automáticamente menús en formato Excel según distintas necesidades dietéticas, como dietas veganas, sin lactosa, sin gluten, sin frutos secos, entre otras.

## ¿Cómo funciona?
1. El usuario sube un archivo Excel con un menú base.
2. Selecciona la dieta a la que desea adaptar el menú.
3. La app sustituye los alimentos del menú base por las versiones adaptadas, según las bases de datos disponibles.
4. El usuario puede descargar el nuevo archivo Excel con las modificaciones.

## Estructura esperada de los archivos de sustitución
Cada archivo Excel contiene una tabla con una columna llamada `platos` que representa el menú base, y columnas con los nombres de las dietas (en mayúsculas) que contienen las sustituciones correspondientes.

Ejemplo:

| platos                            | VEGANO               | CELIACO           |
|-----------------------------------|-----------------------|-------------------|
| Arroz a la cubana con huevo       | Arroz con tomate     | Arroz blanco      |
| Croquetas                         | Filete vegetal        | Croquetas sin gluten |

## Cómo desplegar la app localmente

1. Clona el repositorio:

```
git clone https://github.com/amateorod/menu-app.git
cd menu-app
```

2. Crea un entorno virtual (opcional pero recomendable):

```
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:

```
pip install -r requirements.txt
```

4. Ejecuta la aplicación:

```
streamlit run app.py
```

## Notas importantes

- Los archivos de sustitución deben estar en la misma carpeta que `app.py`.
- Los nombres de las columnas de sustitución deben estar en mayúsculas y coincidir con los valores del desplegable.
- El nombre de la hoja no importa; se detecta automáticamente la hoja y la columna de `platos`.

---

Desarrollado con ❤️ por amateorod.