# CÓMO CREAR / ACTUALIZAR UN BOCETO

Los bocetos son archivos `bocetos/0X-*.html` — HTML + CSS en un solo archivo, sin
build, sin framework. Se abren con doble clic.

---

## Actualizar un boceto existente

1. Abrir `bocetos/0X-nombre.html` en un editor.
2. Editar textos, colores, secciones. Todo el CSS está en el `<style>` del `<head>`.
3. Abrir el archivo en el navegador para revisarlo.
4. (Opcional) Regenerar la captura de página completa — ver abajo.
5. Publicar:
   ```
   git add bocetos/
   git commit -m "boceto 0X: <qué cambió>"
   git push
   ```
   GitHub Pages se actualiza solo en ~1 minuto.
6. Si el cambio importa para el cliente, anotarlo en la ficha de Notion
   (**Observaciones**, con fecha).

**No** crear un archivo nuevo para "otra versión" del mismo prospecto. Se edita el
que ya existe. El historial queda en Git.

---

## Crear un boceto para un prospecto nuevo

1. Duplicar el boceto más parecido en nicho/estética:
   ```
   cp bocetos/01-automotores-andina.html bocetos/05-nombre-prospecto.html
   ```
2. Investigar la identidad visual pública real del prospecto:
   - logo y colores (sacar los HEX de su Instagram / sitio)
   - tipografía aproximada (elegir una de Google Fonts que se acerque)
   - estilo fotográfico
   - productos / servicios reales que vende
   - tono de comunicación
3. Adaptar el HTML: `<title>`, marca en el nav y footer, paleta en `:root`,
   fuentes en el `<link>` de Google Fonts, textos, secciones (el orden se adapta
   al negocio), el "elemento diferencial".
4. Reglas fijas:
   - Marca de agua: `<div class="demo-badge">Boceto conceptual · PAGX Studio · no es el sitio actual</div>`
   - Nota de datos demo visible (ej. *"Imágenes y precios de ejemplo — boceto de demostración PAGX Studio"*).
   - **No** inventar cifras, premios ni testimonios reales. Todo lo no verificable
     se marca como demo.
5. Imágenes:
   - **Autos:** `https://cdn.imagin.studio/getimage?customer=img&width=680&angle=23&make=<marca>&modelFamily=<modelo>` — renders de estudio del modelo real. Ignora `modelYear`: no sirve para autos clásicos/vintage (siempre renderiza un modelo moderno genérico).
   - **Personas:** `https://i.pravatar.cc/800?img=<1-70>` — retratos genéricos (marcar como demo).
   - **Fotografía de stock (todo lo demás — interiores, comida, bodas, moda, nightlife, autos de lujo, etc.):** Unsplash, vía
     `https://images.unsplash.com/photo-<ID>?w=..&h=..&fit=crop&q=75`. Ajustar `w`/`h` al tamaño real del contenedor CSS (hero ≈900×1100, tarjetas de grid ≈700×860, panel ancho ≈900×720).
   - Fallback: fondos con degradado CSS.

   **Verificación obligatoria de cualquier ID de Unsplash antes de usarlo** (los IDs
   adivinados fallan con frecuencia o devuelven contenido genérico que no encaja):
   ```
   curl -s -o candidato.jpg --max-time 8 "https://images.unsplash.com/photo-<ID>?w=400"
   ```
   y luego **abrir `candidato.jpg` y mirarlo** antes de ponerlo en el HTML. No
   asumas el contenido a partir del ID — confírmalo visualmente. Un código HTTP 200
   no garantiza que el ID exista con contenido real (Unsplash puede devolver una
   imagen placeholder).
6. Añadir la tarjeta del nuevo boceto en `index.html`.
7. Generar la captura de página completa (abajo) → `bocetos/preview/05-nombre.png`.
8. `git add / commit / push`.
9. En Notion: **URL del boceto** = link de Pages · pegar la imagen en el cuerpo ·
   **Boceto** = `Listo`.

---

## Regenerar la captura de página completa (PNG)

`tools/stitch.py` une varios screenshots en una sola imagen de página completa.

Método (con cualquier navegador + una extensión de captura, o con el flujo de
Claude/Chrome):

1. Servir la carpeta: `python -m http.server 8777` dentro de `pagx-prospeccion/`.
2. Abrir `http://127.0.0.1:8777/bocetos/0X-nombre.html`.
3. Desactivar animaciones y hacer el nav estático (inyectar CSS:
   `header.nav{position:static!important}` y `html{scroll-behavior:auto!important}`).
4. Tomar screenshots del viewport bajando en pasos iguales (~830 px de scroll),
   anotando el `scrollY` real de cada uno.
5. Unir:
   ```
   python tools/stitch.py bocetos/preview/0X-nombre.png <innerHeight> \
     '[["shot1.jpg",0],["shot2.jpg",830],["shot3.jpg",1660], ...]'
   ```
   Donde `<innerHeight>` es `window.innerHeight` real de la pestaña.

Ver comentarios dentro de `tools/stitch.py`.

---

## Detalle: por qué así y no un sitio de producción

Los bocetos son **para antojar al prospecto**, no para desplegar. Deben verse
específicos, hablar de SU negocio, usar SU oferta y resolver UN problema visible.
Cuando un prospecto acepte, ahí se construye el sitio real (otro proyecto).
