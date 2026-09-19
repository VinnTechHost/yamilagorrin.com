# -*- coding: utf-8 -*-
"""Piezas comunes a todas las páginas y un convertidor mínimo de Markdown."""
import html
import json
import re

from datos import DOMINIO, MENU, CORREO, INSTAGRAM

FUENTES = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?'
    'family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400'
    '&family=Karla:wght@400;500;700&display=swap" rel="stylesheet">\n'
    '<link rel="stylesheet" href="/css/style.css">\n'
)


def cabeza(titulo, meta, url, og, ld=None, noindex=False, extra=''):
    partes = [
        '<!DOCTYPE html>', '<html lang="es">', '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '',
        '<title>' + html.escape(titulo) + '</title>',
        '<meta name="description" content="' + html.escape(meta) + '">',
        '<meta name="author" content="Yamila Gorrín">',
    ]
    if noindex:
        partes.append('<meta name="robots" content="noindex, nofollow">')
    else:
        partes.append('<link rel="canonical" href="' + url + '">')

    partes += [
        '',
        '<meta property="og:type" content="website">',
        '<meta property="og:url" content="' + url + '">',
        '<meta property="og:title" content="' + html.escape(titulo) + '">',
        '<meta property="og:description" content="' + html.escape(meta) + '">',
        '<meta property="og:image" content="' + DOMINIO + og + '">',
        '<meta property="og:locale" content="es_CL">',
        '<meta property="og:site_name" content="Yamila Gorrín">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="' + html.escape(titulo) + '">',
        '<meta name="twitter:description" content="' + html.escape(meta) + '">',
        '<meta name="twitter:image" content="' + DOMINIO + og + '">',
        '',
        FUENTES.rstrip(),
    ]
    if ld:
        partes.append('<script type="application/ld+json">')
        partes.append(json.dumps(ld, ensure_ascii=False, indent=1))
        partes.append('</script>')
    if extra:
        partes.append(extra.rstrip())
    partes += ['</head>', '<body>', '']
    return '\n'.join(partes)


def navegacion(activa):
    filas = []
    for ruta, nombre in MENU:
        href = '/' + (ruta + '/' if ruta else '')
        act = ' aria-current="page"' if ruta == activa else ''
        filas.append('      <li><a href="' + href + '"' + act + '>' +
                     html.escape(nombre) + '</a></li>')
    return ('<a class="saltar" href="#principal">Saltar al contenido</a>\n'
            '<header class="cabecera">\n'
            '  <a class="marca" href="/">\n'
            '    <span class="marca-nombre">Yamila Gorrín</span>\n'
            '    <span class="marca-oficio">Acuarela · Fotografía</span>\n'
            '  </a>\n'
            '  <nav class="menu" aria-label="Secciones">\n    <ul>\n' +
            '\n'.join(filas) +
            '\n    </ul>\n  </nav>\n</header>\n')


PIE = ('<footer class="pie">\n'
       '  <div class="pie-caja">\n'
       '    <p class="pie-lema">El paisaje no es el tema. La sensación es el tema.</p>\n'
       '    <div class="pie-columnas">\n'
       '      <div>\n'
       '        <p class="pie-rotulo">Obra</p>\n'
       '        <ul class="pie-lista">\n'
       '          <li><a href="/plein-air/">Plein Air</a></li>\n'
       '          <li><a href="/paisajes/">Paisajes</a></li>\n'
       '          <li><a href="/naturaleza/">Naturaleza</a></li>\n'
       '          <li><a href="/etnias/">Etnias</a></li>\n'
       '        </ul>\n'
       '      </div>\n'
       '      <div>\n'
       '        <p class="pie-rotulo">Más</p>\n'
       '        <ul class="pie-lista">\n'
       '          <li><a href="/sobre-mi/">Sobre mí</a></li>\n'
       '          <li><a href="/blog/">Blog</a></li>\n'
       '        </ul>\n'
       '      </div>\n'
       '      <div>\n'
       '        <p class="pie-rotulo">Contacto</p>\n'
       '        <ul class="pie-lista">\n'
       '          <li><a href="mailto:' + CORREO + '">' + CORREO + '</a></li>\n'
       '          <li><a href="' + INSTAGRAM + '" rel="me noopener" target="_blank">'
       '@yamy_colors</a></li>\n'
       '          <li>Santiago de Chile</li>\n'
       '        </ul>\n'
       '      </div>\n'
       '    </div>\n'
       '  </div>\n'
       '</footer>\n'
       '</body>\n'
       '</html>\n')


# ------------------------------------------------------------ Markdown

def _en_linea(t):
    t = html.escape(t)
    t = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)\)',
               r'<img src="\2" alt="\1" loading="lazy" decoding="async">', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    return t


def markdown(texto):
    """Convertidor mínimo: encabezados, párrafos, listas, citas e imágenes.

    Deliberadamente sin dependencias: el sitio se construye con la biblioteca
    estándar y nada más, para que la acción de GitHub no dependa de nadie.
    """
    salida, lista, cita, parrafo = [], False, False, []

    def cerrar_parrafo():
        if parrafo:
            salida.append('<p>' + _en_linea(' '.join(parrafo)) + '</p>')
            del parrafo[:]

    for linea in texto.replace('\r\n', '\n').split('\n'):
        cruda = linea.rstrip()
        limpia = cruda.strip()

        if not limpia:
            cerrar_parrafo()
            if lista:
                salida.append('</ul>')
                lista = False
            if cita:
                salida.append('</blockquote>')
                cita = False
            continue

        m = re.match(r'^(#{1,4})\s+(.*)$', limpia)
        if m:
            cerrar_parrafo()
            if lista:
                salida.append('</ul>')
                lista = False
            if cita:
                salida.append('</blockquote>')
                cita = False
            n = len(m.group(1)) + 1
            salida.append('<h%d>%s</h%d>' % (n, _en_linea(m.group(2)), n))
            continue

        if limpia.startswith('> '):
            cerrar_parrafo()
            if not cita:
                salida.append('<blockquote>')
                cita = True
            salida.append('<p>' + _en_linea(limpia[2:]) + '</p>')
            continue

        if re.match(r'^[-*]\s+', limpia):
            cerrar_parrafo()
            if not lista:
                salida.append('<ul>')
                lista = True
            salida.append('<li>' + _en_linea(re.sub(r'^[-*]\s+', '', limpia)) + '</li>')
            continue

        if limpia in ('---', '***'):
            cerrar_parrafo()
            salida.append('<hr>')
            continue

        parrafo.append(limpia)

    cerrar_parrafo()
    if lista:
        salida.append('</ul>')
    if cita:
        salida.append('</blockquote>')
    return '\n'.join(salida)


def resumen(texto, limite=170):
    """Primer párrafo en texto plano, para la meta descripción."""
    plano = re.sub(r'^#.*$', '', texto, flags=re.M)
    plano = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', plano)
    plano = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', plano)
    plano = re.sub(r'[*`>#-]', '', plano)
    plano = ' '.join(plano.split())
    if len(plano) <= limite:
        return plano
    corte = plano[:limite].rsplit(' ', 1)[0]
    return corte + '…'
