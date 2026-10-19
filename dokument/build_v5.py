#!/usr/bin/env python3
"""Bauplan_v5.md (Vorlage) + Berechnungen -> Bauplan_Pizzaofen.md (Fassung 5, Bauanleitung).
Braucht: berechnung/ergebnis.json, berechnung/fassung5.json, zeichnungen/cad.json."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(H, '..', 'berechnung'); Zd = os.path.join(H, '..', 'zeichnungen')
E = json.load(open(os.path.join(B, 'ergebnis.json'))); F = json.load(open(os.path.join(B, 'fassung5.json')))
CAD = json.load(open(os.path.join(Zd, 'cad.json')))
V = E['D80']; K = V['kuppel']; SU = F['summen']; BD = F['bedarf']
def chf(x): return f"{x:,.2f}".replace(',', "'")
def num(x): return f"{x:g}"

ph = dict(BESTAND_ZEIT=F['bestand_zeit'] + ' Uhr', BEZAHLT=chf(SU['bezahlt']), TOTAL_MIN=chf(SU['total_min']), TOTAL_MAX=chf(SU['total_max']),
          ZEMENT_KAUF=str(F['zement_kauf']), ZEMENT_KG=f"{F['zement']['total_kg']:.0f}", ZEMENT_KAUF_KG=str(F['zement_kauf'] * 25),
          ZEMENT_RESERVE=f"{F['zement_kauf'] * 25 - F['zement']['total_kg']:.0f}")
s = open(os.path.join(H, 'Bauplan_v5.md')).read()
for k, v in ph.items():
    s = s.replace('{{' + k + '}}', v)

# 2.1 Mengenbilanz
gek = {}
for t in F['gekauft'].values():
    for p in t['pos']:
        gek[p['id']] = gek.get(p['id'], 0) + p['menge']
kauf = {}
for t in F['fahrt_a']:
    for p in t['pos']:
        if p['pflicht']:
            kauf[p['id']] = kauf.get(p['id'], 0) + p['menge']
kies = {}
for t in F['kies']:
    for name, art, m, d in t['pos']:
        kies[name] = round(kies.get(name, 0) + m, 2)
rows = [
    ('Schamottstein NF 250 × 124 × 64', f"{BD['nf']} ({BD['halbsteine']} Halbsteine) + Reserve", gek['O07'], kauf['O07'], f"{gek['O07'] + kauf['O07']} = {2 * (gek['O07'] + kauf['O07'])} Halbsteine"),
    ('Schamottplatte 40 × 200 × 500', f"{BD['platten']} (11 Boden, 5 Tunnelstreifen, 2 Deckplatten)", gek['O08'], kauf['O08'], f"{gek['O08'] + kauf['O08']}, 1 Reserve"),
    ('Zement CEM I 42.5 N, 25 kg', f"{F['zement']['total_kg']:.0f} kg", 0, kauf['O01'], f"{kauf['O01'] * 25} kg"),
    ('Pflanzen-Perlit 100 l', f"{V['perlit_l']} l = {BD['perlit_sack']} Sack", gek['O10'], kauf['O10'], f"{(gek['O10'] + kauf['O10']) * 100} l"),
    ('Sakret Schamottmörtel 5 kg', f"{V['moertel_kg']:.0f} kg", gek['O09'], 0, f"{gek['O09'] * 5} kg"),
    ('Kann Schalungsstein 24 cm', '25 (24 + 1 zum Halbieren)', gek['O02'], 0, '26, 1 Reserve'),
    ('Baustahlmatte R188A / Estrichgitter', '2 / 2', '2 / 2', '–', 'ok'),
    ('OSB 18 mm / Schalbrett 3 m / Brett 2 m', '2 / 3 / 4', '2 / 3 / 4', '–', 'ok'),
    ('Sechseckgeflecht', f"{V['putz_m2']:.1f} m²", '1 Rolle 10 m²', '–', 'ok'),
    ('Firefix Rauchrohr Ø 150, 1 m', '1', 0, kauf['O11'], 'neu'),
    ('Glattblech 500 × 1000', '1 (Tür, Kaminabdeckung)', 0, kauf['O13'], ''),
    ('Mörtelkasten 90 l / Mörteleimer 20 l', '6 / 10', '0 / 0', f"{kauf['O23']} / {kauf['O24']}", ''),
    ('Betonstampfer', '1 (Kieskoffer)', 0, kauf['O31'], 'neu Pflicht'),
    ('Betonkies 0/16', f"{BD['betonkies_m3']} m³ (25 Mischungen)", 0, f"{kies['Betonkies gewaschen 0/16']} m³", 'Kieswerk'),
    ('Kiesgemisch 0/31.5', f"{BD['kiesgemisch_m3']} m³ (Koffer 15 cm)", 0, f"{kies['Kiesgemisch 0/31.5']} m³", 'Kieswerk'),
    ('Sand 0/4 gewaschen', f"{BD['sand_m3']:.2f} m³ (Mörtelbett, Sandbett, Putz)", 0, f"{kies['Sand gewaschen 0/4']} m³", 'Kieswerk; Sandform aus dem Aushub'),
]
t = ['| Material | Bedarf | schon da | noch kaufen | danach |', '|---|---|---|---|---|']
for r in rows:
    t.append('| ' + ' | '.join(str(x) for x in r) + ' |')
s = s.replace('<!--BILANZ-->', '\n'.join(t))

# 2.2 gekauft
t = []
for key, g in F['gekauft'].items():
    t.append(f"**Fahrt {key} – {g['ort']}: CHF {chf(g['chf'])} (bezahlt)**\n")
    t.append('| Artikel | Art.-Nr. | Menge | CHF |'); t.append('|---|---|---|---|')
    for p in g['pos']:
        t.append(f"| {p['name']} | {p['art']} | {p['menge']} {p['eh']} | {chf(p['chf'])} |")
    t.append('')
zh = ', '.join(p['name'].replace('LUX ', '').split(',')[0] for p in F['zuhause'])
t.append(f"**Bewusst nicht gekauft, weil ihr es zuhause habt:** {zh}. Fehlt davon etwas, nehmt es auf der Fahrt nach Oftringen mit.")
s = s.replace('<!--GEKAUFT-->', '\n'.join(t))

# 2.3 Fahrt A
t = []
for f in F['fahrt_a']:
    t.append(f"**{f['key']} – {f['ort']}** · {f['adr']} · Tel. {f['tel']} · {f['oeffnung']} · {f['weg']}\n")
    t.append('| Artikel | Art.-Nr. | Menge | Bestand heute | CHF | wozu |'); t.append('|---|---|---|---|---|---|')
    for p in f['pos']:
        opt = '' if p['pflicht'] else ' *(nur falls nötig)*'
        t.append(f"| {p['name']}{opt} | {p['art']} | **{p['menge']} {p['eh']}** | {p['bestand']} | {chf(p['chf'])} | {p['warum']} |")
    t.append(f"| **Summe** | | | | **{chf(f['chf_pflicht'])}**" + (f" (mit allem {chf(f['chf_alles'])})" if f['chf_alles'] != f['chf_pflicht'] else '') + " | |")
    t.append('')
s = s.replace('<!--FAHRT_A-->', '\n'.join(t))

# 2.4 Kies
DAT = {'K1': 'Di 20.10. 07:00', 'K2': 'Do 22.10. 07:00', 'K3': 'Fr 23.10. 07:00', 'K4': 'Mo 26.10. 07:00'}
t = ['| Fahrt | Wann | Ladung | Gewicht | CHF | für |', '|---|---|---|---|---|---|']
for k in F['kies']:
    lad = ' + '.join(f"{name} **{num(m)} m³**" for name, art, m, d in k['pos'])
    t.append(f"| {k['key']} | **{DAT[k['key']]}** | {lad} | {k['kg']} kg | {chf(k['chf'])} | {k['zweck']} |")
t.append(f"| **Total** | | | | **{chf(SU['kies'])}** | |")
s = s.replace('<!--KIES-->', '\n'.join(t))

# S8 Backboden
st = CAD['backboden']['stuecke']; by = {}
for p in st:
    by.setdefault(p['quelle'], []).append(p)
rows = ['| Platte | daraus schneiden | für Reihe |', '|---|---|---|']
for q in sorted(by, key=lambda x: int(x[1:])):
    ps = by[q]
    if all(p['ganz'] for p in ps):
        rows.append(f"| {q} | ganze Platte 50 × 20 (nur Kreisrand nachschneiden) | R{ps[0]['reihe']} |")
    else:
        teile = []
        for p in ps:
            teile.append(f"{p['l']:g} × {p['w']:g}" + (' (aus einem 30 × 20-Stück 2 Streifen à 3 cm längs)' if p['w'] < 19.9 and p is ps[-1] and sum(1 for x in ps if x['w'] < 19.9) == 2 else ''))
        rows.append(f"| {q} | {', '.join(teile)} | {', '.join(sorted(set('R' + str(p['reihe']) for p in ps)))} |")
s = s.replace('<!--BACKBODEN-->', f"**Zuschnittliste – {CAD['backboden']['platten']} Platten** (Stücke in cm, Länge × Breite; danach den Kreisrand nach der Schnur nachschneiden):\n\n" + '\n'.join(rows))

# S9 Keile
kz = []
for r in K['reihen']:
    if r['zuschnitt_seite'] >= 0.5:
        kz.append(f"| R{r['reihe']} | {r['halbsteine']} | **{num(r['breite_oben'])} cm** | {num(r['zuschnitt_seite'])} cm |")
    else:
        kz.append(f"| R{r['reihe']} | {r['halbsteine']} | 12.5 (kein Zuschnitt) | – |")
kz.append(f"| Schluss | {K['schluss_halbsteine']} | Viertelkreis r ≈ {K['rest_radius_cm'] + 0.5:.0f} | – |")
kz.append(f"| **Total** | **{K['halbsteine_reihen']}** | Reserve {70 - K['halbsteine_reihen']} | |")
s = s.replace('<!--KEILE-->', '\n'.join(kz))

# S12 Reihen
rr = ['| Reihe | Höhe innen (cm) | Radius innen unten → oben | Neigung Lagerfuge | Halbsteine | Breite oben |', '|---|---|---|---|---|---|']
for r in K['reihen']:
    br = f"{num(r['breite_oben'])} (je Seite {num(r['zuschnitt_seite'])} weg)" if r['zuschnitt_seite'] >= 0.5 else '12.5'
    rr.append(f"| R{r['reihe']} | {num(r['z_innen_von'])}–{num(r['z_innen_bis'])} | {num(r['r_unten'])} → {num(r['r_oben'])} | {r['neigung_grad']:.0f}° | **{r['halbsteine']}**" + (' + Tür 40' if r['tuer'] else '') + f" | {br} |")
rr.append(f"| Schluss | {num(K['rest_z_cm'])}–36 | Öffnung Ø ca. {2 * K['rest_radius_cm']:.0f} | – | **{K['schluss_halbsteine']}** Viertelkreise | – |")
s = s.replace('<!--REIHEN-->', '\n'.join(rr))

# 9 Kosten
fa = {f['key']: f for f in F['fahrt_a']}
opt = round(SU['fahrt_a_max'] - SU['fahrt_a_min'], 2)
t = ['| Posten | Status | CHF |', '|---|---|---|',
     f"| Volketswil Fahrt B | bezahlt | {chf(SU['bezahlt_B'])} |",
     f"| Volketswil Fahrt C | bezahlt | {chf(SU['bezahlt_C'])} |",
     f"| **Schon ausgegeben** | | **{chf(SU['bezahlt'])}** |",
     f"| Oftringen (A1, ohne Extras) | offen | {chf(fa['A1']['chf_pflicht'])} |",
     f"| Basel (A2) | offen | {chf(fa['A2']['chf_pflicht'])} |",
     f"| Extras, nur falls nicht zuhause (Planen, Gurte, Antirutsch, Handschuhe) | offen | 0.00 bis {chf(opt)} |",
     f"| Kieswerk K1–K4 (1.80 m³ à CHF 60) | offen | {chf(SU['kies'])} |",
     f"| **Noch auszugeben** | | **{chf(SU['offen_min'])} bis {chf(SU['offen_max'])}** |",
     f"| **Total Pizzaofen** | | **{chf(SU['total_min'])} bis {chf(SU['total_max'])}** |",
     f"| Reserve bis CHF 2000 | | {chf(2000 - SU['total_max'])} bis {chf(2000 - SU['total_min'])} |"]
s = s.replace('<!--KOSTEN-->', '\n'.join(t))

assert '{{' not in s and '<!--' not in s, [l for l in s.splitlines() if '{{' in l or '<!--' in l]
open(os.path.join(H, 'Bauplan_Pizzaofen.md'), 'w').write(s)
print('ok', ph)
