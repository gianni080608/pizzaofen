#!/usr/bin/env python3
"""Fassung 5: ../einkaufsliste.html (Handy, abhakbar) aus berechnung/fassung5.json.
Zeigt was gekauft ist, was noch fehlt (mit Lagerbestand), Kieswerk-Fahrten und was von zuhause kommt."""
import json, os, html, urllib.parse
H = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(H, '..', 'berechnung')
F = json.load(open(os.path.join(B, 'fassung5.json'))); SU = F['summen']
def esc(x): return html.escape(str(x))
def fmt(x): return f"{x:,.2f}".replace(',', "'")
def nav(dest, waypoints=None):
    q = dict(api=1, destination=dest, travelmode='driving')
    if waypoints: q['waypoints'] = waypoints
    return 'https://www.google.com/maps/dir/?' + urllib.parse.urlencode(q)
ADR = {'A1': 'OBI Oftringen, Ackerweg 2, 4665 Oftringen', 'A2': 'OBI Basel, Reinacherstrasse 29, 4053 Basel',
       'K': 'Tägerhard Kies AG, Tägerhardstrasse 151, 5430 Wettingen'}
WANN = {'A1': 'heute bis 19:00 (Mo–Do) · sonst Di ab 08:00', 'A2': 'direkt nach Oftringen · offen bis 20:00'}
KWANN = {'K1': 'Di 20.10. 07:00', 'K2': 'Do 22.10. 07:00', 'K3': 'Fr 23.10. 07:00', 'K4': 'Mo 26.10. 07:00'}

def item(key, name, meta, q, p, opt=False):
    cls = 'item opt' if opt else 'item'
    return (f'<li class="{cls}"><input type="checkbox" id="c-{esc(key)}" data-k="{esc(key)}"><label for="c-{esc(key)}">'
            f'<span class="nm">{esc(name)}{" <em>nur falls nötig</em>" if opt else ""}</span><span class="meta">{meta}</span></label>'
            f'<span class="q">{esc(q)}</span><span class="p">{p}</span></li>')

cards = []
for f in F['fahrt_a']:
    rows = ''.join(item(f"{f['key']}-{p['id']}", p['name'],
                        f"Art. {esc(p['art'])} · Bestand {p['bestand']} · {esc(p['warum'])}",
                        f"{p['menge']} {p['eh']}", fmt(p['chf']), not p['pflicht']) for p in f['pos'])
    pct = min(100, f['kg'] / 900 * 100)
    cards.append(f'''<section class="trip" id="{f['key']}"><header class="th"><div><h2>Fahrt {f['key'][1]}/2 · {esc(f['ort'])}</h2><p class="when">{esc(WANN[f['key']])}</p></div>
<div class="sum"><b>CHF {fmt(f['chf_pflicht'])}</b><span>{'+ ' + fmt(f['chf_alles'] - f['chf_pflicht']) + ' Extras · ' if f['chf_alles'] != f['chf_pflicht'] else ''}{f['kg']} kg</span></div></header>
<div class="info"><span>{esc(f['adr'])}</span><span>{esc(f['weg'])}</span><span>Offen: {esc(f['oeffnung'])}</span><span class="tel">Tel. <span class="sel">{esc(f['tel'])}</span> <button class="copy" type="button" data-t="{esc(f['tel'])}">kopieren</button></span><a class="nav" href="{esc(nav(ADR[f['key']]))}" target="_blank" rel="noopener">Navigation (Google Maps)</a></div>
<ul class="items"><li class="hdr"><span></span><span>Artikel</span><span>Menge</span><span>CHF</span></li>{rows}</ul></section>''')

kies = []
for k in F['kies']:
    rows = ''.join(item(f"{k['key']}-{i}", name, f"Art. {art} · selbst schaufeln · ca. {round(m * d)} kg", f"{m:g} m³", fmt(m * 60)) for i, (name, art, m, d) in enumerate(k['pos']))
    pct = min(100, k['kg'] / 900 * 100)
    kies.append(f'''<section class="trip kies"><header class="th"><div><h2>{k['key']} · Kieswerk Tägerhard</h2><p class="when">{KWANN[k['key']]} · für {esc(k['zweck'])}</p></div><div class="sum"><b>CHF {fmt(k['chf'])}</b><span>{k['kg']} kg</span></div></header>
<div class="load" role="img" aria-label="Ladung {k['kg']} von 900 kg"><div class="bar" style="width:{pct:.0f}%"></div><span>{k['kg']} / 900 kg</span></div>
<ul class="items">{rows}</ul></section>''')

gek = []
for key, g in F['gekauft'].items():
    li = ''.join(f'<li class="done"><span class="ok" aria-hidden="true">✓</span><span class="nm">{esc(p["name"])}</span><span class="q">{p["menge"]} {esc(p["eh"])}</span><span class="p">{fmt(p["chf"])}</span></li>' for p in g['pos'])
    gek.append(f'<details><summary><b>Fahrt {key} · {esc(g["ort"])}</b><span>CHF {fmt(g["chf"])} bezahlt</span></summary><ul class="donelist">{li}</ul></details>')

haus_namen = ['Maurerschnur', 'Staubmaske FFP2/FFP3', 'Schutzbrille', 'Gehörschutz', 'Löschdecke', 'Metall-Ascheeimer mit Deckel',
              '3 Planen 4 × 5 m', 'Spanngurte + Antirutschmatte', '2 Schaufeln, Spaten, Schubkarre, Rechen', 'Wasserwaage, Rollmeter, Richtlatte 2 m',
              'Handsäge, Akkuschrauber + 3-mm-Bohrer', 'Winkelschleifer 125 mm', 'Gummihammer, Hammer, Meissel, Zange', 'Gartenschlauch mit Brause',
              'alte Decken (Frostschutz)', 'Zeitungen, Klebeband, Karton']
haus = ''.join(item(f'h{i}', n, '', '', '') for i, n in enumerate(haus_namen))
vorher = ['OBI Basel anrufen (058 329 11 00): 21 Schamottsteine Art. 5390067 zurücklegen lassen',
          'Zuhause zählen: Planen (3 nötig), Spanngurte, Antirutschmatte, Handschuhe. Was fehlt, in Oftringen kaufen',
          'Bus leer, Antirutschmatte auf den Boden, 4 Gurte bereit',
          'Abfahrt spätestens 16:15 (Oftringen schliesst 19:00, Basel 20:00). Sonst Di 08:00',
          'Di 07:00 K1: die neuen Mörtelkästen und Eimer mitnehmen']
pre = ''.join(item(f'v{n}', t, '', '', '') for n, t in enumerate(vorher))
route = nav(ADR['A2'], ADR['A1'])
css = open(os.path.join(H, 'einkaufsliste.css')).read()
css += '''
.item.opt .nm em{font-style:normal;font-size:.72rem;color:var(--warn);border:1px solid currentColor;border-radius:4px;padding:0 4px;margin-left:6px;white-space:nowrap}
details{border-top:1px solid var(--line);padding:8px 0}details:first-of-type{border-top:0}
summary{cursor:pointer;display:flex;justify-content:space-between;gap:10px;list-style:none}summary::-webkit-details-marker{display:none}
summary span{color:var(--ok);font-variant-numeric:tabular-nums;font-size:.9rem}
summary:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.donelist{list-style:none;margin:6px 0 0;padding:0;display:grid}
.donelist li{display:grid;grid-template-columns:22px minmax(0,1fr) auto 64px;gap:8px;padding:5px 0;border-top:1px dashed var(--line);font-size:.86rem;color:var(--muted)}
.donelist .ok{color:var(--ok);font-weight:700}.donelist .q,.donelist .p{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.routebtn{display:inline-block;background:var(--blue);color:#fff;font-weight:600;border-radius:8px;padding:8px 12px;text-decoration:none;justify-self:start}
.stand{font-size:.85rem;color:var(--muted)}
#confirm[hidden],#reset[hidden]{display:none}
.trip.kies .when{color:var(--muted)}
'''
page = f'''<title>Pizzaofen Einkaufsliste</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{css}</style>
<main class="wrap">
<header><h1>Pizzaofen Einkaufsliste</h1><p class="lede">Fassung 5 · Stand Mo 19.10.2026 · Lagerbestand OBI live geprüft {esc(F['bestand_zeit'])} Uhr · Preise inkl. MWST</p></header>
<div class="kpis"><div class="kpi"><span>Schon bezahlt</span><b>CHF {fmt(SU['bezahlt'])}</b></div><div class="kpi"><span>Noch offen</span><b>CHF {fmt(SU['offen_min'])}</b></div><div class="kpi"><span>Total</span><b>CHF {fmt(SU['total_min'])}</b></div></div>
<p class="stand">Mit allen Extras (Planen, Gurte, Antirutschmatten, Handschuhe) noch offen CHF {fmt(SU['offen_max'])}, total CHF {fmt(SU['total_max'])}. Reserve bis CHF 2000: mindestens CHF {fmt(2000 - SU['total_max'])}.</p>
<p class="warn"><b>Wichtig:</b> OBI Oftringen hat keine Schamottsteine mehr (heute 0, am 13.10. noch 25). Die 21 fehlenden Steine gibt es nur noch in <b>OBI Basel Dreispitz</b>. Darum geht die Fahrt über Oftringen nach Basel.</p>
<section class="box"><h2>Vor dem Losfahren</h2><ul class="items">{pre}</ul><a class="routebtn" href="{esc(route)}" target="_blank" rel="noopener">Ganze Route: Oftringen → Basel (Google Maps)</a></section>
{''.join(cards)}
<p class="warn"><b>Max. 900 kg pro Fahrt:</b> Mit Kat. B darf der beladene Bus sein Gesamtgewicht im Ausweis nicht überschreiten. Schwere Last nach vorne an die Trennwand, flach laden, Antirutschmatte, 4 Gurte.</p>
<section class="box"><h2>Kieswerk Tägerhard · 4 Fahrten</h2><p class="note">Tägerhardstrasse 151, 5430 Wettingen · Tel. <span class="sel">056 426 70 45</span> · Mo–Fr 07:00–12:00, 13:00–16:45 · selbst schaufeln, CHF 60.–/m³ · <a class="nav" href="{esc(nav(ADR['K']))}" target="_blank" rel="noopener">Navigation</a><br>Mitnehmen: 6 Mörtelkästen + 10 Eimer (630 l), 2 Schaufeln. Bei K1 fragen, ob alle Fahrten als ein Bezug abgerechnet werden.</p></section>
{''.join(kies)}
<section class="box"><h2>Schon gekauft · CHF {fmt(SU['bezahlt'])}</h2>{''.join(gek)}</section>
<section class="box"><h2>Von zuhause (nur abhaken)</h2><p class="note">Fehlt etwas: ausleihen oder auf der Fahrt in Oftringen kaufen.</p><ul class="items">{haus}</ul></section>
<section class="box"><h2>Wenn etwas fehlt</h2><p class="note">Schamottsteine in Basel unter 21 → Rest in OBI Volketswil (9) oder Winterthur (3) · Stampfer in Oftringen weg → Basel (4) · Zement in Oftringen leer → Basel (über 300) · Schamottplatten → Volketswil (7) oder Winterthur (13) · Perlit → Winterthur (7) · Kieswerk lässt nicht selbst schaufeln → Big Bag füllen lassen und vor Ort umschaufeln.</p></section>
<div class="foot"><p class="note">Häkchen werden nur auf diesem Gerät gespeichert.</p><div><button id="reset" type="button">Alle Häkchen löschen</button><span id="confirm" hidden>Wirklich? <button id="yes" type="button" class="copy">Ja, löschen</button><button id="no" type="button" class="copy">Abbrechen</button></span></div></div>
</main>
<script>
(function(){{
 var KEY='pizzaofen-einkauf-v5', st={{}};
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
print('ok', SU)
