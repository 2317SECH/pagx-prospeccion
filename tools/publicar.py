"""Publica un prospecto: lo agrega a jornadas/<fecha>.json, regenera la seccion
fechada de index.html, agrega la tarjeta al grid, hace commit y push.
Uso: python tools/publicar.py <entrada.json> [YYYY-MM-DD]
La entrada es un objeto JSON con num, slug, nombre, ig, lugar, nicho, web,
porque, evidencia[], mensaje."""
import json, os, subprocess, sys, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
entry = json.load(open(sys.argv[1], encoding="utf-8"))
day = sys.argv[2] if len(sys.argv) > 2 else datetime.date.today().isoformat()
y, m, d = day.split("-")
path = f"jornadas/{day}.json"
data = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {"fecha": f"{d}/{m}/{y}", "persona": "Sergio", "nota": "", "prospectos": []}
data["prospectos"] = [p for p in data["prospectos"] if p["slug"] != entry["slug"]] + [entry]
json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
subprocess.run([sys.executable, "tools/jornadas_index.py"], check=True)
s = open("index.html", encoding="utf-8").read()
if f'bocetos/{entry["slug"]}.html">' not in s.split("<!--JORNADAS:END-->")[1]:
    card = f'''    <a class="card" href="bocetos/{entry['slug']}.html">
      <div class="thumb"><img src="bocetos/preview/{entry['slug']}.png" alt="Boceto {entry['nombre']}"></div>
      <div class="body">
        <div class="n">BOCETO {entry['num']} · {data['fecha']}</div>
        <h2>{entry['nombre']}</h2>
        <p>{entry['lugar']} · {entry['nicho']}.</p>
        <div class="links"><span>Ver página →</span> <a href="bocetos/preview/{entry['slug']}.png" style="color:var(--muted)">PNG completo</a></div>
      </div>
    </a>
'''
    s = s.replace("  </div>\n\n  <footer>", card + "  </div>\n\n  <footer>", 1)
    open("index.html", "w", encoding="utf-8").write(s)
subprocess.run(["git", "add", "-A", "bocetos", "index.html", "jornadas", "tools"], check=True)
subprocess.run(["git", "commit", "-q", "-m", f"Jornada {data['fecha']} ({data['persona']}): boceto {entry['num']} ({entry['nombre']})\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"], check=True)
subprocess.run(["git", "push", "-q", "origin", "main"], check=True)
print("publicado", entry["num"], entry["slug"])
