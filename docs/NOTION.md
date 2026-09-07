# NOTION — el CRM de prospección

Base única: **Prospectos** (dentro de *Workspace Comercial — PAGX Studio*).
No se crea otra base. La existente se amplió.

---

## 1. Propiedades de `Prospectos`

### Identificación
| Propiedad | Tipo | Notas |
|---|---|---|
| **Empresa** | Título | Nombre comercial real (no la razón social larga). |
| **Nicho** | Select | *(antes se llamaba "Industria")* Automotriz, Salud y estética, Inmobiliaria, Audiovisual, Educación, Restaurantes, Barberías, Gimnasios, Clínicas, Abogados, Otros. Se pueden añadir más. |
| **País** | Select | Colombia, Argentina, México, España, EE. UU., Chile, Perú, Ecuador, Brasil, Otro. |
| **Ciudad** | Texto | Ciudad(es). Varias sedes → separadas por coma. |
| **Usuario Instagram** | Texto | `@usuario`. La cuenta principal. Otras cuentas → en Observaciones. |
| **URL empresa** | URL | *(este es el "Sitio web")* Dominio del sitio, si existe. |
| **Teléfono** | Teléfono | Formato internacional `+57...`. Se usa para anti-duplicados. |
| **Contacto** | Texto | Todos los canales de contacto público verificables (WhatsApp, email, formulario, IG). |
| **Canal** | Select | Canal por el que se va a abordar (normalmente Instagram DM). |

### Investigación
| Propiedad | Tipo | Notas |
|---|---|---|
| **Fuente del hallazgo** | Texto | *(este es el "Fuente")* Cómo se descubrió (búsqueda X, competidor de Y...). |
| **Fuentes de validación** | Texto | Links / plataformas usadas para verificar que la empresa es real. |
| **Problema identificado** | Texto | Qué está mal en su presencia digital y por qué importa. |
| **Oportunidad detectada** | Texto | Qué propondría PAGX y por qué encaja. |
| **Score** | Número | 0–100, según la rúbrica del prompt maestro. |
| **Prioridad** | Select | Alta / Media / Baja. |
| **Seguidores** | Número | Dato secundario. |
| **Tiene página web** | Select | Sí / No. |
| **Calidad de página** | Select | Sin página / Desactualizada / Aceptable / Muy buena. |

### Boceto
| Propiedad | Tipo | Notas |
|---|---|---|
| **Boceto** | Select | Sin boceto / En progreso / Listo. |
| **URL del boceto** | URL | Link de GitHub Pages a la maqueta. |
| **Mensaje listo** | Texto | El DM que Sergio copia y envía. Nunca se envía automáticamente. |
| *(imagen del boceto)* | — | Se pega en el cuerpo de la página del prospecto, sección "Boceto visual". |

### Pipeline y trazabilidad
| Propiedad | Tipo | Notas |
|---|---|---|
| **Estado** | Select | Ver §2. |
| **Responsable** | Select | Sergio / Palan / Sin asignar. Quién lleva el prospecto ahora. |
| **Descubierto por** | Select | Sergio / Palan. |
| **Auditado por** | Select | Sergio / Palan. |
| **Boceto por** | Select | Sergio / Palan. |
| **Contactado por** | Select | Sergio / Palan. |
| **Fecha de investigación** | Fecha | Cuándo se investigó. |
| **Fecha de auditoría** | Fecha | Cuándo se auditó. |
| **Fecha de contacto** | Fecha | Cuándo se envió el primer mensaje (real). |
| **Próxima acción** | Fecha | Cuándo toca lo siguiente (seguimiento, decisión, etc.). |
| **Resultado** | Texto | Qué pasó tras el contacto. |
| **Observaciones** | Texto | *(antes "Notas rápidas")* Notas libres, siempre con fecha: `[07/09/2026] ...`. |
| **Motivo de descarte** | Texto | Obligatorio si Estado = Descartado. |
| **Clave de deduplicación** | Texto | Nombre normalizado. Ver `ANTIDUPLICADOS.md`. |
| **Bitácora** | Relación | Jornadas de la base `Bitácora de Prospección` en las que se trabajó este prospecto. |

### Mapeo de nombres antiguos → nuevos
| Antes | Ahora |
|---|---|
| Industria | **Nicho** |
| Notas rápidas | **Observaciones** |
| (Score iba dentro de "Notas rápidas" como texto) | **Score** (número propio) |

Las propiedades heredadas **Motivo de prioridad**, **Gancho de personalización** y
**Kit usado** siguen existiendo y no se tocan.

---

## 2. Estados del pipeline

Flujo canónico (en este orden):

```
Descubierto → Investigando → Auditado → Boceto → Listo para contactar
   → Contactado → Seguimiento → Cerrado / No interesado / Descartado
```

| Estado | Significa | Quién lo pone |
|---|---|---|
| **Descubierto** | Empresa encontrada, ficha creada, aún sin investigar a fondo. | quien descubre |
| **Investigando** | Se está validando y auditando (IG + web + fuentes). | quien investiga |
| **Auditado** | Investigación completa, score asignado, supera criterios. | quien audita |
| **Boceto** | Se está construyendo la maqueta visual. | quien hace boceto |
| **Listo para contactar** | Boceto `Listo` + Mensaje listo. Falta que Sergio envíe. | quien termina el boceto |
| **Contactado** | Sergio **ya envió** el mensaje. Se fija **Fecha de contacto**. | Sergio |
| **Seguimiento** | Sin respuesta o conversación en curso, toca insistir. | Sergio |
| **Interesado** / **Reunión agendada** / **Cerrado** | Avance comercial. | Sergio |
| **No interesado** | Dijo que no. | Sergio |
| **Descartado** | No encaja / no vale la pena. Requiere **Motivo de descarte**. | quien decide |

Estados heredados que siguen válidos: `Por auditar`, `Seguimiento 1/2/final`,
`Sin respuesta`. No usarlos para prospectos nuevos; el canónico es el de arriba.

> **Nunca** poner `Contactado` si el mensaje no se ha enviado de verdad.

---

## 3. Vistas

| Vista | Qué muestra |
|---|---|
| **🎯 PROSPECCIÓN — Hoy** | Tablero por Estado. Todo lo que necesita acción (oculta Cerrado / No interesado / Descartado). Es la vista de arranque de la jornada. |
| **👥 Por responsable** | Tablero por Responsable. Qué lleva cada quién. |
| **🔁 Anti-duplicados** | Tabla ordenada por Clave de deduplicación (los duplicados quedan pegados). |
| **🗑️ Descartados / histórico** | Empresas descartadas + su motivo. Leer antes de reconsiderar una empresa. |
| **Pipeline** | Tablero por Estado, todo el embudo. |

---

## 4. La ficha de cada prospecto (cuerpo de la página)

Estructura recomendada dentro de la página (además de las propiedades):

1. **Boceto visual** — la imagen de página completa (si tiene boceto).
2. **Ficha** — identificación, cómo vende hoy.
3. **Auditoría** — Instagram + web.
4. **Problema principal** y secundarios.
5. **Oportunidad para PAGX** + tipo de proyecto.
6. **Puntuación** — desglose de la rúbrica.
7. **Boceto** — hero, secciones, dirección visual, elemento diferencial.
8. **Mensaje listo** — el DM, en bloque de código para copiar.
9. **Confianza y fuentes**.

Los 4 prospectos actuales (Automotores Andina, Infinitum Usados, Centro Automotores,
DDS Clínica Dental) sirven de plantilla.

---

## 5. Bitácora de Prospección (base aparte)

Un registro **por jornada**. Propiedades: Jornada (título), Fecha, Responsable,
Empresas investigadas / descartadas / auditadas (números), Candidatos finales,
Contactos realizados, Prospectos trabajados (relación), Observaciones, Aprendizajes
del día. Ver `BITACORA.md`.
