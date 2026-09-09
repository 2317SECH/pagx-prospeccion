# Plan de réplica — llevar el Claude Code de Alan al mismo nivel

Basado en `CLAUDE_CODE_FORENSIC_AUDIT.md`. Léelo primero si no sabes por qué se
recomienda cada paso — aquí solo están las acciones.

**Principio del plan:** casi ninguna de las causas encontradas es "configuración
que se instala". Son (1) documentación que falta o está desactualizada en el repo
compartido, y (2) verificaciones de cuenta que solo Alan puede confirmar. Por eso
este plan es sobre todo **actualizar el repo** (que Alan sí hereda con `git pull`) y
**una lista de preguntas para Alan**, no una lista de archivos de configuración para
copiar.

---

## PASO 1 — Unificar el prompt maestro

**Qué hacer:** fusionar en un solo archivo lo que hoy está repartido entre
`prompts/PROMPT-MAESTRO.md` (versión corta del repo) y el prompt que Sergio pega en
el chat cada sesión (versión larga con la actualización de "Hola 👋 Somos de PAGX
Studio." y evidencia visual en Notion).

**Archivo a modificar:** `prompts/PROMPT-MAESTRO.md`

**Qué agregar exactamente** (secciones que hoy solo existen en el prompt pegado en
chat, no en el repo):
- El saludo obligatorio de apertura: `"Hola 👋 Somos de PAGX Studio."`
- Regla de nombre correcto: siempre "PAGX Studio", nunca "Pax Studio" / "PAG Studio".
- Estructura del mensaje (saludo → observación → oportunidad → propuesta → mención
  de la preview ~20% → cierre).
- Checklist de control de calidad del mensaje (14 ítems, ver el prompt pegado hoy
  en el chat).
- La sección de pantallazos/evidencia obligatoria: tomar screenshot del perfil de
  Instagram de cada prospecto final y **adjuntarlo como imagen en el cuerpo de la
  ficha de Notion**, en una sección `## Evidencia / Pantallazos`.

**Cómo probarlo:** después de editar, Alan hace `git pull` y abre el archivo — debe
poder leer ahí mismo (sin que Sergio le pegue nada en el chat) todas las reglas que
se usaron en la jornada de hoy.

---

## PASO 2 — Actualizar `docs/COMO-ACTUALIZAR-BOCETO.md` con el flujo real de imágenes

**Archivo a modificar:** `docs/COMO-ACTUALIZAR-BOCETO.md`

**Agregar una sección nueva "Imágenes de stock (Unsplash)"** con:
- La URL base: `https://images.unsplash.com/photo-<ID>?w=..&h=..&fit=crop&q=75`.
- La regla de verificación obligatoria antes de usar un ID nuevo:
  ```
  curl -s -o id.jpg --max-time 8 "https://images.unsplash.com/photo-<ID>?w=400"
  ```
  seguido de abrir `id.jpg` con la herramienta de lectura de imágenes para
  confirmar visualmente el contenido. Motivo: IDs adivinados fallan con frecuencia
  o devuelven contenido genérico.
- Que las imágenes usadas en un boceto no se repitan textualmente dentro del mismo
  boceto salvo que sea la misma foto reutilizada a propósito (hero repetido en un
  panel secundario, patrón ya usado en varios bocetos existentes).

**Cómo probarlo:** pedirle a Alan que verifique un ID de Unsplash con `curl` antes
de su próximo boceto y que confirme que vio la imagen antes de pegarla en el HTML.

---

## PASO 3 — Documentar la captura mobile y la composición desktop+mobile

**Archivo a modificar:** `docs/capturar-boceto.md`

**Agregar:**
1. **Truco del iframe para mobile** (Chrome no reduce de forma fiable una ventana
   maximizada de Windows a 390px): crear un archivo temporal
   `_mobile-wrap.html` en la raíz del repo:
   ```html
   <!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;background:#0b0c10}</style></head>
   <body><iframe id="f" style="width:390px;height:6000px;border:0"></iframe>
   <script>
   const params = new URLSearchParams(location.search);
   document.getElementById('f').src = params.get('src');
   </script>
   </body></html>
   ```
   Navegar a `http://localhost:PUERTO/_mobile-wrap.html?src=/bocetos/0X-nombre.html`,
   esperar a que cargue el iframe, ajustar su altura a
   `contentDocument.body.scrollHeight`, y capturar la página **contenedora**
   (no el iframe directamente). Recortar cada frame a ~319px de ancho antes de
   unir con `stitch.py` (390 CSS px × escala ≈0.816).
   Borrar `_mobile-wrap.html` al terminar — no se comitea.
2. **Composición final:** después de tener `preview/0X-nombre-desktop.png` y
   `preview/0X-nombre-mobile.png`, ejecutar:
   ```
   python tools/compose_preview.py preview/0X-desktop.png preview/0X-mobile.png preview/0X-nombre.png "Nombre del Prospecto"
   ```
   Esto genera la tarjeta combinada "DESKTOP / MOBILE" que es la imagen que
   realmente se sube a Notion e `index.html` — no las capturas sueltas.
3. **Advertencia explícita sobre el parámetro `IH` de `stitch.py`:** debe ser el
   `window.innerHeight` real en píxeles CSS de la pestaña (leído con
   `window.innerHeight` justo antes de cada captura), **nunca** el ancho/alto en
   píxeles del archivo de screenshot resultante — son números distintos por el
   factor de escala del navegador, y si se confunden, la imagen final sale con
   contenido duplicado/fantasma.

**Cómo probarlo:** el próximo boceto de Alan debe producir 3 archivos PNG por
prospecto (`-desktop.png`, `-mobile.png`, y el combinado sin sufijo) — igual que los
36 bocetos actuales del repo.

---

## PASO 4 — Corregir la sintaxis de imagen en Notion (el bug más crítico)

**Archivo a modificar:** `docs/NOTION.md`, sección "La ficha de cada prospecto"

**Agregar una nota de advertencia explícita:**

> **Sintaxis correcta para adjuntar una imagen subida por `notion-create-file-upload`:**
> `![Descripción](file-upload://ID-DEL-UPLOAD)` — es la sintaxis estándar de imagen
> en markdown, usando `file-upload://` como si fuera una URL.
>
> **NO uses** `<image src="file-upload://ID">` — Notion lo guarda como texto plano
> escapado y visible, **no como imagen**, sin ningún mensaje de error. Es un fallo
> silencioso: la ficha se crea "bien" pero la imagen no aparece.
>
> **Verificación obligatoria:** después de crear o actualizar cualquier ficha con
> imágenes, vuelve a leerla (`fetch` de la página) y confirma que el markdown de
> salida muestra una URL de `prod-files-secure.s3.us-west-2.amazonaws.com/...` en
> vez de la cadena `file-upload://...` sin procesar. Si ves la cadena sin procesar,
> corrígela con un `update_content` que reemplace `<image src="file-upload://ID">`
> por `![Descripción](file-upload://ID)`.

**Cómo probarlo:** el próximo prospecto que registre Alan en Notion debe mostrar la
imagen del boceto y la evidencia de Instagram **renderizadas visualmente** al abrir
la página en Notion, no como texto.

---

## PASO 5 — Verificar (preguntando, no adivinando) la cuenta de Alan

Esto **no se puede hacer desde esta máquina**. Es una lista de preguntas/acciones
para que Sergio (o Alan directamente) confirme:

1. **Notion:** ¿la cuenta de claude.ai de Alan tiene el conector de Notion
   conectado en Settings → Connectors? ¿Apunta al mismo workspace "Workspace
   Comercial — PAGX Studio"? ¿Tiene permiso de escritura (no solo lectura) sobre la
   base `Prospectos` y `Bitácora de Prospección`?
2. **Chrome:** ¿tiene la extensión "Claude in Chrome" instalada y emparejada con su
   sesión de Claude Code? ¿Tiene una sesión de Instagram logueada en ese mismo
   Chrome?
3. **Modelo:** ¿qué modelo usa su sesión de Claude Code? (visible en el mensaje de
   sistema al iniciar, o preguntándole a Claude "qué modelo eres" dentro de su
   propia sesión).
4. **Plan/cuenta:** ¿su plan de Claude incluye acceso a Sonnet 5 y a *thinking*
   extendido, o está en un plan/modelo más limitado?

**Cómo probarlo:** pedirle a Alan que pegue la respuesta a estas 4 preguntas —
ninguna requiere acceso técnico avanzado, son todas visibles desde su propia
interfaz de Claude Code / claude.ai.

---

## PASO 6 — Actualizar `docs/FLUJO-ALAN.md` con el Paso 9 corregido

**Archivo a modificar:** `docs/FLUJO-ALAN.md`, Paso 9 ("Vincular el boceto al
prospecto")

**Reemplazar** el texto actual ("Pegar la imagen de página completa en el cuerpo de
la ficha") por una referencia a los pasos 2-4 de este mismo plan (Unsplash
verificado, composición desktop+mobile, sintaxis correcta de imagen), y agregar un
paso 9-bis: tomar y adjuntar el pantallazo de evidencia del perfil de Instagram
(nuevo requisito del Paso 1 de este plan).

---

## PASO 7 — Permisos y hooks: no hace falta tocar nada

Confirmado en la auditoría: no hay ningún hook ni permiso especial en este proyecto
que explique el comportamiento (los únicos hooks activos son del plugin `caveman`,
puramente cosmético). **No hay ningún paso de configuración de hooks o permisos que
replicar.** Si Alan ve más prompts de permisos de los esperados, es un tema de la
configuración global de su propia cuenta (`~/.claude/settings.local.json`), no algo
de este proyecto — se soluciona con la skill `fewer-permission-prompts` si hace
falta, pero es opcional y no relacionado con la calidad del trabajo.

---

## PASO 8 — Agentes/subagentes: no hace falta crear ninguno

Confirmado: esta sesión no usó ningún subagente. No hay ningún agente
`prospección-PAGX` que crear ni instalar. Si el Claude Code de Alan delega en
subagentes por defecto y eso le hace perder contexto entre pasos, la única acción
recomendable es que trabaje el flujo **en una sola conversación continua**, igual
que se hizo hoy, en vez de fragmentarlo.

---

## PASO 9 — Memoria: trasladar (no copiar) lo útil al repo

No se puede copiar el archivo de memoria de Sergio a la máquina de Alan (es privado
por cuenta+ruta de proyecto). Lo que sí corresponde:

- Todo el contenido técnico útil de `boceto-preview-workflow.md` y
  `prospeccion-cadencia.md` que sea **reutilizable por cualquiera** ya quedó
  trasladado a los Pasos 1-4 de este plan (que sí van al repo, vía git).
- Lo que **no** se traslada a propósito: datos operativos específicos de Sergio
  (rutas de su escritorio, IDs de sesión, atribución de quién descubrió qué
  prospecto) — eso sigue siendo memoria privada legítima, no documentación de
  proceso.

---

## PASO 10 — Cómo probar que los cambios funcionan

1. Alan (o Sergio simulando el flujo de Alan) hace `git pull` en
   `pagx-prospeccion`.
2. Abre `prompts/PROMPT-MAESTRO.md` y confirma que ahí está el saludo "Hola 👋
   Somos de PAGX Studio." sin que nadie se lo tenga que pegar en el chat.
3. Ejecuta una jornada de prueba con **un solo prospecto** siguiendo únicamente lo
   que dice el repo (sin ayuda adicional de Sergio).
4. Verifica al final:
   - El boceto tiene composición desktop+mobile (`compose_preview.py` se usó).
   - Las imágenes de Unsplash cargan (no están rotas).
   - La ficha de Notion muestra el boceto y la evidencia de Instagram como
     **imágenes reales**, no como texto `file-upload://...`.
   - El mensaje generado empieza con el saludo correcto y sigue la estructura del
     prompt actualizado.

---

## PASO 11 — Cómo comparar contra este Claude Code

Correr el mismo prospecto (o uno equivalente del mismo nicho) por ambos flujos y
comparar:

| Criterio | Este Claude Code (hoy) | Alan (después del plan) |
|---|---|---|
| Boceto con vista mobile | Sí | ¿? |
| Boceto con vista compuesta desktop+mobile | Sí | ¿? |
| Imagen visible en Notion (no texto roto) | Sí | ¿? |
| Mensaje con saludo "Hola 👋 Somos de PAGX Studio." | Sí | ¿? |
| Evidencia de Instagram adjunta en Notion | Sí | ¿? |
| Dedup verificado contra toda la base antes de crear ficha | Sí | ¿? |

Si las 6 casillas de Alan quedan en "Sí", el comportamiento está replicado al nivel
que importa (resultado), independientemente de si su configuración interna de
Claude Code es idéntica byte a byte a la de Sergio (que, según la auditoría, ni
siquiera existe como "configuración de proyecto" — es casi toda de cuenta y de
prompt).

---

## PASO 12 — Confirmar que Alan quedó equivalente

Checklist final, a repetir después de 2-3 jornadas reales de Alan:

- [ ] Cero fichas nuevas de Alan con el bug de `file-upload://` visible como texto.
- [ ] Todos los bocetos nuevos de Alan tienen el archivo `-desktop.png`,
      `-mobile.png` y el combinado.
- [ ] La Bitácora de Alan sigue llenándose (era un gap ya detectado y corregido
      manualmente hoy para el 07-09/09/2026 — confirmar que no vuelve a faltar).
- [ ] Sergio revisa 1-2 mensajes comerciales de Alan y confirma que siguen la
      estructura y el saludo correctos sin que él tenga que corregirlos.

---

## Resumen de archivos que deben crearse/modificarse

| Archivo | Acción |
|---|---|
| `prompts/PROMPT-MAESTRO.md` | Modificar — fusionar la actualización de saludo + evidencia visual |
| `docs/COMO-ACTUALIZAR-BOCETO.md` | Modificar — agregar sección Unsplash + verificación con `curl` |
| `docs/capturar-boceto.md` | Modificar — agregar truco de iframe móvil + `compose_preview.py` + advertencia sobre `IH` |
| `docs/NOTION.md` | Modificar — agregar advertencia de sintaxis de imagen + verificación obligatoria |
| `docs/FLUJO-ALAN.md` | Modificar — Paso 9 actualizado + nuevo Paso 9-bis (evidencia) |
| `CLAUDE_CODE_FORENSIC_AUDIT.md` | Crear (ya creado) |
| `CLAUDE_CODE_REPLICATION_PLAN.md` | Crear (ya creado, este archivo) |

Ningún archivo de configuración de Claude Code (`settings.json`, `.mcp.json`,
hooks, agentes) necesita crearse o modificarse — la auditoría confirmó que ninguno
de ellos explica la diferencia de comportamiento.
