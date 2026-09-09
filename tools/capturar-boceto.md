# Capturar un boceto a PNG de página completa

El PNG de `bocetos/preview/` es la imagen que se envía al prospecto y se pega en
Notion. Es una captura de la **página completa** (todo el scroll), no del viewport.

## Opción A — extensión de navegador (lo más simple)

1. Abrir `bocetos/0X-nombre.html` en el navegador (doble clic, o servido en local).
2. Usar una extensión de captura de página completa (p. ej. "GoFullPage",
   "Fireshot", o la captura de pantalla completa de las DevTools de Chrome:
   `Ctrl/Cmd + Shift + P` → "Capture full size screenshot").
3. Guardar como `bocetos/preview/0X-nombre.png`.

> Antes de capturar, en la consola de DevTools puedes ejecutar esto para que el
> nav no se repita y no haya animaciones a medias:
> ```js
> const s=document.createElement('style');
> s.textContent='header.nav{position:static!important}html,*{scroll-behavior:auto!important}.wa-fab{display:none!important}';
> document.head.appendChild(s);
> ```

## Opción B — screenshots por tramos + stitch.py

Cuando la captura de página completa recorta o distorsiona (pasa con viewports
que se escalan), se toman varios screenshots y se unen.

1. Servir la carpeta:
   ```
   cd pagx-prospeccion
   python -m http.server 8777
   ```
2. Abrir `http://127.0.0.1:8777/bocetos/0X-nombre.html`.
3. Inyectar el CSS de arriba (nav estático, sin scroll suave).
4. Leer `window.innerHeight` de la pestaña (consola) — llamémoslo `IH`.
5. Bajar en pasos de ~`IH * 0.97` px. En cada paso:
   - `window.scrollTo(0, Y)` y esperar ~300 ms
   - leer el `window.scrollY` **real** (puede quedar clavado en el máximo al final)
   - tomar screenshot del viewport y guardarlo
6. Unir con:
   ```
   python tools/stitch.py bocetos/preview/0X-nombre.png IH \
     '[["shot0.jpg",0],["shot1.jpg",830],["shot2.jpg",1660],["shot3.jpg",2490]]'
   ```
   - argumento 1: ruta de salida
   - argumento 2: `IH` (innerHeight real de la pestaña)
   - argumento 3: JSON con `[[ruta_screenshot, scrollY_real], ...]` en orden

`stitch.py` calcula la escala (imagen vs viewport), coloca cada screenshot en su
posición y produce una sola imagen de página completa.

## Vista mobile

`resize_window` no reduce de forma fiable una ventana de Chrome maximizada en
Windows a un ancho móvil (390px) — el `window.innerWidth` se queda en el ancho de
escritorio. Solución que sí funciona: servir un wrapper con un iframe de ancho fijo
y capturar la página contenedora, no el iframe directamente.

1. Crear `_mobile-wrap.html` en la raíz del repo (temporal — **no se comitea**,
   borrar al terminar):
   ```html
   <!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;background:#0b0c10}</style></head>
   <body><iframe id="f" style="width:390px;height:6000px;border:0"></iframe>
   <script>
   const params = new URLSearchParams(location.search);
   document.getElementById('f').src = params.get('src');
   </script>
   </body></html>
   ```
2. Abrir `http://127.0.0.1:8777/_mobile-wrap.html?src=/bocetos/0X-nombre.html`.
3. Esperar a que el iframe cargue, inyectar el CSS de congelado dentro de su
   `contentDocument`, y ajustar `document.getElementById('f').style.height` a
   `contentDocument.body.scrollHeight` para que no quede scroll interno.
4. Capturar la página **contenedora** (outer), bajando en pasos ≤ `window.innerHeight`
   de esa página exterior, igual que en escritorio.
5. Cada frame capturado tiene ancho de ventana completo con una franja gris muerta
   a la derecha del iframe — recortar cada imagen a ~319px de ancho (390 CSS px ×
   escala ≈0.816) con PIL **antes** de unir con `stitch.py`.

## ⚠️ El parámetro `IH` de `stitch.py` — error común

`IH` debe ser el `window.innerHeight` **real, en píxeles CSS**, leído con
`window.innerHeight` justo antes de cada captura — **no** el alto en píxeles del
archivo de screenshot resultante. Son números distintos: el navegador puede
devolver screenshots a una escala distinta (p. ej. `innerHeight` de 911 pero un
screenshot de 744px de alto), por el panel de la extensión o el DPI del sistema.

Si le pasas a `stitch.py` el alto del *archivo* en vez del `innerHeight` real, el
resultado sale con **contenido duplicado o fantasma** en los puntos donde se
solapan los frames — un bug silencioso, sin ningún error, que solo se nota mirando
la imagen final con atención. Si ves texto o secciones repetidas en el PNG unido,
esta es la causa más probable: vuelve a ejecutar `stitch.py` con el `innerHeight`
correcto.

## Composición final: desktop + mobile en una sola imagen

Una vez generados `preview/0X-nombre-desktop.png` y `preview/0X-nombre-mobile.png`
por separado (pasos de arriba), la imagen que realmente se sube a Notion y se usa
en `index.html` es la **composición combinada**, no las dos sueltas:

```
python tools/compose_preview.py preview/0X-nombre-desktop.png preview/0X-nombre-mobile.png preview/0X-nombre.png "Nombre del Prospecto"
```

Esto genera una sola imagen con el desktop en un marco de navegador y el mobile en
un marco de teléfono, lado a lado, con el título del prospecto — es el formato que
usan todos los bocetos del repo. No mandar solo la captura de escritorio.

## Después de capturar

```
git add bocetos/preview/0X-nombre.png
git commit -m "boceto 0X: captura de pagina completa"
git push
```

En Notion, pegar la imagen en el cuerpo de la ficha (sección "Boceto visual").
