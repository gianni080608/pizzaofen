#!/usr/bin/env python3
"""Erzeugt ../karte.html: Abholkarte mit Route, Stopps, Ladelisten je Fahrt, Phasen (1 Sockel, 2 Ofen) und Nutzlast-Rechner.
Quellen: ../berechnung/stueckliste.json (Touren, Preise, Gewichte), basemap.json (OSM, OSRM)."""
import json, os, re, html, urllib.parse
H = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(H, '..', 'berechnung', 'stueckliste.json')))
M = json.load(open(os.path.join(H, 'basemap.json')))
T = S['touren']
def esc(x): return html.escape(str(x))
def chf(x): return f"{x:,.2f}".replace(',', "'")
def kg(x): return f"{x:,.0f}".replace(',', "'")
def bbox(d):
    n = list(map(float, re.findall(r'-?\d+(?:\.\d+)?', d))); xs, ys = n[0::2], n[1::2]
    return [min(xs), min(ys), max(xs), max(ys)]
RB = {k: bbox(v['d']) for k, v in M['routes'].items()}
def union(*bs): return [min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)]
FIT = {'1': union(RB['oftringen'], RB['volketswil'], RB['kies']), '2': union(RB['volketswil'], RB['winterthur']), 'a': union(*RB.values())}
gmaps = lambda dest, wp=None: 'https://www.google.com/maps/dir/?api=1&' + urllib.parse.urlencode(dict(destination=dest, travelmode='driving', **({'waypoints': wp} if wp else {})))
ORT = {
 'oftringen': dict(name='OBI Oftringen', nav='OBI Oftringen, Ackerweg 2, 4665 Oftringen'),
 'volketswil': dict(name='OBI Volketswil', nav='OBI Volketswil, Industriestrasse 20, 8604 Volketswil'),
 'kies': dict(name='Kieswerk Tägerhard', nav='Tägerhard Kies AG, Tägerhardstrasse 151, 5430 Wettingen'),
 'winterthur': dict(name='OBI Winterthur', nav='OBI Winterthur, Industriestrasse 44, 8404 Winterthur'),
 'home': dict(name='Zuhause', nav='Schulstrasse 26, 5436 Würenlos'),
}
LEG = {k: M['routes'][k]['legs'][0] for k in ('oftringen', 'volketswil', 'kies')}
ph_trips = {p: [t for t in T if str(t['phase']) == p] for p in ('1', '2')}
KPI = {p: dict(chf=round(sum(t['chf'] for t in ts), 2), kg=sum(t['kg'] for t in ts), n=len(ts), vor=round(sum(t['vorgezogen_chf'] for t in ts), 2)) for p, ts in ph_trips.items()}
KPI['a'] = dict(chf=S['summen']['gesamt_mit_werkzeug'], kg=sum(t['kg'] for t in T), n=len(T), vor=0)
assert abs(KPI['1']['chf'] + KPI['2']['chf'] - KPI['a']['chf']) < 0.05
NAME = {'A': 'OBI Oftringen', 'B': 'OBI Volketswil', 'C': 'OBI Volketswil', 'K1': 'Kieswerk', 'K2': 'Kieswerk', 'K3': 'Kieswerk', 'K4': 'Kieswerk'}
EXTRA = {
 'A': '<p class="tip"><b>Vor der Abfahrt anrufen</b> (058 329 15 00): „Guten Tag, ich komme in ca. einer Stunde mit einem Lieferwagen. Können Sie mir bitte 25 Schamottesteine 64 × 124 × 250, Artikel 5390067, und 16 Sack Zement CEM I, Artikel 4793972, an der Abholung bereitlegen? Ich zahle vor Ort.“ Laden: Zement flach ganz vorne an die Trennwand, Steine daneben, Antirutschmatten darunter, 4 Gurte.</p>',
 'K1': '<p class="tip">Ab Wagen: die 4 Mörtelkästen auf die Antirutschmatten an die Trennwand stellen, bis 5 cm unter den Rand füllen (~80 l), dazu 10 Eimer à 15 l. An der Waage sagen: „Privat, ich schaufle selbst, Kiesgemisch 0/31.5.“</p>',
 'B': '<p class="tip">Die 26 Schalungssteine (702 kg) kommen als Erstes in den Wagen: zwei Lagen flach an der Trennwand, nicht stapeln über 2 Lagen. Bretter und OSB obendrauf festgurten. Holz im Markt auf Länge schneiden lassen (Schalbretter halbieren).</p>',
 'C': '<p class="tip"><b>Am Vorabend (So 18.10.) Bestand prüfen</b> auf obi.ch → Produkt → „Verfügbarkeit im Markt": <a href="https://www.obi.ch/grillutensilien/schamottestein-hxbxt-40-x-200-x-500-mm/p/5390026" target="_blank" rel="noopener">Schamottplatte 40 × 200 × 500</a> (17 nötig) und <a href="https://www.obi.ch/perlite-vermiculite/pflanzen-perlit-100-l/p/3798733" target="_blank" rel="noopener">Perlit 100 l</a> (3 nötig). Oder im Repo <code>python3 berechnung/obi_bestand.py</code>.<br><b>Wenn Volketswil zu wenig hat:</b> die fehlenden Platten in OBI Winterthur holen (13 am 13.10., Mo 08–20 Uhr, 058 329 19 00, 25 km weiter, auf der Karte gestrichelt). Perlit: Winterthur 7, Oftringen 11.</p>',
}
cards = []
for t in T:
    o = ORT[t['ort']]; leg = LEG[t['ort']]
    rows = []
    for p in t['pos']:
        tag = '<span class="tag">Ofen · vorgezogen</span>' if p['phase'] > t['phase'] else ''
        k = f"{t['key']}-{p['id']}"
        m = f"{p['menge']:g}"
        rows.append(f'<li class="item"><input type="checkbox" id="c-{k}" data-k="{k}"><label for="c-{k}"><span class="nm">{esc(p["name"])}</span>'
                    f'<span class="meta">Art. {esc(p["art"])} · {kg(p["kg"])} kg {tag}</span></label><span class="q">{m} {esc(p["eh"])}</span><span class="p">{chf(p["chf"])}</span></li>')
    vor = f' · davon Ofen vorgezogen CHF {chf(t["vorgezogen_chf"])}' if t['vorgezogen_chf'] else ''
    cards.append(f'''<article class="trip" id="t-{t['key']}" data-phase="{t['phase']}" data-ort="{t['ort']}" data-key="{t['key']}" data-kg="{t['kg']}">
<header class="th"><span class="badge p{t['phase']}">{t['key']}</span><div class="tt"><h3>{esc(NAME[t['key']])}</h3><p class="when">{esc(t['tag'])} · {esc(t['zeit'])}</p></div>
<div class="sum"><b>CHF {chf(t['chf'])}</b><span>{kg(t['kg'])} kg</span></div></header>
<p class="why">{esc(t['warum'])}</p>
<div class="info"><span>{esc(t['adr'])}</span><span>{leg[0]:g} km · {leg[1]}–{round(leg[1]*1.25)} min pro Weg</span><span>Offen {esc(t['oeffnung'])}</span><span><a href="tel:{t['tel'].replace(' ', '')}">{esc(t['tel'])}</a></span></div>
<div class="acts"><a class="btn go" href="{esc(gmaps(o['nav']))}" target="_blank" rel="noopener">Navigation starten</a><button class="btn show" type="button" data-show="{t['key']}">Auf Karte zeigen</button></div>
<div class="load" role="img" aria-label="Ladung"><div class="bar"></div><span class="lt">{kg(t['kg'])} kg</span></div>
<ul class="items">{''.join(rows)}</ul>
<p class="tot">Summe <b>CHF {chf(t['chf'])}</b> · {kg(t['kg'])} kg{vor}</p>
{EXTRA.get(t['key'], '')}</article>''')
DATA = dict(fit=FIT, routes={k: RB[k] for k in RB}, orte=M['orte'], places=M['places'],
            pins={'1': [['kies', 'K', 'Kieswerk Tägerhard', '1', 'l', -6], ['home', '⌂', 'Zuhause', 'h', 'r', 12], ['oftringen', 'A', 'OBI Oftringen', '1'], ['volketswil', 'B', 'OBI Volketswil', '1']],
                  '2': [['home', '⌂', 'Zuhause', 'h', 'r', 12], ['volketswil', 'C', 'OBI Volketswil', '2'], ['winterthur', '+', 'Plan B: OBI Winterthur', 'x']],
                  'a': [['kies', 'K', 'Kieswerk Tägerhard', '1', 'l', -6], ['home', '⌂', 'Zuhause', 'h', 'r', 12], ['oftringen', 'A', 'OBI Oftringen', '1'], ['volketswil', 'B C', 'OBI Volketswil', '1'], ['winterthur', '+', 'Plan B: OBI Winterthur', 'x']]},
            first={'1': {'kies': 'K1', 'oftringen': 'A', 'volketswil': 'B'}, '2': {'volketswil': 'C', 'winterthur': 'C'}, 'a': {'kies': 'K1', 'oftringen': 'A', 'volketswil': 'B', 'winterthur': 'C'}},
            tripRoute={t['key']: t['ort'] for t in T}, kies_kg=sum(t['kg'] for t in T if t['ort'] == 'kies'), kpi=KPI)
R = M['routes']
svg_routes = (f'<path class="rt p1" data-r="oftringen" d="{R["oftringen"]["d"]}"/>'
              f'<path class="rt p1" data-r="kies" d="{R["kies"]["d"]}"/>'
              f'<path class="rt px" data-r="winterthur" d="{R["winterthur"]["d"]}"/>'
              f'<path class="rt p2" data-r="volketswil2" d="{R["volketswil"]["d"]}"/>'
              f'<path class="rt p1" data-r="volketswil" d="{R["volketswil"]["d"]}"/>')
css = open(os.path.join(H, 'karte.css')).read()
js = open(os.path.join(H, 'karte.js')).read()
page = f'''<title>Abholkarte Pizzaofen</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{css}</style>
<div class="app" data-ph="1">
<header class="top"><h1>Abholkarte Pizzaofen</h1><p class="lede">Erst den Sockel bauen, den Ofen später. Bestand live geprüft am 13.10.2026 um 15:23 Uhr · Preise inkl. MWST</p>
<div class="tabs" role="tablist"><button role="tab" data-ph="1" aria-selected="true">Phase 1 · Sockel</button><button role="tab" data-ph="2" aria-selected="false">Phase 2 · Ofen</button><button role="tab" data-ph="a" aria-selected="false">Alles</button></div>
<div class="kpis"><div class="kpi"><span>Kosten</span><b id="k-chf"></b></div><div class="kpi"><span>Fahrten</span><b id="k-n"></b></div><div class="kpi"><span>Gewicht</span><b id="k-kg"></b></div></div>
<p class="phnote" data-for="1">Fundament, Sockel und Herdplatte: <b>Di 13.10. bis Do 15.10.</b>, gebaut wird bis So 18.10. Knappe Ofen-Teile (alle 39 Schamottsteine, 1 Platte, Türblech, Sand) nehmt ihr gleich mit: <b>CHF <span id="k-vor"></span></b> davon sind Ofen-Material.</p>
<p class="phnote" data-for="2">Der Ofen: <b>eine Fahrt am Mo 19.10.</b> (spätestens Di 20.10.). Am Mi 21.10. wird die Bodendämmung gegossen, dafür braucht es das Perlit.</p>
<p class="phnote" data-for="a">Alle 7 Fahrten. Total CHF {chf(KPI['a']['chf'])}, Reserve bis 2000: CHF {chf(2000 - KPI['a']['chf'])}.</p>
</header>
<section class="mapwrap" aria-label="Karte">
<svg id="map" role="img" aria-label="Karte mit Route Würenlos zu den Abholstellen">
<rect id="bgr" x="-5000" y="-5000" width="10000" height="10000" class="land"/>
<g id="geo"><path class="lake" d="{M['lakes']}"/><path class="river" d="{M['rivers']}"/><path class="mw" d="{M['motorways']}"/>{svg_routes}</g>
<g id="lbl"></g><g id="pins"></g><g id="scale"></g></svg>
<div class="ctl"><button type="button" id="zin" aria-label="Hineinzoomen">+</button><button type="button" id="zout" aria-label="Herauszoomen">−</button><button type="button" id="zfit" aria-label="Ganze Route zeigen">⤢</button></div>
<div class="legend"><span><i class="l1"></i>Phase 1</span><span><i class="l2"></i>Phase 2</span><span><i class="lx"></i>Plan B</span><span><i class="lm"></i>Autobahn</span></div>
<p class="attr">© OpenStreetMap-Mitwirkende · Route OSRM</p>
</section>
<section class="list">
<details class="box payload" open><summary><h2>2 Tonnen pro Fahrt? Nicht mit Kat. B</h2></summary>
<p>Mit Kat. B darf der Bus <b>beladen höchstens so viel wiegen, wie im Fahrzeugausweis als Gesamtgewicht steht</b> – und der Ausweis gilt nur für Fahrzeuge bis 3'500 kg. Ein Talento wiegt leer ca. 1'965 kg inkl. Fahrer. Mit 2'000 kg Ladung wären es <b>ca. 3'965 kg</b>: rund 30 % über dem Gesamtgewicht (Talento 2'900–3'100 kg) und über 3'500 kg. Das ist eine Überladung mit Anzeige statt Busse. In der Probezeit kann das den Ausweis kosten, und bei einem Unfall nimmt die Versicherung Regress. Bremsen und Achsen sind dafür nicht gebaut.</p>
<p>Die <b>2'000 kg</b> im Ausweis sind beim Talento sehr wahrscheinlich die <b>Anhängelast</b>. Die gilt nur für einen Anhänger, und mit Kat. B dürft ihr hinter diesem Bus höchstens einen Anhänger bis 750 kg ziehen.</p>
<p><b>Es bleibt bei max. 900 kg pro Fahrt.</b> Das kostet kaum Zeit: Das Kieswerk ist 3 km entfernt, eine Kiesfahrt dauert 5 Minuten pro Weg. Tragt eure Werte aus dem Fahrzeugausweis ein, dann prüft die Seite jede Fahrt:</p>
<div class="calc"><label>Gesamtgewicht (Ausweis)<input id="gg" type="number" inputmode="numeric" min="1000" max="9000" step="5" value="3060"><span>kg</span></label>
<label>Leergewicht (Ausweis, inkl. Fahrer)<input id="lg" type="number" inputmode="numeric" min="500" max="5000" step="5" value="1965"><span>kg</span></label>
<label>Beifahrer<input id="mf" type="number" inputmode="numeric" min="0" max="2" step="1" value="1"><span>× 75 kg</span></label></div>
<p id="calc-out" class="calc-out" aria-live="polite"></p></details>
{''.join(cards)}
<section class="box planb" data-phase="1"><h2>Wenn etwas nicht klappt</h2><p class="note">Oftringen hat weniger als 25 Schamottsteine → nehmt, was da ist. Fehlende Steine am Mi zusätzlich in Volketswil (24 am Lager), sonst OBI Basel (21). · Zement in Oftringen fehlt → OBI Winterthur (131). · Schalungssteine in Volketswil &lt; 26 → OBI Winterthur (72). · Kieswerk lässt nicht selbst schaufeln → Big Bag füllen lassen (CHF 50) und vor Ort in die Kästen umschaufeln.</p></section>
<p class="note foot">„Unterbau“ heisst hier: Fundament, Sockel aus Schalungssteinen und Herdplatte. Ein Dach ist nicht eingeplant, die Plane schützt den Ofen. Häkchen und Eingaben werden nur auf diesem Gerät gespeichert. <button type="button" id="reset" class="link">Häkchen löschen</button><span id="confirm" hidden> Wirklich? <button type="button" id="yes" class="link">Ja</button> <button type="button" id="no" class="link">Nein</button></span></p>
</section>
</div>
<script>window.KARTE={json.dumps(DATA, ensure_ascii=False, separators=(',', ':'))};
{js}</script>
'''
out = os.path.join(H, '..', 'karte.html')
open(out, 'w').write(page)
print('ok', os.path.getsize(out), {k: (v['chf'], v['kg'], v['n']) for k, v in KPI.items()})
