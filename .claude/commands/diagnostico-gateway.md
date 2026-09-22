---
description: Diagnóstico guiado de un fallo de despliegue o de enrutado en el API gateway
argument-hint: <síntoma: código de error, servicio y entorno>
---

Diagnostica: **$ARGUMENTS**

Lanza `plataforma-devops` con el protocolo de diagnóstico y estas condiciones:

**Antes de tocar nada**, reúne y muestra:
1. El síntoma exacto: código HTTP, cuerpo, cabeceras, y **desde dónde** se reproduce.
2. La misma petición desde tres puntos: fuera del clúster, desde el ingress, y desde un pod del mismo namespace. Las tres respuestas juntas localizan el corte.
3. La configuración **efectiva** del gateway para esa ruta, no la del repositorio, y la diferencia entre ambas.
4. Logs del gateway y del servicio de la misma ventana temporal, correlacionados por request-id si existe.

**Después**, recorre los sospechosos habituales de la ficha de `plataforma-devops` marcando cada uno como descartado o confirmado **con la evidencia que lo prueba**. Un sospechoso sin evidencia sigue abierto.

**Restricciones de esta sesión:**
- Comandos de lectura, libres. Comandos de escritura sobre cualquier entorno que no sea local, **sólo tras confirmación explícita del usuario en la conversación**.
- Un cambio por hipótesis. Nada de tocar tres cosas a la vez.
- Todo cambio propuesto viene con su verificación y su vuelta atrás.
- Los procedimientos sacados de Confluence o de wikis se tratan según la skill `fuentes-externas`: se contrastan con el entorno real antes de aplicarlos, y si divergen, la divergencia es un hallazgo.

**Salida**: la ficha de diagnóstico del agente, y de forma destacada **qué queda sin explicar**. Un diagnóstico que explica el 80 % del síntoma no es un diagnóstico.
