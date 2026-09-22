#!/usr/bin/env python3
"""Comprueba que un pase de estilo no ha alterado contenido tecnico.

Extrae de ambas versiones los elementos que la redaccion NUNCA debe tocar
-- codigos de requisito, referencias a secciones, cifras, identificadores,
endpoints, URLs y bloques de codigo -- y compara los conjuntos.

Uso:  python3 scripts/invariantes_texto.py antes.md despues.md
Salida: 0 si los invariantes se conservan, 1 si alguno cambio.
"""
import re
import sys
from collections import Counter

PATRONES = {
    "requisitos":   r"\bR(?:N)?F-\d{3,}\b",
    "referencias":  r"§\s?\d+(?:\.\d+)*",
    "adr":          r"\bADR-\d{3,}\b",
    "endpoints":    r"\b(?:GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+/[^\s`\)\|]*",
    "urls":         r"https?://[^\s`\)\|]+",
    "identificadores": r"`[^`\n]+`",
    "versiones":    r"\bv?\d+\.\d+(?:\.\d+)*\b",
    "cifras":       r"(?<![\w.])\d{1,3}(?:[.,]\d+)?\s?(?:ms|s|min|h|KB|MB|GB|%|€|reintentos?|segundos?|minutos?)\b",
}
BLOQUE_CODIGO = re.compile(r"```.*?```", re.S)
TABLA = re.compile(r"^\s*\|.*\|\s*$", re.M)


def extraer(texto):
    fuera = {"bloques_codigo": Counter(
        b.strip() for b in BLOQUE_CODIGO.findall(texto))}
    fuera["filas_tabla"] = Counter(
        re.sub(r"\s+", " ", f).strip() for f in TABLA.findall(texto))
    sin_codigo = BLOQUE_CODIGO.sub(" ", texto)
    for nombre, patron in PATRONES.items():
        fuera[nombre] = Counter(m.strip() for m in re.findall(patron, sin_codigo))
    return fuera


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    antes, despues = (open(p, encoding="utf-8").read() for p in sys.argv[1:3])
    a, d = extraer(antes), extraer(despues)

    incidencias = 0
    for clave in a:
        perdidos = a[clave] - d[clave]
        nuevos = d[clave] - a[clave]
        if not perdidos and not nuevos:
            continue
        incidencias += sum(perdidos.values()) + sum(nuevos.values())
        print(f"\n[{clave}]")
        for item, n in perdidos.items():
            print(f"  DESAPARECE (x{n}): {item[:110]}")
        for item, n in nuevos.items():
            print(f"  APARECE    (x{n}): {item[:110]}")

    palabras_antes = len(antes.split())
    palabras_despues = len(despues.split())
    delta = (palabras_despues - palabras_antes) / max(palabras_antes, 1) * 100

    print(f"\nPalabras: {palabras_antes} -> {palabras_despues} ({delta:+.1f} %)")
    if abs(delta) > 25:
        print("  AVISO: variacion de extension superior al 25 %. Un pase de estilo")
        print("         reformula; si el texto crece o encoge tanto, se ha anadido")
        print("         o eliminado contenido.")

    if incidencias:
        print(f"\n{incidencias} invariantes alterados. REVISAR: el pase de estilo toco contenido.")
        return 1
    print("\nInvariantes conservados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
