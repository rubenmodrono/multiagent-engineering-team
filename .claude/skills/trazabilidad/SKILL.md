---
name: trazabilidad
description: Mantener y consultar la matriz de trazabilidad que enlaza requisitos, componentes de código, endpoints, tests y secciones de documentación. Usar al implementar un requisito, al actualizar documentación, al diseñar pruebas y al auditar coherencia entre documento y código.
---

# Matriz de trazabilidad

Es el mecanismo que convierte "la documentación es coherente con el código" en algo **comprobable** en vez de opinable. Sin ella, cada auditoría vuelve a empezar de cero.

## Fichero
`docs/trazabilidad/matriz.csv`, una fila por requisito.

| columna | contenido | ejemplo |
|---|---|---|
| `rf` | código del requisito | `RF-041` |
| `titulo` | enunciado corto | `Baja de cliente con motivo obligatorio` |
| `estado` | `implementado` / `parcial` / `pendiente` / `retirado` | `implementado` |
| `version` | versión del entregable donde entra | `2.4` |
| `seccion_df` | sección del Diseño Funcional | `4.3.2` |
| `seccion_dt` | sección del Diseño Técnico | `5.1.7` |
| `componentes` | rutas de código, separadas por `;` | `svc-clientes/src/baja/handler.go` |
| `endpoints` | método y ruta, separados por `;` | `DELETE /v1/clientes/{id}` |
| `ruta_gateway` | ruta declarada en el API gateway | `/api/clientes/*` |
| `tests` | rutas de test, separadas por `;` | `svc-clientes/test/baja_test.go` |
| `adr` | ADRs que la afectan | `0007` |
| `notas` | lo que no cabe arriba | |

## Quién la toca
- `desarrollador`: `estado`, `componentes`, `endpoints` al implementar.
- `qa-tester`: `tests`, y detecta filas con `estado: implementado` y `tests` vacío.
- `analista-funcional` / `redactor-tecnico`: `seccion_df`, `seccion_dt`.
- `plataforma-devops`: `ruta_gateway`.
- `auditor-coherencia`: no la edita; la usa como punto de partida y reporta lo que falta.

## Validación automática
```bash
python3 scripts/validar_trazabilidad.py
```
Comprueba que las rutas de código y de test existen, que no hay RF duplicados, que todo RF implementado tiene test y sección documental, y que los ADR referenciados existen. Es un gate barato: se ejecuta antes de cada revisión documental.

## Uso en auditoría
La matriz da la **dirección A** (requisito → código). La **dirección B** (código → documento) no puede salir de la matriz por definición: hay que enumerar el repositorio. Las dos direcciones son obligatorias.
