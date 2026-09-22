---
description: Ciclo completo de una funcionalidad — diseño, implementación, revisiones y actualización documental
argument-hint: <descripción de la funcionalidad o código de requisito>
---

Coordina el ciclo completo para: **$ARGUMENTS**

Eres el coordinador. No implementas tú: delegas en los agentes del equipo y haces de puerta entre fases. Entre fase y fase, resume en tres líneas y continúa; sólo paras a preguntar cuando una decisión sea del usuario.

## Fase 1 — Diseño
Lanza `arquitecto`. Si el cambio es local y no toca contratos ni infraestructura, sáltate esta fase y dilo.
**Puerta:** si el arquitecto necesita una decisión de negocio, para y pregunta al usuario.

## Fase 2 — Implementación
Lanza `desarrollador` con el ADR (si lo hay) y el requisito. Exige la nota de implementación con su apartado de **impacto documental**.

## Fase 3 — Revisiones técnicas, en paralelo
Lanza a la vez, en un solo bloque, `revisor-codigo`, `seguridad` y `qa-tester`.
**Puerta:** los hallazgos BLOQUEANTE y CRÍTICO vuelven a `desarrollador` y se repite la fase 3 sobre el nuevo diff. No se avanza con bloqueantes abiertos.

## Fase 4 — Trazabilidad
Actualiza `docs/trazabilidad/matriz.csv` y ejecuta `python3 scripts/validar_trazabilidad.py`. Corrige lo que salga.

## Fase 5 — Documentación
Invoca `/sync-docs` con el alcance de este cambio.

## Cierre
Informe final:
- qué se entregó
- hallazgos cerrados y hallazgos aceptados conscientemente, con su motivo
- resultado real de la suite de tests, con números
- secciones documentales tocadas
- **qué queda pendiente**, explícito
