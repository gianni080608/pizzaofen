#!/usr/bin/env python3
"""Erzeugt ../einkaufsliste.html (Handy, abhakbar, druckbar) aus stueckliste.json."""
import json, os, html, re
H = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(H, '..', 'berechnung', 'stueckliste.json')))
import importlib.util
spec = importlib.util.spec_from_file_location('b', os.path.join(H, 'build.py'))
WORDS = []
src = open(os.path.join(H, 'build.py')).read()
exec(src[src.index('WORDS = ['):src.index('# --- Platzhalter')], g := {})
de = g['de']
R = {r['pos']: r for r in S['rows']}
M = {m['pos']: m for m in S['mieten']}
def art(b):
    m = re.search(r'Art\. ?(\d+)', b); return m.group(1) if m else ''
def clean(b): return de(re.sub(r'\s*\((OBI )?Art\. ?\d+\)', '', b))
def it(pos, menge=None, note=''):
    r = R[pos]; q = r['menge'] if menge is None else menge
    return dict(id=f'{pos}', name=clean(r['bez']), art=art(r['bez']), menge=q, eh=de(r['eh']), kg=round(q * r['kg_einheit']),
                chf=round(q * r['ep'], 2), note=note or de(r['status']) if 'unbest' in r['status'] or 'ANNAHME' in r['status'] else note)
def kies(id_, name, m3, rg, art_):
    return dict(id=id_, name=name, art=art_, menge=m3, eh='m³', kg=round(m3 * rg), chf=round(m3 * 60, 2), note='selbst in Säcke/Kübel, Privatpreis 60.–/m³ bestätigen')
F = [
 dict(key='F1', title='Fahrt 1 · HORNBACH Affoltern a. A.', when='heute ca. 12:30–14:45', addr='Obfelderstrasse 37, 8910 Affoltern am Albis', km='26.6 km · ca. 25–30 min', open_='Di 07:00–19:00 (Verzeichnis, prüfen)', tel='044 204 40 00',
      items=[it('6'), it('7'), it('4'), it('8'), it('13'), it('15'), it('16')]),
 dict(key='K1', title='Fahrt K1 · Kieswerk Tägerhard', when='heute ca. 15:00–16:30', addr='Tägerhardstrasse 151, 5430 Wettingen', km='2.8 km · ca. 5 min', open_='07:00–12:00 · 13:00–16:45', tel='056 426 70 45',
      items=[kies('K1a', 'Kiesgemisch UG22 0/31.5 (Kieskoffer)', 0.56, 1600, '60201')]),
 dict(key='F2', title='Fahrt 2 · OBI Volketswil', when='heute ca. 17:00–19:15', addr='Industriestrasse 20, 8604 Volketswil', km='31.8 km · ca. 30–35 min', open_='Di 08:00–20:00', tel='058 329 12 00',
      items=[it('11'), it('12'), it('14'), it('5'), it('9'), it('10', note='im Markt halbieren lassen (1.5 m)'), it('10b'), it('17'), it('18'), it('19'), it('20')] +
            [dict(id=p, name=de(re.sub(r'\s*\(OBI Mietgeraet \d+\)', '', M[p]['bez'])), art='Miete', menge=M[p]['menge'], eh=de(M[p]['eh']), kg=M[p]['kg'], chf=M[p]['gp'], note=de(M[p]['spez'])) for p in ('M1', 'M2')]),
 dict(key='K2', title='Fahrt K2 · Kieswerk Tägerhard', when='Mi 14.10., 07:00', addr='Tägerhardstrasse 151, 5430 Wettingen', km='2.8 km', open_='07:00–12:00 · 13:00–16:45', tel='056 426 70 45',
      items=[kies('K2a', 'Kiesgemisch UG22 0/31.5 (Rest)', 0.19, 1600, '60201'), kies('K2b', 'Betonkies gewaschen 0/16', 0.33, 1800, '20001')]),
 dict(key='K3', title='Fahrt K3 · Kieswerk Tägerhard', when='Mi/Do', addr='Tägerhardstrasse 151, 5430 Wettingen', km='2.8 km', open_='07:00–12:00 · 13:00–16:45', tel='056 426 70 45',
      items=[kies('K3a', 'Betonkies gewaschen 0/16', 0.50, 1800, '20001')]),
 dict(key='K4', title='Fahrt K4 · Kieswerk Tägerhard', when='Do 15.10.', addr='Tägerhardstrasse 151, 5430 Wettingen', km='2.8 km', open_='07:00–12:00 · 13:00–16:45', tel='056 426 70 45',
      items=[kies('K4a', 'Betonkies gewaschen 0/16', 0.27, 1800, '20001'), kies('K4b', 'Sand gewaschen 0/4', 0.25, 1500, '40001')]),
]
for f in F:
    f['kg'] = sum(i['kg'] for i in f['items']); f['chf'] = round(sum(i['chf'] for i in f['items']), 2)
tot = round(sum(f['chf'] for f in F), 2); totkg = sum(f['kg'] for f in F)
assert abs(tot - S['gesamt']) < 1, (tot, S['gesamt'])
vorher = ['Hornbach anrufen: Schalungssteine einzeln? Kaminrohr an Lager?', 'OBI online reservieren (Reservieren & Abholen, ca. 4 h) + Mietgeräte erfragen',
          'Kieswerk anrufen: Selbstverlad in Säcke ok? 60.–/m³?', 'Fahrzeugausweis: Gesamtgewicht − Leergewicht = Nutzlast notieren',
          'Mitnehmen: 4 Spanngurte, Antirutschmatte, 2 Schaufeln, 40 PP-Säcke/Kübel, Malervlies', 'ID/Karte für Mietkautionen (CHF 450)',
          'Bauverwaltung Würenlos 056 436 87 50 (Di 14:00–16:00)']
def esc(x): return html.escape(str(x))
def fmt(x): return f"{x:,.2f}".replace(',', "'")
cards = []
for f in F:
    pct = min(100, f['kg'] / 900 * 100)
    rows = ''.join(f'''<li class="item"><input type="checkbox" id="c-{esc(i['id'])}" data-k="{esc(i['id'])}"><label for="c-{esc(i['id'])}"><span class="nm">{esc(i['name'])}</span><span class="meta">{' · '.join(x for x in [('Art. ' + esc(i['art'])) if i['art'] and i['art'] != 'Miete' else ('Miete' if i['art'] == 'Miete' else ''), '<span class="mw">' + str(i['kg']) + ' kg</span>', esc(i['note']) if i['note'] else ''] if x)}</span></label><span class="q">{esc(i['menge'])} {esc(i['eh'])}</span><span class="p">{fmt(i['chf'])}</span></li>''' for i in f['items'])
    cards.append(f'''<section class="trip" id="{f['key']}"><header class="th"><div><h2>{esc(f['title'])}</h2><p class="when">{esc(f['when'])}</p></div><div class="sum"><b>CHF {fmt(f['chf'])}</b><span>{f['kg']} kg</span></div></header>
<div class="info"><span>{esc(f['addr'])}</span><span>{esc(f['km'])}</span><span>Offen: {esc(f['open_'])}</span><span class="tel">Tel. <span class="sel">{esc(f['tel'])}</span> <button class="copy" type="button" data-t="{esc(f['tel'])}">kopieren</button></span></div>
<div class="load" role="img" aria-label="Ladung {f['kg']} von 900 kg"><div class="bar" style="width:{pct:.0f}%"></div><span>{f['kg']} / 900 kg Planungsgrenze</span></div>
<ul class="items"><li class="hdr"><span></span><span>Artikel · Gewicht</span><span>Menge</span><span>CHF</span></li>{rows}</ul></section>''')
pre = ''.join(f'<li class="item pre"><input type="checkbox" id="v-{n}" data-k="v{n}"><label for="v-{n}"><span class="nm">{esc(t)}</span></label></li>' for n, t in enumerate(vorher))
page = f'''<title>Pizzaofen Einkaufsliste</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: eine Spalte wie ein Lieferschein, pro Fahrt eine Karte mit Ladebalken */
:root{{--bg:#f3f4f2;--paper:#ffffff;--ink:#1d2226;--muted:#5d666d;--line:#d9dcd8;--accent:#b5592a;--blue:#1c4f8a;--ok:#2e7d4f;--warn:#b7791f;
--fd:"Barlow Semi Condensed","Arial Narrow",Arial,sans-serif;--fb:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--fm:"IBM Plex Mono",ui-monospace,Menlo,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#15191c;--paper:#1e2327;--ink:#e8eae7;--muted:#9aa3a9;--line:#323a40;--accent:#e08a57;--blue:#7fb0e6;--ok:#6cc08e;--warn:#e0b05c;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#15191c;--paper:#1e2327;--ink:#e8eae7;--muted:#9aa3a9;--line:#323a40;--accent:#e08a57;--blue:#7fb0e6;--ok:#6cc08e;--warn:#e0b05c;color-scheme:dark}}
body{{background:var(--bg);color:var(--ink);font-family:var(--fb);font-size:15px;line-height:1.45}}
.wrap{{max-width:760px;margin:0 auto;padding-inline:16px;padding-block:20px 48px;display:grid;gap:18px}}
h1,h2{{font-family:var(--fd);font-weight:700;text-wrap:balance;margin:0;letter-spacing:.01em}}
h1{{font-size:clamp(1.7rem,6vw,2.3rem);line-height:1.05}}
h2{{font-size:1.25rem;line-height:1.15}}
.lede{{color:var(--muted);margin:.35rem 0 0}}
.kpis{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}}
.kpi{{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:10px 12px;min-width:0}}
.kpi b{{display:block;font-family:var(--fd);font-size:1.35rem;font-variant-numeric:tabular-nums}}
.kpi span{{font-size:.78rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}}
.trip,.box{{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:14px;display:grid;gap:10px;min-width:0}}
.th{{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}}
.when{{margin:.15rem 0 0;color:var(--accent);font-weight:600;font-size:.9rem}}
.sum{{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}}.sum b{{display:block;font-family:var(--fd);font-size:1.15rem}}.sum span{{color:var(--muted);font-size:.85rem}}
.info{{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:.85rem;color:var(--muted)}}
.sel{{user-select:all;color:var(--ink);font-family:var(--fm)}}
.copy{{font:inherit;font-size:.75rem;border:1px solid var(--line);background:transparent;color:var(--blue);border-radius:6px;padding:1px 7px;cursor:pointer}}
.copy:focus-visible,input:focus-visible{{outline:2px solid var(--blue);outline-offset:2px}}
.load{{position:relative;height:22px;border-radius:6px;background:color-mix(in srgb,var(--line) 60%,transparent);overflow:hidden}}
.load .bar{{position:absolute;inset:0 auto 0 0;background:color-mix(in srgb,var(--ok) 35%,transparent);border-right:2px solid var(--ok)}}
.load span{{position:relative;font-size:.75rem;font-family:var(--fm);padding-left:8px;line-height:22px}}
.items{{list-style:none;margin:0;padding:0;display:grid}}
.item,.hdr{{display:grid;grid-template-columns:28px minmax(0,1fr) auto 76px;gap:8px;align-items:start;padding:9px 0;border-top:1px solid var(--line)}}
.hdr{{font-size:.7rem;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);padding:2px 0 6px;border-top:0}}
.hdr span:nth-child(n+3),.q,.w,.p{{text-align:right;font-variant-numeric:tabular-nums;font-family:var(--fm);font-size:.85rem;white-space:nowrap}}
.item input{{width:22px;height:22px;margin:0;accent-color:var(--ok)}}
.item label{{display:grid;gap:2px;min-width:0;cursor:pointer}}
.nm{{font-weight:500}}.meta{{font-size:.78rem;color:var(--muted)}}
.item:has(input:checked) .nm{{text-decoration:line-through;color:var(--muted)}}
.pre{{grid-template-columns:28px minmax(0,1fr)}}
.note{{font-size:.85rem;color:var(--muted);margin:0}}
.warn{{border-left:3px solid var(--warn);padding:8px 10px;background:color-mix(in srgb,var(--warn) 10%,transparent);border-radius:6px;font-size:.88rem}}
.foot{{display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;align-items:center}}
#reset{{font:inherit;border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:8px;padding:6px 12px;cursor:pointer}}
#confirm{{display:flex;gap:8px;align-items:center;font-size:.9rem}}
@media (max-width:480px){{.item,.hdr{{grid-template-columns:26px minmax(0,1fr) auto 66px;}}.kpi b{{font-size:1rem;white-space:nowrap}}}}
@media print{{body{{background:#fff;color:#000;font-size:11px}}.copy,#reset,#confirm{{display:none!important}}.trip,.box{{break-inside:avoid;border-color:#999}}.wrap{{max-width:none}}}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
</style>
<main class="wrap">
<header><h1>Pizzaofen Einkaufsliste</h1><p class="lede">Variante B · Kuppel Ø 90 cm · Dienstag 13.10.2026 · Preise inkl. MWST, Stand 13.10.2026 (Markt kann abweichen)</p></header>
<div class="kpis"><div class="kpi"><span>Total</span><b>CHF {fmt(tot)}</b></div><div class="kpi"><span>Reserve bis 2000</span><b>CHF {fmt(2000 - tot)}</b></div><div class="kpi"><span>Gewicht</span><b>{totkg/1000:.2f} t</b></div></div>
<p class="warn"><b>Max. 900 kg pro Fahrt.</b> Kies und Steine sehen nach wenig aus, sind aber sehr schwer. Schweres an die Trennwand bzw. über die Hinterachse, flach laden, gurten.</p>
<section class="box"><h2>Vor dem Losfahren</h2><ul class="items">{pre}</ul></section>
{''.join(cards)}
<section class="box"><h2>Optional / später</h2><p class="note">Regenhut Ø150 Edelstahl (Hornbach Art. 5860174, CHF 134.40, ca. 8 Tage Lieferzeit) · Steintrennmaschine mieten nur ohne Winkelschleifer (OBI CHF 120/Tag) · Keramikfasermatte 25 mm online (Dämm-Upgrade) · Deponie Aushub Tägerhard ca. CHF 22 (oder Aushub im Garten verteilen).</p></section>
<div class="foot"><p class="note">Häkchen werden nur auf diesem Gerät gespeichert.</p><div><button id="reset" type="button">Alle Häkchen löschen</button><span id="confirm" hidden>Wirklich? <button id="yes" type="button" class="copy">Ja, löschen</button><button id="no" type="button" class="copy">Abbrechen</button></span></div></div>
</main>
<script>
(function(){{
 var KEY='pizzaofen-einkauf-v1', st={{}};
 try{{st=JSON.parse(localStorage.getItem(KEY)||'{{}}')||{{}}}}catch(e){{st={{}}}}
 var boxes=[].slice.call(document.querySelectorAll('input[type=checkbox]'));
 boxes.forEach(function(b){{ if(st[b.dataset.k]) b.checked=true; b.addEventListener('change',function(){{ st[b.dataset.k]=b.checked; try{{localStorage.setItem(KEY,JSON.stringify(st))}}catch(e){{}} }}); }});
 document.querySelectorAll('.copy[data-t]').forEach(function(btn){{ btn.addEventListener('click',function(){{ var t=btn.dataset.t; var done=function(){{btn.textContent='kopiert';setTimeout(function(){{btn.textContent='kopieren'}},1500)}};
   try{{navigator.clipboard.writeText(t).then(done,function(){{sel(btn)}})}}catch(e){{sel(btn)}} }}); }});
 function sel(btn){{var s=btn.previousElementSibling; var r=document.createRange(); r.selectNodeContents(s); var w=getSelection(); w.removeAllRanges(); w.addRange(r);}}
 var reset=document.getElementById('reset'), conf=document.getElementById('confirm');
 reset.addEventListener('click',function(){{reset.hidden=true;conf.hidden=false}});
 document.getElementById('no').addEventListener('click',function(){{reset.hidden=false;conf.hidden=true}});
 document.getElementById('yes').addEventListener('click',function(){{st={{}};try{{localStorage.removeItem(KEY)}}catch(e){{}};boxes.forEach(function(b){{b.checked=false}});reset.hidden=false;conf.hidden=true}});
}})();
</script>
'''
open(os.path.join(H, '..', 'einkaufsliste.html'), 'w').write(page)
print('ok', tot, totkg, [(f['key'], f['kg'], f['chf']) for f in F])
