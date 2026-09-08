#!/usr/bin/env python3
"""
notion_upsert.py — crea (o actualiza) una ficha de prospecto en la base Notion
"Prospectos" directamente por API, sin tocar la interfaz.

Reemplaza el flujo lento de clicar campo por campo en el navegador: con esto,
subir un prospecto completo (todas las propiedades + imagen del boceto en el
cuerpo) toma segundos.

Requiere NOTION_TOKEN con capacidades de lectura + inserción + actualización
(ver docs/NOTION.md y el token en .env — debe estar conectado a la base
Prospectos desde notion.so/my-integrations).

Uso:
    python tools/notion_upsert.py prospecto.json
    python tools/notion_upsert.py prospecto.json --page-id <id>   # actualiza en vez de crear

El JSON es un diccionario plano: {"Empresa": "...", "Nicho": "Automotriz", ...}
usando los NOMBRES EXACTOS de las propiedades de Notion (ver esquema abajo).
El tipo de cada propiedad (select, rich_text, number, date, url, phone_number,
title) se detecta automáticamente consultando el esquema de la base.

Claves especiales (no son propiedades de Notion, se procesan aparte):
    "_boceto_image_url": URL pública de la imagen del boceto — se inserta
        como bloque de imagen en el cuerpo de la página.

Ejemplo de prospecto.json:
{
  "Empresa": "Ejemplo SAS",
  "Nicho": "Automotriz",
  "País": "Chile",
  "Ciudad": "Santiago",
  "Usuario Instagram": "@ejemplo",
  "URL empresa": "https://ejemplo.cl",
  "Teléfono": "+56 9 1234 5678",
  "Contacto": "Tel. ... · email ...",
  "Fuente del hallazgo": "...",
  "Fuentes de validación": "...",
  "Problema identificado": "...",
  "Oportunidad detectada": "...",
  "Mensaje listo": "...",
  "Score": 78,
  "Seguidores": 1000,
  "Prioridad": "Alta",
  "Tiene página web": "Sí",
  "Calidad de página": "Desactualizada",
  "Canal": "Instagram",
  "Clave de deduplicación": "ejemplo",
  "Estado": "Listo para contactar",
  "Responsable": "Sergio",
  "Descubierto por": "Alan",
  "Auditado por": "Alan",
  "Boceto por": "Alan",
  "Boceto": "Listo",
  "Fecha de investigación": "2026-09-08",
  "Fecha de auditoría": "2026-09-08",
  "URL del boceto": "https://2317sech.github.io/pagx-prospeccion/bocetos/NN-slug.html",
  "_boceto_image_url": "https://2317sech.github.io/pagx-prospeccion/bocetos/preview/NN-slug.png"
}

Solo usa la librería estándar de Python (urllib). Sin dependencias.
"""
import json
import os
import sys
import urllib.request
import urllib.error

NOTION_DB = "e11a0765-546f-4d1c-b57d-e72d28520210"  # base Prospectos
NOTION_VERSION = "2022-06-28"


def cargar_env():
    ruta = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.isfile(ruta):
        for linea in open(ruta, encoding="utf-8"):
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            k, v = linea.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def notion_request(token, method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        f"https://api.notion.com{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"ERROR {e.code} en {method} {path}: {e.read().decode()}")


def get_schema(token):
    data = notion_request(token, "GET", f"/v1/databases/{NOTION_DB}")
    return {name: p["type"] for name, p in data["properties"].items()}


def build_property(ptype, value):
    if ptype == "title":
        return {"title": [{"text": {"content": str(value)}}]}
    if ptype == "rich_text":
        return {"rich_text": [{"text": {"content": str(value)}}]}
    if ptype == "select":
        return {"select": {"name": str(value)}}
    if ptype == "number":
        return {"number": value}
    if ptype == "url":
        return {"url": str(value)}
    if ptype == "phone_number":
        return {"phone_number": str(value)}
    if ptype == "date":
        return {"date": {"start": str(value)}}
    raise ValueError(f"Tipo de propiedad no soportado: {ptype}")


def build_properties_payload(schema, fields):
    props = {}
    for name, value in fields.items():
        if name.startswith("_"):
            continue
        if name not in schema:
            print(f"AVISO: propiedad '{name}' no existe en la base, se ignora.", file=sys.stderr)
            continue
        if value is None or value == "":
            continue
        props[name] = build_property(schema[name], value)
    return props


def append_image_block(token, page_id, image_url):
    body = {
        "children": [
            {
                "object": "block",
                "type": "image",
                "image": {"type": "external", "external": {"url": image_url}},
            }
        ]
    }
    notion_request(token, "PATCH", f"/v1/blocks/{page_id}/children", body)


def main():
    cargar_env()
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        sys.exit("ERROR: falta NOTION_TOKEN (variable de entorno o .env).")

    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)

    page_id = None
    if "--page-id" in args:
        i = args.index("--page-id")
        page_id = args[i + 1]
        del args[i:i + 2]

    json_path = args[0]
    with open(json_path, encoding="utf-8") as f:
        fields = json.load(f)

    schema = get_schema(token)
    properties = build_properties_payload(schema, fields)

    if page_id:
        notion_request(token, "PATCH", f"/v1/pages/{page_id}", {"properties": properties})
        print(f"Actualizada: https://notion.so/{page_id.replace('-', '')}")
    else:
        body = {"parent": {"database_id": NOTION_DB}, "properties": properties}
        result = notion_request(token, "POST", "/v1/pages", body)
        page_id = result["id"]
        print(f"Creada: {result.get('url', page_id)}")

    image_url = fields.get("_boceto_image_url")
    if image_url:
        append_image_block(token, page_id, image_url)
        print("Imagen del boceto insertada en el cuerpo de la página.")


if __name__ == "__main__":
    main()
