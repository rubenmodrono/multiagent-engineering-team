# Equipo de ingeniería multiagente

Quince agentes especializados, cuatro flujos de trabajo y dos gates automáticos, sobre
Claude Code. Cubre el ciclo de ingeniería y, sobre todo, el mantenimiento de los
entregables documentales de Diseño Funcional y Diseño Técnico coherentes con el código.

## Instalación

Copia la carpeta `.claude/`, `CLAUDE.md`, `docs/` y `scripts/` a la raíz del repositorio
del proyecto. Los agentes y comandos quedan disponibles en cuanto abras una sesión allí.

```
.claude/agents/      15 agentes especializados
.claude/skills/      conocimiento compartido (plantillas, estilo, trazabilidad, fuentes externas)
.claude/commands/    los cuatro flujos
.claude/settings.json permisos: lectura libre, escritura en entornos con confirmación
docs/plantillas/     perfil de plantilla extraído de los documentos del cliente
docs/entregables/    versiones vigentes de los documentos
docs/trazabilidad/   matriz RF ↔ código ↔ test ↔ sección
docs/adr/            decisiones de arquitectura
scripts/             gates automáticos
```

## Puesta en marcha, en orden

1. **Extraer las plantillas reales.** Los perfiles de `docs/plantillas/` están vacíos.
   Con la versión vigente de cada entregable delante:
   > Extrae el perfil de plantilla del Diseño Técnico a partir de `docs/entregables/diseno-tecnico/DT-...v2.3.docx`
   
   Sin este paso, los agentes documentales no deben tocar los entregables. Es el paso que
   hace que la documentación salga con el formato del cliente y no con uno inventado.

2. **Cargar la matriz de trazabilidad** con los requisitos reales, y ejecutar el validador:
   ```bash
   python3 scripts/validar_trazabilidad.py
   ```
   La primera ejecución suele ser incómoda: saca los requisitos sin test y los
   implementados sin sección documental. Ese es exactamente su trabajo.

3. **Calibrar la voz del documento.** La primera vez que uses `editor-estilo`, pídele
   que escriba la calibración de voz y guárdala. Las siguientes rondas parten de ahí.

4. **Primer ciclo en seco**: `/revision-docs docs/entregables/...` sobre la versión
   vigente, sin cambiar nada. Te dice el estado real de partida.

## Uso

```
/feature RF-041 baja de cliente con motivo obligatorio
/sync-docs versión 2.4
/revision-docs docs/entregables/diseno-tecnico/DT-PROY-001_v2.4.md
/diagnostico-gateway 502 en /api/clientes desde preproducción
```

También puedes invocar un agente suelto: *"lanza el auditor-coherencia sobre la sección 5"*.

## El ciclo documental

```
R0 línea base ─→ R1 auditoría ─→ R2 redacción ─→ R3 verificación ─→ R4 estilo ─→ R5 entrega
                      ▲                                │
                      └────────── mientras queden ─────┘
                                  bloqueantes
```

Tres decisiones de diseño que sostienen el resultado:

- **El auditor no escribe y el redactor no se audita.** Un agente que corrige lo que él
  mismo escribió confirma su propio trabajo. La separación es lo que hace que la revisión
  valga algo.
- **La auditoría va en las dos direcciones.** Del documento al código (¿es cierto lo que
  dice?) y del código al documento (¿está documentado lo que existe?). La segunda es la
  que nadie hace y la que saca los endpoints, los parámetros de configuración y los
  códigos de error que nunca llegaron al entregable.
- **El estilo va al final.** Pulir texto que todavía va a cambiar es trabajo tirado, y
  pulir antes de verificar hace que una frase falsa suene mejor.

## Gates automáticos

`validar_trazabilidad.py` — requisitos duplicados, rutas inexistentes, implementados sin
test o sin sección documental, endpoints sin ruta en el gateway, ADRs fantasma.

`invariantes_texto.py` — compara el texto antes y después del pase de estilo y falla si
han cambiado identificadores, cifras, referencias `§x.y`, códigos `RF-nnn`, endpoints,
tablas o bloques de código. Es la red que permite dejar reescribir prosa sin miedo a que
se corrompa el contenido.

## Límites que conviene conocer

- Los agentes leen el repositorio, no la cabeza de quien escribió el documento hace un
  año. Las afirmaciones de intención o de negocio salen como `NO VERIFICABLE` y las tiene
  que resolver una persona.
- El pase de estilo mejora prosa; no convierte un documento vacío en uno bueno. Si una
  sección no dice nada, el arreglo es contenido, no redacción.
- Nada de esto sustituye la revisión humana antes de entregar al cliente. Acorta el
  camino hasta ella.
