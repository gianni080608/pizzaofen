#!/usr/bin/env python3
"""Fuellt Bauplan_vorlage.md mit Werten/Tabellen aus ../berechnung/*.json -> Bauplan_Pizzaofen.md (Fassung 2)"""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(H, '..', 'berechnung')
L = lambda f: json.load(open(os.path.join(B, f)))
E, S, VA, BE, WX = L('ergebnis.json'), L('stueckliste.json'), L('varianten.json'), L('obi_bestand.json'), L('wetter_2026-10-13.json')
V, U, K = E[S['d']], E['unterbau'], E[S['d']]['kuppel']
SU = S['summen']
def chf(x): return f"{x:,.2f}".replace(',', "'")
fp = S['fahrten']; TO = {t['key']: t for t in S['touren']}; PH = S['phasen']
ph = dict(GESAMT=chf(SU['gesamt_mit_werkzeug']), RESERVE=chf(2000 - SU['gesamt_mit_werkzeug']), BUDGET_MAT=chf(SU['material'] + SU['klein']),
          S_M=chf(SU['material']), S_K=chf(SU['klein']), S_G=chf(SU['gebinde']), S_S=chf(SU['schutz']), S_W=chf(SU['werkzeug']), S_B=chf(SU['betrieb']),
          GEWICHT_KG=f"{S['gewicht']:,.0f}".replace(',', "'"),
          TA=TO['A']['kg'], TB=TO['B']['kg'], TC=TO['C']['kg'], K1=TO['K1']['kg'], K2=TO['K2']['kg'], K3=TO['K3']['kg'], K4=TO['K4']['kg'],
          P1=chf(sum(t['chf'] for t in S['touren'] if t['phase'] == 1)), P2=chf(sum(t['chf'] for t in S['touren'] if t['phase'] == 2)),
          VOR=chf(sum(t['vorgezogen_chf'] for t in S['touren'])),
          MERIDIAN=K['meridian_cm'], RESTBOGEN=K['rest_bogen_cm'], SCHLUSS=K['schluss_halbsteine'], HALBE=K['halbsteine_reihen'], FLAECHE=K['kontrolle_flaeche_m2'],
          HALBE_KONTROLLE=K['halbsteine_flaechenkontrolle'], HALBE_V=V['halbsteine_mit_verschnitt'], NF_KUPPEL=V['nf_kuppel'], BODEN_M2=V['boden_m2'],
          MOERTEL_L=V['moertel_liter'], MOERTEL_KG=V['moertel_kg'], P_BODEN=V['perlit_mix_m3']['boden'], P_KUPPEL=V['perlit_mix_m3']['kuppel'],
          P_TUNNEL=V['perlit_mix_m3']['tunnel'], P_TOTAL=V['perlit_mix_m3']['total'], PERLIT_L=V['perlit_l'], Z_PERLIT=V['zement_perlit_kg'],
          BETON_M3=U['beton_total_m3'], Z_BETON=U['zement_beton_kg'], BETONKIES_KG=f"{U['betonkies_kg']:,}".replace(',', "'"), BETONKIES_M3=U['betonkies_m3_lose'],
          Z_PUTZ=V['zement_putz_kg'], Z_TOTAL=S['zement_total_kg'],
          D90_TOTAL=chf(VA['D90']['total']), D100_TOTAL=chf(VA['D100']['total']), A_TOTAL=chf(VA['A']['total']), A_KIT=chf(VA['A']['kit_chf']),
          C_TOTAL=chf(VA['C']['total']), CUPPO=chf(VA['A']['cuppo90_chf']),
          DE_BRUTTO=chf(VA['DE_Waldshut']['brutto_eur']), DE_NETTO=chf(VA['DE_Waldshut']['netto_eur']), DE_CHF=chf(VA['DE_Waldshut']['chf']),
          DE_MIT=chf(VA['DE_Waldshut']['mit']), DE_OHNE=chf(VA['DE_Waldshut']['ohne']), DE_CH=chf(VA['DE_Waldshut']['ch']),
          DE_DIFF=chf(VA['DE_Waldshut']['ch'] - VA['DE_Waldshut']['mit']), DE_ONLINE=chf(VA['DE_online']['total_chf']), DE_WERT=chf(VA['DE_online']['wert_ch']))
for k in ('D80', 'D90', 'D100'):
    v = VA[k]
    ph.update({f'{k}_FL': v['backflaeche'], f'{k}_AD': v['aussen'], f'{k}_TUN': v['tunnel'], f'{k}_NFK': v['nf_kauf'], f'{k}_M': round(v['masse']), f'{k}_KWH': v['kwh']})
s = open(os.path.join(H, 'Bauplan_vorlage.md')).read()
for k, v in ph.items():
    s = s.replace('{{' + k + '}}', str(v))
assert '{{' not in s, re.findall(r'\{\{[A-Z0-9_]+\}\}', s)
KAT = dict(M='Material', K='Kleinmaterial', G='Gebinde', S='Schutz', W='Werkzeug', B='Brandschutz')
best = BE['artikel']
def bestand_txt(r):
    if r['quelle'] != 'OBI': return 'Kieswerk: Bezug immer möglich'
    parts = []
    for mk, m in r['bezug'].items():
        key = r['art'] if len(r['bezug']) == 1 else f"{r['art']}@{mk}"
        b = best.get(key, {}).get('bestand', {}).get(mk, '?')
        parts.append(f"{mk}: {m} von {b}")
    return '; '.join(parts)
t = ['| Nr. | Kat. | Produkt (Art.-Nr.) | Spezifikation / Rechnung | Menge | CHF/Einheit | CHF total | Gewicht | Händler: Menge von Bestand | Quelle |', '|---|---|---|---|---|---|---|---|---|---|']
for r in S['rows']:
    t.append(f"| {r['id']} | {r['kat']} | {r['name']} ({r['art']}) | {r['spez']} | {r['menge']} {r['eh']} | {r['ep']:.2f} | **{r['gp']:.2f}** | {r['kg_einheit']} kg × {r['menge']} = {r['kg']:.0f} kg | {bestand_txt(r)} | [Link]({r['url']}) |")
s = s.replace('<!--STUECKLISTE-->', '\n'.join(t))
rr = ['| Reihe | Höhe innen | Radius innen | Neigung Lagerfuge | Halbsteine |', '|---|---|---|---|---|']
for r in K['reihen']:
    rr.append(f"| {r['reihe']} | {r['z_innen_von']}–{r['z_innen_bis']} cm | {r['r_innen']} cm | {r['neigung_grad']}° | **{r['halbsteine']}**" + (f" (−{r['tuerabzug']} Tür)" if r['tuerabzug'] else '') + ' |')
rr.append(f"| Schluss | {K['reihen'][-1]['z_innen_bis']}–{V['h']} cm | – | – | **{K['schluss_halbsteine']}** (zugeschnitten) |")
s = s.replace('<!--REIHEN-->', '\n'.join(rr))
fahrt_von = lambda r: ', '.join(t['key'] for t in S['touren'] if any(p['id'] == r['id'] for p in t['pos']))
kgf = lambda x: f'{x:,}'.replace(',', "'")
ORTN = {'oftringen': 'OBI Oftringen', 'volketswil': 'OBI Volketswil', 'kies': 'Kieswerk Tägerhard'}
tt = [f"| **{t['key']}** | {t['tag']} {t['zeit']} | {ORTN[t['ort']]} | {t['phase']} · {'Sockel' if t['phase'] == 1 else 'Ofen'} | {kgf(t['kg'])} kg | {chf(t['chf'])}" + (f" (davon Ofen vorgezogen {chf(t['vorgezogen_chf'])})" if t['vorgezogen_chf'] else '') + ' |' for t in S['touren']]
s = s.replace('<!--TOUREN-->', '\n'.join(tt))
g = ['| Position | Stückgewicht | Menge | Gewicht | Fahrt |', '|---|---|---|---|---|'] + [f"| {r['name']} | {r['kg_einheit']} kg/{r['eh']} | {r['menge']} {r['eh']} | **{r['kg']:.0f} kg** | {fahrt_von(r)} |" for r in sorted(S['rows'], key=lambda r: -r['kg']) if r['kg'] >= 1]
g.append(f"| übrige Kleinteile (< 1 kg je Position) | – | – | {sum(r['kg'] for r in S['rows'] if r['kg'] < 1):.1f} kg | A, B, C |")
g.append('')
g.append('| Fahrt | Gewicht | Planungsgrenze 900 kg |'); g.append('|---|---|---|')
for k2, v2 in fp.items(): g.append(f"| {k2} | **{v2:.0f} kg** | {'✔' if v2 <= 900 else '✘'} |")
s = s.replace('<!--GEWICHTE-->', '\n'.join(g))
h = ['| Werkzeug | vorhanden? | sonst kaufen (OBI Volketswil) | CHF | Bestand |', '|---|---|---|---|---|'] + [f"| {x['name']} | ☐ | Art. {x['art']} | {x['gp']:.2f} | {x['bestand']} |" for x in S['haus']]
h.append(f"| **Alle fehlen (Maximum)** | | | **{SU['haus_falls_fehlend']:.2f}** | |")
h.append('')
h.append(f"**Regel:** Für jedes fehlende Werkzeug fragt ihr zuerst Familie, Nachbarn oder den Lehrbetrieb. Wenn das bis 15:30 nicht klappt, kauft ihr es. Bis CHF {2000 - SU['gesamt_mit_werkzeug']:.2f} bleibt ihr unter 2000. Fehlt mehr, gilt die Sparliste 10.2 (Rührwerk, Stampfer, Kellen ausleihen spart CHF 175.90).")
s = s.replace('<!--HAUS-->', '\n'.join(h))
bud = ['| Bereich | CHF |', '|---|---|',
       f"| Material (Steine, Platten, Mörtel, Dämmung, Kaminrohr, Tür, Sockel, Beton, Kies) | {chf(SU['material'])} |",
       f"| Kleinmaterial | {chf(SU['klein'])} |",
       f"| Gebinde und Ladungssicherung | {chf(SU['gebinde'])} |",
       f"| Schutzausrüstung | {chf(SU['schutz'])} |",
       f"| Werkzeug (Stampfer, Rührwerk, Kellen) | {chf(SU['werkzeug'])} |",
       f"| Brandschutz Betrieb (Löschdecke, Ascheeimer) | {chf(SU['betrieb'])} |",
       f"| **Total Variante B, alles inklusive** | **{chf(SU['gesamt_mit_werkzeug'])}** |",
       f"| **Reserve bis CHF 2000** | **{chf(2000 - SU['gesamt_mit_werkzeug'])}** |",
       f"| nur falls Haushaltswerkzeug fehlt (max.) | {chf(SU['haus_falls_fehlend'])} |",
       f"| Variante C (Werkzeug ausgeliehen) | {chf(VA['C']['total'])} |",
       '', 'Nicht im Budget: Benzin (ca. 330 km insgesamt, ca. CHF 50), Brennholz.',
       '', '**Nach Händler:**', '', '| Händler | CHF | kg |', '|---|---|---|']
by = {}
for r in S['rows']:
    for mk, m in r['bezug'].items():
        by.setdefault(mk, [0, 0]); by[mk][0] += m * r['ep']; by[mk][1] += m * r['kg_einheit']
for mk, (c, kg) in by.items(): bud.append(f"| {mk} | {chf(c)} | {kg:.0f} |")
s = s.replace('<!--BUDGET-->', '\n'.join(bud))
d = WX['daily']; W = ['| Datum | max °C | min °C | Regen mm | Regenrisiko | Eignung Beton/Mörtel |', '|---|---|---|---|---|---|']
wt = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
import datetime
for i, day in enumerate(d['time']):
    dt = datetime.date.fromisoformat(day); mn = d['temperature_2m_min'][i]
    ok = '✔' if mn >= 5 else ('⚠ abdecken' if mn >= 0 else '✘')
    p = d['precipitation_probability_max'][i]
    W.append(f"| {wt[dt.weekday()]} {dt.day}.{dt.month}. | {d['temperature_2m_max'][i]} | {mn} | {d['precipitation_sum'][i]} | {'–' if p is None else str(p) + ' %'} | {ok} |")
W.append(''); W.append('Ab Tag 8 ist die Prognose unsicher. Deshalb gilt für jeden Arbeitstag mit Zement die Regel 7.3.')
s = s.replace('<!--WETTER-->', '\n'.join(W))
Q = [
 ('OBI Schweiz: Produktseiten aller Positionen (Links in der Stückliste) und Bestandsschnittstelle /article-service/store-availabilities (Abfrage 13.10.2026, Rohdaten berechnung/obi_bestand.json)', 'https://www.obi.ch/grillutensilien/schamottestein-hxbxt-64-x-124-x-250-mm/p/5390067'),
 ('OBI Markt Oftringen (Öffnungszeiten, Telefon)', 'https://www.obi.ch/markt/oftringen'),
 ('OBI Markt Volketswil (Öffnungszeiten, Telefon)', 'https://www.obi.ch/markt/volketswil'),
 ('OBI Märkte Winterthur, Schaffhausen, Basel (Plan B)', 'https://www.obi.ch/markt/'),
 ('OBI Preisliste Mietgeräte (Vergleich Miete/Kauf)', 'https://www.obi.ch/public/specials/baumarkt-services/assets/pdf/preisliste-obi-mietgeraete-ch-de.pdf'),
 ('Tägerhard Kies AG: Preisliste 2026 inkl. Bar-/Privatpreise, Öffnungszeiten, Telefon', 'https://taegerhardkies.ch/wp-content/uploads/2025/12/Grundpreisliste-2026.pdf'),
 ('KANN Schalungsstein: Datenblatt (Füllbeton 121 l/m² bei 24 cm), via Globus', 'https://www.globus-baumarkt.de/media/cb/95/54/1665251341/4024991601493_dc847960a23b1cafd629351c02a0a124__105497131.pdf'),
 ('Open-Meteo: 16-Tage-Prognose Würenlos (47.443 N / 8.366 E), Rohdaten berechnung/wetter_2026-10-13.json', 'https://api.open-meteo.com/v1/forecast?latitude=47.4429&longitude=8.3661&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=Europe%2FZurich&forecast_days=16'),
 ('MeteoSchweiz: Klimanormwerte 1991–2020', 'https://data.geo.admin.ch/ch.meteoschweiz.klima/normwerte/normwerte.zip'),
 ('OBI Deutschland: Markt Waldshut-Tiengen; Firefix Schamottstein €9.49', 'https://www.obi.de/p/2269678/firefix-schamottstein-250-mm-x-124-mm-x-64-mm'),
 ('schamotte-shop.de: NF2 €4.29/€4.20 ab 10; Zahlung und Versand (Paket 0–150 kg €7.90–79.90)', 'https://www.schamotte-shop.de/zahlung-versand.html'),
 ('Lieferadresse Konstanz: Preisliste Paketannahme', 'https://lieferadresse-konstanz.ch/'),
 ('kuppelofen.de: Les Cheminées FD-Serie ab €1’149; CS-Platte €60; Keramikfaser €80; Schamottemörtel €45', 'https://www.kuppelofen.de/les-cheminees-fd-serie/'),
 ('holz-feuer.shop: CUPPO 90 €2’220 + €150 Spedition', 'https://holz-feuer.shop/products/cuppo-pizzaofen-bausatz'),
 ('pizzaofenbau.ch: Bausätze CHF 3’490–5’490 (Suchindex)', 'https://www.pizzaofenbau.ch/bausatz/'),
 ('TheFiredome: 2026 keine neuen Bausätze', 'https://www.thefiredome.ch/'),
 ('BAZG: Wertfreigrenze CHF 150, MWST 8.1 %', 'https://www.bazg.admin.ch/de/wertfreigrenze-mehrwertsteuer-einreise-150-franken'),
 ('BAZG: App QuickZoll', 'https://www.bazg.admin.ch/de/quickzoll-app-waren-anmelden-private'),
 ('Ratgeber Ausfuhrschein (Bagatellgrenze €50.01)', 'https://lieferadresse-konstanz.ch/mehrwertsteuer-zurueckholen-so-klappts-fuer-schweizer/'),
 ('EZB-Referenzkurse (1 EUR = 0.9312 CHF, 12.10.2026)', 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'),
 ('Kanton Aargau: Bauverordnung (SAR 713.121), §§ 19, 49', 'https://gesetzessammlungen.ag.ch/app/de/texts_of_law/713.121'),
 ('Gemeinde Würenlos: Bauverwaltung', 'https://www.wuerenlos.ch/verwaltung/bauverwaltung/bauverwaltung/'),
 ('ADAC Autokatalog: Fiat Talento L2H2 1.2t (Leergewicht 1965 kg, zGG 3060 kg)', 'https://www.adac.de/rund-ums-fahrzeug/autokatalog/marken-modelle/fiat/talento/296/308458'),
 ('Fedlex: VTS (Leergewicht inkl. Führer 75 kg)', 'https://www.fedlex.admin.ch/eli/cc/1995/4425_4425_4425/de'),
 ('Kanton Aargau: Merkblatt Führerausweis Kategorie B', 'https://ag.ch/media/kanton-aargau/dvi/dokumente/stva/fuehrerausweise/ausweiskategorien/kategorie-b-03072024.pdf'),
 ('OpenStreetMap Nominatim / OSRM: Distanzen und Fahrzeiten', 'https://router.project-osrm.org/'),
]
s = s.replace('<!--QUELLEN-->', '\n'.join(f'{i}. {a}: <{u}>' for i, (a, u) in enumerate(Q, 1)))
open(os.path.join(H, 'Bauplan_Pizzaofen.md'), 'w').write(s)
print('ok', len(s))
