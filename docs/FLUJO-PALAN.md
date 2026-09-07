# FLUJO DE TRABAJO — Palan

Los 11 pasos de una jornada de prospección. Mismo estándar que se usó con los 4
prospectos actuales. La calidad importa más que la cantidad: la meta diaria son
**máximo 4 candidatos finales**, pero puedes investigar muchos antes de filtrar.

---

## PASO 1 — Descubrir empresas

- Trabajar dentro de los **nichos del prompt maestro** (`prompts/PROMPT-MAESTRO.md`).
  Automotriz/concesionarios es prioridad, pero cualquier nicho definido es válido.
- Investigación **global**: no limitarse a un país, idioma o plataforma.
- Fuentes: Google, Google Maps, Instagram (búsqueda activa, no el feed), directorios
  empresariales, sitios oficiales, LinkedIn, TikTok, YouTube, marketplaces,
  asociaciones, competidores de una empresa ya encontrada.
- Distinguir **empresa real** de: profesional individual, cuenta personal, página de
  contenido, marketplace, negocio sin capacidad comercial, empresa duplicada.

## PASO 2 — Comprobar si ya existe en Notion

Antes de tocar nada, los **5 checks** de `ANTIDUPLICADOS.md`:
nombre → dominio → Instagram → teléfono → otros identificadores.
Abrir la vista **🔁 Anti-duplicados** y buscar la Clave de deduplicación.

## PASO 3 — Si ya existe → NO duplicar

- Coincidencia clara → abrir la ficha existente, añadir lo nuevo en **Observaciones**
  con fecha. No crear otra ficha.
- Coincidencia ambigua → anotar `⚠️ POSIBLE DUPLICADO` en la ficha existente y avisar
  a Sergio. No crear todavía.
- Si estaba `Descartado` → leer **Motivo de descarte** antes de reconsiderar.

## PASO 4 — Si es nueva → crear prospecto

Crear la ficha en `Prospectos` con, como mínimo:

- **Empresa**, **Nicho**, **País**, **Ciudad**, **Usuario Instagram**, **URL empresa**
- **Clave de deduplicación** (calcularla ya)
- **Fuente del hallazgo**
- **Descubierto por** = Palan · **Responsable** = Palan
- **Fecha de investigación** = hoy
- **Estado** = `Descubierto`

## PASO 5 — Investigar y validar

Estado → `Investigando`.

- **Instagram:** bio, link, frecuencia, contenido reciente, oferta, CTA, tipo de
  audiencia, calidad visual, señales de demanda (lanzamientos, "escríbeme DM",
  "últimos cupos", nueva sede, están contratando...).
- **Sitio web** (si tiene): diseño, UX, conversión (CTA, formularios, WhatsApp,
  reservas), mobile, contenido, prueba social, performance visible.
- **Si no tiene web:** cómo vende hoy (IG como catálogo, WhatsApp, link en bio,
  reservas...) y qué podría hacer una web que hoy no puede hacer.
- **Cruzar fuentes:** Google, Maps, directorios, redes. Registrar todo en
  **Fuentes de validación**.
- Rellenar **Problema identificado** y **Oportunidad detectada**.
- Diferenciar siempre: HECHO VERIFICADO vs INFERENCIA. No inventar precios,
  ingresos, clientes, testimonios ni datos técnicos.

## PASO 6 — Score y prioridad

Rúbrica del prompt maestro (0–100):

| Bloque | Puntos |
|---|---|
| Calidad / actividad | 15 |
| Potencial comercial | 25 |
| Problema digital | 25 |
| Oportunidad para PAGX | 25 |
| Contactabilidad | 10 |

- 90–100 excepcional · 80–89 muy bueno · 70–79 válido · 60–69 solo si hay razón
  especial · <60 descartar.
- Rellenar **Score** (número) y **Prioridad**.

## PASO 7 — Si supera los criterios → Auditado

- Score ≥ 70 y oportunidad clara y demostrable → Estado `Auditado`,
  **Auditado por** = Palan, **Fecha de auditoría** = hoy.
- Si no supera → Estado `Descartado` + **Motivo de descarte**. No se borra.

## PASO 8 — Crear el boceto (cuando corresponda)

Estado → `Boceto` · **Boceto** = `En progreso` · **Boceto por** = Palan.

- Investigar la identidad visual pública real: logo, colores, tipografías
  aproximadas, estilo fotográfico, productos/servicios, tono.
- El boceto debe sentirse como **evolución de su marca**, no una plantilla.
- Base técnica: duplicar uno de los `bocetos/0X-*.html` existentes y adaptarlo.
  Ver `COMO-ACTUALIZAR-BOCETO.md`.
- Mantener la marca de agua: *"Boceto conceptual · PAGX Studio · no es el sitio actual"*.
- Datos de demostración → etiquetados como demo. No inventar cifras, premios ni
  testimonios reales.
- Redactar el **Mensaje listo** (DM personalizado, con ≥ 2 detalles específicos
  verificados del negocio).

## PASO 9 — Vincular el boceto al prospecto

- `git add / commit / push` del nuevo HTML.
- Copiar la URL de GitHub Pages → propiedad **URL del boceto** de la ficha.
- Pegar la imagen de página completa en el cuerpo de la ficha (sección "Boceto visual").
- **Boceto** = `Listo`.

## PASO 10 — Listo para contactar

Estado → `Listo para contactar`. **Próxima acción** = fecha de revisión.
Aquí termina el trabajo del sistema: la ficha está completa y el mensaje redactado.

**El contacto se hace manual y revisado** (Sergio, o Palan con visto bueno de
Sergio). Nunca automático.

## PASO 11 — Cuando exista contacto

Al enviar el mensaje (manualmente) → Estado `Contactado`, **Contactado por** =
quien lo envió, **Fecha de contacto** = hoy. Luego **Resultado** y **Próxima
acción** para el seguimiento.

---

## Al final de la jornada

Registrar la jornada en la base **Bitácora de Prospección** (ver `BITACORA.md`):
qué investigaste, qué descartaste, qué auditaste, candidatos finales, observaciones
y aprendizaje del día.
