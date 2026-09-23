/* ============================================================
   Administración — acceso con Google y las cinco secciones.

   Sin credenciales configuradas entra en MODO DEMOSTRACIÓN: se ve todo
   con datos de ejemplo, pero no guarda nada. Así se puede revisar el
   diseño antes de conectar Firebase.
   ============================================================ */

const CONFIG = window.CONFIG || {};
const HAY_FIREBASE = !!(CONFIG.firebase && CONFIG.firebase.apiKey);

const $ = (s) => document.querySelector(s);
const $$ = (s) => Array.from(document.querySelectorAll(s));

let db = null;
let auth = null;
let usuaria = null;

/* ------------------------------------------------------------ avisos */

function avisar(titulo, cuerpo) {
  $('#aviso-titulo').textContent = titulo;
  $('#aviso-cuerpo').textContent = cuerpo || '';
  $('#aviso').hidden = false;
}
$('#cerrar-aviso').addEventListener('click', () => { $('#aviso').hidden = true; });

/* ------------------------------------------------------------ Firebase */

async function arrancarFirebase() {
  if (!HAY_FIREBASE) return false;
  try {
    const [{ initializeApp }, autenticacion, firestore] = await Promise.all([
      import('https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js'),
      import('https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js'),
      import('https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js'),
    ]);

    const app = initializeApp(CONFIG.firebase);
    auth = { ...autenticacion, instancia: autenticacion.getAuth(app) };
    db = { ...firestore, instancia: firestore.getFirestore(app) };

    auth.onAuthStateChanged(auth.instancia, (u) => {
      if (u && !autorizada(u.email)) {
        auth.signOut(auth.instancia);
        avisar('Esta cuenta no tiene acceso',
               u.email + ' no está en la lista de personas autorizadas.');
        return;
      }
      usuaria = u;
      pintar();
    });
    return true;
  } catch (e) {
    avisar('No se pudo conectar con Firebase', e.message);
    return false;
  }
}

function autorizada(correo) {
  const lista = CONFIG.autorizados || [];
  return lista.length === 0 || lista.includes(correo);
}

$('#btn-entrar').addEventListener('click', async () => {
  if (!HAY_FIREBASE) {
    usuaria = { displayName: 'Modo demostración', email: 'sin conectar', photoURL: '' };
    pintar();
    avisar('Modo demostración',
           'Firebase no está configurado todavía. Puedes ver el panel, pero nada se guarda.');
    return;
  }
  try {
    const proveedor = new auth.GoogleAuthProvider();
    await auth.signInWithPopup(auth.instancia, proveedor);
  } catch (e) {
    if (e.code === 'auth/popup-closed-by-user') return;
    avisar('No se pudo entrar', e.message);
  }
});

$('#btn-salir').addEventListener('click', async () => {
  if (auth) await auth.signOut(auth.instancia);
  usuaria = null;
  pintar();
});

/* ------------------------------------------------------------ guardar */

async function leer(coleccion) {
  if (!db || !usuaria) return null;
  const ref = db.collection(db.instancia, 'proyecto', usuaria.uid, coleccion);
  const snap = await db.getDocs(ref);
  return snap.docs.map((d) => ({ id: d.id, ...d.data() }));
}

async function guardar(coleccion, id, datos) {
  if (!db || !usuaria) {
    avisar('No se guardó', 'Firebase no está conectado. Esto es solo una vista previa.');
    return false;
  }
  try {
    const ref = db.doc(db.instancia, 'proyecto', usuaria.uid, coleccion, id);
    await db.setDoc(ref, { ...datos, actualizado: Date.now() }, { merge: true });
    return true;
  } catch (e) {
    avisar('No se pudo guardar', e.message);
    return false;
  }
}

/* ------------------------------------------------------------ vistas */

function pintar() {
  const dentro = !!usuaria;
  $('#vista-entrar').hidden = dentro;
  $('#vista-panel').hidden = !dentro;
  if (!dentro) return;

  $('#nombre-usuaria').textContent = usuaria.displayName || 'Sin nombre';
  $('#correo-usuaria').textContent = usuaria.email || '';
  const foto = $('#foto-usuaria');
  if (usuaria.photoURL) { foto.src = usuaria.photoURL; foto.hidden = false; }
  else { foto.hidden = true; }

  pendientes();
  cuaderno();
  entregables();
  metricas();
  usuarios();
}

$$('.pestana[data-seccion]').forEach((b) => {
  b.addEventListener('click', () => {
    $$('.pestana[data-seccion]').forEach((x) => x.removeAttribute('aria-current'));
    b.setAttribute('aria-current', 'page');
    $$('.seccion').forEach((s) => { s.hidden = true; });
    $('#seccion-' + b.dataset.seccion).hidden = false;
  });
});

function aviso(caja, texto) {
  const p = document.createElement('p');
  p.className = 'nota-seccion';
  p.textContent = texto;
  caja.appendChild(p);
}

/* ---------------------------------------------------- 1. Pendientes */

async function pendientes() {
  const caja = $('#seccion-pendientes');
  caja.textContent = '';

  /* La lista vive en Firestore, no en el repositorio: incluye tarifas,
     estrategia y decisiones de negocio, y el repositorio es público. */
  const filas = await leer('pendientes');

  if (!filas || !filas.length) {
    const c = document.createElement('div');
    c.className = 'vacio-caja';
    c.innerHTML =
      '<h2>Todavía no hay pendientes cargados</h2>' +
      '<p>La lista <strong>no está en el repositorio a propósito</strong>: incluye ' +
      'tus tarifas y tu estrategia, y todo lo que vive en GitHub Pages es ' +
      'descargable por cualquiera.</p>' +
      '<p>Se sube a Firestore con <code>_construir/subir-privado.py</code>, que lee ' +
      'PENDIENTES.md y lo deja acá.</p>';
    caja.appendChild(c);
    return;
  }

  const porArea = {};
  filas.forEach((f) => {
    const a = f.area || 'Sin área';
    if (!porArea[a]) porArea[a] = [];
    porArea[a].push(f);
  });

  const datos = Object.keys(porArea).map((area) => ({
    area,
    puntos: porArea[area].sort((a, b) => Number(a.id) - Number(b.id))
      .map((p) => ({ n: Number(p.id), texto: p.texto, prioridad: p.prioridad, hecho: p.hecho })),
  }));

  const estado = {};
  filas.forEach((f) => { estado[f.id] = f.hecho; });

  const total = filas.length;
  const hechos = filas.filter((f) => f.hecho).length;

  const resumen = document.createElement('div');
  resumen.className = 'resumen-pendientes';
  resumen.innerHTML =
    '<strong>' + hechos + ' de ' + total + '</strong>' +
    '<span class="riel"><span class="riel-lleno" style="width:' +
    Math.round((hechos / total) * 100) + '%"></span></span>';
  caja.appendChild(resumen);

  datos.forEach((grupo) => {
    const h = document.createElement('h2');
    h.className = 'grupo-titulo';
    h.textContent = grupo.area;
    caja.appendChild(h);

    const ul = document.createElement('ul');
    ul.className = 'lista-pendientes';

    grupo.puntos.forEach((p) => {
      const li = document.createElement('li');
      const marcado = estado[String(p.n)] ?? p.hecho;
      if (marcado) li.setAttribute('data-hecho', 'si');

      const etiqueta = document.createElement('label');
      const caj = document.createElement('input');
      caj.type = 'checkbox';
      caj.checked = marcado;
      caj.addEventListener('change', async () => {
        const ok = await guardar('pendientes', String(p.n), { hecho: caj.checked });
        if (ok || !db) {
          li.toggleAttribute('data-hecho', caj.checked);
          pendientes();
        }
      });
      etiqueta.appendChild(caj);

      const txt = document.createElement('span');
      txt.className = 'pendiente-texto';
      txt.innerHTML = '<b>' + p.n + '.</b> ' + p.texto;
      etiqueta.appendChild(txt);

      if (p.prioridad) {
        const pri = document.createElement('span');
        pri.className = 'prioridad';
        pri.setAttribute('data-nivel', p.prioridad);
        pri.textContent = p.prioridad;
        etiqueta.appendChild(pri);
      }

      li.appendChild(etiqueta);
      ul.appendChild(li);
    });

    caja.appendChild(ul);
  });
}

/* ---------------------------------------------------- 2. Cuaderno */

const PREGUNTAS = [
  '¿Qué te hizo parar en esta escena?',
  '¿Qué sacaste, o qué dejaste sin pintar a propósito?',
  '¿Hubo un momento en que no te gustaba? ¿Qué hiciste?',
];

async function cuaderno() {
  const caja = $('#seccion-cuaderno');
  caja.textContent = '';

  let obras = [];
  try {
    const r = await fetch('/datos/obras.json');
    if (r.ok) obras = await r.json();
  } catch (e) { /* se genera al construir */ }

  if (!obras.length) { aviso(caja, 'No se encontró el catálogo de obras.'); return; }

  const guardadas = await leer('cuaderno');
  const porObra = {};
  (guardadas || []).forEach((d) => { porObra[d.id] = d; });

  const intro = document.createElement('p');
  intro.className = 'nota-seccion';
  intro.textContent = 'Las mismas tres preguntas para cada obra. Se guarda solo, ' +
    'y desde acá no depende de ninguna plataforma ajena.';
  caja.appendChild(intro);

  const lista = document.createElement('div');
  lista.className = 'cuaderno-lista';

  obras.forEach((o) => {
    const guardada = porObra[o.id] || {};
    const respondidas = PREGUNTAS.filter((_, i) => (guardada['p' + (i + 1)] || '').trim()).length;

    const det = document.createElement('details');
    det.className = 'obra-fila';

    const res = document.createElement('summary');
    res.innerHTML =
      '<img src="' + o.img + '" alt="" loading="lazy" decoding="async">' +
      '<span class="obra-datos"><strong>' + o.titulo + '</strong>' +
      '<span class="obra-serie">' + o.serie + ' · ' + o.ficha + '</span></span>' +
      '<span class="obra-estado" data-lleno="' + (respondidas === 3 ? 'si' : 'no') + '">' +
      (respondidas === 0 ? 'sin empezar' : respondidas + ' de 3') + '</span>';
    det.appendChild(res);

    PREGUNTAS.forEach((texto, i) => {
      const campo = document.createElement('div');
      campo.className = 'campo-pregunta';

      const lab = document.createElement('label');
      lab.textContent = (i + 1) + '. ' + texto;
      lab.htmlFor = 'p-' + o.id + '-' + i;
      campo.appendChild(lab);

      const area = document.createElement('textarea');
      area.id = 'p-' + o.id + '-' + i;
      area.value = guardada['p' + (i + 1)] || '';
      area.placeholder = 'Escribe lo que salga. No corrijas.';

      let reloj = null;
      area.addEventListener('input', () => {
        clearTimeout(reloj);
        reloj = setTimeout(async () => {
          const cambio = {};
          cambio['p' + (i + 1)] = area.value;
          cambio.titulo = o.titulo;
          await guardar('cuaderno', o.id, cambio);
        }, 800);
      });

      campo.appendChild(area);
      det.appendChild(campo);
    });

    lista.appendChild(det);
  });

  caja.appendChild(lista);
}

/* ---------------------------------------------------- 3. Entregables */

async function entregables() {
  const caja = $('#seccion-entregables');
  caja.textContent = '';

  const docs = await leer('entregables');

  if (!docs || !docs.length) {
    const c = document.createElement('div');
    c.className = 'vacio-caja';
    c.innerHTML =
      '<h2>Todavía no hay documentos</h2>' +
      '<p>Los entregables de la fase 0 <strong>no están en el repositorio a ' +
      'propósito</strong>: contienen tu estrategia de marca y el análisis de ' +
      'monetización, y todo lo que vive en GitHub Pages es descargable por ' +
      'cualquiera.</p>' +
      '<p>Se suben a Firestore, donde las reglas sí los protegen. Hay un script ' +
      'que lo hace de una vez: <code>_construir/subir-entregables.py</code>.</p>';
    caja.appendChild(c);
    return;
  }

  docs.sort((a, b) => (a.orden || 0) - (b.orden || 0));
  docs.forEach((d) => {
    const det = document.createElement('details');
    det.className = 'doc-fila';
    const res = document.createElement('summary');
    res.textContent = d.titulo || d.id;
    det.appendChild(res);
    const cuerpo = document.createElement('div');
    cuerpo.className = 'doc-cuerpo';
    cuerpo.textContent = d.texto || '';
    det.appendChild(cuerpo);
    caja.appendChild(det);
  });
}

/* ---------------------------------------------------- 4. Métricas */

const MOTORES = ['Perplexity', 'Gemini', 'Claude', 'ChatGPT'];

async function metricas() {
  const caja = $('#seccion-metricas');
  caja.textContent = '';

  const intro = document.createElement('p');
  intro.className = 'nota-seccion';
  intro.textContent = 'Cada 4-6 semanas: preguntar a cada motor por tu nombre, en ' +
    'ventana de incógnito, y anotar si te encuentra y si cita tu sitio.';
  caja.appendChild(intro);

  const forma = document.createElement('form');
  forma.className = 'forma-medicion';
  forma.innerHTML =
    '<label>Fecha <input type="date" name="fecha" required></label>' +
    MOTORES.map((m) =>
      '<label class="motor">' + m +
      '<select name="' + m + '">' +
      '<option value="no">No me encuentra</option>' +
      '<option value="parcial">Me encuentra, no cita el sitio</option>' +
      '<option value="si">Me encuentra y cita el sitio</option>' +
      '</select></label>').join('') +
    '<button class="boton" type="submit">Guardar medición</button>';

  forma.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const d = new FormData(forma);
    const fecha = d.get('fecha');
    if (!fecha) return;
    const fila = {};
    MOTORES.forEach((m) => { fila[m] = d.get(m); });
    const ok = await guardar('metricas', fecha, fila);
    if (ok) { avisar('Medición guardada', fecha); metricas(); }
  });

  caja.appendChild(forma);

  const filas = await leer('metricas');
  if (!filas || !filas.length) { aviso(caja, 'Todavía no hay mediciones.'); return; }

  filas.sort((a, b) => b.id.localeCompare(a.id));
  const tabla = document.createElement('table');
  tabla.className = 'tabla-metricas';
  tabla.innerHTML =
    '<thead><tr><th>Fecha</th>' + MOTORES.map((m) => '<th>' + m + '</th>').join('') +
    '</tr></thead><tbody>' +
    filas.map((f) => '<tr><td>' + f.id + '</td>' +
      MOTORES.map((m) => '<td data-v="' + (f[m] || 'no') + '">' +
        ({ si: 'sí', parcial: 'parcial', no: 'no' }[f[m]] || 'no') + '</td>').join('') +
      '</tr>').join('') +
    '</tbody>';
  caja.appendChild(tabla);
}

/* ---------------------------------------------------- 5. Usuarios */

function usuarios() {
  const caja = $('#seccion-usuarios');
  caja.textContent = '';

  const intro = document.createElement('p');
  intro.className = 'nota-seccion';
  intro.textContent = 'Quién puede entrar a esta administración.';
  caja.appendChild(intro);

  const ul = document.createElement('ul');
  ul.className = 'lista-usuarios';
  (CONFIG.autorizados || []).forEach((correo) => {
    const li = document.createElement('li');
    li.innerHTML = '<strong>' + correo + '</strong>' +
      (usuaria && usuaria.email === correo ? '<span class="chip">esta sesión</span>' : '');
    ul.appendChild(li);
  });
  caja.appendChild(ul);

  const nota = document.createElement('div');
  nota.className = 'vacio-caja';
  nota.innerHTML =
    '<h2>Cómo se agrega a alguien</h2>' +
    '<p>La lista vive en <code>js/config.js</code> y se edita en el repositorio. ' +
    'Es a propósito: así queda registrado en el historial quién dio acceso y cuándo.</p>' +
    '<p><strong>Esa lista sola no protege nada.</strong> Solo evita mostrar el panel. ' +
    'La protección de verdad son las reglas de Firestore, que hay que actualizar ' +
    'también. Están en <code>CONFIGURACION.md</code>, paso 2.</p>';
  caja.appendChild(nota);
}

/* ------------------------------------------------------------ arranque */

(async function () {
  const listo = await arrancarFirebase();
  if (!listo) {
    $('#aviso-entrar').textContent =
      'Firebase no está configurado. Puedes entrar en modo demostración para ver el panel.';
  }
  pintar();
})();
