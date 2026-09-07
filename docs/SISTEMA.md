# SISTEMA — visión general

El sistema de prospección de PAGX Studio tiene **tres piezas**:

| Pieza | Dónde | Para qué |
|---|---|---|
| **GitHub** (este repo) | `github.com/<usuario>/pagx-prospeccion` | Versionar el código, los bocetos HTML y la documentación. |
| **GitHub Pages** | `https://<usuario>.github.io/pagx-prospeccion/` | URLs estables para ver los bocetos y mandárselos a los prospectos. |
| **Notion** | Base `Prospectos` + `Bitácora de Prospección` | El CRM vivo: cada empresa, su estado, su ficha, su boceto, su responsable. |

## Fuente de verdad

- El **estado de cada prospecto** vive en Notion. Nunca en el repo.
- El **código de cada boceto** vive en el repo. Notion solo guarda la URL y la imagen.
- La **bitácora diaria** vive en Notion (base `Bitácora de Prospección`).

## URLs de los bocetos (GitHub Pages)

> Rellenar con las URLs reales una vez publicado. Base:
> `https://<usuario>.github.io/pagx-prospeccion/`

| Prospecto | Página (para enviar) | PNG de página completa |
|---|---|---|
| Índice | `/` | — |
| 01 · Automotores Andina | `/bocetos/01-automotores-andina.html` | `/bocetos/preview/01-automotores-andina.png` |
| 02 · Infinitum Usados | `/bocetos/02-infinitum-usados.html` | `/bocetos/preview/02-infinitum-usados.png` |
| 03 · Centro Automotores | `/bocetos/03-centro-automotores.html` | `/bocetos/preview/03-centro-automotores.png` |
| 04 · DDS Clínica Dental | `/bocetos/04-dds-clinica-dental.html` | `/bocetos/preview/04-dds-clinica-dental.png` |

Cada URL de página también queda escrita en la ficha de Notion del prospecto,
propiedad **URL del boceto**.

## IDs de Notion (referencia)

| Recurso | ID / URL |
|---|---|
| Base `Prospectos` | `e11a0765-546f-4d1c-b57d-e72d28520210` |
| Data source `Prospectos` | `88376280-f3f7-4ae7-a9db-34144929c8fe` |
| Base `Bitácora de Prospección` | `5a0bd591-b861-4b36-916b-d8d697d3d873` |
| Página `Workspace Comercial — PAGX Studio` | `3a42956a-b7d3-815a-9ab6-ca43e42e988d` |

## Vistas de Notion en `Prospectos`

| Vista | Tipo | Para |
|---|---|---|
| **🎯 PROSPECCIÓN — Hoy** | Tablero por Estado | Qué hay que hacer hoy (excluye Cerrado / No interesado / Descartado) |
| **👥 Por responsable** | Tablero por Responsable | Qué lleva Sergio, qué lleva Palan |
| **🔁 Anti-duplicados** | Tabla ordenada por Clave de deduplicación | Detectar fichas repetidas (quedan pegadas) |
| **🗑️ Descartados / histórico** | Tabla | Empresas descartadas y su motivo (leer antes de reconsiderar) |
| **Pipeline** | Tablero por Estado | Todo el embudo |
| **Alta prioridad / Seguimientos pendientes / Hoy** | Tablas | Vistas heredadas, siguen funcionando |
