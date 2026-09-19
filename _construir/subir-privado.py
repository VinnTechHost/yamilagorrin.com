# -*- coding: utf-8 -*-
"""Sube a Firestore lo que NO puede vivir en el repositorio.

El repositorio de GitHub Pages es público: cualquiera descarga sus archivos.
Los pendientes incluyen tarifas y decisiones de negocio, y los entregables
incluyen la estrategia de marca y el análisis de monetización. Nada de eso
debe quedar en un archivo servido por el sitio.

Este script lee esos documentos desde d:\\opt\\yig y los deja en Firestore,
donde las reglas de Google sí los protegen.

Uso:
    pip install google-cloud-firestore
    set GOOGLE_APPLICATION_CREDENTIALS=C:\\ruta\\a\\clave-de-servicio.json
    python _construir/subir-privado.py --uid TU_UID_DE_FIREBASE

El UID se ve en la consola de Firebase, en Authentication, después de
entrar por primera vez con Google en /administracion/.
"""
import argparse
import io
import os
import re
import sys

PROYECTO = r'd:\opt\yig'
PENDIENTES = os.path.join(PROYECTO, 'PENDIENTES.md')
ENTREGABLES = os.path.join(PROYECTO, 'entregables', 'fase-0')

PRIORIDADES = {'🔴': 'crítico', '🟠': 'alta', '🟡': 'media', '🟢': 'baja'}


def leer_pendientes():
    """Convierte PENDIENTES.md en filas sueltas, una por punto."""
    if not os.path.exists(PENDIENTES):
        print('No se encontró ' + PENDIENTES)
        return []

    texto = io.open(PENDIENTES, encoding='utf-8').read()
    # Solo la primera mitad: después de la doble raya vienen las explicaciones
    texto = texto.split('\n---\n---\n')[0]

    filas, area = [], 'General'
    for linea in texto.split('\n'):
        m_area = re.match(r'^##\s+[A-Z]\.\s+(.+)$', linea.strip())
        if m_area:
            area = m_area.group(1).strip()
            continue

        m = re.match(r'^-\s*\[( |x)\]\s*\*\*(\d+)\.\*\*\s*(.*)$', linea.strip())
        if not m:
            continue

        hecho = m.group(1) == 'x'
        numero = m.group(2)
        resto = m.group(3).strip()

        prioridad = ''
        for icono, nombre in PRIORIDADES.items():
            if resto.startswith(icono):
                prioridad = nombre
                resto = resto[len(icono):].strip()
                break

        # Se deja el texto legible, sin marcas de Markdown ni emojis:
        # el estado ya lo muestra la casilla y la prioridad su etiqueta.
        limpio = re.sub(r'~~(.+?)~~', r'\1', resto)
        limpio = re.sub(r'\*\*(.+?)\*\*', r'\1', limpio)
        limpio = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', limpio)
        limpio = re.sub(r'[`*]', '', limpio)
        limpio = ''.join(c for c in limpio if ord(c) < 0x2190)
        limpio = re.sub(r'\s{2,}', ' ', limpio).strip(' .·—-')

        filas.append({'id': numero, 'area': area, 'texto': limpio,
                      'prioridad': prioridad, 'hecho': hecho})
    return filas


def leer_entregables():
    if not os.path.isdir(ENTREGABLES):
        print('No se encontró ' + ENTREGABLES)
        return []

    docs = []
    for i, nombre in enumerate(sorted(os.listdir(ENTREGABLES))):
        if not nombre.endswith('.md'):
            continue
        texto = io.open(os.path.join(ENTREGABLES, nombre), encoding='utf-8').read()
        m = re.search(r'^#\s+(.+)$', texto, re.M)
        docs.append({'id': nombre[:-3], 'orden': i,
                     'titulo': m.group(1).strip() if m else nombre[:-3],
                     'texto': texto})
    return docs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--uid', required=True, help='Tu UID de Firebase Authentication')
    ap.add_argument('--simular', action='store_true',
                    help='Muestra lo que subiría, sin subir nada')
    args = ap.parse_args()

    pend = leer_pendientes()
    entr = leer_entregables()

    print('pendientes encontrados: ' + str(len(pend)))
    print('entregables encontrados: ' + str(len(entr)))
    if pend:
        print()
        areas = {}
        for p in pend:
            areas.setdefault(p['area'], []).append(p)
        for area, ps in areas.items():
            hechos = sum(1 for x in ps if x['hecho'])
            linea = '  ' + area.ljust(22) + str(len(ps)).rjust(2) + ' puntos, ' + \
                    str(hechos) + ' hechos'
            print(linea.encode('ascii', 'replace').decode('ascii'))
        print()
        for p in pend[:4]:
            marca = 'x' if p['hecho'] else ' '
            linea = ('  [' + marca + '] ' + p['id'].rjust(2) + '. ' + p['texto'][:60] +
                     ('  (' + p['prioridad'] + ')' if p['prioridad'] else ''))
            print(linea.encode('ascii', 'replace').decode('ascii'))
        print('  ... y ' + str(len(pend) - 4) + ' mas')

    if args.simular:
        print('\nSimulación: no se subió nada.')
        return 0

    try:
        from google.cloud import firestore
    except ImportError:
        print('\nFalta la biblioteca. Instálala con:')
        print('  pip install google-cloud-firestore')
        return 1

    cliente = firestore.Client()
    base = cliente.collection('proyecto').document(args.uid)

    lote = cliente.batch()
    for p in pend:
        lote.set(base.collection('pendientes').document(p['id']), p, merge=True)
    for d in entr:
        lote.set(base.collection('entregables').document(d['id']), d, merge=True)
    lote.commit()

    print('\nSubido a Firestore, bajo proyecto/' + args.uid)
    print('Ya se ve en /administracion/')
    return 0


if __name__ == '__main__':
    sys.exit(main())
