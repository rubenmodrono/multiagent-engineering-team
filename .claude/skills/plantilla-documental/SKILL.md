---
name: plantilla-documental
description: Extraer, fijar y respetar la plantilla y el formato de un entregable documental existente (Diseño Funcional, Diseño Técnico u otro). Usar antes de editar cualquier documento de entrega, cuando haya que crear el perfil de plantilla de un documento nuevo, o cuando haya dudas sobre si un cambio respeta el formato del cliente.
---

# Plantilla y formato de entregables

El documento del cliente manda. No existe "mi forma de estructurar un diseño técnico": existe la de este documento.

## 1. Extraer el perfil de plantilla

De la versión vigente del entregable, extrae y guarda en `docs/plantillas/perfil-<documento>.yaml`:

```yaml
documento: Diseño Técnico
codigo: DT-PROY-001
formato_fuente: docx | confluence | markdown | asciidoc
version_analizada: "2.3"

portada:
  campos: [titulo, codigo, version, fecha, cliente, proyecto, clasificacion, autor, aprobador]

control_versiones:
  ubicacion: "sección 0.1"
  columnas: [version, fecha, autor, descripcion, aprobado_por]
  convencion_version: "mayor.menor — mayor si cambia alcance"

estructura:
  - { n: "1",   titulo: "Introducción",        obligatoria: true }
  - { n: "1.1", titulo: "Objeto",              obligatoria: true }
  - { n: "1.2", titulo: "Alcance",             obligatoria: true }
  - { n: "2",   titulo: "Arquitectura",        obligatoria: true }
  # ... la estructura real, completa

convenciones:
  numeracion_secciones: "1.2.3 hasta tercer nivel"
  figuras: "Figura N: <título>, pie debajo, referenciada desde el texto"
  tablas: "Tabla N: <título>, título encima"
  marca_pendiente: "[PENDIENTE v2.4]"   # cómo marca ESTE documento lo no implementado
  requisitos: "RF-nnn / RNF-nnn"
  referencias_cruzadas: "ver §4.2.1"
  diagramas: { herramienta: plantuml, fuente: "docs/diagramas/*.puml" }

terminologia_cliente:
  - usar "expediente", nunca "caso" ni "ticket"
  - usar "tramitador", nunca "usuario backoffice"

prohibiciones:
  - no renumerar secciones existentes
  - no cambiar la herramienta de diagramado
  - no introducir secciones nuevas sin aprobación registrada
```

Si el perfil ya existe, **verifícalo contra el documento actual** antes de usarlo: las plantillas del cliente cambian sin avisar.

## 2. Reglas de edición

- **La numeración es un contrato externo.** Actas, correos y tickets del cliente referencian "§4.2.1". Renumerar rompe trazabilidad fuera de tu control. Si hay que insertar, se usa un sufijo (4.2.1.bis) o se propone la renumeración explícitamente.
- **Sección nueva = decisión, no iniciativa.** Se propone en la change-list; el usuario decide.
- **Nivel de abstracción por documento**: el funcional no baja a tecnología, el técnico no sube a narrativa de negocio. Si un contenido está en el documento equivocado, se reporta; no se mueve por cuenta propia.
- **Lo no implementado se marca con la marca de la plantilla.** Nunca se describe en presente.
- **Control de versiones**: fila nueva por cada entrega, con la convención del documento.

## 3. Trabajar con cada formato fuente

**Markdown / AsciiDoc en repositorio** — el caso cómodo. Edición directa, diff revisable. Es el formato destino recomendado si algún día se puede negociar con el cliente.

**.docx** — usar la skill `docx`. Conservar estilos nombrados (`Heading 2`, `Tabla-Cliente`), no formato directo: el índice y la numeración automática dependen de ellos. Si el cliente revisa con control de cambios, entregar con los cambios marcados.

**Confluence** — el contenido vive en *storage format* (XHTML con macros). Al editar:
- Conservar las macros (`toc`, `status`, `expand`, `jira`, `info`) tal cual; romper una macro rompe la página para todos.
- Conservar los anchors: los enlaces entrantes de otras páginas dependen de ellos.
- Confluence versiona cada guardado. Una edición = una versión con comentario de versión descriptivo.
- **Nunca publicar una edición sin que el usuario la haya revisado.** Una página de Confluence es visible para todo el cliente en cuanto se guarda.

## 4. Salida obligatoria: change-list antes de editar

```
§4.2.1 <título>  — MODIFICAR        — <qué y por qué, con la evidencia>
§4.3   <título>  — AÑADIR           — <qué y por qué>
§6.1   <título>  — MARCAR PENDIENTE — <no implementado en esta versión>
§7     <título>  — SIN CAMBIOS
```
Se presenta, se espera confirmación, y entonces se edita.
