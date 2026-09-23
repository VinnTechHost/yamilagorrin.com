/* ============================================================
   Visor de obras — pantalla completa, con flechas.

   Sin librerías: son unas líneas de código y no hay motivo para
   cargarle a nadie un paquete entero por esto.

   Si el navegador no ejecuta JavaScript, las obras se siguen viendo
   en la galería. El visor suma, no sustituye.
   ============================================================ */

(function () {
  'use strict';

  var figuras = Array.prototype.slice.call(
    document.querySelectorAll('.galeria .obra'));
  if (!figuras.length) return;

  // Se lee del propio HTML: la galería ya tiene todos los datos.
  var obras = figuras.map(function (f) {
    var img = f.querySelector('img');
    var t = f.querySelector('h2');
    var ficha = f.querySelector('.ficha');
    var cred = f.querySelector('.credencial');
    return {
      src: img ? img.getAttribute('src') : '',
      alt: img ? img.getAttribute('alt') : '',
      titulo: t ? t.textContent.trim() : '',
      ficha: ficha ? ficha.textContent.trim() : '',
      credencial: cred ? cred.textContent.trim() : ''
    };
  });

  var actual = 0;
  var abierto = false;
  var ultimoFoco = null;

  // ---------------------------------------------------------- montaje

  var visor = document.createElement('div');
  visor.className = 'visor';
  visor.setAttribute('role', 'dialog');
  visor.setAttribute('aria-modal', 'true');
  visor.setAttribute('aria-label', 'Obra a pantalla completa');
  visor.hidden = true;

  visor.innerHTML =
    '<button class="visor-cerrar" type="button" aria-label="Cerrar">&times;</button>' +
    '<button class="visor-flecha visor-antes" type="button" aria-label="Obra anterior">' +
    '<span aria-hidden="true">&#8249;</span></button>' +
    '<figure class="visor-marco">' +
    '  <img alt="">' +
    '  <figcaption>' +
    '    <strong></strong>' +
    '    <span class="visor-ficha"></span>' +
    '    <span class="visor-credencial"></span>' +
    '    <span class="visor-cuenta"></span>' +
    '  </figcaption>' +
    '</figure>' +
    '<button class="visor-flecha visor-despues" type="button" aria-label="Obra siguiente">' +
    '<span aria-hidden="true">&#8250;</span></button>';

  document.body.appendChild(visor);

  var img = visor.querySelector('img');
  var titulo = visor.querySelector('figcaption strong');
  var ficha = visor.querySelector('.visor-ficha');
  var credencial = visor.querySelector('.visor-credencial');
  var cuenta = visor.querySelector('.visor-cuenta');
  var antes = visor.querySelector('.visor-antes');
  var despues = visor.querySelector('.visor-despues');

  // ---------------------------------------------------------- pintar

  function mostrar(i) {
    actual = (i + obras.length) % obras.length;   // da la vuelta en los extremos
    var o = obras[actual];

    img.src = o.src;
    img.alt = o.alt;
    titulo.textContent = o.titulo;
    ficha.textContent = o.ficha;
    credencial.textContent = o.credencial;
    credencial.hidden = !o.credencial;
    cuenta.textContent = (actual + 1) + ' de ' + obras.length;

    var sola = obras.length < 2;
    antes.hidden = sola;
    despues.hidden = sola;

    // Se precarga la siguiente para que el salto no parpadee
    if (!sola) {
      var sig = new Image();
      sig.src = obras[(actual + 1) % obras.length].src;
    }
  }

  function abrir(i, origen) {
    ultimoFoco = origen || document.activeElement;
    mostrar(i);
    visor.hidden = false;
    document.body.classList.add('con-visor');
    abierto = true;
    visor.querySelector('.visor-cerrar').focus();
  }

  function cerrar() {
    visor.hidden = true;
    document.body.classList.remove('con-visor');
    abierto = false;
    if (ultimoFoco && ultimoFoco.focus) ultimoFoco.focus();
  }

  // ---------------------------------------------------------- eventos

  figuras.forEach(function (f, i) {
    var marco = f.querySelector('.obra-marco');
    if (!marco) return;

    // El marco pasa a ser un botón de verdad, no un div al que se le
    // pega un click: así funciona con teclado y lo anuncian los lectores.
    marco.setAttribute('role', 'button');
    marco.setAttribute('tabindex', '0');
    marco.setAttribute('aria-label', 'Ver ' + obras[i].titulo + ' a pantalla completa');

    marco.addEventListener('click', function () { abrir(i, marco); });
    marco.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter' || ev.key === ' ') {
        ev.preventDefault();
        abrir(i, marco);
      }
    });
  });

  antes.addEventListener('click', function (ev) {
    ev.stopPropagation();
    mostrar(actual - 1);
  });
  despues.addEventListener('click', function (ev) {
    ev.stopPropagation();
    mostrar(actual + 1);
  });
  visor.querySelector('.visor-cerrar').addEventListener('click', cerrar);

  // Tocar el fondo cierra; tocar la obra o el pie, no.
  visor.addEventListener('click', function (ev) {
    if (ev.target === visor) cerrar();
  });

  document.addEventListener('keydown', function (ev) {
    if (!abierto) return;
    if (ev.key === 'Escape') cerrar();
    else if (ev.key === 'ArrowLeft') mostrar(actual - 1);
    else if (ev.key === 'ArrowRight') mostrar(actual + 1);
  });

  // Deslizar con el dedo, que en el teléfono es lo natural
  var x0 = null;
  visor.addEventListener('touchstart', function (ev) {
    x0 = ev.changedTouches[0].clientX;
  }, { passive: true });
  visor.addEventListener('touchend', function (ev) {
    if (x0 === null) return;
    var d = ev.changedTouches[0].clientX - x0;
    if (Math.abs(d) > 50) mostrar(actual + (d < 0 ? 1 : -1));
    x0 = null;
  }, { passive: true });
})();
