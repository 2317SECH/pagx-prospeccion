#!/usr/bin/env python3
"""
check-duplicado.py  —  verificador OPCIONAL de duplicados contra la base Prospectos de Notion.

NO es obligatorio. Los 5 checks manuales de docs/ANTIDUPLICADOS.md bastan.
Esto solo agiliza la comprobación cuando hay muchas fichas.

Uso:
    export NOTION_TOKEN=secret_xxx           # o ponerlo en .env (ver .env.example)
    python tools/check-duplicado.py "Automotores Andina Pereira"
    python tools/check-duplicado.py --ig @automotoresandina
    python tools/check-duplicado.py --web automotoresandina.com.co
    python tools/check-duplicado.py --tel "+57 314 881 6462"

Requisitos:
    - Una integración interna de Notion con acceso de LECTURA a la base Prospectos.
      Crear en https://www.notion.so/my-integrations  y conectarla a la base.
    - El token NUNCA se sube al repo. Va en la variable de entorno NOTION_TOKEN
      o en el archivo .env (que está en .gitignore).

Solo usa la librería estándar de Python (urllib). Sin dependencias.
"""
import json
import os
import re
import sys
import unicodedata
import urllib.request

NOTION_DB = "e11a0765-546f-4d1c-b57d-e72d28520210"  # base Prospectos
NOTION_VERSION = "2022-06-28"

SUFIJOS = [
    "s a s", "sas", "s a", "s.a", "sa", "ltda", "s r l", "srl", "inc", "llc",
    "group", "grupo", "holding", "oficial", "co", "com",
]


def cargar_env():
    """Lee .env (KEY=VALUE por línea) si existe, sin sobreescribir el entorno real."""
    ruta = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.isfile(ruta):
        for linea in open(ruta, encoding="utf-8"):
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            k, v = linea.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def normalizar(nombre: str) -> str:
    s = nombre.lower().strip()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    for suf in SUFIJOS:
        s = re.sub(rf"\b{re.escape(suf)}\b", "", s)
    return re.sub(r"\s+", " ", s).strip()


def dominio_raiz(url: str) -> str:
    if not url:
        return ""
    u = url.lower().strip()
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    return u.split("/")[0].strip()


def solo_digitos(tel: str) -> str:
    return re.sub(r"\D", "", tel or "")


def notion_query(token: str):
    """Devuelve todas las páginas (fichas) de la base."""
    resultados = []
    cursor = None
    while True:
        cuerpo = {"page_size": 100}
        if cursor:
            cuerpo["start_cursor"] = cursor
        req = urllib.request.Request(
            f"https://api.notion.com/v1/databases/{NOTION_DB}/query",
            data=json.dumps(cuerpo).encode(),
            headers={
                "Authorization": f"Bearer {token}",
                "Notion-Version": NOTION_VERSION,
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req) as r:
            data = json.load(r)
        resultados.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return resultados


def prop_text(page, nombre):
    p = page.get("properties", {}).get(nombre)
    if not p:
        return ""
    t = p.get("type")
    if t in ("rich_text", "title"):
        return "".join(x.get("plain_text", "") for x in p.get(t, []))
    if t == "url":
        return p.get("url") or ""
    if t == "phone_number":
        return p.get("phone_number") or ""
    if t == "select":
        return (p.get("select") or {}).get("name", "")
    return ""


def main():
    cargar_env()
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        sys.exit("ERROR: falta NOTION_TOKEN (variable de entorno o .env). Ver .env.example")

    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)

    modo, valor = "nombre", None
    if args[0] in ("--ig", "--web", "--tel"):
        modo = {"--ig": "instagram", "--web": "web", "--tel": "telefono"}[args[0]]
        valor = " ".join(args[1:])
    else:
        valor = " ".join(args)

    print(f"Buscando coincidencias por {modo}: {valor!r}\n")

    try:
        paginas = notion_query(token)
    except Exception as e:
        sys.exit(f"ERROR consultando Notion: {e}\n"
                 f"Revisa que el token sea válido y que la integración esté conectada a la base.")

    clave_busqueda = normalizar(valor)
    dom_busqueda = dominio_raiz(valor)
    ig_busqueda = valor.lower().lstrip("@").strip()
    tel_busqueda = solo_digitos(valor)

    hits = []
    for pg in paginas:
        empresa = prop_text(pg, "Empresa")
        clave = normalizar(prop_text(pg, "Clave de deduplicación") or empresa)
        ig = prop_text(pg, "Usuario Instagram").lower().lstrip("@").strip()
        web = dominio_raiz(prop_text(pg, "URL empresa"))
        tel = solo_digitos(prop_text(pg, "Teléfono"))
        estado = prop_text(pg, "Estado")
        url = pg.get("url", "")

        motivo = None
        if modo == "nombre" and clave_busqueda and (clave_busqueda in clave or clave in clave_busqueda):
            motivo = f"clave de deduplicación ~ {clave!r}"
        elif modo == "instagram" and ig and ig_busqueda and (ig_busqueda in ig or ig in ig_busqueda):
            motivo = f"Instagram @{ig}"
        elif modo == "web" and web and dom_busqueda and web == dom_busqueda:
            motivo = f"dominio {web}"
        elif modo == "telefono" and tel and tel_busqueda and tel[-9:] == tel_busqueda[-9:]:
            motivo = f"teléfono …{tel[-9:]}"
        # cruces siempre útiles
        elif clave_busqueda and clave and clave_busqueda == clave:
            motivo = "mismo nombre normalizado"

        if motivo:
            hits.append((empresa, estado, motivo, url))

    if not hits:
        print("✅ Sin coincidencias. Se puede crear la ficha (rellena la Clave de deduplicación).")
    else:
        print("⚠️  POSIBLES DUPLICADOS — NO crear ficha nueva sin revisar:\n")
        for empresa, estado, motivo, url in hits:
            print(f"  • {empresa}  [{estado}]")
            print(f"    coincide por: {motivo}")
            print(f"    {url}\n")
        print("Ver docs/ANTIDUPLICADOS.md → sección 3 para decidir qué hacer.")


if __name__ == "__main__":
    main()
