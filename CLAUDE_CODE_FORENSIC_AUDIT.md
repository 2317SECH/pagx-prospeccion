# Auditoría forense — Claude Code en el entorno de prospección PAGX Studio

**Fecha:** 09/09/2026
**Autor:** Claude Sonnet 5, dentro de la sesión de Sergio (`session_015Z1SU13WqvEJkkKAEDSdLm`)
**Alcance:** el entorno local de Sergio (`C:\Users\Sergio`), el repo `2317SECH/pagx-prospeccion`, y la cuenta de Claude conectada a esta sesión.

## Límite de la investigación — léase primero

Esta auditoría inspeccionó **archivos reales** en disco y **configuración real** de esta
cuenta/sesión. Todo lo que sigue está respaldado por una ruta de archivo, un comando
ejecutado o un valor leído — no por suposición.

**No tengo, y no puedo obtener, acceso al entorno de Alan.** No hay ningún archivo,
proceso, API ni credencial en esta máquina que exponga su `settings.json`, su
`.claude.json`, sus conectores de claude.ai, su extensión de Chrome, su modelo, ni su
historial de sesiones. Cualquier afirmación sobre "el Claude Code de Alan" en este
documento es **inferencia a partir de lo que el repo compartido le dice a Alan que
haga** (`docs/FLUJO-ALAN.md`, `prompts/PROMPT-MAESTRO.md`) — nunca una lectura directa
de su configuración. Donde no hay evidencia, este documento lo dice explícitamente en
vez de rellenar el hueco.

---

## 1. Resumen ejecutivo

Investigué mi propia configuración (la de esta sesión/cuenta) y el repositorio
compartido. Hallazgo principal, en una frase:

> **La diferencia no está en skills, MCP ni hooks especiales — no existe ninguna
> configuración de prospección instalada en este Claude Code.** Existen tres
> factores reales: (1) un **prompt maestro más nuevo y más largo** que Sergio pega
> directamente en el chat cada sesión y que **nunca se sincronizó al repo** que lee
> Alan; (2) un **sistema de memoria privado por cuenta/máquina** (`~/.claude/projects/.../memory/`)
> que acumula lecciones técnicas duramente aprendidas (bugs de `stitch.py`, sintaxis
> correcta para adjuntar imágenes en Notion, truco del iframe para capturas mobile,
> IDs de Unsplash verificados) que **no están en ningún archivo del repo** y por
> tanto son invisibles para Alan; y (3) **conectores de cuenta** (Notion, Chrome)
> que dependen enteramente de que la cuenta de claude.ai de cada persona los tenga
> conectados y con los permisos correctos — algo que no puedo verificar para Alan.

No hay skill de "prospección PAGX". No hay subagente dedicado. No hay hook que
valide bocetos o Notion. Todo el comportamiento correcto de esta sesión viene de
**instrucciones en el prompt + memoria privada + disciplina de verificación manual**
(re-leer lo que se escribió en Notion, verificar imágenes de Unsplash con `curl`
antes de usarlas, etc.), no de una pieza de configuración que se pueda "instalar".

---

## 2. Arquitectura del entorno

```
C:\Users\Sergio\
├── .claude.json              ← config de cuenta: proyectos conocidos, uso/costos, NO mcpServers
├── .claude\
│   ├── settings.json         ← hooks (solo caveman), plugin caveman, tema, voz
│   ├── settings.local.json   ← permisos: solo "Bash(claude *)"
│   ├── hooks\                ← 5 scripts, todos del plugin caveman (cosmético)
│   ├── plugins\               ← 1 plugin instalado: caveman (marketplace externo)
│   └── projects\
│       └── C--Users-Sergio-Desktop-PAGX-Studio\
│           └── memory\        ← MEMORY.md + 2 archivos — PRIVADO, no está en git
└── Desktop\PAGX Studio\
    ├── pagx-prospeccion\      ← el repo real, remote origin = 2317SECH/pagx-prospeccion
    │   ├── prompts\PROMPT-MAESTRO.md   ← versión CANÓNICA pero más antigua que la pegada en chat
    │   ├── docs\*.md                    ← 6 docs operativos (ver §3 más abajo)
    │   ├── tools\*.py                   ← 4 scripts Python, sin dependencias
    │   ├── bocetos\*.html + preview\*.png
    │   └── .env.example                ← plantilla; NOTION_TOKEN nunca presente en disco
    └── (sin CLAUDE.md — no existe ningún archivo CLAUDE.md en este proyecto)
```

**No existe ningún directorio `.claude/` dentro del proyecto** (ni en `PAGX Studio/`
ni en `pagx-prospeccion/`). Todo lo que afecta el comportamiento de Claude Code aquí
es **global a la cuenta de Sergio**, no del repo. Esto es clave: significa que nada
de "configuración de Claude Code" viaja con `git clone` — Alan no hereda nada de esto
por tener el repo.

---

## 3. Skills

Inspeccioné la lista de skills disponibles en esta sesión (viene declarada en el
`<system-reminder>` de skills disponibles, no en un archivo del proyecto). Ninguna es
específica de PAGX Studio o de prospección:

| Skill | Qué hace | ¿Específica de PAGX? |
|---|---|---|
| `caveman`, `caveman-*` (7 variantes) | Comprime la comunicación del chat (menos texto, mismo contenido técnico) | No — solo estilo de respuesta |
| `design`, `artifact-design`, `artifact-diagramming`, `artifact-capabilities` | Crear/editar Artifacts (páginas HTML publicadas) | No |
| `dataviz` | Guía de diseño para gráficos/dashboards | No |
| `code-review`, `simplify`, `security-review` | Revisión de código | No |
| `update-config`, `keybindings-help`, `fewer-permission-prompts` | Configurar el propio Claude Code | No |
| `loop`, `schedule` | Tareas recurrentes/cron | No |
| `claude-api` | Referencia de la API de Anthropic | No |
| `claude-in-chrome` | **Solo dice**: "antes de usar herramientas `mcp__claude-in-chrome__*`, cárgalas todas juntas con un `ToolSearch` en una sola llamada" — es una nota de rendimiento sobre *cómo llamar* las herramientas, no contiene lógica de negocio ni instrucciones de Instagram/prospección | No |
| `run`, `init` | Ejecutar apps / documentar repos nuevos | No |

**No encontré ninguna skill de "prospección", "PAGX", "boceto" ni "Notion CRM".**
Verifiqué esto de dos formas: (1) la lista de skills que Claude Code me expone al
inicio de la sesión, y (2) una búsqueda en disco (`find ~/.claude -iname "*skill*"`)
que solo encontró skills del plugin `caveman` y del marketplace oficial de plugins
(Discord, iMessage, Telegram, `claude-md-management`, `claude-security`) — ninguna
relacionada con este proyecto.

**Conclusión:** las skills que uso en esta sesión son **skills genéricas del
producto Claude Code**, iguales para cualquier usuario (incluido Alan, si tiene la
misma versión). No explican la diferencia de comportamiento.

---

## 4. MCP — auditoría completa

Busqué `mcpServers` en dos lugares: `~/.claude.json` (global) → **vacío (`{}`)** — y
la entrada específica del proyecto PAGX Studio dentro de ese mismo archivo → también
**vacío** (`"mcpServers": {}`, `"enabledMcpjsonServers": []`). No existe ningún
archivo `.mcp.json` en el repo.

**Hallazgo importante:** los servidores MCP que uso (`claude-in-chrome`,
`claude_ai_Notion`, `claude_ai_Google_Drive`, `claude_ai_artlist`) **no vienen de
ningún archivo de configuración local ni del repo**. El prefijo `claude_ai_` indica
que son **conectores de la cuenta de claude.ai** (Settings → Connectors), vinculados
a la cuenta de Anthropic de Sergio, no al proyecto. Evidencia indirecta: `.claude.json`
tiene la clave `claudeAiMcpEverConnected` y `chromeExtension` /
`cachedChromeExtensionInstalled` / `claudeInChromeDefaultEnabled` a nivel de cuenta,
no de proyecto.

Herramientas concretas usadas hoy y para qué exactamente:

| Herramienta MCP | Para qué la usé hoy |
|---|---|
| `mcp__claude_ai_Notion__notion-query-data-sources` (modo `sql`) | Anti-duplicados: `SELECT Empresa, Nicho, "Clave de deduplicación" FROM ...` contra toda la base antes de elegir candidatos |
| `mcp__claude_ai_Notion__notion-fetch` | Leer el esquema completo de la base (`<sqlite-table>`) y **releer cada ficha después de crearla** para verificar que las imágenes quedaron adjuntas de verdad |
| `mcp__claude_ai_Notion__notion-create-pages` | Crear las 8 fichas + las 3 entradas de Bitácora |
| `mcp__claude_ai_Notion__notion-update-page` (`update_content`) | Corregir la sintaxis de imagen cuando falló la primera vez (ver §6) |
| `mcp__claude_ai_Notion__notion-create-file-upload` | Generar una URL de subida de un solo uso por archivo |
| `mcp__claude-in-chrome__tabs_context_mcp` / `navigate` / `computer` / `javascript_tool` | Toda la navegación e investigación en Instagram, y la captura de screenshots |

**No usé** `claude_ai_Google_Drive` ni `claude_ai_artlist` en esta jornada — están
conectados a la cuenta pero no aplican al flujo de prospección.

**Lo que no puedo verificar para Alan:** si su cuenta de claude.ai tiene el
conector de Notion conectado, si ese conector apunta al mismo workspace, si tiene
permiso de escritura sobre la base `Prospectos`, ni si tiene la extensión de Chrome
instalada y emparejada. Esto se prueba **haciéndoselo preguntar a él directamente**
(ver plan de réplica, paso 5).

---

## 5. Chrome / navegador

Mecanismo real, verificado por uso en esta sesión (no por documentación):

1. `mcp__claude-in-chrome__tabs_context_mcp {createIfEmpty:true}` — abre/recupera
   un grupo de pestañas propio de la sesión.
2. `navigate` con URL directa a `instagram.com/explore/search/` o a un perfil
   (`instagram.com/<usuario>/`) — **no** se usa un motor de búsqueda externo para
   encontrar cuentas de Instagram; la búsqueda de nichos se hace escribiendo en el
   buscador nativo de Instagram (clic + `type` en el campo de búsqueda).
3. `computer {action: screenshot}` para leer visualmente bio, seguidores, grid.
4. `javascript_tool` para: inyectar CSS que congela el nav y desactiva
   `scroll-behavior: smooth` antes de capturar, esperar `document.fonts.ready` y que
   todas las `<img>` terminen de cargar, y leer `window.scrollY` /
   `window.innerHeight` reales antes de cada captura.
5. **Regla operativa descubierta por prueba y error (está en memoria privada, no en
   el repo):** nunca meter `computer{action:screenshot}` dentro de un
   `browser_batch` — se cuelga con "Page.captureScreenshot timed out". Los
   screenshots van siempre como llamada independiente.
6. El "contexto de qué prospecto se está procesando" no lo guarda ninguna
   herramienta: lo mantengo yo en el hilo de la conversación (nombre de archivo,
   IDs de Notion, coordenadas de scroll) — es memoria de trabajo del propio agente,
   no un mecanismo externo.

`mcp__claude-in-chrome__browser_batch` se usó extensivamente para encadenar
navegación + clic + escritura + espera en una sola llamada — es la razón principal
de por qué esta sesión hace menos idas y vueltas que si cada acción fuera una
llamada separada (ver §10, velocidad).

---

## 6. Imágenes — el flujo real

Este es el punto donde más diferencia hay entre lo que dice el repo y lo que
realmente hago. Documentando el flujo real, paso por paso, con archivos:

### 6.1 Imágenes de los bocetos (fondo/fotografía del sitio del prospecto)

- **Fuente:** Unsplash, vía URL directa `images.unsplash.com/photo-<ID>?w=..&h=..&fit=crop&q=75`.
  `docs/COMO-ACTUALIZAR-BOCETO.md` **no menciona Unsplash en absoluto** — solo
  documenta `cdn.imagin.studio` (autos) y `i.pravatar.cc` (personas). El uso de
  Unsplash para todo lo demás (interiores, comida, bodas, autos de lujo, DJ, moda)
  es una técnica que solo existe en mi memoria privada
  (`boceto-preview-workflow.md`), nunca comiteada al repo.
- **Por qué funciona sin fallos visibles:** antes de usar un ID de Unsplash lo
  descargo con `curl -s -o id.jpg "https://images.unsplash.com/photo-<ID>?w=400"` y
  lo **abro con la herramienta `Read`** para confirmar visualmente que el contenido
  coincide con lo que necesito — porque IDs adivinados fallan ~30-40% de las veces
  (o devuelven contenido genérico). Esto lo hice explícitamente hoy: verifiqué 34+
  IDs candidatos antes de usar ~20 en los 8 bocetos de hoy.
- **Formato/dimensiones:** decididas por mí en cada `<img>` según el layout CSS
  (hero 900×1100, tarjetas de grid 700×860, panel ancho 900×720) — no hay ninguna
  herramienta que calcule esto; es una convención que repito de boceto en boceto.

### 6.2 Capturas de pantalla del boceto (el PNG que se sube a Notion)

Proceso real (ninguno de estos pasos está completo en `docs/capturar-boceto.md`,
que solo cubre la idea general):

1. Servir el repo local: `python -m http.server 8899` en background.
2. Abrir el boceto, inyectar CSS de congelado, esperar fuentes/imágenes.
3. Leer `window.innerHeight` real de la pestaña (varía entre ~854 y ~980 según el
   panel de la extensión — esto lo aprendí de memoria previa, no es obvio).
4. Capturar en pasos de scroll (`~650px` escritorio, `~700px` móvil) con
   solape, screenshot por screenshot, `save_to_disk:true`.
5. **Para móvil:** el viewport de escritorio no se puede reducir a 390px de forma
   fiable (`resize_window` no funciona en ventanas maximizadas de Windows) — la
   solución real es servir una página `_mobile-wrap.html` con un `<iframe
   style="width:390px">` y capturar la página contenedora. **Esto no está
   documentado en ningún archivo del repo.**
6. Unir con `tools/stitch.py <salida> <IH> '[[archivo,scrollY],...]'`.
   **Bug real que encontré y corregí hoy mismo, en vivo:** si a `IH` le pasas la
   altura en píxeles del screenshot (p. ej. 744) en vez del `window.innerHeight`
   real en píxeles CSS (p. ej. 911), el resultado tiene **contenido duplicado
   visible** (la escala interna de `stitch.py` calcula mal el punto de pegado). Lo
   detecté, lo diagnostiqué y re-ejecuté con el valor correcto en los primeros 4
   bocetos de hoy. Este bug es sutil y **cualquiera que siga la documentación tal
   cual está escrita puede caer en él**, porque `capturar-boceto.md` dice "IH =
   innerHeight real de la pestaña" pero no explica que el screenshot devuelto NO
   tiene esas mismas dimensiones en píxeles.
7. Componer la vista combinada desktop+mobile con `tools/compose_preview.py` — **no
   mencionado en ningún doc del repo**, solo lo sé porque está en mi memoria
   privada. Sin este paso, un boceto quedaría con una sola imagen (o dos imágenes
   sueltas) en vez de la tarjeta pulida "DESKTOP / MOBILE" que ven los prospectos.

### 6.3 Subida a Notion

1. `mcp__claude_ai_Notion__notion-create-file-upload {filename}` → devuelve
   `upload_url` + `upload_headers` de un solo uso.
2. `curl -X POST <upload_url> -H "authorization: Bearer ..." -F "file=@ruta.png"`
   vía la herramienta Bash — **no** vía la herramienta MCP (el MCP solo entrega la
   URL firmada; la subida real del binario se hace con `curl` porque no hay
   herramienta MCP que suba bytes directamente).
3. **El paso que rompió la primera vez, hoy, y cómo lo until:** al crear la página
   escribí `<image src="file-upload://ID">` en el contenido — la sintaxis que
   recordaba de memoria previa. **Esa sintaxis no funciona**: Notion la guarda como
   texto plano escapado, visible pero no como imagen. La sintaxis correcta,
   confirmada leyendo `notion://docs/enhanced-markdown-spec` en vivo, es
   `![Caption](file-upload://ID)` (markdown estándar de imagen, no una etiqueta
   `<image>`). Lo descubrí porque **releí la ficha después de crearla** (`notion-fetch`)
   y vi el texto escapado en vez de una imagen — y corregí las 4 primeras fichas
   con `update_content` antes de seguir. Esta lección específica **la voy a guardar
   en memoria ahora**, pero hasta hoy no existía en ningún lado, ni en el repo ni en
   memoria previa.
4. **Verificación, no asunción:** después de cada corrección, volví a hacer
   `notion-fetch` y confirmé que el markdown de salida mostraba una URL firmada de
   S3 (`prod-files-secure.s3.us-west-2.amazonaws.com/...`) en vez del texto
   `file-upload://...` — esa es la prueba real de que la imagen quedó adjunta, no
   solo "seguí los pasos y asumí que funcionó".

---

## 7. Generación de textos (mensajes comerciales)

Flujo real de hoy, INVESTIGACIÓN → DATOS → ANÁLISIS → REDACCIÓN → REVISIÓN → MENSAJE FINAL:

1. **Investigación:** leer bio completa (clic en "...más" cuando el texto está
   truncado), contar publicaciones/seguidores, abrir highlights relevantes, hacer
   scroll al grid para ver el contenido real (no solo la miniatura de la foto de
   perfil).
2. **Datos:** extraigo solo hechos verificables — número de bodas, nombre real de
   venues, premios mencionados en la bio, dirección física si está publicada. Nunca
   cifras inventadas (coherente con la regla §27 de `PROMPT-MAESTRO.md`: "Si no se
   sabe algo: No pude verificarlo").
3. **Análisis:** decido problema + oportunidad comparando "qué tiene" (contenido,
   seguidores, actividad) contra "qué le falta" (web propia, catálogo navegable,
   formulario) — esto es razonamiento del modelo, no un template rígido.
4. **Redacción:** sigo la estructura fijada por la actualización del prompt maestro
   que Sergio pegó en el chat hoy — saludo "Hola 👋 Somos de PAGX Studio.", gancho
   personalizado, oportunidad, propuesta, mención de la preview ~20%, CTA suave.
   **Esta estructura de mensaje (el saludo con el nombre correcto "PAGX Studio" y no
   "Pax Studio") viene de un documento pegado en el chat de HOY, y no existe en
   ningún archivo del repo** — ver §14.
5. **Revisión:** antes de dar por bueno un mensaje lo paso mentalmente por el
   checklist de control de calidad que el propio prompt trae (empieza con el
   saludo correcto, está personalizado con datos reales, no sensacionalista, cierre
   no agresivo). No hay una segunda llamada de modelo dedicada a "revisar" — la
   reviso yo mismo antes de escribirla en Notion.
6. **Mensaje final:** se guarda en la propiedad `Mensaje listo` y se repite en el
   cuerpo de la página bajo `## Mensaje`.

---

## 8. Notion — cómo se consigue el flujo completo

```
PROSPECTO → INVESTIGACIÓN → MENSAJE → ESTADO → PANTALLAZOS → IMÁGENES → todo en Notion
```

Mecanismo real, en orden:

1. **Dedup primero** (§9) — consulta SQL sobre toda la base antes de decidir
   candidatos.
2. **Una sola llamada `notion-create-pages` por lote** (hoy: 4 páginas a la vez, dos
   veces) con **todas** las propiedades + el contenido completo del cuerpo
   (incluyendo el markdown de imagen) en la misma llamada — no llamada por campo.
3. **Estructura del cuerpo** (fija, la repito en cada ficha): Información general →
   Investigación → Web → Comercial → Propuesta → Boceto (con imagen) → Mensaje →
   Contacto → Estado → Próximo paso → **Evidencia / Pantallazos** (con imagen). Los
   dos últimos bloques con imagen (`## Boceto` y `## Evidencia / Pantallazos`) son
   el punto exacto donde use `![Caption](file-upload://ID)`.
4. **Verificación posterior, siempre:** `notion-fetch` de cada página después de
   crearla, específicamente para confirmar que las imágenes renderizaron (regla que
   yo mismo me impuse hoy después del fallo de §6.3, no algo que el sistema fuerce).
5. **Bitácora:** una entrada nueva por jornada (o por tanda, cuando hice dos tandas
   el mismo día), con la relación `Prospectos trabajados` apuntando a las URLs
   exactas de las páginas recién creadas.

---

## 9. Anti-duplicados — mecanismo real

**No es el script `tools/check-duplicado.py`.** Ese script existe en el repo, es
opcional, y requiere `NOTION_TOKEN` en un `.env` que **no existe en esta máquina**
(confirmado: `ls .env` → no existe). No lo usé ni una vez hoy.

Lo que uso de verdad: `mcp__claude_ai_Notion__notion-query-data-sources` en modo
`sql`, con una consulta tipo:

```sql
SELECT "Empresa", "Nicho", "Clave de deduplicación"
FROM "collection://88376280-f3f7-4ae7-a9db-34144929c8fe"
```

Traigo **toda la tabla** (hoy: 37 y luego 41 filas) a mi contexto de conversación y
comparo manualmente los nombres/usuarios de Instagram de los candidatos nuevos
contra esa lista, antes de decidir cuáles investigar a fondo. Es más simple que los
"5 checks" documentados en `ANTIDUPLICADOS.md` (nombre, dominio, Instagram,
teléfono, otros) porque con la tabla completa en contexto puedo comparar de un
vistazo — pero **el resultado es equivalente** al procedimiento documentado, solo
que ejecutado por lectura directa del MCP en vez de por scroll manual en la UI de
Notion.

---

## 10. Velocidad — por qué esta sesión encadena tanto sin detenerse

No puedo comparar contra la sesión real de Alan (no la vi). Lo que sí puedo
documentar es **qué hace que esta sesión sea eficiente**, con evidencia:

| Factor | Evidencia en esta sesión |
|---|---|
| `browser_batch` agrupa navegación+clic+escritura+espera | Usado en casi todos los pasos de investigación de Instagram — evita 1 llamada por acción |
| Verificación de imágenes por lote (`curl` + `Read`) en vez de una por una en el navegador | 8-12 IDs de Unsplash verificados por llamada `Bash` |
| Creación de Notion por lote (`notion-create-pages` con 4 páginas en una llamada) en vez de página por página | Reduce 4 llamadas a 1 |
| Subida de archivos a Notion por lote (4 `notion-create-file-upload` en paralelo, luego 4 `curl` en un solo bloque Bash) | Igual que arriba |
| **Ningún subagente (`Task`/`Agent`) usado hoy** | Cero llamadas a la herramienta `Agent` en toda la sesión — todo el trabajo lo hizo el agente principal, secuencialmente pero con alto paralelismo *dentro* de cada llamada |
| Memoria previa evita re-descubrir bugs ya resueltos (sintaxis de Notion, escala de `stitch.py`, truco del iframe móvil) | Ver §6 — cada uno de esos bugs, si se repite desde cero, cuesta una ronda extra de intento-fallo-diagnóstico-corrección |
| `reasoning_effort` configurado en un nivel medio (40) para esta sesión, más uso confirmado de *extended thinking* en la sesión anterior (154.072 tokens de pensamiento según `.claude.json` → `lastModelUsage.claude-sonnet-5.thinkingTokens`) | Dato leído directamente del archivo, no inferido |

**Lo que NO explica la velocidad:** no hay subagentes paralelos, no hay hooks que
precomputen nada, no hay caché de resultados de Instagram. La eficiencia viene de
**agrupar llamadas de herramienta** y de **no repetir errores ya resueltos**, no de
arquitectura especial.

---

## 11. Agents / Subagentes

**No usé ninguno hoy.** Cero llamadas a la herramienta `Agent` (ni `fork` ni
ningún `subagent_type`) en las dos jornadas completas de prospección. Todo el
trabajo — investigación de Instagram, diseño de bocetos, captura de screenshots,
escritura en Notion — lo ejecutó el agente principal de esta conversación,
secuencialmente.

Existen agentes disponibles en el sistema (`Explore`, `Plan`, `general-purpose`,
`claude-code-guide`, y los de un plugin externo `caveman:cavecrew-*`), pero
**ninguno está configurado ni se invocó para este flujo**. Si el Claude Code de
Alan sí delega en subagentes por defecto (algo que no puedo verificar), eso
introduciría pérdida de contexto entre llamadas que esta sesión no tiene.

---

## 12. Hooks

Únicos hooks activos, leídos directamente de `~/.claude/settings.json`:

| Hook | Cuándo | Qué hace | Relacionado con prospección? |
|---|---|---|---|
| `SessionStart` → `caveman-activate.js` | Al iniciar sesión | Activa el modo de comunicación comprimida "caveman" | No |
| `UserPromptSubmit` → `caveman-mode-tracker.js` | En cada mensaje del usuario | Mantiene el estado del modo caveman activo | No |
| `statusLine` → `caveman-statusline.ps1` | Continuo | Barra de estado visual | No |

**No hay ningún hook `PreToolUse` ni `PostToolUse`** que valide bocetos, revise
duplicados, o fuerce algún paso del flujo de prospección. Todo el orden
("investigar antes de actuar", "verificar antes de dar por hecho") es
**comportamiento del modelo siguiendo el prompt**, no una automatización externa
que lo obligue.

---

## 13. Memoria / contexto / estado

Esta es la pieza más importante y menos visible de la investigación.

**Ubicación:** `C:\Users\Sergio\.claude\projects\C--Users-Sergio-Desktop-PAGX-Studio\memory\`
**Contenido actual (leído hoy):**
- `MEMORY.md` — índice de 2 líneas.
- `prospeccion-cadencia.md` — dónde vive todo (repo, IDs de Notion, reglas de
  atribución Sergio/Alan, numeración de bocetos, flujo por jornada).
- `boceto-preview-workflow.md` — **exactamente** los bugs y trucos de §6: escala de
  `stitch.py`, truco del iframe móvil, IDs de Unsplash verificados por categoría,
  cómo recuperar una pestaña con screenshots congelados, `compose_preview.py`.

**Confirmé con `git status --short --ignored` que esta carpeta NO está dentro del
repo** (vive en `~/.claude/`, fuera del working directory de git) — es imposible
que viaje por `git clone`, `git pull` ni ningún mecanismo del repo. Es
**estrictamente privada de esta cuenta de claude.ai en esta máquina**.

Esto significa: aunque Alan clone el repo completo hoy mismo, **no hereda ni una
sola línea de esta memoria**. Si su Claude Code tiene el mismo sistema de memoria
habilitado (probablemente sí, es una función del producto, no algo que Sergio
activó a mano), su memoria estará vacía o contendrá solo lo que él mismo haya
acumulado en sus propias sesiones — que no incluye ninguna de las lecciones
documentadas arriba, porque esas las aprendí yo, hoy y en sesiones previas de
Sergio, no él.

---

## 14. Modelo / thinking / effort

- **Modelo de esta sesión:** `claude-sonnet-5` (confirmado por el `<system-reminder>`
  de la sesión y por `lastModelUsage` en `.claude.json`).
- **Uso de *extended thinking*:** confirmado por datos reales — la sesión anterior
  de este mismo proyecto registró `154,072` `thinkingTokens` bajo `claude-sonnet-5`
  en `.claude.json` → `projects["C:/Users/Sergio/Desktop/PAGX Studio"].lastModelUsage`.
  Esta sesión actual tiene razonamiento extendido configurado en un nivel medio.
- **Consumo de contexto vía caché:** la misma entrada registra
  `189,773,915` tokens de caché leídos frente a solo `6,474` tokens de entrada
  "frescos" — es decir, esta cuenta reutiliza contexto cacheado masivamente entre
  turnos, lo cual abarata y acelera turnos largos como los de hoy.
- **No hay ninguna skill ni archivo que fije el modelo o el effort a nivel de
  proyecto.** Es una propiedad de la sesión/cuenta, elegida al iniciar la
  conversación (o por defecto de la cuenta), no del repo.

**Lo que no puedo saber sobre Alan:** qué modelo tiene disponible en su plan, si su
sesión usa *thinking* extendido, ni su nivel de *effort*. Esto se pregunta
directamente, no se adivina (ver plan de réplica).

---

## 15. Comparación con el entorno de Alan

| Dimensión | Este Claude Code (verificado) | Claude Code de Alan (según documentación compartida — NO verificado en su máquina) |
|---|---|---|
| CLAUDE.md del proyecto | No existe ninguno | No existe ninguno (mismo repo) |
| Prompt maestro que realmente sigue | El que Sergio **pega en el chat cada sesión** — más largo, con la actualización de "Hola 👋 Somos de PAGX Studio" y evidencia visual en Notion, **nunca comiteado** | Solo el `prompts/PROMPT-MAESTRO.md` del repo (más corto, sin la actualización de hoy), leído vía `docs/FLUJO-ALAN.md` |
| Memoria privada de lecciones técnicas | Sí — 2 archivos con bugs y trucos ya resueltos | Ninguna (su memoria, si existe, es propia y no contiene estas lecciones) |
| Documentación de imágenes de boceto | Repo dice `imagin.studio` + `pravatar.cc` solamente; Unsplash + verificación con `curl` solo en memoria privada | Solo lo que dice el repo → probablemente no usa Unsplash, o lo usa sin verificar IDs |
| Documentación de captura de screenshots | Repo cubre desktop; el truco de iframe para móvil y `compose_preview.py` no están documentados en ningún archivo | Sin esta información, un boceto de Alan probablemente carece de la vista mobile o de la composición desktop+mobile lado a lado |
| Sintaxis correcta para adjuntar imágenes en Notion | Descubierta y corregida hoy mismo (`![](file-upload://ID)`, no `<image src=...>`) | Sin este dato en ningún doc — riesgo real de que sus fichas tengan el mismo fallo silencioso que tuve yo al principio de hoy |
| MCP de Notion/Chrome | Conectados a la cuenta de Sergio, con acceso confirmado de escritura a la base `Prospectos` | Desconocido — memoria (`prospeccion-cadencia.md`) dice "acceso Notion confirmado" para Alan, pero no puedo verificar permisos exactos ni si su Chrome está emparejado |
| Modelo / thinking | Sonnet 5, effort medio, thinking extendido usado en sesiones previas | Desconocido |
| Subagentes | Ninguno usado | Desconocido si su Claude Code delega por defecto |
| Hooks | Solo cosméticos (caveman) | Desconocido, probablemente ninguno relacionado (no hay hooks de proyecto en el repo) |
| Anti-duplicados | Consulta SQL completa vía MCP antes de cada jornada | Documentado como "5 checks manuales en la UI de Notion" — más lento, más propenso a error humano si se salta un check |

---

## 16. Causa probable de la diferencia de calidad

En orden de impacto probable (mayor a menor):

1. **El prompt que Sergio pega en el chat es más nuevo que el que lee Alan del
   repo.** La actualización de hoy (saludo "Hola 👋 Somos de PAGX Studio.", la
   exigencia de adjuntar evidencia visual en Notion) **no existe en
   `prompts/PROMPT-MAESTRO.md`**. Si Alan solo tiene el repo, literalmente no sabe
   que esas reglas existen.
2. **La memoria privada evita fallos silenciosos que yo mismo cometí hoy** (sintaxis
   de imagen en Notion) y que un Claude Code sin esa memoria repetiría — con la
   diferencia de que quizás nadie se dé cuenta, porque el fallo es silencioso (el
   texto queda escrito, solo que como texto plano feo en vez de imagen).
3. **Documentación incompleta de las partes más difíciles técnicamente** (captura
   mobile, composición desktop+mobile, verificación de Unsplash) — un Claude Code
   que solo tenga el repo como fuente de verdad construirá bocetos más pobres
   (sin vista mobile, o con imágenes que no cargan) simplemente porque el repo no
   le enseña cómo evitarlo.
4. **Verificación activa como hábito, no como regla escrita.** Releer cada ficha de
   Notion después de escribirla, y descargar+mirar cada imagen antes de usarla, no
   está impuesto por ninguna herramienta — es un patrón de trabajo. Si Alan (o su
   Claude Code) no lo hace por costumbre, puede terminar con fichas rotas sin
   notarlo.

## 17. Causa probable de la diferencia de velocidad

1. **Llamadas agrupadas** (`browser_batch`, lotes de `notion-create-pages`, lotes de
   `notion-create-file-upload` + subida en un solo bloque `curl`) — menos turnos de
   ida y vuelta por la misma cantidad de trabajo.
2. **Cero reintentos por errores ya conocidos** — no perder tiempo en la escala de
   `stitch.py` o en la sintaxis de imagen de Notion porque ya se sabía (o se
   corrigió una vez y no dos).
3. **Reutilización de caché de prompt** (189M tokens de caché leídos en la sesión
   anterior) reduce el costo/latencia de mantener contexto largo.
4. No hay evidencia de que el modelo o el nivel de esfuerzo sean distintos — no
   puedo confirmar que Alan tenga un modelo más lento; es más probable que la
   diferencia esté en el **número de intentos fallidos** que en la velocidad bruta
   del modelo.

---

## 18. Riesgos — qué NO tocar

- **No** crear un `.mcp.json` en el repo intentando "fijar" los conectores de
  Notion/Chrome — son de cuenta, no de proyecto; un `.mcp.json` mal puesto podría
  romper la conexión existente de Sergio sin arreglar la de Alan.
- **No** modificar `~/.claude/settings.json` de Sergio pensando que eso afecta a
  Alan — es un archivo por máquina/usuario, no se comparte.
- **No** borrar ni reescribir `docs/FLUJO-ALAN.md` ni `prompts/PROMPT-MAESTRO.md`
  existentes — se actualizan, no se reemplazan, para no perder el trabajo de
  referencia que ya usa la numeración de bocetos 01-04 como plantilla.
- **No** intentar replicar la memoria privada de Sergio copiando literalmente sus
  archivos de `~/.claude/projects/.../memory/` a la máquina de Alan — esos archivos
  son específicos de la ruta del proyecto en la máquina de Sergio
  (`C--Users-Sergio-Desktop-PAGX-Studio`) y de su cuenta; en la máquina de Alan ese
  sistema generará su propia carpeta con su propio hash de ruta. Lo que sí se
  puede — y se debe — hacer es **trasladar el contenido útil a documentación del
  repo**, que sí es compartible.
- **No** instalar el plugin `caveman` para Alan pensando que es parte de "por qué
  funciona mejor" — es puramente cosmético (comprime las respuestas de chat) y no
  tiene ninguna relación con la calidad de la investigación o el boceto.

---

## 19. Checklist de validación (cómo comprobar que Alan quedó equivalente)

- [ ] Alan puede abrir `prompts/PROMPT-MAESTRO.md` y encontrar ahí el saludo
      "Hola 👋 Somos de PAGX Studio." y la exigencia de evidencia visual (después de
      aplicar el plan de réplica, §17 del plan).
- [ ] `docs/COMO-ACTUALIZAR-BOCETO.md` menciona explícitamente Unsplash + el paso
      de verificación con `curl`, el truco del iframe para móvil, y
      `compose_preview.py`.
- [ ] Alan confirma (auto-reporte, no verificable desde aquí) que su cuenta de
      claude.ai tiene el conector de Notion activo apuntando al mismo workspace, y
      la extensión de Chrome instalada y emparejada con una sesión de Instagram
      logueada.
- [ ] El próximo boceto que produzca Alan tiene: vista desktop + vista mobile
      compuestas lado a lado, imágenes de Unsplash que cargan (no rotas), y en
      Notion la imagen del boceto y la evidencia de Instagram **se ven como
      imagen**, no como texto `file-upload://...` sin procesar.
- [ ] La Bitácora de la próxima jornada de Alan sigue el mismo formato de título
      (`DD/MM/AAAA — Alan`, sin paréntesis) que las entradas ya existentes.

---

## 20. Lo que descubrí que Sergio probablemente no sabía

- El repo tiene **dos versiones del prompt maestro que ya divergieron**: la que
  vive en `prompts/PROMPT-MAESTRO.md` (corta, refinada) y la que Sergio pega en el
  chat cada sesión (larga, con las actualizaciones de PAGX Studio branding y
  evidencia visual). Ninguna de las dos contiene exactamente lo que la otra tiene.
- `docs/capturar-boceto.md` y `docs/COMO-ACTUALIZAR-BOCETO.md` describen un proceso
  de captura que **no incluye la composición desktop+mobile** que en la práctica se
  usa en todos los bocetos recientes (`compose_preview.py`) — ese script existe en
  `tools/` pero **ningún doc lo menciona ni explica cómo usarlo**.
- Hay un bug real y reproducible en el flujo de Notion (sintaxis `<image
  src="file-upload://...">` vs `![](file-upload://...)`) que **no estaba
  documentado en ningún lado antes de hoy** — ni en el repo ni en memoria. Se
  corrigió en vivo durante esta sesión y ahora queda documentado aquí y se
  guardará en memoria.
- La carpeta `tools/__pycache__/` está presente en disco (bytecode compilado de
  Python) — no afecta nada, pero confirma que `tools/check-duplicado.py` sí se
  ejecutó localmente en algún momento pasado, aunque no en esta sesión.
