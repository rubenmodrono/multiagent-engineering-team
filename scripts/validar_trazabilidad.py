#!/usr/bin/env python3
"""Valida la matriz de trazabilidad RF -> codigo -> test -> documentacion.

Gate barato que se ejecuta antes de cada revision documental. Sin dependencias.
Uso:  python3 scripts/validar_trazabilidad.py [ruta_matriz]
Salida: 0 si todo correcto, 1 si hay errores.
"""
import csv
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATRIZ = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "docs/trazabilidad/matriz.csv")

COLUMNAS = ["rf", "titulo", "estado", "version", "seccion_df", "seccion_dt",
            "componentes", "endpoints", "ruta_gateway", "tests", "adr", "notas"]
ESTADOS = {"implementado", "parcial", "pendiente", "retirado"}

errores, avisos = [], []


def rutas(celda):
    return [p.strip() for p in (celda or "").split(";") if p.strip()]


def main():
    if not os.path.exists(MATRIZ):
        print(f"ERROR: no existe la matriz en {MATRIZ}")
        return 1

    with open(MATRIZ, newline="", encoding="utf-8") as fh:
        filas = list(csv.DictReader(fh))

    if not filas:
        print("AVISO: la matriz esta vacia.")
        return 0

    faltan = [c for c in COLUMNAS if c not in filas[0]]
    if faltan:
        errores.append(f"cabecera: faltan columnas {faltan}")

    vistos = set()
    for i, fila in enumerate(filas, start=2):
        rf = (fila.get("rf") or "").strip()
        ref = f"fila {i} ({rf or 'sin rf'})"

        if not rf:
            errores.append(f"{ref}: falta el codigo de requisito")
        elif not re.fullmatch(r"R(N?)F-\d{3,}", rf):
            avisos.append(f"{ref}: codigo con formato inesperado (se espera RF-nnn o RNF-nnn)")
        elif rf in vistos:
            errores.append(f"{ref}: requisito duplicado")
        vistos.add(rf)

        estado = (fila.get("estado") or "").strip().lower()
        if estado not in ESTADOS:
            errores.append(f"{ref}: estado '{estado}' no valido (permitidos: {sorted(ESTADOS)})")

        for columna in ("componentes", "tests"):
            for ruta in rutas(fila.get(columna)):
                if not os.path.exists(os.path.join(RAIZ, ruta)):
                    errores.append(f"{ref}: {columna} apunta a una ruta inexistente -> {ruta}")

        for adr in rutas(fila.get("adr")):
            patron = re.compile(rf"^0*{re.escape(adr.lstrip('0') or '0')}\b")
            dir_adr = os.path.join(RAIZ, "docs/adr")
            encontrado = os.path.isdir(dir_adr) and any(
                patron.match(n) for n in os.listdir(dir_adr))
            if not encontrado:
                errores.append(f"{ref}: ADR {adr} referenciado pero no existe en docs/adr/")

        if estado == "implementado":
            if not rutas(fila.get("componentes")):
                errores.append(f"{ref}: implementado sin componentes de codigo")
            if not rutas(fila.get("tests")):
                errores.append(f"{ref}: implementado sin tests -> hueco de cobertura")
            if not (fila.get("seccion_df") or "").strip():
                errores.append(f"{ref}: implementado sin seccion en el Diseno Funcional")
            if not (fila.get("seccion_dt") or "").strip():
                errores.append(f"{ref}: implementado sin seccion en el Diseno Tecnico")
            if (fila.get("endpoints") or "").strip() and not (fila.get("ruta_gateway") or "").strip():
                avisos.append(f"{ref}: expone endpoints sin ruta declarada en el gateway")

        if estado == "pendiente" and rutas(fila.get("componentes")):
            avisos.append(f"{ref}: marcado pendiente pero ya tiene codigo asociado")

    mostrar = os.path.relpath(MATRIZ, RAIZ)
    if mostrar.startswith(".."):
        mostrar = MATRIZ
    print(f"Matriz: {mostrar} — {len(filas)} requisitos\n")
    for a in avisos:
        print(f"  AVISO  {a}")
    for e in errores:
        print(f"  ERROR  {e}")
    print(f"\n{len(errores)} errores, {len(avisos)} avisos")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
