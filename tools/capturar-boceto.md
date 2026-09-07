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

## Después de capturar

```
git add bocetos/preview/0X-nombre.png
git commit -m "boceto 0X: captura de pagina completa"
git push
```

En Notion, pegar la imagen en el cuerpo de la ficha (sección "Boceto visual").
