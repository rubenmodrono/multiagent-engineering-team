---
description: Revisión de un documento ya redactado — coherencia, estilo y formato, sin volver a redactar
argument-hint: <ruta del documento>
---

Revisa el documento **$ARGUMENTS** sin reescribirlo. Tres pasadas, tres agentes, un informe.

1. `auditor-coherencia` — contra el código actual, las dos direcciones.
2. `editor-estilo` — **en modo informe, sin editar**: lista de párrafos que suenan a relleno, secciones con voz distinta al resto del documento, y afirmaciones sin anclaje concreto. Que no aplique cambios.
3. `revisor-documental` — checklist de entrega completo.

Informe único, ordenado por severidad, con el destinatario de cada hallazgo y una estimación de esfuerzo de corrección (bajo / medio / alto).

Termina con la pregunta al usuario: ¿lanzo `/sync-docs` para corregir, o entrego el informe tal cual?
