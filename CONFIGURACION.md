# Configuración — lo que falta conectar

El sitio, el blog y la Administración ya están construidos y funcionando.
Lo que falta son **tres credenciales que solo tú puedes crear**, porque viven en
tus cuentas.

Mientras no las pongas, todo sigue funcionando así:

| Parte | Sin configurar | Configurada |
|---|---|---|
| El sitio y las obras | ✅ Funciona | ✅ Funciona |
| El blog | ✅ Se ve; las entradas se escriben a mano | ✅ Se escribe desde `/admin/` |
| Administración | ✅ Se ve en modo demostración | ✅ Guarda de verdad |

**Tiempo total: unos 45 minutos.** Todo es gratuito.

---

## Antes de empezar: qué protege qué

Conviene tenerlo claro para no confiar en lo que no corresponde.

**La página `/administracion/` es pública.** Cualquiera puede escribir la dirección y
descargar su HTML y su JavaScript. En GitHub Pages no hay servidor que pueda negarlo.

**Lo que sí está protegido son los datos**, y lo protege Google, no la página:

- Los pendientes, el cuaderno y los entregables viven en **Firestore**. Las reglas del
  paso 2 solo se los entregan a tu cuenta.
- Las entradas del blog se escriben en **tu repositorio**. Solo quien tenga permiso de
  escritura puede publicar.

La lista de `autorizados` en `js/config.js` **no protege nada**: solo evita mostrar el
panel. Si alguien la borrara de su copia local, seguiría sin poder leer tus datos, porque
la comprobación real está en las reglas de Firestore.

---

## Paso 1 — Firebase (unos 15 minutos)

Sirve para entrar con Google y para guardar el cuaderno, los pendientes y las métricas.

1. Entra en [console.firebase.google.com](https://console.firebase.google.com) y crea un
   proyecto. Ponle el nombre que quieras; no se ve en ningún lado.
2. Dentro del proyecto, **Compilación → Authentication → Comenzar**.
   En la pestaña **Sign-in method**, activa **Google**.
3. En **Authentication → Settings → Authorized domains**, agrega:
   - `galeria.yamilagorrin.com`
   - `localhost` *(para poder probar en tu computador)*
4. **Compilación → Firestore Database → Crear base de datos.** Elige el modo de
   producción y la región `southamerica-east1`, que es la más cercana.
5. Vuelve a **Descripción general del proyecto**, toca el icono `</>` para agregar una
   aplicación web, y copia el bloque `firebaseConfig` que te da.
6. Pega esos valores en **`js/config.js`**.

---

## Paso 2 — Las reglas de Firestore (5 minutos)

**Este paso es el que protege de verdad.** Sin él, cualquiera con la dirección de tu
proyecto podría leer tus datos.

En **Firestore Database → Reglas**, reemplaza todo por esto:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Cada usuaria solo alcanza sus propios documentos, y solo si su
    // correo es el autorizado. Esta comprobación corre en los servidores
    // de Google: no se puede saltar desde el navegador.
    match /proyecto/{uid}/{documento=**} {
      allow read, write: if request.auth != null
                         && request.auth.uid == uid
                         && request.auth.token.email == 'yamilagorrin@gmail.com';
    }

    // Todo lo demás, cerrado.
    match /{documento=**} {
      allow read, write: if false;
    }
  }
}
```

Toca **Publicar**.

> Si algún día quieres dar acceso a alguien más, se agrega su correo acá **y** en
> `js/config.js`. Los dos, o no funciona.

---

## Paso 3 — El proxy de OAuth para el blog (unos 20 minutos)

Este es el paso más incómodo, y conviene que sepas por qué existe.

GitHub Pages solo entrega archivos: no puede ejecutar código. Pero el intercambio de
credenciales con GitHub necesita un **secreto** que no puede vivir en un archivo estático,
porque cualquiera lo descargaría. Por eso hace falta un servicio mínimo en el medio.
Es gratuito y se configura una sola vez.

### 3.1 Crear la aplicación OAuth en GitHub

1. [github.com/settings/developers](https://github.com/settings/developers) →
   **OAuth Apps** → **New OAuth App**
2. Rellena:
   - **Application name:** `Editor del blog`
   - **Homepage URL:** `https://galeria.yamilagorrin.com`
   - **Authorization callback URL:** la dejas en blanco por ahora; vuelves en 3.3
3. Guarda el **Client ID** y genera un **Client Secret**. Cópialos.

### 3.2 Desplegar el proxy en Cloudflare

1. Crea una cuenta gratuita en [dash.cloudflare.com](https://dash.cloudflare.com)
2. Usa el proxy ya hecho de
   [sterlingwes/decap-proxy](https://github.com/sterlingwes/decap-proxy) — sigue su
   README, que explica cómo desplegarlo como Worker.
3. En la configuración del Worker, agrega dos variables secretas:
   - `GITHUB_OAUTH_ID` → tu Client ID
   - `GITHUB_OAUTH_SECRET` → tu Client Secret
4. Anota la dirección que te queda, algo como
   `https://decap-proxy.tu-cuenta.workers.dev`

### 3.3 Cerrar el círculo

1. Vuelve a la aplicación OAuth de GitHub y pon como **Authorization callback URL**
   la dirección del worker seguida de `/callback`:
   `https://decap-proxy.tu-cuenta.workers.dev/callback`
2. En **`admin/config.yml`**, reemplaza la línea `base_url` por la dirección de tu worker.

---

## Paso 4 — Subir lo privado a Firestore (5 minutos)

Los pendientes y los entregables **no están en el repositorio a propósito**: contienen tus
tarifas, tu estrategia de marca y el análisis de monetización, y todo lo que vive en
GitHub Pages es descargable por cualquiera.

1. Entra una primera vez en `https://galeria.yamilagorrin.com/administracion/` con Google.
2. En la consola de Firebase, **Authentication → Users**, copia tu **UID**.
3. En Firebase, **Configuración del proyecto → Cuentas de servicio → Generar nueva clave
   privada**. Te descarga un archivo JSON. **Ese archivo nunca va al repositorio.**
4. Desde `d:\opt\yamilagorrin.com`:

```
pip install google-cloud-firestore
set GOOGLE_APPLICATION_CREDENTIALS=C:\ruta\a\la\clave.json
python _construir/subir-privado.py --uid TU_UID
```

Para ver qué subiría sin subir nada todavía, agrega `--simular`.

---

## Paso 5 — Activar la acción de GitHub

Ya está escrita, en `.github/workflows/construir.yml`. Solo hay que permitirle escribir:

**Settings → Actions → General → Workflow permissions** → marca
**Read and write permissions** → Guardar.

Desde ahí, cada vez que publiques una entrada desde `/admin/`, la acción reconstruye el
sitio sola.

---

## Cómo publicar una entrada, una vez configurado

1. Entra a `https://galeria.yamilagorrin.com/admin/`
2. Inicia sesión con GitHub
3. **Entradas del blog → New Entrada**
4. Escribe y toca **Publish**

La entrada se guarda como archivo en tu repositorio, la acción la convierte en HTML, y
en un par de minutos está en línea. Como es HTML real, Google y los motores de IA la leen
completa — que es la razón de haberlo montado así y no con una base de datos.

> **Para dejar algo a medias:** activa la casilla **Borrador**. Se guarda pero no se
> publica.

---

## Qué revisar si algo falla

| Síntoma | Causa más probable |
|---|---|
| «Firebase no está configurado» | Falta pegar los valores en `js/config.js` |
| Entra pero no guarda nada | Faltan las reglas del paso 2, o el correo no coincide |
| «Esta cuenta no tiene acceso» | El correo no está en `autorizados` de `js/config.js` |
| `/admin/` no deja entrar | La `base_url` del `config.yml` no apunta al worker, o el callback de GitHub está mal |
| Publicas y no aparece | La acción no tiene permiso de escritura: paso 5 |
| El panel se ve sin estilos | Se abrió el archivo con doble clic. Hay que servirlo por HTTP |

---

## Para probar en tu computador

```
cd d:\opt\yamilagorrin.com
python -m http.server 8000
```

Y abres `http://localhost:8000`. Tiene que ser con servidor: las rutas del sitio son
absolutas, como corresponde en producción, y abriendo el archivo directamente no
encuentran nada.
