#!/usr/bin/env python3
"""Erzeugt ../einkaufsliste.html (Handy, abhakbar, druckbar) aus stueckliste.json (Touren) + obi_bestand.json (Fassung 3, Phasen)."""
import json, os, html, urllib.parse
H = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(H, '..', 'berechnung')
S = json.load(open(os.path.join(B, 'stueckliste.json'))); BE = json.load(open(os.path.join(B, 'obi_bestand.json')))['artikel']
SU = S['summen']
def esc(x): return html.escape(str(x))
def fmt(x): return f"{x:,.2f}".replace(',', "'")
def bst(r, mk):
    key = r['art'] if len(r['bezug']) == 1 else f"{r['art']}@{mk}"
    return BE.get(key, {}).get('bestand', {}).get(mk, '?')
NAV = {'oftringen': 'OBI Oftringen, Ackerweg 2, 4665 Oftringen', 'volketswil': 'OBI Volketswil, Industriestrasse 20, 8604 Volketswil', 'kies': 'Tägerhard Kies AG, Tägerhardstrasse 151, 5430 Wettingen'}
WEG = {'oftringen': '42.3 km · 31–39 min pro Weg', 'volketswil': '31.8 km · 27–34 min pro Weg', 'kies': '3.3 km · 6–8 min pro Weg'}
ORTN = {'oftringen': 'OBI Oftringen', 'volketswil': 'OBI Volketswil', 'kies': 'Kieswerk Tägerhard'}
T = []
for t in S['touren']:
    items = []
    for p in t['pos']:
        if p['eh'] == 'm³': note = 'selbst schaufeln, CHF 60.–/m³ (Privatpreis)'
        else:
            r = next(x for x in S['rows'] if x['id'] == p['id']); mk = 'Oftringen' if t['ort'] == 'oftringen' else 'Volketswil'
            note = f"Bestand {bst(r, mk)}"
        if p['phase'] > t['phase']: note += ' · Ofen, vorgezogen'
        items.append(dict(id=f"{t['key']}-{p['id']}", name=p['name'], art=p['art'], menge=p['menge'], eh=p['eh'], kg=p['kg'], chf=p['chf'], note=note))
    T.append(dict(key=t['key'], phase=t['phase'], title=f"{'Phase 1 · Sockel' if t['phase'] == 1 else 'Phase 2 · Ofen'} – Fahrt {t['key']}: {ORTN[t['ort']]}",
                  when=f"{t['tag']} {t['zeit']}", addr=t['adr'], km=WEG[t['ort']], open_=t['oeffnung'], tel=t['tel'], items=items,
                  nav='https://www.google.com/maps/dir/?api=1&' + urllib.parse.urlencode(dict(destination=NAV[t['ort']], travelmode='driving'))))
for t in T:
    t['kg'] = round(sum(i['kg'] for i in t['items'])); t['chf'] = round(sum(i['chf'] for i in t['items']), 2)
tot = round(sum(t['chf'] for t in T), 2); totkg = sum(t['kg'] for t in T)
P1 = round(sum(t['chf'] for t in T if t['phase'] == 1), 2); P2 = round(sum(t['chf'] for t in T if t['phase'] == 2), 2); VOR = round(sum(t['vorgezogen_chf'] for t in S['touren']), 2)
assert abs(tot - SU['gesamt_mit_werkzeug']) < 0.5, (tot, SU)
vorher = ['Vor Fahrt A: OBI Oftringen anrufen (058 329 15 00) und 25 Schamottsteine + 16 Zement bereitlegen lassen',
          'Werkzeug zuhause prüfen (Liste unten). Fehlendes ausleihen oder am Mi bei Fahrt B in Volketswil kaufen',
          'Abstand Ofen–Nachbargrenze messen: ≥ 2 m ok, sonst Zustimmungsformular (Bauplan 9.4)',
          'Fahrzeugausweis: Gesamtgewicht − Leergewicht = Nutzlast; Planungsgrenze ≥ 900 kg?',
          'Bauverwaltung 056 436 87 50 (14–16 Uhr) oder E-Mail aus Bauplan 9.3',
          'Regel: Fahrt A heute nicht bis 17:30 losgefahren → Mi 08:00 A, 10:15 K1, 11:00 B, 14:00 K2; Donnerstag bleibt',
          'So 18.10. abends: Bestand Platten und Perlit in Volketswil prüfen (für Fahrt C)']
cards = []
for t in T:
    title = t['title']; kg = t['kg']
    pct = min(100, kg / 900 * 100)
    lab = f"{kg} / 900 kg"
    rows = ''.join(f'''<li class="item"><input type="checkbox" id="c-{esc(i['id'])}" data-k="{esc(i['id'])}"><label for="c-{esc(i['id'])}"><span class="nm">{esc(i['name'])}</span><span class="meta">Art. {esc(i['art'])} · {i['kg']} kg · {esc(i['note'])}</span></label><span class="q">{esc(i['menge'])} {esc(i['eh'])}</span><span class="p">{fmt(i['chf'])}</span></li>''' for i in t['items'])
    cards.append(f'''<section class="trip" id="{t['key']}"><header class="th"><div><h2>{esc(title)}</h2><p class="when">{esc(t['when'])}</p></div><div class="sum"><b>CHF {fmt(t['chf'])}</b><span>{kg} kg</span></div></header>
<div class="info"><span>{esc(t['addr'])}</span><span>{esc(t['km'])}</span><span>Offen: {esc(t['open_'])}</span><span class="tel">Tel. <span class="sel">{esc(t['tel'])}</span> <button class="copy" type="button" data-t="{esc(t['tel'])}">kopieren</button></span><a class="nav" href="{esc(t['nav'])}" target="_blank" rel="noopener">Navigation (Google Maps)</a></div>
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
<header><h1>Pizzaofen Einkaufsliste</h1><p class="lede">Fassung 3 · Phase 1 Sockel (Di–Do), Phase 2 Ofen (Mo 19.10.) · Kuppel Ø 80 cm · Preise inkl. MWST · Bestand live geprüft am 13.10. um 15:23 Uhr</p></header>
<div class="kpis"><div class="kpi"><span>Total alles inkl.</span><b>CHF {fmt(tot)}</b></div><div class="kpi"><span>Reserve bis 2000</span><b>CHF {fmt(2000 - tot)}</b></div><div class="kpi"><span>Gewicht</span><b>{totkg/1000:.2f} t</b></div></div>
<div class="kpis"><div class="kpi"><span>Phase 1 · Sockel</span><b>CHF {fmt(P1)}</b></div><div class="kpi"><span>Phase 2 · Ofen</span><b>CHF {fmt(P2)}</b></div><div class="kpi"><span>davon in Ph. 1 vorgezogen</span><b>CHF {fmt(VOR)}</b></div></div>
<p class="warn"><b>Max. 900 kg pro Fahrt, auch wenn der Bus mehr tragen könnte:</b> Mit Kat. B darf der beladene Bus nicht mehr wiegen als sein Gesamtgewicht im Ausweis (Talento ca. 3'060 kg, leer ca. 1'965 kg) – 2 t Ladung gehen nicht. Schwere Last nach vorne an die Trennwand, flach laden, Antirutschunterlage, 4 Gurte. Der Wagen sieht leer aus und ist trotzdem voll.</p>
<section class="box"><h2>Vor dem Losfahren</h2><ul class="items">{pre}</ul></section>
{''.join(cards)}
<section class="box"><h2>Haushaltswerkzeug (nur falls nicht vorhanden)</h2><p class="note">Zuerst ausleihen. Was fehlt, am Mi bei Fahrt B in Volketswil kaufen (vor dem Aushub am Mi braucht ihr Schaufel, Spaten, Kreuzhacke, Schubkarre: die heute leihen).</p><ul class="items">{haus}</ul></section>
<section class="box"><h2>Wenn etwas fehlt</h2><p class="note">Schamottsteine Oftringen &lt; 25 → Rest am Mi zusätzlich in Volketswil (24) · Platten in Volketswil &lt; 17 (Fahrt C) → OBI Winterthur (13, 058 329 19 00) · Schalungssteine &lt; 26 → OBI Winterthur (72, 058 329 19 00) · Zement Oftringen leer → OBI Winterthur (131) · Kieswerk lässt nicht selbst schaufeln → Big Bag füllen lassen (CHF 50) und vor Ort umschaufeln.</p></section>
<div class="foot"><p class="note">Häkchen werden nur auf diesem Gerät gespeichert.</p><div><button id="reset" type="button">Alle Häkchen löschen</button><span id="confirm" hidden>Wirklich? <button id="yes" type="button" class="copy">Ja, löschen</button><button id="no" type="button" class="copy">Abbrechen</button></span></div></div>
</main>
<script>
(function(){{
 var KEY='pizzaofen-einkauf-v3', st={{}};
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
