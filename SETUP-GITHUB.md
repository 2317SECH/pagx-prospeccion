# SETUP GITHUB — pasos que faltan (los ejecuta Sergio)

El repositorio ya está **inicializado y commiteado en local**
(`C:\Users\Sergio\Desktop\PAGX Studio\pagx-prospeccion`, rama `main`, 3 commits).

Falta crear el repo remoto, subirlo, activar GitHub Pages y dar acceso a Palan.
Estas acciones requieren tu cuenta (`gh` autenticado como `2317SECH`) y no las
puede hacer el asistente por seguridad. Cópialas y pégalas en la terminal.

> En Claude Code puedes prefijar cada línea con `!` para ejecutarla dentro de la
> sesión y que el asistente vea el resultado y continúe la verificación.

---

## 1. Crear el repo y subir

**Opción A — PÚBLICO** (recomendado: GitHub Pages gratis, URLs estables).
El repo no contiene secretos; los bocetos usan datos de demostración.

```bash
cd "C:/Users/Sergio/Desktop/PAGX Studio/pagx-prospeccion"
gh repo create pagx-prospeccion --public --source . --remote origin \
  --description "Sistema de prospeccion comercial de PAGX Studio: bocetos + flujo + CRM Notion" \
  --push
```

**Opción B — PRIVADO.** GitHub Pages en repos privados necesita plan de pago
(GitHub Pro). Si usas cuenta gratis y eliges privado, **no habrá URLs de Pages**:
los bocetos se comparten solo por el PNG o abriendo el HTML en local.

```bash
gh repo create pagx-prospeccion --private --source . --remote origin \
  --description "Sistema de prospeccion comercial de PAGX Studio" --push
```

---

## 2. Activar GitHub Pages  (solo si elegiste PÚBLICO, o PRIVADO con GitHub Pro)

```bash
echo '{"source":{"branch":"main","path":"/"}}' | \
  gh api -X POST repos/2317SECH/pagx-prospeccion/pages --input -
```

En ~1–2 min los bocetos quedan en:

- `https://2317sech.github.io/pagx-prospeccion/`
- `https://2317sech.github.io/pagx-prospeccion/bocetos/01-automotores-andina.html`
- `.../bocetos/02-infinitum-usados.html`
- `.../bocetos/03-centro-automotores.html`
- `.../bocetos/04-dds-clinica-dental.html`

(Esas URLs ya están escritas en la propiedad **URL del boceto** de cada ficha de
Notion. Si el repo se llama distinto, hay que actualizarlas.)

---

## 3. Dar acceso a Palan (Alan)

Usuario de GitHub: **`ptala611-oss`** (verificado, existe).

```bash
gh api -X PUT repos/2317SECH/pagx-prospeccion/collaborators/ptala611-oss \
  -f permission=admin
```

`permission` puede ser: `pull` (solo lectura), `push` (leer + subir),
`maintain`, `admin` (todo). Sergio pidió acceso completo → `admin`.
Palan recibe un email/invitación que debe aceptar.

---

## 4. Verificar

```bash
gh repo view 2317SECH/pagx-prospeccion --web        # abre el repo
gh api repos/2317SECH/pagx-prospeccion/pages -q .html_url   # URL de Pages
gh api repos/2317SECH/pagx-prospeccion/collaborators -q '.[].login'  # colaboradores
```

Abrir una URL de boceto en el navegador y comprobar que se ve completa y sin errores.

---

## Notas

- Notion: Palan ya tiene acceso (Sergio lo compartió). Conviene verificar que el
  acceso incluya la base **Prospectos** y la base **Bitácora de Prospección**
  (ambas dentro de *Workspace Comercial — PAGX Studio*), con permiso de edición.
- Si más adelante se añade algo sensible al repo → pasarlo a privado:
  `gh repo edit 2317SECH/pagx-prospeccion --visibility private --accept-visibility-change-consequences`
