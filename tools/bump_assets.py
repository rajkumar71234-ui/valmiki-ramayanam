"""Give style.css / app.js a new ?v= number in index.html so browsers load the fresh files.
Run after changing anything in assets/:  python3 tools/bump_assets.py
"""
import hashlib, re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
idx = root / "index.html"
html = idx.read_text(encoding="utf-8")
for name in ("style.css", "app.js"):
    digest = hashlib.sha1((root / "assets" / name).read_bytes()).hexdigest()[:8]
    html = re.sub(r'assets/' + re.escape(name) + r'(\?v=[0-9a-f]+)?"', f'assets/{name}?v={digest}"', html)
idx.write_text(html, encoding="utf-8")
print("index.html now points to:", re.findall(r'assets/(?:style\.css|app\.js)\?v=[0-9a-f]+', html))
