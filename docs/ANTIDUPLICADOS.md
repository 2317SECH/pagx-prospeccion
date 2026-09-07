# ANTI-DUPLICADOS

> **Regla de oro:** antes de crear cualquier ficha nueva en `Prospectos`, hay que
> demostrar que la empresa **no está ya registrada**. Si hay duda, NO se crea.

Notion no bloquea duplicados por sí solo. El bloqueo es este **procedimiento** +
la propiedad **Clave de deduplicación** + la vista **🔁 Anti-duplicados**.

---

## 1. La "Clave de deduplicación"

Cada ficha lleva una propiedad de texto **Clave de deduplicación**: el nombre de la
empresa **normalizado**. Se calcula así:

1. Todo en minúsculas.
2. Quitar tildes/acentos (`á→a`, `ñ→n`).
3. Quitar sufijos legales y de forma jurídica: `s.a.s`, `sas`, `s.a`, `sa`, `ltda`,
   `s.r.l`, `srl`, `inc`, `llc`, `group`, `grupo`, `holding`, `oficial`.
4. Quitar la ciudad o país si aparece pegada al nombre (`... pereira`, `... colombia`).
5. Quitar signos de puntuación y espacios sobrantes.

**Ejemplos:**

| Nombre encontrado | Clave de deduplicación |
|---|---|
| `Automotores Andina S.A.S.` | `automotores andina` |
| `Automotores Andina Pereira` | `automotores andina` |
| `AUTOMOTORES ANDINA` | `automotores andina` |
| `Clínica DDS · Odontología Bogotá` | `clinica dds` *(ojo, ver paso 2)* |
| `DDS Clínica Dental` | `dds clinica dental` |

> Si dos empresas distintas comparten nombre genérico (ej. "Auto 2", "Centro
> Automotores"), añade a la clave un identificador que las diferencie de verdad:
> la ciudad **solo si son negocios distintos** (`centro automotores cordoba` vs
> `centro automotores medellin`). Nunca uses la ciudad para separar sedes de la
> misma empresa.

---

## 2. Búsqueda obligatoria antes de crear (los 5 checks)

En la base `Prospectos`, buscar coincidencia por cada uno de estos, en orden:

### Check 1 — Nombre y variantes
- Buscar en Notion (`Ctrl/Cmd + P` dentro de la base, o el buscador de la vista).
- Probar: nombre exacto, nombre sin sufijos, nombre + ciudad, primera palabra sola.
- Abrir la vista **🔁 Anti-duplicados** y buscar la **Clave de deduplicación** que
  calculaste. Si ya aparece → es la misma empresa.

### Check 2 — Dominio del sitio web
- Comparar el dominio raíz, no la URL completa.
  `automotoresandina.com.co/catalogo` y `automotoresandina.com.co` → mismo dominio.
- Buscar el dominio en la propiedad **URL empresa**.

### Check 3 — Usuario de Instagram
- Buscar el `@usuario` (sin `@` y con `@`) en la propiedad **Usuario Instagram**.
- Ojo con cuentas paralelas de la misma empresa: `@marca`, `@marca.oficial`,
  `@marca.usados`, `@marca_pereira` suelen ser el **mismo negocio**.

### Check 4 — Teléfono
- Cuando la empresa tenga teléfono público, normalizarlo a formato internacional
  (`+57 3XX XXX XXXX` → `+573XXXXXXXXX`) y buscarlo en la propiedad **Teléfono**.
- Un teléfono repetido = casi seguro la misma empresa (o el mismo grupo).

### Check 5 — Otros identificadores
- Página de Facebook, dirección física, nombre del grupo empresarial, NIT/CUIT si
  es público. Un mismo grupo con varias marcas: registrar **una** ficha por marca
  comercial real, no una por cuenta social.

---

## 3. Qué hacer según el resultado

| Situación | Acción |
|---|---|
| **Coincidencia clara** (1+ checks apuntan a la misma empresa) | **NO crear ficha.** Abrir la existente. Añadir en **Observaciones** lo nuevo que encontraste (otra cuenta, otra sede, otro dato). Si estaba desactualizada, actualizarla. |
| **Coincidencia ambigua** (nombre parecido, pero podría ser otra empresa) | **NO crear todavía.** En la ficha existente, añadir en **Observaciones**: `⚠️ POSIBLE DUPLICADO con "<nombre nuevo>" — revisar`. Avisar a Sergio. Solo crear ficha nueva cuando se confirme que son empresas distintas. |
| **Sin coincidencia** | Crear ficha nueva. Rellenar **Clave de deduplicación** de inmediato. |
| **La empresa ya existe y está `Descartado`** | Abrir la ficha. Leer **Motivo de descarte**. Si las condiciones cambiaron y vale la pena reconsiderarla, cambiar el Estado a `Descubierto` o `Investigando` y anotar en **Observaciones** por qué se retoma. **Nunca** crear una segunda ficha. |
| **La empresa ya existe y está `Contactado` / `Seguimiento` / `Cerrado`** | No tocar el pipeline. Si encontraste info útil, añadirla en **Observaciones**. Avisar a Sergio si parece relevante para el seguimiento. |
| **La empresa ya tiene boceto (`Boceto: Listo`)** | No generar otro boceto. Si el existente necesita cambios, editar el HTML del repo (ver `COMO-ACTUALIZAR-BOCETO.md`), no crear uno nuevo. |

---

## 4. Sedes y cuentas múltiples

- **Una empresa con varias sedes** = **una** ficha. Las sedes se listan en
  **Observaciones** o en **Ciudad** (varias ciudades separadas por coma).
- **Una empresa con varias cuentas de Instagram** = **una** ficha. La cuenta
  principal va en **Usuario Instagram**; las demás, en **Observaciones**.
- **Un grupo empresarial con varias marcas comerciales** = una ficha **por marca**
  (si cada marca vende por separado y podría comprar por separado). Anotar el grupo
  en **Observaciones** de todas.

---

## 5. La información histórica nunca se borra

- No se elimina una ficha. Si una empresa ya no sirve → Estado `Descartado` +
  **Motivo de descarte**.
- No se sobrescribe el historial. La info nueva se **añade** a **Observaciones**
  con fecha (`[07/09/2026] ...`).
- Si te equivocaste y creaste un duplicado: **no lo borres**. Cámbiale el Estado a
  `Descartado`, pon en **Motivo de descarte**: `Duplicado de <URL de la ficha buena>`,
  y traslada a la ficha buena cualquier dato útil.

---

## 6. Herramienta opcional de verificación

`tools/check-duplicado.py` consulta la API de Notion y te dice si una empresa
(por nombre, dominio o Instagram) ya existe. Requiere `NOTION_TOKEN` en `.env`
(ver `.env.example`). **No es obligatoria** — los 5 checks manuales bastan — pero
ayuda cuando hay muchas fichas.
