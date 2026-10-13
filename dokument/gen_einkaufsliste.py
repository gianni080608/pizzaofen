#!/usr/bin/env python3
"""Erzeugt ../einkaufsliste.html (Handy, abhakbar, druckbar) aus stueckliste.json + obi_bestand.json (Fassung 2)."""
import json, os, html
H = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(H, '..', 'berechnung')
S = json.load(open(os.path.join(B, 'stueckliste.json'))); BE = json.load(open(os.path.join(B, 'obi_bestand.json')))['artikel']
SU = S['summen']; F2 = {'O02', 'O04', 'O05', 'O06', 'O10'}
def esc(x): return html.escape(str(x))
def fmt(x): return f"{x:,.2f}".replace(',', "'")
def bst(r, mk):
    key = r['art'] if len(r['bezug']) == 1 else f"{r['art']}@{mk}"
    return BE.get(key, {}).get('bestand', {}).get(mk, '?')
def items_for(mk, pred):
    out = []
    for r in S['rows']:
        if mk in r['bezug'] and pred(r):
            m = r['bezug'][mk]
            out.append(dict(id=f"{r['id']}-{mk}", name=r['name'], art=r['art'], menge=m, eh=r['eh'], kg=round(m * r['kg_einheit'], 1), chf=round(m * r['ep'], 2), note=f"Bestand {bst(r, mk)}"))
    return out
def kies(id_, name, m3, rg, art):
    return dict(id=id_, name=name, art=art, menge=m3, eh='m³', kg=round(m3 * rg), chf=round(m3 * 60, 2), note='selbst schaufeln, CHF 60.–/m³ (Privatpreis)')
T = [
 dict(key='F1a', title='Fahrt 1 · Stopp 1: OBI Oftringen', when='heute, nach Abholbestätigung (spätestens 18:25 dort)', addr='Ackerweg 2, 4665 Oftringen', km='42.3 km · 31–40 min ab Würenlos', open_='Di 08:00–19:00', tel='058 329 15 00', items=items_for('Oftringen', lambda r: True)),
 dict(key='F1b', title='Fahrt 1 · Stopp 2: OBI Volketswil', when='heute, danach (73 km ab Oftringen)', addr='Industriestrasse 20, 8604 Volketswil', km='Rückweg 32 km · 27–35 min', open_='Di 08:00–20:00', tel='058 329 12 00', items=items_for('Volketswil', lambda r: r['id'] not in F2)),
 dict(key='K1', title='Fahrt K1: Kieswerk Tägerhard', when='Mi 14.10., 07:00', addr='Tägerhardstrasse 151, 5430 Wettingen', km='2.8 km · 5 min', open_='07:00–12:00 · 13:00–16:45', tel='056 426 70 45', items=[kies('K1a', 'Kiesgemisch UG22 0/31.5 (Kieskoffer)', 0.56, 1600, '60201')]),
 dict(key='F2', title='Fahrt 2: OBI Volketswil', when='Mi 14.10., 08:15', addr='Industriestrasse 20, 8604 Volketswil', km='31.8 km · 27–35 min', open_='08:00–20:00', tel='058 329 12 00', items=items_for('Volketswil', lambda r: r['id'] in F2)),
 dict(key='K2', title='Fahrt K2: Kieswerk Tägerhard', when='Mi 14.10., 13:00', addr='Tägerhardstrasse 151, 5430 Wettingen', km='2.8 km', open_='07:00–12:00 · 13:00–16:45', tel='056 426 70 45', items=[kies('K2a', 'Kiesgemisch UG22 0/31.5 (Rest)', 0.19, 1600, '60201'), kies('K2b', 'Betonkies gewaschen 0/16', 0.33, 1800, '20001')]),
 dict(key='K3', title='Fahrt K3: Kieswerk Tägerhard', when='Do 15.10., 07:00', addr='Tägerhardstrasse 151, 5430 Wettingen', km='2.8 km', open_='07:00–12:00 · 13:00–16:45', tel='056 426 70 45', items=[kies('K3a', 'Betonkies gewaschen 0/16', 0.50, 1800, '20001')]),
 dict(key='K4', title='Fahrt K4: Kieswerk Tägerhard', when='Do 15.10., 08:00', addr='Tägerhardstrasse 151, 5430 Wettingen', km='2.8 km', open_='07:00–12:00 · 13:00–16:45', tel='056 426 70 45', items=[kies('K4a', 'Betonkies gewaschen 0/16', 0.27, 1800, '20001'), kies('K4b', 'Sand gewaschen 0/4', 0.25, 1500, '40001')]),
]
for t in T:
    t['kg'] = round(sum(i['kg'] for i in t['items'])); t['chf'] = round(sum(i['chf'] for i in t['items']), 2)
tot = round(sum(t['chf'] for t in T), 2); totkg = sum(t['kg'] for t in T)
assert abs(tot - SU['gesamt_mit_werkzeug']) < 0.5, (tot, SU)
f1 = T[0]['kg'] + T[1]['kg']
vorher = ['12:15 obi.ch: Reservierung 1 = Markt Oftringen (Liste „Stopp 1")',
          '12:15 obi.ch: Reservierung 2 = Markt Volketswil (Liste „Stopp 2" + „Fahrt 2")',
          'Werkzeug zuhause prüfen (Liste unten). Fehlendes ausleihen oder auf Reservierung 2 setzen',
          'Abstand Ofen–Nachbargrenze messen: ≥ 2 m ok, sonst Zustimmungsformular (Bauplan 9.4)',
          'Fahrzeugausweis: Gesamtgewicht − Leergewicht = Nutzlast; Planungsgrenze ≥ 900 kg?',
          'Bauverwaltung 056 436 87 50 (14–16 Uhr) oder E-Mail aus Bauplan 9.3',
          'Regel: Bestätigung Oftringen nach 17:45 → heute nur Volketswil, Oftringen Mi 08:00']
cards = []
for t in T:
    title = t['title']; kg = t['kg']
    load = f1 if t['key'].startswith('F1') else kg
    pct = min(100, load / 900 * 100)
    lab = f"Fahrt 1 total {f1} / 900 kg" if t['key'].startswith('F1') else f"{kg} / 900 kg"
    rows = ''.join(f'''<li class="item"><input type="checkbox" id="c-{esc(i['id'])}" data-k="{esc(i['id'])}"><label for="c-{esc(i['id'])}"><span class="nm">{esc(i['name'])}</span><span class="meta">Art. {esc(i['art'])} · {i['kg']} kg · {esc(i['note'])}</span></label><span class="q">{esc(i['menge'])} {esc(i['eh'])}</span><span class="p">{fmt(i['chf'])}</span></li>''' for i in t['items'])
    cards.append(f'''<section class="trip" id="{t['key']}"><header class="th"><div><h2>{esc(title)}</h2><p class="when">{esc(t['when'])}</p></div><div class="sum"><b>CHF {fmt(t['chf'])}</b><span>{kg} kg</span></div></header>
<div class="info"><span>{esc(t['addr'])}</span><span>{esc(t['km'])}</span><span>Offen: {esc(t['open_'])}</span><span class="tel">Tel. <span class="sel">{esc(t['tel'])}</span> <button class="copy" type="button" data-t="{esc(t['tel'])}">kopieren</button></span></div>
<div class="load" role="img" aria-label="Ladung {lab}"><div class="bar" style="width:{pct:.0f}%"></div><span>{lab}</span></div>
<ul class="items"><li class="hdr"><span></span><span>Artikel</span><span>Menge</span><span>CHF</span></li>{rows}</ul></section>''')
haus = ''.join(f'<li class="item"><input type="checkbox" id="h-{x["id"]}" data-k="h{x["id"]}"><label for="h-{x["id"]}"><span class="nm">{esc(x["name"])}</span><span class="meta">vorhanden? sonst Art. {x["art"]} · {esc(x["bestand"])}</span></label><span class="q">{x["menge"]} Stk</span><span class="p">{fmt(x["gp"])}</span></li>' for x in S['haus'])
pre = ''.join(f'<li class="item pre"><input type="checkbox" id="v-{n}" data-k="v{n}"><label for="v-{n}"><span class="nm">{esc(t)}</span></label></li>' for n, t in enumerate(vorher))
css = open(os.path.join(H, 'einkaufsliste.css')).read()
page = f'''<title>Pizzaofen Einkaufsliste</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{css}</style>
<main class="wrap">
<header><h1>Pizzaofen Einkaufsliste</h1><p class="lede">Fassung 2 · Kuppel Ø 80 cm · Di 13.10.2026 · Preise inkl. MWST · Bestand live geprüft um ca. 12:15 Uhr</p></header>
<div class="kpis"><div class="kpi"><span>Total alles inkl.</span><b>CHF {fmt(tot)}</b></div><div class="kpi"><span>Reserve bis 2000</span><b>CHF {fmt(2000 - tot)}</b></div><div class="kpi"><span>Gewicht</span><b>{totkg/1000:.2f} t</b></div></div>
<p class="warn"><b>Max. 900 kg pro Fahrt.</b> Schwere Last nach vorne an die Trennwand, flach laden, Antirutschunterlage, 4 Gurte. Der Wagen sieht leer aus und ist trotzdem voll.</p>
<section class="box"><h2>Vor dem Losfahren</h2><ul class="items">{pre}</ul></section>
{''.join(cards)}
<section class="box"><h2>Haushaltswerkzeug (nur falls nicht vorhanden)</h2><p class="note">Zuerst ausleihen. Was bis 15:30 fehlt, auf Reservierung 2 (Volketswil) setzen.</p><ul class="items">{haus}</ul></section>
<section class="box"><h2>Wenn etwas fehlt</h2><p class="note">Schamottsteine &lt; 35 → OBI Schaffhausen (9 Stk, 058 329 22 00) · Platten &lt; 18 → OBI Winterthur (13) · Schalungssteine &lt; 26 → OBI Winterthur (72, 058 329 19 00) · Zement Oftringen leer → OBI Winterthur (131) · Kieswerk lässt nicht selbst schaufeln → Big Bag füllen lassen (CHF 50) und vor Ort umschaufeln.</p></section>
<div class="foot"><p class="note">Häkchen werden nur auf diesem Gerät gespeichert.</p><div><button id="reset" type="button">Alle Häkchen löschen</button><span id="confirm" hidden>Wirklich? <button id="yes" type="button" class="copy">Ja, löschen</button><button id="no" type="button" class="copy">Abbrechen</button></span></div></div>
</main>
<script>
(function(){{
 var KEY='pizzaofen-einkauf-v2', st={{}};
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
print('ok', tot, totkg, [(t['key'], t['kg'], t['chf']) for t in T])
