"""
Gera o Manual de Programação de Tanques em HTML e abre no navegador.
Para exportar como PDF: Ctrl+P no navegador → Salvar como PDF.
"""
import os
import webbrowser
import subprocess
import sys

# Tenta instalar 'markdown' se não estiver disponível
try:
    import markdown
except ImportError:
    print("Instalando biblioteca markdown...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown"])
    import markdown

# ── Caminho do arquivo de origem ──────────────────────────────────────────────
MANUAL_MD = r"C:\Users\PC_OXE\.gemini\antigravity\brain\b4dcb79e-db51-4577-a882-7f653c4ede60\artifacts\MANUAL_PROGRAMACAO_TANQUES.md"
OUTPUT_HTML = os.path.join(os.path.dirname(__file__), "MANUAL_TANQUES.html")

# ── CSS embutido ───────────────────────────────────────────────────────────────
CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    line-height: 1.65;
    color: #1a1a2e;
    max-width: 860px;
    margin: 0 auto;
    padding: 40px 50px;
    background: #fff;
}
h1 {
    font-size: 26px;
    color: #1e3a5f;
    border-bottom: 3px solid #3a7bd5;
    padding-bottom: 10px;
    margin: 0 0 24px 0;
}
h2 {
    font-size: 18px;
    color: #1e3a5f;
    border-left: 5px solid #3a7bd5;
    padding-left: 10px;
    margin: 32px 0 14px 0;
    page-break-after: avoid;
}
h3 {
    font-size: 14px;
    color: #2c5282;
    margin: 20px 0 8px 0;
    page-break-after: avoid;
}
h4 { font-size: 13px; color: #444; margin: 14px 0 6px 0; }

p { margin: 8px 0 10px 0; }

a { color: #3a7bd5; }

blockquote {
    border-left: 4px solid #3a7bd5;
    background: #eef4ff;
    margin: 12px 0;
    padding: 10px 16px;
    border-radius: 0 6px 6px 0;
    color: #2d4a7a;
    font-size: 12.5px;
}

code {
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    background: #f0f4f8;
    padding: 1px 5px;
    border-radius: 3px;
    color: #c7254e;
}

pre {
    background: #1a1a2e;
    color: #e0e8f5;
    padding: 16px 20px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 12px 0;
    page-break-inside: avoid;
}
pre code {
    background: none;
    color: #a8d4ff;
    padding: 0;
    font-size: 12px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 12.5px;
    page-break-inside: avoid;
}
th {
    background: #1e3a5f;
    color: #fff;
    padding: 9px 12px;
    text-align: left;
    font-weight: 600;
}
td {
    padding: 8px 12px;
    border-bottom: 1px solid #dce6f5;
}
tr:nth-child(even) td { background: #f5f8ff; }

ul, ol {
    padding-left: 24px;
    margin: 8px 0 10px 0;
}
li { margin: 4px 0; }

hr {
    border: none;
    border-top: 2px solid #dce6f5;
    margin: 28px 0;
}

.cover {
    text-align: center;
    padding: 60px 0 50px 0;
    border-bottom: 3px solid #3a7bd5;
    margin-bottom: 36px;
}
.cover h1 {
    font-size: 34px;
    border: none;
    color: #1e3a5f;
}
.cover .subtitle { font-size: 15px; color: #555; margin-top: 8px; }
.cover .version  { font-size: 12px; color: #999; margin-top: 6px; }

.toc-box {
    background: #f5f8ff;
    border: 1px solid #c5d8f5;
    border-radius: 8px;
    padding: 18px 24px;
    margin: 0 0 28px 0;
    page-break-inside: avoid;
}
.toc-box h2 { border: none; margin: 0 0 10px 0; font-size: 15px; color: #1e3a5f; }
.toc-box ol { margin: 0; }
.toc-box li { margin: 3px 0; font-size: 13px; }

@media print {
    body { padding: 20px 30px; font-size: 12px; }
    h2 { page-break-before: auto; }
    pre { white-space: pre-wrap; word-break: break-word; }
}
"""

# ── Lê o Markdown ─────────────────────────────────────────────────────────────
with open(MANUAL_MD, encoding="utf-8") as f:
    md_text = f.read()

# Remove o índice manual (será gerado pela capa)
# Converte para HTML
md_ext = ["tables", "fenced_code", "nl2br", "sane_lists"]
body_html = markdown.markdown(md_text, extensions=md_ext)

# ── Capa personalizada ────────────────────────────────────────────────────────
cover_html = """
<div class="cover">
    <h1>🎮 ArenaCode</h1>
    <div class="subtitle">Manual de Programação de Tanques</div>
    <div class="version">Versão 2025 · Batalha de Tanques Programáveis</div>
</div>
"""

# ── HTML final ────────────────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ArenaCode — Manual de Programação de Tanques</title>
    <style>{CSS}</style>
</head>
<body>
{cover_html}
{body_html}
<hr>
<p style="text-align:center;color:#aaa;font-size:11px;margin-top:20px;">
    ArenaCode · Manual gerado automaticamente · 2025
</p>
</body>
</html>
"""

# ── Salva e abre no navegador ─────────────────────────────────────────────────
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"HTML gerado em: {OUTPUT_HTML}")
print()
print("O arquivo foi aberto no seu navegador.")
print("Para salvar como PDF:")
print("  1. Pressione Ctrl+P (Imprimir)")
print("  2. Em 'Destino' selecione 'Salvar como PDF'")
print("  3. Clique em 'Salvar'")

webbrowser.open(f"file:///{OUTPUT_HTML.replace(chr(92), '/')}")
