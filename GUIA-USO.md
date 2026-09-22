# Guía de uso, paso a paso

## Idea principal, antes de nada

`SIITEAM` es la **copia maestra** de la plantilla. Los agentes no trabajan desde aquí:
se copian **dentro del repositorio del proyecto**, porque necesitan tener delante el
código y los documentos a la vez. Esa es toda la mecánica.

```
~/Documents/SIITEAM/          ← maestra. Se mejora aquí y se propaga.
   └── se copia a →  ~/code/proyecto-cliente/   ← aquí trabajan
                        ├── .claude/     (agentes, skills, comandos)
                        ├── CLAUDE.md
                        ├── docs/
                        ├── scripts/
                        └── src/ ...     (el código real del proyecto)
```

Si copias sólo `.claude/` tendrás los agentes pero no los gates ni las plantillas.
Cópialo todo la primera vez.

---

## Paso 1 — Instalar en un proyecto

```bash
cp -R ~/Documents/SIITEAM/.claude ~/Documents/SIITEAM/CLAUDE.md \
      ~/Documents/SIITEAM/docs ~/Documents/SIITEAM/scripts \
      /ruta/al/repo-del-proyecto/
```

Si el repo ya tiene un `CLAUDE.md`, **no lo machaques**: abre los dos y funde el
contenido a mano. El del proyecto manda sobre convenciones del código; el de la
plantilla aporta las reglas del equipo de agentes.

Abre una sesión de Claude Code en la raíz de ese repositorio. Comprueba que ha
cargado escribiendo `/` — deben aparecer `feature`, `sync-docs`, `revision-docs` y
`diagnostico-gateway`. Para los agentes, basta con pedir uno por su nombre.

---

## Paso 2 — Colocar los entregables del cliente

```
docs/entregables/
├── diseno-funcional/
│   ├── DF-PROY-001_v2.3.docx     ← última versión entregada
│   └── DF-PROY-001_v2.4.docx     ← copia de trabajo
└── diseno-tecnico/
    ├── DT-PROY-001_v2.3.docx
    └── DT-PROY-001_v2.4.docx
```

Regla: **nunca se edita una versión ya entregada**. Se parte de ella y se escribe la
siguiente. El histórico es lo que permite justificar ante el cliente qué cambió y cuándo.

---

## Paso 3 — Extraer la plantilla (obligatorio, una sola vez por documento)

Los perfiles de `docs/plantillas/` están vacíos (`extraido: false`) y los agentes
documentales tienen instrucción de **negarse a editar** mientras lo estén. Es
deliberado: sin este paso escribirían con un formato inventado en lugar del del cliente.

Pide:

> Extrae el perfil de plantilla del Diseño Técnico a partir de
> `docs/entregables/diseno-tecnico/DT-PROY-001_v2.3.docx` y guárdalo en
> `docs/plantillas/perfil-diseno-tecnico.yaml`

Repite con el funcional. Después **revisa el YAML tú**, sobre todo tres campos:

- `estructura` — que estén todas las secciones y con su numeración exacta.
- `marca_pendiente` — cómo marca *este* documento lo que aún no está implementado.
- `terminologia_cliente` — las palabras que el cliente usa y sus sinónimos prohibidos.
  Este campo es el que más rentabilidad da por minuto invertido: es lo que evita que
  el revisor del cliente te devuelva el documento por decir "usuario" donde ellos
  dicen "tramitador".

---

## Paso 4 — Cargar la matriz de trazabilidad

Edita `docs/trazabilidad/matriz.csv` con los requisitos reales (borra la fila de
muestra). Una fila por RF. No hace falta rellenarlo todo de golpe: lo que no sepas,
en blanco. Después:

```bash
python3 scripts/validar_trazabilidad.py
```

La primera ejecución es incómoda a propósito: saca los requisitos implementados sin
test y sin sección documental. Ese es su trabajo. No lo arregles todavía — es tu
foto de partida.

---

## Paso 5 — Primera pasada en seco

Antes de dejar que nadie escriba, mira cómo está lo que ya tienes:

```
/revision-docs docs/entregables/diseno-tecnico/DT-PROY-001_v2.3.docx
```

Tres agentes revisan sin tocar nada: coherencia contra el código, estilo en modo
informe, y checklist de entrega. Sale un informe con severidades y destinatarios.

Esto es también tu prueba de calibración: si el informe dice cosas que sabes que son
falsas, el problema está en el perfil de plantilla o en la matriz, y se arregla ahí
antes de seguir.

---

## Paso 6 — El ciclo documental completo

```
/sync-docs versión 2.4
```

Cinco rondas con puerta en cada una. Tú intervienes en dos momentos:

1. **Tras R2**, cuando te presenta las *change-lists* de ambos documentos: qué sección
   se toca, qué se hace y por qué. Es el punto donde decides. Léelas: aprobar aquí a
   ciegas es aprobar todo el ciclo a ciegas.
2. **Tras R3**, si quedan hallazgos IMPORTANTE abiertos y hay que justificarlos por
   escrito.

Lo que pasa por dentro:

| Ronda | Quién | Qué |
|---|---|---|
| R0 | — | versión vigente, perfil de plantilla, delta del código |
| R1 | `auditor-coherencia` | qué dice el documento que el código desmiente, y qué existe en el código sin documentar |
| R2 | `analista-funcional` + `redactor-tecnico` | change-list → tu visto bueno → redacción |
| R3 | `auditor-coherencia` | vuelve a auditar lo recién escrito. Con bloqueantes, se repite R2 |
| R4 | `editor-estilo` | pase de naturalidad, sección a sección, con verificación de invariantes |
| R5 | `revisor-documental` | veredicto APTO / NO APTO |

**El orden importa.** El estilo va al final porque pulir texto que todavía va a cambiar
es trabajo tirado, y porque pulir antes de verificar sólo consigue que una frase falsa
suene mejor.

---

## Paso 7 — Ciclo de una funcionalidad

```
/feature RF-041 baja de cliente con motivo de baja obligatorio
```

Arquitectura (si toca) → implementación → revisión de código, seguridad y QA **en
paralelo** → trazabilidad → documentación. Los bloqueantes vuelven al desarrollador y
la fase de revisión se repite sobre el diff nuevo.

Si el cambio es pequeño y local, sáltate el comando y pide directamente al
`desarrollador`. `/feature` tiene sentido cuando el cambio cruza servicios o toca un
contrato.

---

## Paso 8 — Diagnóstico de despliegue y gateway

```
/diagnostico-gateway 502 en /api/clientes desde preproducción, Kong 3.4
```

Impone diagnóstico antes que cambio: reproducir, leer la configuración **efectiva**
(no la del repo), comparar, y recorrer los sospechosos habituales marcando cada uno
como descartado o confirmado con evidencia.

Restricción incorporada: comandos de lectura libres, comandos de escritura sobre
cualquier entorno que no sea local **sólo con tu confirmación explícita**. Está en
`.claude/settings.json` y no depende de que el agente se porte bien.

---

## Invocar un agente suelto

No hace falta comando para todo:

> Lanza el `auditor-coherencia` sobre la sección 5 del Diseño Técnico
> Que el `editor-estilo` me haga un pase sobre el apartado 4.2, sólo informe
> `seguridad`: revisa el endpoint nuevo de bajas

Es lo que más vas a usar en el día a día.

---

## Cosas que conviene saber

**Cada agente arranca sin tu conversación.** Tiene su propio contexto y sólo ve lo que
se le pasa en el encargo más lo que lea del repositorio. Si una decisión importante se
tomó hablando conmigo y no está escrita en ningún sitio, el agente no la conoce. Por
eso los ADR y la matriz no son burocracia: son el canal por donde los agentes se
enteran de las cosas.

**El pase de estilo tiene red.** Tras cada sección:

```bash
python3 scripts/invariantes_texto.py antes.md despues.md
```

Falla si cambió un identificador, una cifra, un `§x.y`, un `RF-nnn`, un endpoint, una
fila de tabla o un bloque de código. Es lo que te permite dejar reescribir prosa sin
vigilar cada línea. Sólo funciona con documentos en texto (Markdown); con `.docx`
habrá que exportar la sección para comparar.

**El estilo no arregla el vacío.** Si una sección no dice nada, el arreglo es
contenido, no redacción. `editor-estilo` reformula; no inventa.

**`NO VERIFICABLE` no es un fallo.** Las afirmaciones de intención o de negocio no se
pueden contrastar contra el código. Salen marcadas y las resuelve una persona.

**Nada de esto sustituye tu revisión antes de entregar.** Acorta el camino hasta ella.

---

## Mantenimiento de la plantilla

Cuando afines algo en un proyecto y funcione — un tic de redacción típico de tu
cliente, un sospechoso nuevo del gateway, una regla de formato — llévalo de vuelta a
`~/Documents/SIITEAM` para que lo herede el siguiente proyecto. Es lo que convierte
esto en un activo en vez de en una configuración de usar y tirar.
