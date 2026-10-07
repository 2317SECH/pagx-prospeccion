"""Genera en index.html la seccion de jornadas fechadas (mas reciente arriba)
a partir de jornadas/*.json. Cada tarjeta: boceto, @IG, mensaje listo para copiar,
evidencia IG. Uso: python tools/jornadas_index.py"""
import json, glob, html, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START, END = "<!--JORNADAS:START-->", "<!--JORNADAS:END-->"
CSS = """<style id="jornadas-css">
  .jor{margin-top:40px}
  .jor h2.day{font-size:22px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding-bottom:12px;border-bottom:1px solid var(--line)}
  .jor h2.day .pill{font-size:12px;background:var(--accent);color:#fff;padding:4px 10px;border-radius:999px;letter-spacing:.04em}
  .jor h2.day small{font-size:13px;color:var(--muted);font-weight:500}
  .pros{display:grid;grid-template-columns:1fr;gap:22px;margin-top:22px}
  .pro{display:grid;grid-template-columns:340px 1fr;background:var(--panel);border:1px solid var(--line);border-radius:16px;overflow:hidden}
  .pro .thumb{background:#0f1218;border-right:1px solid var(--line)}
  .pro .thumb img{width:100%;height:100%;max-height:520px;object-fit:cover;object-position:top}
  .pro .bd{padding:18px 20px}
  .pro .n{font-size:12px;font-weight:700;letter-spacing:.08em;color:var(--muted)}
  .pro h3{font-size:20px;margin:4px 0 4px}
  .pro .meta{font-size:13px;color:var(--muted)}
  .pro .meta a{color:var(--accent);font-weight:600}
  .pro .why{font-size:13.5px;margin:10px 0 12px;color:#cfd3da}
  .pro pre{white-space:pre-wrap;font-family:inherit;font-size:13.5px;background:#0f1218;border:1px solid var(--line);border-radius:10px;padding:12px 14px;max-height:300px;overflow:auto}
  .pro .acts{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
  .pro .acts a,.pro .acts button{font:600 12.5px system-ui;padding:8px 12px;border-radius:8px;border:1px solid var(--line);background:#1b1f29;color:var(--text);cursor:pointer}
  .pro .acts .main{background:var(--accent);border-color:var(--accent)}
  .old-h{margin-top:46px;font-size:22px;padding-bottom:12px;border-bottom:1px solid var(--line)}
  @media (max-width:760px){.pro{grid-template-columns:1fr}.pro .thumb{border-right:0;border-bottom:1px solid var(--line)}.pro .thumb img{max-height:360px}}
</style>
<script>function cp(id,b){navigator.clipboard.writeText(document.getElementById(id).innerText).then(()=>{b.textContent='¡Copiado!';setTimeout(()=>b.textContent='Copiar mensaje',1500)})}</script>"""

def card(p):
    e = html.escape
    mid = "msg-" + p["slug"]
    ev = "".join(f' <a href="{e(x)}" target="_blank">Evidencia IG{"" if i==0 else " "+str(i+1)}</a>' for i, x in enumerate(p.get("evidencia", [])))
    return f"""<div class="pro">
  <a class="thumb" href="bocetos/{e(p['slug'])}.html"><img src="bocetos/preview/{e(p['slug'])}.png" alt="Boceto {e(p['nombre'])}" loading="lazy"></a>
  <div class="bd">
    <div class="n">BOCETO {p['num']} · {e(p['fecha'])}</div>
    <h3>{e(p['nombre'])}</h3>
    <div class="meta"><a href="https://instagram.com/{e(p['ig'])}" target="_blank">@{e(p['ig'])}</a> · {e(p['lugar'])} · {e(p['nicho'])} · Web: {e(p['web'])}</div>
    <p class="why">{e(p['porque'])}</p>
    <pre id="{mid}">{e(p['mensaje'])}</pre>
    <div class="acts"><button class="main" onclick="cp('{mid}',this)">Copiar mensaje</button> <a href="bocetos/preview/{e(p['slug'])}.png" download>Descargar imagen</a> <a href="bocetos/{e(p['slug'])}.html" target="_blank">Ver boceto en vivo</a>{ev}</div>
  </div>
</div>"""

def main():
    days = []
    for f in sorted(glob.glob(os.path.join(ROOT, "jornadas", "*.json")), reverse=True):
        d = json.load(open(f, encoding="utf-8"))
        for p in d["prospectos"]:
            p["fecha"] = d["fecha"]
        days.append(f"""<section class="jor">
  <h2 class="day"><span class="pill">JORNADA</span> {html.escape(d['fecha'])} <small>{html.escape(d['persona'])} · {len(d['prospectos'])} prospectos · {html.escape(d.get('nota',''))}</small></h2>
  <div class="pros">{''.join(card(p) for p in d['prospectos'])}</div>
</section>""")
    block = START + "\n" + CSS + "\n" + "\n".join(days) + '\n<h2 class="old-h">Bocetos anteriores (hasta 14/09/2026)</h2>\n' + END
    path = os.path.join(ROOT, "index.html")
    s = open(path, encoding="utf-8").read()
    if START in s:
        s = s[:s.index(START)] + block + s[s.index(END) + len(END):]
    else:
        s = s.replace("  </header>\n", "  </header>\n" + block + "\n", 1)
    open(path, "w", encoding="utf-8").write(s)
    print("ok", len(days), "jornadas")

if __name__ == "__main__":
    main()
