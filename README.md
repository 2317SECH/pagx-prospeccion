# PAGX Studio — Sistema de Prospección

Infraestructura de prospección comercial de PAGX Studio: descubrir negocios, investigarlos,
auditarlos, generar un boceto visual y dejar todo registrado en Notion **sin duplicar trabajo**.

Este repositorio contiene:

- **Los bocetos** (maquetas HTML) de cada prospecto que ya tiene propuesta visual.
- **La documentación** del flujo de trabajo, el CRM de Notion y el sistema anti-duplicados.
- **El prompt maestro** de prospección.
- **Herramientas** de apoyo (stitcher de screenshots, verificador opcional de duplicados).

> El trabajo vivo (los prospectos, sus estados, sus fichas) vive en **Notion → base `Prospectos`**.
> Este repo es el archivo versionado del código, los bocetos y las instrucciones.

---

## 1. Estructura del proyecto

```
pagx-prospeccion/
├── index.html                 Landing con los 4 bocetos (raíz de GitHub Pages)
├── bocetos/
│   ├── 01-automotores-andina.html      HTML editable del boceto
│   ├── 02-infinitum-usados.html
│   ├── 03-centro-automotores.html
│   ├── 04-dds-clinica-dental.html
│   └── preview/*.png                    Captura de página completa de cada boceto
├── docs/
│   ├── SISTEMA.md              Visión general (GitHub + Notion + Pages)
│   ├── FLUJO-PALAN.md          Los 11 pasos de una jornada de prospección
│   ├── ANTIDUPLICADOS.md       Reglas y procedimiento anti-duplicados  ← LEER SIEMPRE
│   ├── NOTION.md               Esquema del CRM, propiedades, estados, vistas
│   ├── PROSPECCION-DIARIA.md   Qué hacer hoy
│   ├── BITACORA.md             Cómo registrar la jornada
│   └── COMO-ACTUALIZAR-BOCETO.md
├── prompts/
│   └── PROMPT-MAESTRO.md       El estándar de investigación de PAGX
├── tools/
│   ├── stitch.py              Une varios screenshots en una imagen de página completa
│   ├── capturar-boceto.md     Cómo exportar un boceto a PNG
│   └── check-duplicado.py     (OPCIONAL) Verifica duplicados contra la API de Notion
├── .env.example              Plantilla de variables de entorno (sin secretos)
└── .gitignore
```

---

## 2. Ver los bocetos

**URLs estables (GitHub Pages):**

| Boceto | URL |
|---|---|
| Índice | `https://2317sech.github.io/pagx-prospeccion/` |
| 01 · Automotores Andina | `https://2317sech.github.io/pagx-prospeccion/bocetos/01-automotores-andina.html` |
| 02 · Infinitum Usados | `https://2317sech.github.io/pagx-prospeccion/bocetos/02-infinitum-usados.html` |
| 03 · Centro Automotores | `https://2317sech.github.io/pagx-prospeccion/bocetos/03-centro-automotores.html` |
| 04 · DDS Clínica Dental | `https://2317sech.github.io/pagx-prospeccion/bocetos/04-dds-clinica-dental.html` |

> Las URLs exactas quedan escritas en `docs/SISTEMA.md` y en cada ficha de Notion
> (propiedad **URL del boceto**).

También puedes abrir cualquier `bocetos/*.html` localmente con doble clic — son
archivos autónomos (solo cargan fuentes e imágenes desde CDNs públicos).

---

## 3. Actualizar un boceto

1. Edita el `bocetos/0X-*.html` correspondiente. Son HTML+CSS planos, sin build.
2. Ábrelo localmente para revisarlo.
3. (Opcional) Regenera la captura de página completa — ver `tools/capturar-boceto.md`.
4. `git add`, `git commit`, `git push`. GitHub Pages se actualiza solo en ~1 min.
5. Si cambió algo relevante para el cliente, avisa en la ficha de Notion (**Observaciones**).

Detalle completo en `docs/COMO-ACTUALIZAR-BOCETO.md`.

---

## 4. Flujo de prospección (resumen)

```
Descubrir  →  ¿Ya existe en Notion?  →  SÍ: recuperar ficha, NO duplicar
                                     →  NO: crear prospecto (Estado: Descubierto)
        →  Investigar y validar  (Estado: Investigando)
        →  Score + Prioridad
        →  Si supera criterios: Auditoría  (Estado: Auditado)
        →  Boceto visual  (Estado: Boceto  ·  Boceto: En progreso → Listo)
        →  Vincular boceto a la ficha  (URL del boceto)
        →  Estado: Listo para contactar
        →  Sergio contacta manualmente  →  Estado: Contactado + Fecha de contacto
        →  Seguimiento  →  Cerrado / No interesado
```

Cada paso registra **quién** lo hizo (Descubierto por / Auditado por / Boceto por /
Contactado por) y **cuándo**. Nada se marca como "Contactado" hasta que el mensaje
se envió de verdad.

Paso a paso en `docs/FLUJO-PALAN.md`.

---

## 5. Anti-duplicados (LO MÁS IMPORTANTE)

**Antes de crear cualquier prospecto nuevo**, buscar coincidencia por:

1. Nombre (y variantes: `S.A.S.`, `Pereira`, `Group`, etc.)
2. Dominio del sitio web
3. Usuario de Instagram
4. Teléfono (cuando exista)
5. Otros identificadores (Facebook, dirección, grupo empresarial)

Si hay coincidencia o ambigüedad → **NO se crea otra ficha**. Se recupera la existente.

El sistema usa la propiedad **Clave de deduplicación** (nombre normalizado) y una vista
de Notion **"Anti-duplicados"** para detectar choques.

Procedimiento completo y ejemplos en `docs/ANTIDUPLICADOS.md`.

---

## 6. Notion — el CRM

Base: **Prospectos** (dentro de *Workspace Comercial — PAGX Studio*).

- **NO crear otra base.** Se amplió la existente.
- Vistas clave: **PROSPECCIÓN (Hoy)**, **Pipeline** (tablero por Estado),
  **Por responsable**, **Anti-duplicados**.
- Bitácora diaria: base **Bitácora de Prospección**.

Esquema completo (propiedades, mapeos de nombres antiguos, estados) en `docs/NOTION.md`.

---

## 7. Seguridad

- **Ningún** token, API key o secreto se guarda en HTML, JS, README, commits ni en el repo.
- Los secretos van en `.env` (ignorado por git). Plantilla: `.env.example`.
- Este repo es **público** solo porque no contiene datos sensibles: los bocetos usan
  datos de demostración y CDNs públicos. Si en el futuro se añade algo sensible,
  el repo debe pasar a privado.
- Antes de cada push: revisar que no se cuele nada. `git diff` y buscar
  `token`, `secret`, `key`, `Bearer`, `NOTION_`.

---

## 8. Quién trabaja qué

| Persona | GitHub | Notion | Rol |
|---|---|---|---|
| Sergio | `2317SECH` | admin workspace | dueño, contacto con prospectos |
| Palan | `ptala611-oss` | acceso compartido por Sergio | prospección diaria, investigación, bocetos |

Acceso mínimo: Palan tiene permiso **write** al repo (no admin) y acceso a la
base `Prospectos` en Notion. **Palan no contacta prospectos** — deja todo en
"Listo para contactar" y Sergio envía.
