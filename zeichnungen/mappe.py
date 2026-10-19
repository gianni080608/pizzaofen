#!/usr/bin/env python3
"""Zeichnungsmappe: alle 19 Zeichnungen je eine A4-Seite quer, mit Fusszeile -> Zeichnungsmappe_A4.pdf.
Braucht Playwright (Chromium). Aufruf: python3 mappe.py"""
import base64, os, sys
from playwright.sync_api import sync_playwright

H = os.path.dirname(os.path.abspath(__file__))
STAND = sys.argv[1] if len(sys.argv) > 1 else 'Fassung 5 · 19.10.2026'
BLAETTER = [
    ('Z1', 'iso_fertig', 'Fertiger Ofen'), ('Z2', 'iso_explosion', 'Explosionszeichnung'), ('Z3', 'frontansicht', 'Frontansicht'),
    ('Z4', 'schnitt_A_A', 'Längsschnitt A–A'), ('Z5', 'draufsicht', 'Draufsicht'), ('Z6', 'iso_etappen', 'Bauetappen'),
    ('Z7', 'lageplan', 'Lageplan und Aushub'), ('Z8', 'fundament', 'Fundament'), ('Z9', 'sockel_verlegeplan', 'Sockel Verlegeplan'),
    ('Z10', 'herdplatte_schalung', 'Herdplatte'), ('Z11', 'bodendaemmung', 'Bodendämmung'), ('Z12', 'backboden', 'Backboden'),
    ('Z13', 'zuschnitt', 'Zuschnitt und Keilsteine'), ('Z14', 'eingang', 'Eingang, Deckplatten'), ('Z15', 'schablone', 'Sandform-Schablone'),
    ('Z16', 'kuppel_reihe1', 'Kuppel Reihe 1'), ('Z17', 'kuppelschnitt_steinreihen', 'Kuppelschnitt'), ('Z18', 'detail_wand', 'Detail Wand'),
    ('Z19', 'tuer', 'Tür'),
]
pages = []
for nr, f, name in BLAETTER:
    data = base64.b64encode(open(os.path.join(H, f + '.svg'), 'rb').read()).decode()
    pages.append(f'<section><div class="z"><img src="data:image/svg+xml;base64,{data}"></div>'
                 f'<footer>{nr} {name} · Pizzaofen Würenlos · {STAND} · Masse in cm</footer></section>')
html = '''<!doctype html><html><head><meta charset="utf-8"><style>
@page{size:A4 landscape;margin:8mm}
body{margin:0;font-family:"DejaVu Sans",Arial,sans-serif}
section{height:193mm;display:flex;flex-direction:column;break-after:page}
section:last-child{break-after:auto}
.z{flex:1;min-height:0;display:flex;align-items:center;justify-content:center}
.z img{max-width:100%;max-height:100%;object-fit:contain}
footer{font-size:9pt;color:#444;text-align:center;padding-top:2mm;border-top:0.3mm solid #bbb}
</style></head><body>''' + ''.join(pages) + '</body></html>'
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.set_content(html, wait_until='load')
    pg.wait_for_timeout(500)
    pg.pdf(path=os.path.join(H, 'Zeichnungsmappe_A4.pdf'), format='A4', landscape=True, print_background=True,
           margin=dict(top='8mm', bottom='8mm', left='8mm', right='8mm'))
    b.close()
print('ok', len(BLAETTER), 'Blätter')
