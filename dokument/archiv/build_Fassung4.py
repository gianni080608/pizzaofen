#!/usr/bin/env python3
"""Bauplan_v4.md (Vorlage) + Berechnungen -> Bauplan_Pizzaofen.md (Fassung 4, Bauanleitung)."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(H, '..', 'berechnung'); Zd = os.path.join(H, '..', 'zeichnungen')
S = json.load(open(os.path.join(B, 'stueckliste.json'))); E = json.load(open(os.path.join(B, 'ergebnis.json')))
CAD = json.load(open(os.path.join(Zd, 'cad.json')))
K = E[S['d']]['kuppel']
R = {r['id']: r for r in S['rows']}
def chf(x): return f"{x:,.2f}".replace(',', "'")
# Stand 14.10.: B und C bezahlt ohne die weggelassenen Artikel, A mit 21 statt 25 Schamottsteinen
WEG_B = ['O21', 'O27', 'O28', 'O29']                      # Mauerschnur, FFP3, Brillen, Gehoerstoepsel
WEG_C = ['O11', 'O35', 'O36']                             # Kaminrohr (Kollege), Loeschdecke, Ascheeimer
tour = {t['key']: t for t in S['touren']}
b = tour['B']['chf'] - sum(R[i]['gp'] for i in WEG_B)
c = tour['C']['chf'] - sum(R[i]['gp'] for i in WEG_C)
a_max = tour['A']['chf'] - 4 * R['O07']['ep']
OPTIONAL = ['O25', 'O26', 'O18', 'O30', 'O31']            # Gurte, Antirutsch, Planen, Handschuhe, Stampfer
a_min = a_max - sum(R[i]['gp'] for i in OPTIONAL)
kies = round((1.03 + 0.10 + 0.12) * 60, 2)
ph = dict(B=chf(b), C=chf(c), A_MIN=chf(a_min), A_MAX=chf(a_max), KIES=chf(kies), TOTAL_MIN=chf(b + c + a_min + kies), TOTAL_MAX=chf(b + c + a_max + kies))
s = open(os.path.join(H, 'Bauplan_v4.md')).read()
for k, v in ph.items():
    s = s.replace('{{' + k + '}}', v)
# Backboden-Zuschnitt je Platte
st = CAD['backboden']['stuecke']
by = {}
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
        rows.append(f"| {q} | {', '.join(t for t in teile)} | {', '.join(sorted(set('R' + str(p['reihe']) for p in ps)))} |")
bb = (f"**Zuschnittliste – {CAD['backboden']['platten']} Platten** (Stücke in cm, Länge × Breite; danach den Kreisrand nach der Schnur nachschneiden):\n\n" + '\n'.join(rows))
s = s.replace('<!--BACKBODEN-->', bb)
rr = ['| Reihe | Höhe innen (cm) | Radius innen (cm) | Neigung Lagerfuge | Halbsteine | Teilung |', '|---|---|---|---|---|---|']
for r in K['reihen']:
    n = r['halbsteine'] + r['tuerabzug']
    rr.append(f"| R{r['reihe']} | {r['z_innen_von']}–{r['z_innen_bis']} | {r['r_innen']} | {r['neigung_grad']:.0f}° | **{r['halbsteine']}**" + (f" (+{r['tuerabzug']} Tür frei)" if r['tuerabzug'] else '') + f" | {360 / n:.1f}° |")
rr.append(f"| Schluss | {K['reihen'][-1]['z_innen_bis']}–36 | – | – | **{K['schluss_halbsteine']}** (zugeschnitten) | – |")
s = s.replace('<!--REIHEN-->', '\n'.join(rr))
assert '{{' not in s and '<!--' not in s
open(os.path.join(H, 'Bauplan_Pizzaofen.md'), 'w').write(s)
print('ok', ph)
