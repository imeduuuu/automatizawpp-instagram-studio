#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de generacion de posts de Instagram para automatizawpp.
Genera 6 posts 1080x1080 en HTML usando la identidad premium REAL
(paleta y tipografia extraidas de automatizawpp-premium/assets/styles.css)
y los exporta a PNG con Chrome headless.

Este mismo motor alimenta el generador de posts del dashboard:
el array CONTENIDO es el "feed" editable; cambiar el texto = nuevo post.
"""
import os, html

BASE = os.path.dirname(os.path.abspath(__file__))
POSTS = os.path.join(BASE, "posts")
EXPORT = os.path.join(BASE, "export")

# --- Identidad de marca (igual que assets/styles.css del sitio premium) ---
BRAND = {
    "green":      "#25D366",
    "green_deep": "#0E6B3C",
    "bg":         "#0A0F0D",
    "bg2":        "#0F1614",
    "surface":    "#141C19",
    "text":       "#E8F1ED",
    "muted":      "#8FA39B",
    "gold":       "#D4B36A",
    "line":       "rgba(255,255,255,.08)",
}

# Icono de burbuja de chat (WhatsApp-style) en SVG inline
BUBBLE_SVG = """<svg width="34" height="34" viewBox="0 0 24 24" fill="none">
<path d="M12 2C6.5 2 2 6 2 11c0 2 .7 3.8 2 5.3L3 22l6-1.5c1 .3 2 .5 3 .5 5.5 0 10-4 10-9S17.5 2 12 2z"
fill="url(#g)"/><defs><linearGradient id="g" x1="2" y1="2" x2="22" y2="22">
<stop stop-color="#25D366"/><stop offset="1" stop-color="#0E6B3C"/></linearGradient></defs></svg>"""

# --- Plantilla de un post 1080x1080 ---
def render(label, headline_html, sub="", cta="", stat="", motif_bubble=False):
    motif = ""
    if motif_bubble:
        motif = """<svg class="motif" viewBox="0 0 24 24"><path d="M12 2C6.5 2 2 6 2 11c0 2 .7 3.8 2 5.3L3 22l6-1.5c1 .3 2 .5 3 .5 5.5 0 10-4 10-9S17.5 2 12 2z" stroke="#25D366" stroke-width="0.4" fill="none"/></svg>"""
    stat_html = f'<div class="stat">{stat}</div>' if stat else ""
    sub_html = f'<p class="sub">{sub}</p>' if sub else ""
    cta_html = f'<div class="cta">{cta}</div>' if cta else ""
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@500&family=Inter:wght@400;500&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1080px;overflow:hidden}}
body{{
  background:{BRAND['bg']};
  font-family:'Inter',sans-serif;color:{BRAND['text']};
  position:relative;
}}
body::before{{
  content:"";position:absolute;inset:0;
  background:
    radial-gradient(620px 520px at 88% -8%, rgba(37,211,102,.18), transparent 60%),
    radial-gradient(560px 460px at -8% 108%, rgba(212,179,106,.10), transparent 60%),
    linear-gradient(180deg,{BRAND['bg']} 0%, {BRAND['bg2']} 100%);
}}
.frame{{position:relative;width:100%;height:100%;padding:96px;display:flex;flex-direction:column;justify-content:space-between;z-index:2}}
.top{{display:flex;align-items:center;gap:16px}}
.label{{font-family:'JetBrains Mono',monospace;font-size:24px;letter-spacing:.32em;color:{BRAND['muted']};text-transform:uppercase}}
.top .dot{{width:11px;height:11px;border-radius:50%;background:{BRAND['green']};box-shadow:0 0 16px {BRAND['green']}}}
.hairline{{height:1px;width:120px;background:linear-gradient(90deg,{BRAND['gold']},transparent);margin-top:18px}}
.hero{{flex:1;display:flex;flex-direction:column;justify-content:center;position:relative}}
h1{{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:92px;line-height:1.04;letter-spacing:-.02em;max-width:880px}}
h1 em{{font-style:normal;color:{BRAND['green']}}}
.sub{{margin-top:30px;font-size:32px;line-height:1.45;color:{BRAND['muted']};max-width:760px}}
.stat{{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:300px;line-height:.9;color:{BRAND['green']};letter-spacing:-.04em;text-shadow:0 0 60px rgba(37,211,102,.35);margin-bottom:10px}}
.cta{{margin-top:46px;display:inline-flex;align-items:center;gap:14px;align-self:flex-start;
  background:linear-gradient(135deg,{BRAND['green']},{BRAND['green_deep']});
  color:#04130b;font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:34px;
  padding:26px 46px;border-radius:18px;box-shadow:0 16px 50px rgba(37,211,102,.30)}}
.motif{{position:absolute;right:-120px;top:50%;transform:translateY(-50%);width:760px;height:760px;opacity:.5}}
.brand{{display:flex;align-items:center;gap:16px}}
.brand .wm{{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:34px;letter-spacing:-.01em}}
.brand .wm b{{color:{BRAND['green']}}}
.brand .tag{{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:22px;color:{BRAND['muted']}}}
</style></head>
<body><div class="frame">
  <div>
    <div class="top"><span class="dot"></span><span class="label">{label}</span></div>
    <div class="hairline"></div>
  </div>
  <div class="hero">{motif}{stat_html}<h1>{headline_html}</h1>{sub_html}{cta_html}</div>
  <div class="brand">{BUBBLE_SVG}<span class="wm">automatiza<b>wpp</b></span><span class="tag">@automatizawpp</span></div>
</div></body></html>"""

# --- El FEED: 6 posts (orden de cuadricula) ---
CONTENIDO = [
    ("post1", dict(label="Automatización con IA",
        headline_html="Tu WhatsApp no debería <em>dormir</em>.",
        sub="IA que responde, vende y atiende mientras tú descansas.",
        motif_bubble=True)),
    ("post2", dict(label="El problema",
        headline_html="Cada mensaje sin responder es un <em>cliente perdido</em>.",
        sub="El 70% de la gente compra a quien responde primero.")),
    ("post3", dict(label="Más ventas",
        headline_html="Convierte chats en <em>ventas automáticas</em>.",
        sub="De la primera pregunta al cierre, sin intervención manual.")),
    ("post4", dict(label="Disponible 24/7",
        headline_html="Atención al cliente que <em>nunca para</em>.",
        sub="Festivos, madrugadas y fines de semana. Siempre activo.")),
    ("post5", dict(label="El dato",
        headline_html="de los WhatsApp se leen en los primeros <em>3 minutos</em>.",
        stat="90%")),
    ("post6", dict(label="Empieza ya",
        headline_html="Empieza <em>gratis</em> hoy.",
        sub="Configúralo en minutos. Sin tarjeta, sin compromiso.",
        cta="Prueba gratis &rarr;")),
]

if __name__ == "__main__":
    for name, kw in CONTENIDO:
        path = os.path.join(POSTS, f"{name}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(**kw))
        print("HTML:", path)
    print("OK - 6 posts HTML generados")
