#!/usr/bin/env python3
"""Bauplan_Pizzaofen.md (aus build_v5.py) -> Bauplan_Pizzaofen.html (eigenstaendig, Zeichnungen eingebettet)."""
import subprocess, base64, os, re
H = os.path.dirname(os.path.abspath(__file__)); Z = os.path.join(H, '..', 'zeichnungen')
md = open(os.path.join(H, 'Bauplan_Pizzaofen.md')).read()
md = re.sub(r'^---\n.*?\n---\n', '', md, count=1, flags=re.S)
body = subprocess.run(['pandoc', '-f', 'gfm+pipe_tables', '-t', 'html5', '--wrap=none'], input=md, capture_output=True, text=True, check=True).stdout
def svg_uri(m):
    name = os.path.splitext(os.path.basename(m.group(1)))[0]
    data = base64.b64encode(open(os.path.join(Z, name + '.svg'), 'rb').read()).decode()
    return f'<figure><img src="data:image/svg+xml;base64,{data}" alt="{m.group(2)}"><figcaption>{m.group(2)}</figcaption></figure>'
body = re.sub(r'<img src="\.\./zeichnungen/([^"]+)" alt="([^"]*)"\s*/?>', svg_uri, body)
body = re.sub(r'<p>(<figure>.*?</figure>)</p>', r'\1', body, flags=re.S)
body = body.replace('<table>', '<div class="tw"><table>').replace('</table>', '</table></div>')
body = re.sub(r'<h1[^>]*>.*?</h1>', '', body, count=1, flags=re.S)
body = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', body)
css = '''
/* Layout: technisches Dossier – schmale Lesespalte, breite Tabellen scrollen in eigener Box, Zeichnungen auf weissem Planpapier */
:root{--bg:#f2f3f1;--paper:#ffffff;--ink:#1c2125;--muted:#5b646b;--line:#d6d9d5;--accent:#a9542a;--blue:#1c4f8a;--quote:#eef1f4;
--fd:"Barlow Semi Condensed","Arial Narrow",Arial,sans-serif;--fb:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--fm:"IBM Plex Mono",ui-monospace,Menlo,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#14181b;--paper:#1c2125;--ink:#e6e8e5;--muted:#9aa3a9;--line:#323a40;--accent:#e08a57;--blue:#86b6ea;--quote:#20282f;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#14181b;--paper:#1c2125;--ink:#e6e8e5;--muted:#9aa3a9;--line:#323a40;--accent:#e08a57;--blue:#86b6ea;--quote:#20282f;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font-family:var(--fb);font-size:15.5px;line-height:1.55}
.wrap{max-width:980px;margin:0 auto;padding-inline:16px;padding-block:28px 64px}
.doc{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding-inline:clamp(16px,4vw,48px);padding-block:clamp(20px,4vw,44px)}
.doc>*{max-width:72ch}.doc>.tw,.doc>figure,.doc>blockquote{max-width:none}
.kicker{font-family:var(--fm);font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin:0 0 .4rem}
.title{font-family:var(--fd);font-weight:700;font-size:clamp(2rem,6vw,3.1rem);line-height:1.02;margin:0 0 .5rem;text-wrap:balance}
h2,h3{font-family:var(--fd);font-weight:700;text-wrap:balance;line-height:1.15}
h2{font-size:1.75rem;margin:2.6rem 0 .6rem;padding-top:1rem;border-top:2px solid var(--ink)}
h3{font-size:1.25rem;margin:1.8rem 0 .4rem;color:var(--ink)}
a{color:var(--blue);overflow-wrap:anywhere}
hr{border:0;border-top:1px solid var(--line);margin:2rem 0}
blockquote{margin:1.2rem 0;padding:.9rem 1.1rem;background:var(--quote);border-left:4px solid var(--accent);border-radius:6px}
blockquote p{margin:.3rem 0}
code{font-family:var(--fm);font-size:.88em;background:var(--quote);padding:.05em .3em;border-radius:4px}
.tw{overflow-x:auto;margin:1rem 0;border:1px solid var(--line);border-radius:8px}
table{border-collapse:collapse;width:100%;font-size:.86rem;font-variant-numeric:tabular-nums}
th,td{padding:.5rem .6rem;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}
th{font-family:var(--fd);font-size:.85rem;letter-spacing:.03em;text-transform:uppercase;background:var(--quote);position:sticky;top:0}
tr:last-child td{border-bottom:0}
figure{margin:1.4rem 0;background:#ffffff;border:1px solid var(--line);border-radius:8px;padding:10px;overflow-x:auto}
figure img{display:block;width:100%;min-width:560px;height:auto}
figcaption{font-size:.8rem;color:#4b545a;margin-top:6px;font-family:var(--fm)}
ol,ul{padding-left:1.3rem}li{margin:.2rem 0}
strong{font-weight:600}
@media print{body{background:#fff;color:#000;font-size:11.5px}.wrap{max-width:none;padding:0}.doc{border:0;padding:0}.doc>*{max-width:none}
 h2{break-before:page;border-top:0}h2:first-of-type{break-before:auto}figure{break-inside:avoid}figure img{min-width:0}table{font-size:9px}.tw{overflow:visible;border:0}th{position:static}a{color:#000}}
'''
page = f'''<title>Pizzaofen Würenlos Bauplan</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{css}</style>
<main class="wrap"><article class="doc">
<p class="kicker">Vertiefungsarbeit · Bauanleitung mit Werkzeichnungen · Fassung 5 · 19.10.2026</p>
<h1 class="title">Pizzaofen Würenlos</h1>
{body}
</article></main>
'''
open(os.path.join(H, 'Bauplan_Pizzaofen.html'), 'w').write(page)
print('ok', len(page) // 1024, 'KB')
