/* ============================================================
   Configuración del sitio — AQUÍ VAN TUS CREDENCIALES

   Este archivo es PÚBLICO: cualquiera puede descargarlo. Eso no es un
   descuido, es como funciona Firebase: la configuración identifica al
   proyecto, no da permisos. Quien protege de verdad son las reglas de
   Firestore y la lista de correos autorizados, que se comprueban en el
   servidor de Google y no acá.

   NUNCA pongas en este archivo una clave de API con permisos de
   escritura, un token de GitHub ni una contraseña.

   Instrucciones paso a paso: CONFIGURACION.md, en la raíz del repositorio.
   ============================================================ */

window.CONFIG = {

  /* 1. Firebase — consola.firebase.google.com
     Crea un proyecto, agrega una aplicación web, y pega acá lo que te dé.
     Mientras esté sin rellenar, Administración funciona en modo
     demostración: se ve todo, pero no guarda nada. */
  firebase: {
    apiKey: '',
    authDomain: '',
    projectId: '',
    storageBucket: '',
    messagingSenderId: '',
    appId: ''
  },

  /* 2. Quién puede entrar.
     La comprobación de verdad está en las reglas de Firestore; esto solo
     evita mostrar el panel a quien no corresponde. */
  autorizados: [
    'yamilagorrin@gmail.com'
  ],

  /* 3. El repositorio donde se publica el blog. */
  repositorio: 'VinnTechHost/yamilagorrin.com',
  rama: 'main'
};
