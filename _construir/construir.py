# -*- coding: utf-8 -*-
"""Genera el sitio completo. Se ejecuta a mano o desde la acción de GitHub."""
import html
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datos import (DOMINIO, CORREO, INSTAGRAM, OBRAS, SERIES, REDIRECCIONES,
                   MENU, comprobar)
from plantilla import cabeza, navegacion, PIE, markdown, resumen

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENIDO = os.path.join(RAIZ, 'contenido', 'blog')
escritos = []


def escribir(rel, contenido):
    destino = os.path.join(RAIZ, rel)
    carpeta = os.path.dirname(destino)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    io.open(destino, 'w', encoding='utf-8', newline='\n').write(contenido)
    escritos.append(rel.replace('\\', '/'))


def img(clave):
    return '/img_webp/' + clave + '.webp'


def ficha(o):
    return ' · '.join(x for x in [o.get('medidas'), o.get('tecnica'), o.get('anio')] if x)


# ------------------------------------------------------- datos estructurados

PERSONA = {
    "@type": "Person", "@id": DOMINIO + "/#yamila-gorrin",
    "name": "Yamila Gorrín", "givenName": "Yamila", "familyName": "Gorrín",
    "jobTitle": "Artista visual, acuarelista y fotógrafa",
    "description": "Acuarelista y fotógrafa venezolana radicada en Santiago de Chile. "
                   "Pinta paisajes atmosféricos en acuarela y enseña a mirar antes de pintar.",
    "url": DOMINIO + "/", "image": DOMINIO + "/img_webp/yamilagorrinBalncoyNegro.webp",
    "email": "mailto:" + CORREO,
    "nationality": {"@type": "Country", "name": "Venezuela"},
    "homeLocation": {"@type": "Place", "name": "Santiago, Chile"},
    "knowsAbout": ["Acuarela", "Pintura de paisaje", "Plein air", "Fotografía",
                   "Pintura botánica", "Retrato"],
    "sameAs": [INSTAGRAM],
    "alumniOf": [{"@type": "EducationalOrganization", "name": "Academia Chaplin"},
                 {"@type": "EducationalOrganization", "name": "Academia CAPA"}],
    "award": ["Seleccionada, concurso Visiones del Agua, International Watercolor "
              "Society (IWS) 2025"],
}

SITIO = {"@type": "WebSite", "@id": DOMINIO + "/#sitio", "url": DOMINIO + "/",
         "name": "Yamila Gorrín · Acuarela", "inLanguage": "es-CL",
         "about": {"@id": DOMINIO + "/#yamila-gorrin"}}


def obra_ld(clave):
    o = OBRAS[clave]
    d = {"@type": "VisualArtwork", "name": o['titulo'], "artform": "Acuarela",
         "artMedium": o.get('tecnica', 'Acuarela sobre papel'),
         "image": DOMINIO + img(clave),
         "creator": {"@id": DOMINIO + "/#yamila-gorrin"}}
    if o.get('anio'):
        d["dateCreated"] = o['anio']
    m = re.match(r'^([\d,\.]+)\s*×\s*([\d,\.]+)', o.get('medidas', ''))
    if m:
        d["width"] = {"@type": "QuantitativeValue",
                      "value": m.group(1).replace(',', '.'), "unitCode": "CMT"}
        d["height"] = {"@type": "QuantitativeValue",
                       "value": m.group(2).replace(',', '.'), "unitCode": "CMT"}
    return d


# --------------------------------------------------------------- portada

CREDENCIALES = [
    ('IWS 2025', 'Seleccionada en «Visiones del Agua»'),
    ('Art Week Santiago', 'Expositora y demostradora técnica, 2024 y 2025'),
    ('Santiago Sur 2025', 'Festival de Arte Contemporáneo'),
    ('Academia CAPA', 'Formación avanzada en acuarela'),
]


def portada(entradas):
    destacada = 'Dominicos_Yamila_Gorrin'
    o = OBRAS[destacada]

    p = [cabeza('Yamila Gorrín | Acuarelista, artista visual y fotógrafa | Santiago de Chile',
                'Acuarelas originales de Yamila Gorrín: paisajes atmosféricos, plein air, '
                'naturaleza y retrato. El paisaje no es el tema, la sensación es el tema. '
                'Santiago de Chile.',
                DOMINIO + '/', img(destacada),
                {"@context": "https://schema.org", "@graph": [PERSONA, SITIO]})]
    p.append(navegacion(''))
    p.append('<main id="principal">\n')

    # 1. Tesis
    p.append('''  <section class="portada">
    <div class="portada-texto-col">
      <p class="portada-eyebrow">Acuarela de paisaje · Santiago de Chile</p>
      <h1 class="portada-lema">El paisaje no es el tema.<br><em>La sensación es el tema.</em></h1>
      <p class="portada-texto">
        Soy Yamila Gorrín, acuarelista y fotógrafa. Pinto lo que un lugar produce —la hora
        del día, la humedad del aire, lo que se disuelve— y no el lugar en sí.
      </p>
      <p class="portada-texto apagado">
        Pintar una obra me toma unas tres horas. Decidir qué pintar puede tomarme semanas.
        Ese desequilibrio no es un defecto del método: es el método.
      </p>
      <nav class="portada-acciones" aria-label="Accesos rápidos">
        <a class="boton" href="/plein-air/">Plein Air</a>
        <a class="boton" href="/paisajes/">Paisajes</a>
        <a class="boton" href="/naturaleza/">Naturaleza</a>
        <a class="boton boton-plano" href="/blog/">Blog</a>
      </nav>
    </div>
    <figure class="portada-figura">
      <img src="''' + img(destacada) + '''" width="1000" height="1335"
           alt="''' + html.escape(o['alt']) + '''"
           fetchpriority="high" decoding="async">
      <figcaption>
        <strong>''' + o['titulo'] + '''</strong> · ''' + ficha(o) + '''<br>
        <span class="credencial">''' + o['credencial'] + '''</span>
      </figcaption>
    </figure>
  </section>

''')

    # 2. Franja de credenciales — señales de confianza, y lo que leen las IA
    p.append('  <section class="credenciales">\n    <div class="contenedor-ancho">\n      <ul>\n')
    for titulo, detalle in CREDENCIALES:
        p.append('        <li><strong>' + html.escape(titulo) + '</strong>'
                 '<span>' + html.escape(detalle) + '</span></li>\n')
    p.append('      </ul>\n    </div>\n  </section>\n\n')

    # 3. Series
    p.append('  <section class="franja">\n    <div class="contenedor">\n')
    p.append('      <div class="encabezado-seccion">\n'
             '        <p class="rotulo">La obra</p>\n'
             '        <h2>Cuatro maneras de mirar</h2>\n'
             '      </div>\n')
    p.append('      <ul class="series">\n')
    for s in SERIES:
        clave = s['obras'][0]
        p.append('        <li><a class="serie-tarjeta" href="/' + s['ruta'] + '/">\n')
        p.append('          <div class="serie-marco"><img src="' + img(clave) +
                 '" alt="' + html.escape(OBRAS[clave]['alt']) +
                 '" loading="lazy" decoding="async"></div>\n')
        p.append('          <h3 class="serie-nombre">' + html.escape(s['nombre']) + '</h3>\n')
        p.append('          <p class="serie-pie">' + str(len(s['obras'])) + ' obras</p>\n')
        p.append('        </a></li>\n')
    p.append('      </ul>\n    </div>\n  </section>\n\n')

    # 4. El método, con obra de apoyo
    p.append('''  <section class="franja metodo">
    <div class="contenedor metodo-caja">
      <figure class="metodo-figura">
        <img src="''' + img('atmosfera1') + '''" loading="lazy" decoding="async"
             alt="''' + html.escape(OBRAS['atmosfera1']['alt']) + '''">
      </figure>
      <div>
        <p class="rotulo">El método</p>
        <h2>La mirada antes que el pincel</h2>
        <p>
          Cuatro años de formación fotográfica me enseñaron a leer una escena antes de
          registrarla: el encuadre, la jerarquía, qué dejar fuera. La acuarela me enseñó que
          esa decisión hay que tomarla antes, porque después no hay vuelta atrás.
        </p>
        <p>
          Por eso puedo pintar lugares donde nunca estuve. No copio un paisaje: leo una
          imagen —qué la sostiene, dónde está la luz, qué sobra— y traduzco eso al papel.
        </p>
        <p><a class="enlace-flecha" href="/sobre-mi/">Cómo llegué hasta acá</a></p>
      </div>
    </div>
  </section>

''')

    # 5. Blog
    if entradas:
        p.append('  <section class="franja">\n    <div class="contenedor">\n')
        p.append('      <div class="encabezado-seccion">\n'
                 '        <p class="rotulo">Del cuaderno</p>\n'
                 '        <h2>Lo que decido mientras pinto</h2>\n'
                 '      </div>\n')
        p.append('      <ul class="entradas">\n')
        for e in entradas[:3]:
            p.append('        <li><a class="entrada-tarjeta" href="/blog/' + e['slug'] + '/">\n')
            p.append('          <time datetime="' + e['fecha'] + '">' + e['fecha_larga'] + '</time>\n')
            p.append('          <h3>' + html.escape(e['titulo']) + '</h3>\n')
            p.append('          <p>' + html.escape(e['resumen']) + '</p>\n')
            p.append('        </a></li>\n')
        p.append('      </ul>\n')
        p.append('      <p><a class="enlace-flecha" href="/blog/">Todas las entradas</a></p>\n')
        p.append('    </div>\n  </section>\n\n')

    # 6. Contacto
    # El cierre no anuncia disponibilidad: describe lo que recibe quien
    # escribe, y le da la primera frase ya escrita.
    p.append('''  <section class="franja cierre">
    <div class="contenedor cierre-caja">
      <h2>Un encargo</h2>
      <p class="cierre-lema">Tú eliges el lugar que te importa. Yo decido cómo mirarlo.</p>
      <p class="cierre-texto">
        Escríbeme contándome qué lugar es y por qué, y te respondo con el proceso completo,
        el plazo y el precio. Sin compromiso.
      </p>
      <p class="cierre-credencial">
        Seleccionada en «Visiones del Agua», International Watercolor Society 2025
      </p>
      <p class="portada-acciones">
        <a class="boton" href="mailto:''' + CORREO +
             '''?subject=Encargo%20de%20una%20obra">Escribir sobre un encargo</a>
        <a class="boton boton-plano" href="mailto:''' + CORREO +
             '''?subject=Salidas%20a%20pintar%20al%20aire%20libre">Salidas a pintar al aire libre</a>
      </p>
    </div>
  </section>
</main>
''')

    # Las direcciones viejas con ancla no quedan rotas
    p.append('<script>\n(function () {\n  var mapa = ' +
             json.dumps(REDIRECCIONES, ensure_ascii=False) + ';\n'
             '  var destino = mapa[location.hash];\n'
             '  if (destino) location.replace(destino);\n})();\n</script>\n')
    p.append(PIE)
    escribir('index.html', ''.join(p))


# --------------------------------------------------------------- series

def pagina_serie(s):
    claves = s['obras']
    og = img(claves[0])
    ld = {"@context": "https://schema.org", "@type": "CollectionPage",
          "name": s['nombre'], "description": s['meta'],
          "url": DOMINIO + '/' + s['ruta'] + '/',
          "isPartOf": {"@id": DOMINIO + "/#sitio"},
          "about": {"@id": DOMINIO + "/#yamila-gorrin"},
          "hasPart": [obra_ld(c) for c in claves]}

    p = [cabeza(s['titulo'] + ' | Yamila Gorrín', s['meta'],
                DOMINIO + '/' + s['ruta'] + '/', og, ld)]
    p.append(navegacion(s['ruta']))
    p.append('<main id="principal">\n')
    p.append('  <section class="intro-serie">\n')
    p.append('    <p class="migas"><a href="/">Inicio</a> <span>/</span> ' +
             html.escape(s['nombre']) + '</p>\n')
    p.append('    <h1>' + html.escape(s['nombre']) + '</h1>\n')
    p.append('    <p class="entradilla">' + html.escape(s['intro']) + '</p>\n')
    if s.get('apunte'):
        p.append('    <p class="apunte">' + html.escape(s['apunte']) + '</p>\n')
    p.append('    <p class="conteo">' + str(len(claves)) + ' obras</p>\n')
    p.append('  </section>\n\n  <section class="galeria">\n')

    for c in claves:
        o = OBRAS[c]
        p.append('      <figure class="obra">\n'
                 '        <div class="obra-marco">\n'
                 '          <img src="' + img(c) + '" alt="' + html.escape(o['alt']) + '"'
                 ' loading="lazy" decoding="async">\n'
                 '        </div>\n'
                 '        <figcaption>\n'
                 '          <h2>' + html.escape(o['titulo']) + '</h2>\n'
                 '          <p class="ficha">' + html.escape(ficha(o)) + '</p>\n')
        if o.get('credencial'):
            p.append('          <p class="credencial">' + html.escape(o['credencial']) + '</p>\n')
        p.append('        </figcaption>\n      </figure>\n')

    p.append('  </section>\n')
    p.append('  <nav class="siguientes" aria-label="Otras series">\n'
             '    <h2>Otras series</h2>\n    <ul>\n')
    for x in SERIES:
        if x['ruta'] != s['ruta']:
            p.append('      <li><a href="/' + x['ruta'] + '/">' +
                     html.escape(x['nombre']) + '</a></li>\n')
    p.append('    </ul>\n  </nav>\n</main>\n')
    p.append(PIE)
    escribir(os.path.join(s['ruta'], 'index.html'), ''.join(p))


# ------------------------------------------------------------- sobre mí

def pagina_sobre_mi():
    ruta = os.path.join(RAIZ, 'contenido', 'sobre-mi.html')
    cuerpo = io.open(ruta, encoding='utf-8').read().strip()

    ld = {"@context": "https://schema.org", "@type": "AboutPage",
          "url": DOMINIO + "/sobre-mi/", "name": "Sobre mí | Yamila Gorrín",
          "isPartOf": {"@id": DOMINIO + "/#sitio"},
          "mainEntity": {"@id": DOMINIO + "/#yamila-gorrin"}}

    p = [cabeza('Sobre mí | Yamila Gorrín, acuarelista y fotógrafa',
                'Yamila Gorrín, artista visual venezolana radicada en Santiago de Chile. '
                'Empezó en la pandemia pintando un cactus. Fotógrafa por Academia Chaplin '
                'y acuarelista por Academia CAPA. Seleccionada en IWS 2025.',
                DOMINIO + '/sobre-mi/', '/img_webp/yamilagorrinBalncoyNegro.webp', ld)]
    p.append(navegacion('sobre-mi'))
    # No usa .ensayo: esta página es de bandas anchas, no una columna de lectura.
    p.append('<main id="principal">\n  <article class="biografia">\n')
    p.append(cuerpo + '\n')
    p.append('  </article>\n</main>\n')
    p.append(PIE)
    escribir(os.path.join('sobre-mi', 'index.html'), ''.join(p))


# ----------------------------------------------------------------- blog

MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
         'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']


def leer_entradas():
    if not os.path.isdir(CONTENIDO):
        return []
    entradas = []
    for nombre in sorted(os.listdir(CONTENIDO)):
        if not nombre.endswith('.md'):
            continue
        crudo = io.open(os.path.join(CONTENIDO, nombre), encoding='utf-8').read()

        meta, cuerpo = {}, crudo
        m = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', crudo, re.S)
        if m:
            for linea in m.group(1).split('\n'):
                if ':' in linea:
                    k, v = linea.split(':', 1)
                    meta[k.strip()] = v.strip().strip('"\'')
            cuerpo = m.group(2)

        if str(meta.get('borrador', '')).lower() in ('true', 'si', 'sí'):
            continue

        fecha = meta.get('fecha', nombre[:10])
        try:
            a, mes, d = fecha.split('-')
            larga = '%d de %s de %s' % (int(d), MESES[int(mes) - 1], a)
        except Exception:
            larga = fecha

        entradas.append({
            'slug': meta.get('slug') or re.sub(r'^\d{4}-\d{2}-\d{2}-', '', nombre[:-3]),
            'titulo': meta.get('titulo', 'Sin título'),
            'fecha': fecha, 'fecha_larga': larga,
            'imagen': meta.get('imagen', ''),
            'resumen': meta.get('resumen') or resumen(cuerpo),
            'cuerpo': cuerpo,
        })
    entradas.sort(key=lambda e: e['fecha'], reverse=True)
    return entradas


def pagina_entrada(e):
    og = e['imagen'] or img('atmosfera1')
    ld = {"@context": "https://schema.org", "@type": "BlogPosting",
          "headline": e['titulo'], "description": e['resumen'],
          "datePublished": e['fecha'],
          "url": DOMINIO + '/blog/' + e['slug'] + '/',
          "image": DOMINIO + og,
          "author": {"@id": DOMINIO + "/#yamila-gorrin"},
          "publisher": {"@id": DOMINIO + "/#yamila-gorrin"},
          "inLanguage": "es-CL",
          "isPartOf": {"@id": DOMINIO + "/#sitio"}}

    p = [cabeza(e['titulo'] + ' | Yamila Gorrín', e['resumen'],
                DOMINIO + '/blog/' + e['slug'] + '/', og, ld)]
    p.append(navegacion('blog'))
    p.append('<main id="principal">\n  <article class="ensayo">\n')
    p.append('    <p class="migas"><a href="/">Inicio</a> <span>/</span> '
             '<a href="/blog/">Blog</a> <span>/</span> Entrada</p>\n')
    p.append('    <p class="fecha-entrada"><time datetime="' + e['fecha'] + '">' +
             e['fecha_larga'] + '</time></p>\n')
    p.append('    <h1>' + html.escape(e['titulo']) + '</h1>\n')
    if e['imagen']:
        p.append('    <figure class="entrada-imagen"><img src="' + e['imagen'] +
                 '" alt="' + html.escape(e['titulo']) + '" decoding="async"></figure>\n')
    p.append(markdown(e['cuerpo']) + '\n')
    p.append('    <p class="volver-blog"><a class="enlace-flecha" href="/blog/">'
             'Todas las entradas</a></p>\n')
    p.append('  </article>\n</main>\n')
    p.append(PIE)
    escribir(os.path.join('blog', e['slug'], 'index.html'), ''.join(p))


def indice_blog(entradas):
    ld = {"@context": "https://schema.org", "@type": "Blog",
          "name": "Blog de Yamila Gorrín", "url": DOMINIO + "/blog/",
          "inLanguage": "es-CL",
          "author": {"@id": DOMINIO + "/#yamila-gorrin"},
          "blogPost": [{"@type": "BlogPosting", "headline": e['titulo'],
                        "datePublished": e['fecha'],
                        "url": DOMINIO + '/blog/' + e['slug'] + '/'} for e in entradas]}

    p = [cabeza('Blog | Yamila Gorrín',
                'Lo que decido mientras pinto: el proceso, las series y las decisiones '
                'detrás de cada acuarela.',
                DOMINIO + '/blog/', img('atmosfera1'), ld)]
    p.append(navegacion('blog'))
    p.append('<main id="principal">\n')
    p.append('  <section class="intro-serie">\n'
             '    <p class="migas"><a href="/">Inicio</a> <span>/</span> Blog</p>\n'
             '    <h1>Blog</h1>\n'
             '    <p class="entradilla">Lo que decido mientras pinto. Qué me detuvo en una '
             'escena, qué saqué, y qué hago cuando una obra no me gusta.</p>\n'
             '  </section>\n')

    if not entradas:
        p.append('  <section class="contenedor"><p class="vacio">Todavía no hay entradas '
                 'publicadas.</p></section>\n')
    else:
        p.append('  <section class="contenedor">\n    <ul class="entradas entradas-lista">\n')
        for e in entradas:
            p.append('      <li><a class="entrada-tarjeta" href="/blog/' + e['slug'] + '/">\n')
            p.append('        <time datetime="' + e['fecha'] + '">' + e['fecha_larga'] + '</time>\n')
            p.append('        <h2>' + html.escape(e['titulo']) + '</h2>\n')
            p.append('        <p>' + html.escape(e['resumen']) + '</p>\n')
            p.append('      </a></li>\n')
        p.append('    </ul>\n  </section>\n')

    p.append('</main>\n')
    p.append(PIE)
    escribir(os.path.join('blog', 'index.html'), ''.join(p))


# ------------------------------------------------------------ sitemap, etc.

def sitemap(entradas):
    from datetime import date
    hoy = date.today().isoformat()
    urls = [(DOMINIO + '/', '1.0'), (DOMINIO + '/sobre-mi/', '0.8'),
            (DOMINIO + '/blog/', '0.8')]
    urls += [(DOMINIO + '/' + s['ruta'] + '/', '0.9') for s in SERIES]
    urls += [(DOMINIO + '/blog/' + e['slug'] + '/', '0.7') for e in entradas]

    x = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, pr in urls:
        x += ['  <url>', '    <loc>' + u + '</loc>',
              '    <lastmod>' + hoy + '</lastmod>',
              '    <changefreq>monthly</changefreq>',
              '    <priority>' + pr + '</priority>', '  </url>']
    x.append('</urlset>')
    escribir('sitemap.xml', '\n'.join(x) + '\n')

    escribir('robots.txt',
             'User-agent: *\nAllow: /\n\n'
             '# La administración no se indexa: es una herramienta, no contenido.\n'
             'Disallow: /_administracion/\nDisallow: /_admin/\n\n'
             '# Los rastreadores de los motores de IA están permitidos a propósito:\n'
             '# aparecer en sus respuestas es parte del objetivo del sitio.\n\n'
             'Sitemap: ' + DOMINIO + '/sitemap.xml\n')


def catalogo_para_admin():
    """El cuaderno de Administración necesita la lista de obras.

    Esto sí puede ser público: son las mismas obras que ya se ven en el sitio.
    Lo que NO va al repositorio son los pendientes y los entregables.
    """
    lista = []
    for s in SERIES:
        for c in s['obras']:
            o = OBRAS[c]
            lista.append({'id': c, 'titulo': o['titulo'], 'serie': s['nombre'],
                          'ficha': ficha(o), 'img': img(c)})
    escribir(os.path.join('datos', 'obras.json'),
             json.dumps(lista, ensure_ascii=False, indent=1) + '\n')


def pagina_404():
    p = [cabeza('Página no encontrada | Yamila Gorrín',
                'La página que buscas no existe.', DOMINIO + '/404.html',
                img('atmosfera1'), noindex=True)]
    p.append(navegacion(''))
    p.append('<main id="principal">\n  <section class="perdida">\n'
             '    <h1>Esta página no existe</h1>\n'
             '    <p>Puede que el enlace haya cambiado. La obra está toda acá.</p>\n'
             '    <p class="portada-acciones"><a class="boton" href="/">Ir al inicio</a></p>\n'
             '  </section>\n</main>\n')
    p.append(PIE)
    escribir('404.html', ''.join(p))


def main():
    problemas, total = comprobar()
    if problemas:
        print('DATOS INCONSISTENTES:')
        for x in problemas:
            print('  ! ' + x)
        return 1

    entradas = leer_entradas()

    portada(entradas)
    for s in SERIES:
        pagina_serie(s)
    pagina_sobre_mi()
    indice_blog(entradas)
    for e in entradas:
        pagina_entrada(e)
    sitemap(entradas)
    catalogo_para_admin()
    pagina_404()

    print('obras publicadas: ' + str(total))
    print('series: ' + str(len(SERIES)))
    print('entradas de blog: ' + str(len(entradas)))
    print('archivos escritos: ' + str(len(escritos)))
    for f in escritos:
        print('  ' + f)
    return 0


if __name__ == '__main__':
    sys.exit(main())
