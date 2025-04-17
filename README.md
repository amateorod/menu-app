# 🥦 Adaptador de Menús con IA para Restauración Colectiva

Esta app permite adaptar menús automáticamente según distintos tipos de dieta y necesidades alimentarias, como:

- Dieta vegana
- Dieta ovolactovegetariana
- Dieta sin gluten (celíacos)
- Dieta sin lactosa
- Dieta sin frutos secos
- Dieta sin legumbres
- Dieta sin huevo
- Dieta sin cerdo

## 🚀 ¿Qué hace esta app?

🔄 Sube un menú en formato Excel y selecciona el tipo de dieta.  
🤖 La IA reemplazará automáticamente los alimentos que no se ajustan a esa dieta por opciones alternativas.  
📄 Puedes descargar el menú corregido en Excel manteniendo el formato original.

---

## 📁 Estructura del repositorio

```
├── app.py                    # Código principal de la app
├── requirements.txt         # Dependencias necesarias
├── README.md                # Descripción del proyecto
└── data/
    ├── OVOLACTEOVEGETARIANA Y VEGANA.xlsx
    ├── SIN LACTOSA Y CELIACO.xlsx
    └── SIN FRUTOS SECOS Y LEGUMBRES.xlsx
```

---

## ▶️ Cómo ejecutar la app

1. Clona este repositorio:
```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta la app:
```bash
streamlit run app.py
```

---

## 📌 Notas

- Asegúrate de subir tu archivo Excel con el menú original.
- Elige el tipo de dieta desde el menú desplegable.
- La app mantendrá el formato original del archivo.

---

## 💡 Próximas mejoras

- Exportación directa a PDF con formato intacto
- Versión móvil y web pública
- Integración con bases de datos online

---

## 👩‍🍳 Creado por una técnica en dietética

Este proyecto está diseñado especialmente para profesionales de la restauración colectiva, familias, colegios y cualquier entorno que necesite adaptar menús según necesidades específicas.