"""Build the installable app from app.html.

app.html is the page body (the same file that is published as the Claude artifact).
This script wraps it in a full HTML document with the PWA head, stamps the version
into sw.js, and draws the icons.

    python3 build.py
"""
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
APP = (ROOT / "app.html").read_text(encoding="utf-8")

build = re.search(r"const APP_BUILD=(\d+);", APP).group(1)
major = re.search(r"const APP_MAJOR=(\d+);", APP).group(1)

HEAD = """<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#F2F1EF">
<meta name="description" content="متابعة مخزون قطع الغيار: خطوط الإنتاج والمعدات، سحب وإيداع بسجل كامل، وتنبيه عند الحد الأدنى.">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="المخزن">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<style>:root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}html{scroll-padding-top:env(safe-area-inset-top,0px)}body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif}img{max-width:100%}[hidden]:not([hidden=until-found i]){display:none!important}</style>
</head>
<body>
"""

(ROOT / "index.html").write_text(HEAD + APP + "\n</body>\n</html>\n", encoding="utf-8")

sw = (ROOT / "sw.js").read_text(encoding="utf-8")
sw = re.sub(r"const CACHE = '[^']*';", f"const CACHE = 'spare-parts-v{major}.{build}';", sw)
(ROOT / "sw.js").write_text(sw, encoding="utf-8")

# ---- icons: safety-orange bearing on steel graphite ----
BG = (35, 40, 46)
FG = (255, 107, 26)
INK = (241, 243, 245)


def draw_icon(size, scale, rounded):
    s = size * 4  # supersample for smooth edges
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if rounded:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.22), fill=BG)
    else:
        d.rectangle([0, 0, s, s], fill=BG)
    c = s / 2
    r_out = s * 0.34 * scale
    w = s * 0.055 * scale
    d.ellipse([c - r_out, c - r_out, c + r_out, c + r_out], outline=FG, width=int(w))
    r_in = s * 0.14 * scale
    d.ellipse([c - r_in, c - r_in, c + r_in, c + r_in], outline=INK, width=int(w * 0.85))
    r_ball_orbit = (r_out + r_in) / 2 + w * 0.05
    r_ball = s * 0.052 * scale
    for i in range(8):
        a = math.pi / 2 + i * math.pi / 4
        x, y = c + r_ball_orbit * math.cos(a), c - r_ball_orbit * math.sin(a)
        d.ellipse([x - r_ball, y - r_ball, x + r_ball, y + r_ball], fill=FG)
    return im.resize((size, size), Image.LANCZOS)


draw_icon(192, 1.0, True).save(ROOT / "icon-192.png")
draw_icon(512, 1.0, True).save(ROOT / "icon-512.png")
draw_icon(512, 0.78, False).save(ROOT / "icon-maskable-512.png")
draw_icon(180, 1.0, False).convert("RGB").save(ROOT / "apple-touch-icon.png")

print(f"built v{major}.{build}")
