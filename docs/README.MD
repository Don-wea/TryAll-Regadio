# 📖 Documentación del Proyecto

Este directorio contiene toda la documentación técnica y de despliegue del proyecto, así como los diagramas y documentos de soporte.

## 📂 Estructura de `docs/`

### 📁 src/

Contiene todos los archivos fuente de la documentación y diagramas del proyecto. Aquí se incluyen:

- Diagramas en **PlantUML** (`.puml`)
- Diagramas en **Markdown Mermaid** (`.mmd`)
- Documentos en **LaTeX** (`.tex`)
- Manuales y otros documentos en **Markdown** (`.md`)

> 💡 Todo archivo editable de documentación debe mantenerse en esta carpeta.

---

### 📁 export/

Aquí se almacenan los archivos generados a partir de los archivos fuente de `src/`. Por ejemplo:

- Imágenes exportadas desde PlantUML (`.png`)
- PDFs generados desde LaTeX (`.pdf`)
- Diagramas renderizados desde Mermaid (`.png` o `.svg`)

> 💡 Esta carpeta puede vaciarse y regenerarse en cualquier momento, ya que todos los outputs provienen de los archivos en `src/`.

---

### 📁 deployment/

Incluye documentación específica para el despliegue del proyecto:

- Guías para levantar servicios con Docker
- Variables de entorno necesarias
- Notas sobre instalación o configuración de servidores

---

### 📄 changelog.md

Registro de cambios importantes en la documentación, arquitectura o despliegue del sistema.

---

## 📌 Notas

- Mantener siempre actualizado el contenido de `src/` y sus respectivos archivos en `export/`.
- Evitar subir archivos temporales o innecesarios.
- Se recomienda incluir un `.gitignore` en `export/` para controlar qué archivos se versionan.

