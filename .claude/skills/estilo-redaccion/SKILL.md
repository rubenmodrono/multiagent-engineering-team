---
name: estilo-redaccion
description: Guía de redacción y naturalidad para los entregables documentales — cómo conseguir que el texto se lea como escrito por una persona del equipo, con la voz del documento original, sin tocar el contenido técnico. Usar en el pase de estilo de cualquier documento de entrega y cuando el texto redactado suene genérico, plano o mecánico.
---

# Estilo y naturalidad en documentación de entrega

## Qué significa aquí "humanizar"

No es disfrazar nada. Es un problema editorial concreto y viejo: un documento de entrega lo escriben varias manos en varias rondas, con prisa, y acaba con costuras — un apartado denso y otro hueco, una sección en impersonal y la siguiente en primera del plural, párrafos que no dicen nada y ocupan seis líneas. El pase de estilo cose eso.

El objetivo operativo es doble:
1. **Voz única**: todo el documento suena al mismo equipo.
2. **Densidad honesta**: cada párrafo aporta algo que el lector no sabía. Lo que no aporta, se va.

El texto generado por modelos tiene defectos característicos, pero son los mismos defectos que produce un humano escribiendo con desgana y prisa: abstracción, simetría excesiva y falta de compromiso. Corregirlos es escribir mejor, no camuflar.

## Paso 0 — Calibrar la voz (obligatorio, antes de tocar nada)

Toma dos o tres secciones que sepas escritas por el equipo humano (versiones anteriores del documento, otros entregables del mismo proyecto) y anota:

- **Longitud media de frase y, sobre todo, su varianza.** La prosa mecánica produce frases de longitud casi uniforme, entre 18 y 25 palabras, una detrás de otra. La prosa humana alterna: una de 35, una de 8, una de 20.
- **Persona y tratamiento**: impersonal ("se define"), primera del plural ("definimos"), sujeto sistema ("el módulo valida").
- **Grado de pasiva y de pasiva refleja.**
- **Cuándo listas y cuándo prosa.** Muchos equipos reservan las listas para enumeraciones cerradas y explican los procesos en prosa.
- **Terminología del cliente**: la palabra que usan ellos, exacta.
- **Nivel de hedging**: si el documento dice "se estima" o dice "será".

Escribe la calibración en dos líneas antes de empezar. Es tu vara de medir, y sustituye a cualquier preferencia propia.

## Catálogo de tics, con corrección

**1. Frases de longitud uniforme**
El defecto más delator y el menos evidente. Rómpelo deliberadamente: mezcla una frase larga con subordinadas, una media, y una corta que sentencie. Una frase de cinco palabras después de dos largas hace más por la naturalidad que cualquier otra técnica.

**2. Tricolon automático** — tres elementos siempre, por costumbre.
> ❌ La solución aporta escalabilidad, mantenibilidad y trazabilidad.
> ✅ La solución mejora la trazabilidad de las operaciones. En escalabilidad no cambia nada respecto a la versión anterior.

**3. Preámbulos vacíos**
`Es importante destacar que`, `cabe señalar que`, `en este sentido`, `a continuación se detalla`, `el presente documento tiene por objeto describir cómo`.
> ❌ Es importante destacar que el servicio valida el token en cada petición.
> ✅ El servicio valida el token en cada petición.
Regla: si al borrar la primera oración de un párrafo el párrafo sigue diciendo lo mismo, esa oración sobraba.

**4. Párrafo-resumen al final de cada sección**
`En conclusión, esta arquitectura permite…`. Ninguna sección de un diseño técnico necesita resumirse a sí misma. Bórralos.

**5. Simetría estructural excesiva**
Todas las secciones con la misma forma: intro de dos líneas, lista de cuatro puntos, cierre de dos líneas. La realidad no es simétrica: hay componentes que merecen dos páginas y otros dos líneas. Deja que el documento sea desigual, porque el sistema lo es.

**6. Listas con paralelismo perfecto**
Seis viñetas empezando todas por gerundio y todas de la misma longitud. Si tres de los seis puntos son triviales, van en una frase de prosa y la lista se queda con los tres que importan.

**7. Adjetivos en pareja sin contenido**
`robusto y escalable`, `eficiente y flexible`, `moderno y desacoplado`.
> ❌ Se ha implementado una arquitectura robusta y escalable.
> ✅ Cada servicio se despliega por separado, así que un error en liquidación no tumba el alta de clientes.
Sustituye siempre el adjetivo por el mecanismo que lo justifica. Si no hay mecanismo, el adjetivo era mentira.

**8. Conectores sobre-señalizados**
`Además,` `Por otro lado,` `Asimismo,` `En consecuencia,` al principio de cada párrafo. El español técnico aguanta muy bien la yuxtaposición. Deja un conector cuando marque una relación real, quita el resto.

**9. Abstracción sin anclaje**
> ❌ Se han aplicado mecanismos de control de errores adecuados.
> ✅ Los errores de la pasarela se reintentan tres veces con espera exponencial; a partir de ahí la operación se marca como fallida y salta a la cola de revisión manual.

**10. Falta de compromiso**
Un documento de diseño que no dice qué se descartó ni qué duele es un folleto. Donde haya una decisión, que aparezca la alternativa descartada y el precio que se paga. Eso es lo que más "suena a persona", porque sólo lo escribe quien estuvo en la discusión.

**11. Guion largo y dos puntos en exceso**
Bien usados, un recurso. Tres por página, un tic. Cuenta y reparte.

**12. Presente atemporal para lo no implementado**
`El sistema notifica al usuario` cuando aún no notifica. Esto no es estilo, es un defecto de contenido: repórtalo al redactor en vez de reescribirlo.

## Técnicas positivas

- **Empieza por el dato, no por el marco.** "El `timeout` del gateway son 30 segundos" antes que "en cuanto a la configuración de tiempos de espera…".
- **Nombra agentes.** "El gateway rechaza" se lee mejor y se audita mejor que "las peticiones son rechazadas".
- **Detalle concreto donde lo haya.** Un número, un nombre de fichero, un caso real valen más que un párrafo de cualidades.
- **Admite lo que no se sabe.** "No hemos medido el impacto en p99 con más de 200 conexiones concurrentes" es una frase excelente en un diseño técnico y ningún generador la escribe solo.
- **Lee en voz alta el párrafo.** Si te quedas sin aire o te aburres, el lector también.

## Invariantes: prohibido tocar

Identificadores, rutas, endpoints, nombres de campo/tabla/servicio. Cifras, umbrales, versiones, fechas. Códigos `RF-nnn` y referencias `§x.y`. Tablas, bloques de código, diagramas. Términos del glosario. Títulos y numeración.

Comprobación tras cada sección:
```bash
python3 scripts/invariantes_texto.py <antes.md> <despues.md>
```
Si el script reporta diferencias en identificadores, cifras o referencias, el pase de estilo ha corrompido contenido: revierte esa sección.

**Si mejorar el estilo exige cambiar un invariante, párate y repórtalo.** El estilo nunca gana al contenido.
