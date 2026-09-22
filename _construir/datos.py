# -*- coding: utf-8 -*-
"""Fuente de verdad del sitio: series, obras y textos.

Todo lo que se publica sale de aquí. Si una obra cambia de serie, se cambia
en este archivo y se regenera; no se edita el HTML a mano.
"""

DOMINIO = 'https://galeria.yamilagorrin.com'
CORREO = 'yamilagorrin@gmail.com'
INSTAGRAM = 'https://www.instagram.com/yamy_colors/'

# --------------------------------------------------------------- obras
# clave = nombre del archivo en img_webp, sin extensión

OBRAS = {
    'Valparaiso_Plein_air_Yamila_Gorrin': {
        'titulo': 'Valparaíso Plein Air', 'anio': '2025',
        'tecnica': 'Acuarela sobre papel, in situ', 'medidas': '26 × 36 cm',
        'alt': 'Acuarela de Valparaíso pintada al aire libre por Yamila Gorrín'},
    'Dominicos_Yamila_Gorrin': {
        'titulo': 'Dominicos Plein Air', 'anio': '2025',
        'tecnica': 'Acuarela sobre papel, in situ', 'medidas': '36 × 26 cm',
        'alt': 'Dominicos Plein Air, acuarela pintada al aire libre en Los Dominicos, '
               'Santiago, seleccionada en Visiones del Agua IWS 2025',
        'destacada': True,
        'credencial': 'Seleccionada en «Visiones del Agua», International Watercolor Society 2025'},
    'Vina_del_mar_plein_air_Yamila_Gorrin': {
        'titulo': 'Viña del Mar Plein Air', 'anio': '2025',
        'tecnica': 'Acuarela sobre papel, in situ', 'medidas': '26 × 36 cm',
        'alt': 'Acuarela de Viña del Mar pintada al aire libre por Yamila Gorrín'},

    'Mapocho_hoy_Yamila_gorrin': {
        'titulo': 'Mapocho Hoy', 'anio': '2025',
        'tecnica': 'Acuarela sobre papel', 'medidas': '20 × 30 cm',
        'alt': 'Acuarela del río Mapocho en Santiago, pintada por Yamila Gorrín'},
    'Mapocho_historico_Yamila_gorrin': {
        'titulo': 'Mapocho Histórico', 'anio': '2025',
        'tecnica': 'Acuarela sobre papel', 'medidas': '20 × 30 cm',
        'alt': 'Acuarela del río Mapocho en su época histórica, por Yamila Gorrín'},
    'Venesia_Yamila_Gorrin': {
        'titulo': 'Venesia', 'anio': '2025',
        'tecnica': 'Acuarela sobre papel', 'medidas': '29,8 × 23,8 cm',
        'alt': 'Venesia, acuarela de canales venecianos por Yamila Gorrín'},
    'Urbano1_Yamila_Gorrin': {
        'titulo': 'Urbano I', 'anio': '2025',
        'tecnica': 'Acuarela sobre papel', 'medidas': '23,8 × 29,8 cm',
        'alt': 'Urbano I, acuarela de paisaje urbano por Yamila Gorrín'},
    'Urbano2_Yamila_Gorrin': {
        'titulo': 'Urbano II', 'anio': '2025',
        'tecnica': 'Acuarela sobre papel', 'medidas': '30 × 20 cm',
        'alt': 'Urbano II, acuarela de paisaje urbano por Yamila Gorrín'},
    'Urbano3_Yamila_Gorrin': {
        'titulo': 'Urbano III', 'anio': '2025',
        'tecnica': 'Acuarela sobre papel', 'medidas': '29,8 × 23,8 cm',
        'alt': 'Urbano III, acuarela de paisaje urbano por Yamila Gorrín'},
    'Faro1_Yamila_Gorrin': {
        'titulo': 'Faro', 'anio': '2025',
        'tecnica': 'Acuarela sobre papel', 'medidas': '30 × 20 cm',
        'alt': 'Faro, acuarela de paisaje costero por Yamila Gorrín'},
    'Neruda1_Yamila_Gorrin': {
        'titulo': 'Neruda', 'anio': '2025',
        'tecnica': 'Acuarela sobre papel', 'medidas': '23,8 × 29,8 cm',
        'alt': 'Neruda, acuarela inspirada en la casa del poeta, por Yamila Gorrín'},
    'atmosfera1': {
        'titulo': 'Añoranza', 'anio': '2023',
        'tecnica': 'Acuarela sobre papel', 'medidas': '17 × 23,7 cm',
        'alt': 'Añoranza, acuarela atmosférica con un bote y bordes disueltos, '
               'por Yamila Gorrín'},
    'atmosfera2': {
        'titulo': 'Atmósfera I', 'anio': '2023',
        'tecnica': 'Acuarela sobre papel', 'medidas': '23,7 × 17 cm',
        'alt': 'Atmósfera I, acuarela de embarcaciones entre la bruma, por Yamila Gorrín'},

    'Tulipan1_Yamila_Gorrin': {
        'titulo': 'Tulipán I', 'anio': '2025',
        'tecnica': 'Acuarela sobre papel', 'medidas': '45,5 × 30,5 cm',
        'alt': 'Tulipán I, acuarela botánica por Yamila Gorrín'},
    'Tulipan2_Yamila_Gorrin': {
        'titulo': 'Tulipán II', 'anio': '2025',
        'tecnica': 'Acuarela sobre papel', 'medidas': '29,8 × 23,8 cm',
        'alt': 'Tulipán II, acuarela botánica de tulipanes en un jarrón, por Yamila Gorrín'},
    'Rosas_Yamila_Gorrin': {
        'titulo': 'Rosas', 'anio': '2025',
        'tecnica': 'Acuarela sobre papel', 'medidas': '26 × 36 cm',
        'alt': 'Rosas, acuarela botánica por Yamila Gorrín'},
    'atmosfera3': {
        'titulo': 'Atmósfera II', 'anio': '2023',
        'tecnica': 'Acuarela sobre papel', 'medidas': '17 × 23,7 cm',
        'alt': 'Atmósfera II, acuarela de un árbol entre la bruma, por Yamila Gorrín'},
    'bosque1': {
        'titulo': 'Susurro entre la luz y la bruma', 'anio': '2024',
        'tecnica': 'Acuarela sobre papel', 'medidas': '52,4 × 39,5 cm',
        'alt': 'Susurro entre la luz y la bruma, acuarela de gran formato de un bosque, '
               'por Yamila Gorrín'},
    'bosque2': {
        'titulo': 'Fuego', 'anio': '2024',
        'tecnica': 'Acuarela sobre papel', 'medidas': '48 × 38 cm',
        'alt': 'Fuego, acuarela de gran formato sobre luz entre árboles, por Yamila Gorrín'},
    'otras1': {
        'titulo': 'Fantasy of tears', 'anio': '2024',
        'tecnica': 'Acuarela sobre papel', 'medidas': '24 × 30 cm',
        'alt': 'Fantasy of tears, acuarela por Yamila Gorrín'},
    'otras2': {
        'titulo': 'Natura', 'anio': '2023',
        'tecnica': 'Acuarela sobre papel', 'medidas': '41 × 29 cm',
        'alt': 'Natura, acuarela de un árbol por Yamila Gorrín'},

    'etnias1': {
        'titulo': 'Etnias I', 'anio': '2023',
        'tecnica': 'Acuarela sobre papel', 'medidas': '29,8 × 23,8 cm',
        'alt': 'Etnias I, retrato en acuarela por Yamila Gorrín'},
    'etnias2': {
        'titulo': 'Etnias II', 'anio': '2023',
        'tecnica': 'Acuarela sobre papel', 'medidas': '34,9 × 26,5 cm',
        'alt': 'Etnias II, retrato en acuarela por Yamila Gorrín'},
    'etnias3': {
        'titulo': 'Etnias III', 'anio': '2023',
        'tecnica': 'Acuarela sobre papel', 'medidas': '29,8 × 23,8 cm',
        'alt': 'Etnias III, retrato en acuarela por Yamila Gorrín'},
}

# --------------------------------------------------------------- series
# Segmentación confirmada por Yamy el 2026-09-19.

SERIES = [
    {
        'ruta': 'plein-air', 'nombre': 'Plein Air',
        'titulo': 'Plein Air | Acuarela pintada al aire libre',
        'meta': 'Acuarelas de Yamila Gorrín pintadas in situ en Valparaíso, Viña del Mar y '
                'Santiago. Obras terminadas en el lugar donde fueron vistas.',
        'intro': 'Pintar afuera no admite correcciones. La luz se mueve, el viento seca el '
                 'papel antes de tiempo, y hay que resolver en minutos lo que en taller '
                 'tomaría horas. Estas obras se terminaron en el mismo lugar donde fueron '
                 'vistas.',
        'apunte': 'El plein air es donde mejor se nota la diferencia entre mirar y copiar: '
                  'no hay tiempo de registrarlo todo, así que pintar se vuelve elegir qué '
                  'dejar fuera.',
        'obras': ['Dominicos_Yamila_Gorrin', 'Valparaiso_Plein_air_Yamila_Gorrin',
                  'Vina_del_mar_plein_air_Yamila_Gorrin'],
    },
    {
        'ruta': 'paisajes', 'nombre': 'Paisajes',
        'titulo': 'Paisajes | Acuarelas de río, faro, ciudad y bruma',
        'meta': 'Paisajes en acuarela de Yamila Gorrín: el río Mapocho, faros, escenas '
                'urbanas y obras atmosféricas donde los bordes se disuelven.',
        'intro': 'Ríos, faros, ciudad, bruma. Escenas donde el tema aparente es el lugar, '
                 'pero lo que se pinta es lo que ese lugar produce: la hora del día, la '
                 'humedad del aire, qué se ve nítido y qué se disuelve.',
        'apunte': 'El Mapocho aparece dos veces en esta serie, en dos épocas distintas. No '
                  'es repetición: es el mismo río mirado con dos preguntas diferentes.',
        'obras': ['Mapocho_hoy_Yamila_gorrin', 'Mapocho_historico_Yamila_gorrin',
                  'Venesia_Yamila_Gorrin', 'Urbano1_Yamila_Gorrin', 'Urbano2_Yamila_Gorrin',
                  'Urbano3_Yamila_Gorrin', 'Faro1_Yamila_Gorrin', 'Neruda1_Yamila_Gorrin',
                  'atmosfera1', 'atmosfera2'],
    },
    {
        'ruta': 'naturaleza', 'nombre': 'Naturaleza',
        'titulo': 'Naturaleza | Acuarelas de flores, bosque y árboles',
        'meta': 'Naturaleza en acuarela por Yamila Gorrín: pintura botánica, bosques de '
                'gran formato y árboles. Obras originales sobre papel.',
        'intro': 'Flores, bosque, árboles. Lo que crece. Aquí la decisión más fuerte casi '
                 'siempre es el fondo: cuánto dejar en blanco, dónde cortar el tallo, qué '
                 'se resuelve y qué apenas se sugiere.',
        'apunte': 'El blanco del papel no es ausencia de pintura. Es una decisión tan '
                  'deliberada como cualquier pincelada, y en varias de estas obras sostiene '
                  'el peso de la composición.',
        'obras': ['Tulipan1_Yamila_Gorrin', 'Tulipan2_Yamila_Gorrin', 'Rosas_Yamila_Gorrin',
                  'atmosfera3', 'bosque1', 'bosque2', 'otras1', 'otras2'],
    },
    {
        'ruta': 'etnias', 'nombre': 'Etnias',
        'titulo': 'Etnias | Retrato en acuarela',
        'meta': 'Serie Etnias de Yamila Gorrín: retratos en acuarela sobre papel, '
                'trabajados por capas de pigmento.',
        'intro': 'Retrato y textura. Una serie distinta del resto, donde el pigmento '
                 'trabaja sobre el rostro con la misma lógica de capas que sobre un paisaje.',
        'apunte': 'Pintar un rostro con método de paisaje cambia lo que se busca: no el '
                  'parecido, sino la luz que lo atraviesa.',
        'obras': ['etnias1', 'etnias2', 'etnias3'],
    },
]

# Las direcciones viejas con ancla no deben quedar rotas.
REDIRECCIONES = {
    '#pleinair': '/plein-air/', '#paisaje': '/paisajes/', '#flores': '/naturaleza/',
    '#atmosfera': '/paisajes/', '#bosque': '/naturaleza/', '#etnias': '/etnias/',
    '#otras': '/naturaleza/', '#bio': '/sobre-mi/',
}

MENU = ([('', 'Inicio')] + [(s['ruta'], s['nombre']) for s in SERIES] +
        [('sobre-mi', 'Sobre mí'), ('blog', 'Blog')])


def comprobar():
    """Ninguna obra sin serie, ninguna repetida, ningún archivo inventado."""
    import os
    usadas = []
    for s in SERIES:
        usadas.extend(s['obras'])

    problemas = []
    repetidas = [o for o in set(usadas) if usadas.count(o) > 1]
    if repetidas:
        problemas.append('obras en más de una serie: ' + ', '.join(repetidas))

    sueltas = set(OBRAS) - set(usadas)
    if sueltas:
        problemas.append('obras sin serie: ' + ', '.join(sorted(sueltas)))

    inventadas = set(usadas) - set(OBRAS)
    if inventadas:
        problemas.append('obras que no existen: ' + ', '.join(sorted(inventadas)))

    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        'img_webp')
    faltan = [o for o in usadas if not os.path.exists(os.path.join(base, o + '.webp'))]
    if faltan:
        problemas.append('sin archivo de imagen: ' + ', '.join(faltan))

    return problemas, len(usadas)
