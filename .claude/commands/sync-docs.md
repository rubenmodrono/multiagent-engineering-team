---
description: Ciclo documental completo con rondas de revisión — actualiza Diseño Funcional y Técnico y los deja aptos para entrega
argument-hint: <alcance: versión, funcionalidad o "todo">
---

Ciclo documental para el alcance: **$ARGUMENTS**

Las rondas son secuenciales y cada una tiene una puerta. Saltarse una ronda invalida el ciclo: dilo si el usuario lo pide y hazlo sólo si insiste.

## R0 — Línea base
1. Identifica la versión vigente de cada entregable en `docs/entregables/`.
2. Verifica o extrae los perfiles de plantilla (skill `plantilla-documental`).
3. Reúne el delta: notas de implementación, ADRs, diff entregado, matriz de trazabilidad.

## R1 — Auditoría previa
Lanza `auditor-coherencia` sobre los entregables vigentes contra el código actual, en **las dos direcciones**.
Salida: lista de hallazgos con destinatario. Esta lista es el encargo de las siguientes rondas — no se redacta nada que no salga de ella o del delta.

## R2 — Redacción
Lanza en paralelo `analista-funcional` y `redactor-tecnico`.
Ambos entregan **change-list primero**. Presenta las dos change-lists juntas al usuario.
**Puerta:** el usuario confirma antes de aplicar. Las secciones nuevas necesitan aprobación explícita.

## R3 — Auditoría de verificación
Lanza otra vez `auditor-coherencia`, ahora sobre los documentos ya editados.
**Puerta:** cero hallazgos BLOQUEANTE. Los IMPORTANTE abiertos requieren justificación escrita del usuario. Si quedan bloqueantes, vuelta a R2 — y se cuenta la iteración.

## R4 — Pase de estilo
Lanza `editor-estilo` sobre las secciones modificadas, nunca sobre el documento entero.
Tras cada sección, verifica invariantes con `scripts/invariantes_texto.py`.
**Puerta:** si el editor reporta que una mejora exigía tocar contenido, vuelve a R2 para esa sección.

## R5 — Revisión de entrega
Lanza `revisor-documental`.
**Puerta:** veredicto APTO. Cada bloqueante vuelve a su responsable y se repite R5.

## Cierre
```
Entregables actualizados: <fichero> vX.Y → vX.Z
Iteraciones R2↔R3: N
Hallazgos: cerrados A / aceptados B (con motivo) / abiertos C
Veredicto de entrega: APTO | NO APTO
Trazabilidad: RF sin sección documental → lista
Secciones tocadas: ...
```
