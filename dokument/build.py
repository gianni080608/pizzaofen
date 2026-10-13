#!/usr/bin/env python3
"""Fuellt Bauplan_vorlage.md mit Werten/Tabellen aus ../berechnung/*.json -> Bauplan_Pizzaofen.md"""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(H, '..', 'berechnung')
E = json.load(open(os.path.join(B, 'ergebnis.json'))); S = json.load(open(os.path.join(B, 'stueckliste.json')))
VA = json.load(open(os.path.join(B, 'varianten.json'))); HO = json.load(open(os.path.join(H, '..', 'zeichnungen', 'hoehen.json')))
V, U, K = E['D90'], E['unterbau'], E['D90']['kuppel']
def chf(x): return f"{x:,.2f}".replace(',', "'")
WORDS = [('Taegerhard','Tägerhard'),(' m3',' m³'),('/m3','/m³'),('m2','m²'),(' x ',' × '),('->','→'),(' - ',' – '),(' x1.25',' × 1.25'),('lt. ','laut '),('n.v.','nicht verfügbar'),('waehrend','während'),('Sockelfuellung','Sockelfüllung'),('Qualitaet','Qualität'),('Ofentuer','Ofentür'),('Daemm','Dämm'),('bestaetigen','bestätigen'),('unbestaetigt','unbestätigt'),('pruefen','prüfen'),('Moertel','Mörtel'),
 ('moertel','mörtel'),('Daemmung','Dämmung'),('Stuetzen','Stützen'),('Tuer','Tür'),('saegerau','sägerau'),('verfuegbar','verfügbar'),
 ('Fuellbeton','Füllbeton'),('Fuellung','Füllung'),('Mietgeraet','Mietgerät'),('Koernung','Körnung'),('Putztraeger','Putzträger'),
 ('Haendler','Händler'),('naeher','näher'),('spaeter','später'),('Plaene','Pläne'),('fuer','für'),('Laenge','Länge'),('Stueck','Stück'),
 ('Gebaeude','Gebäude'),('Schalungsstein','Schalungsstein'),('zugeschnitten','zugeschnitten'),('Waende','Wände'),('Rueck','Rück'),
 ('1000 C','1000 °C'),('1200 C','1200 °C'),('1260 C','1260 °C'),('>= ','≥ '),('Regenhut Ø','Regenhut Ø'),('Wochentarif','Wochentarif'),
 ('Ruettelplatte','Rüttelplatte'),('Erstellungsdatum','Erstellungsdatum'),('Steckeisen','Steckeisen'),('abgekantet','abgekantet'),
 ('halbieren','halbieren'),('Abschluss','Abschluss'),('gaengig','gängig'),('Oeffnung','Öffnung'),('Grosse','Grosse')]
def de(s):
    for a, b in WORDS:
        s = s.replace(a, b)
    return s
# --- Platzhalter
fp = S['fahrten']
ph = dict(GESAMT=chf(S['gesamt']), RESERVE=chf(S['reserve']), SUMME_MAT=chf(S['summe_material']), SUMME_MIET=chf(S['summe_mieten']),
          GEWICHT_KG=f"{S['gewicht_material']:,.0f}".replace(',', "'"), GEWICHT_T=f"{S['gewicht_material']/1000:.1f}",
          H_KAMIN=f"{HO['kamin_oben']:.0f}", H_KAMIN_RH=f"{HO['kamin_oben']+15:.0f}", H_BODEN=f"{HO['boden'][1]}",
          MERIDIAN=K['meridian_cm'], RESTBOGEN=K['rest_bogen_cm'], HALBE=K['halbsteine_reihen'], FLAECHE=K['kontrolle_flaeche_m2'],
          HALBE_KONTROLLE=K['halbsteine_flaechenkontrolle'], HALBE_V=V['halbsteine_mit_verschnitt'], NF_KUPPEL=V['nf_kuppel'],
          NF_TUNNEL=V['nf_tunnel'], NF_TOTAL=V['nf_total'], BODEN_M2=V['boden_m2'], MOERTEL_L=V['moertel_liter'], MOERTEL_KG=V['moertel_kg'],
          P_BODEN=V['perlit_mix_m3']['boden'], P_KUPPEL=V['perlit_mix_m3']['kuppel'], P_TUNNEL=V['perlit_mix_m3']['tunnel'], P_TOTAL=V['perlit_mix_m3']['total'],
          PERLIT_L=V['perlit_l'], Z_PERLIT=V['zement_perlit_kg'], KIES_M3=U['kies_lose_m3'], KIES_KG=f"{U['kies_kg']:,}".replace(',', "'"),
          BETON_M3=U['beton_total_m3'], Z_BETON=U['zement_beton_kg'], BETONKIES_KG=f"{U['betonkies_kg']:,}".replace(',', "'"), BETONKIES_M3=U['betonkies_m3_lose'],
          Z_PUTZ=V['zement_putz_kg'], Z_TOTAL=S['zement_total_kg'], PUTZ_M2=V['putz_m2'], PUTZ_M3=V['putz_m3'],
          F1=f"{fp['F1 HORNBACH Affoltern']:.0f}", F2=f"{fp['F2 OBI Volketswil']:.0f}", K1=fp['K1 Taegerhard'], K2=fp['K2 Taegerhard'], K3=fp['K3 Taegerhard'], K4=fp['K4 Taegerhard'],
          A_TOTAL=chf(VA['A']['total']), C_TOTAL=chf(VA['C']['total']), DE_MIT=chf(VA['DE_OBI_Waldshut']['total_mit_rueckerstattung']),
          DE_OHNE=chf(VA['DE_OBI_Waldshut']['total_ohne_rueckerstattung']), DE_ONLINE=chf(VA['DE_online_90']['total_chf']),
          D80_MINUS=chf(VA['C']['minus_80']))
for k in ('D80', 'D90', 'D100'):
    v = E[k]
    ph.update({f'{k}_FL': VA[k]['backflaeche_m2'], f'{k}_AD': v['aussendurchmesser'], f'{k}_NF': v['nf_total'], f'{k}_M': round(VA[k]['masse']),
               f'{k}_KWH': VA[k]['kwh'], f'{k}_TUN': v['tunnel_laenge']})
s = open(os.path.join(H, 'Bauplan_vorlage.md')).read()
for k, v in ph.items():
    s = s.replace('{{' + k + '}}', str(v))
assert '{{' not in s, re.findall(r'\{\{[A-Z0-9_]+\}\}', s)
# --- Tabellen
def link(u, t='Link'): return f'[{t}]({u})' if u.startswith('http') else '–'
rows = S['rows']
t = ['| Pos. | Produktbezeichnung | Spezifikation / Rechnung | Menge | Einzelpreis CHF | Gesamt CHF | Gewicht | Händler | Verfügbarkeit / Preisstatus | Quelle |', '|---|---|---|---|---|---|---|---|---|---|']
for r in rows:
    t.append(f"| {r['pos']} | {de(r['bez'])} | {de(r['spez'])} | {r['menge']} {de(r['eh'])} | {r['ep']:.2f} | **{r['gp']:.2f}** | {r['kg_einheit']} kg/{de(r['eh'])} × {r['menge']} = {r['kg']:.0f} kg | {de(r['haendler'])} | {de(r['verf'])}; {de(r['status'])} | {link(r['url'])} |")
for m in S['mieten']:
    t.append(f"| {m['pos']} | {de(m['bez'])} | {de(m['spez'])} | {m['menge']} {m['eh']} | {m['ep']:.2f} | **{m['gp']:.2f}** | ~{m['kg']} kg | {de(m['haendler'])} | Miete, Verfügbarkeit telefonisch prüfen | {link(m['url'], 'Preisliste')} |")
s = s.replace('<!--STUECKLISTE-->', '\n'.join(t))
o = ['| Pos. | Artikel | Hinweis | CHF | Quelle |', '|---|---|---|---|---|'] + [f"| {x['pos']} | {de(x['bez'])} | {de(x['spez'])} | {x['gp']:.2f} | {link(x['url'])} |" for x in S['optional']]
s = s.replace('<!--OPTIONAL-->', '\n'.join(o))
rr = ['| Reihe | Höhe innen (z) | Radius innen | Neigung Lagerfuge | Halbsteine (nach Türabzug) |', '|---|---|---|---|---|']
for r in K['reihen']:
    rr.append(f"| {r['reihe']} | {r['z_innen_von']}–{r['z_innen_bis']} cm | {r['r_innen']} cm | {r['neigung_grad']}° | **{r['halbsteine']}**" + (f" (−{r['tuerabzug']} Tür)" if r['tuerabzug'] else '') + ' |')
rr.append(f"| Schluss | {K['reihen'][-1]['z_innen_bis']}–40 cm | – | – | **{K['schluss_halbsteine']}** (zugeschnitten) |")
s = s.replace('<!--REIHEN-->', '\n'.join(rr))
g = ['| Position | Stückgewicht | Menge | Gewicht | Fahrt |', '|---|---|---|---|---|'] + [f"| {de(r['bez'])} | {r['kg_einheit']} kg/{de(r['eh'])} | {r['menge']} {de(r['eh'])} | **{r['kg']:.0f} kg** | {r['fahrt']} |" for r in sorted(rows, key=lambda r: -r['kg'])]
s = s.replace('<!--GEWICHTE-->', '\n'.join(g))
nh = S['nach_haendler']
bud = ['| Bereich | CHF |', '|---|---|',
       f"| Kieswerk Tägerhard (Kies, Betonkies, Sand) | {chf(nh['Taegerhard'][0])} |",
       f"| HORNBACH Affoltern (Schalungssteine, Zement, Matten, Mörtel, Kaminrohr, Drahtgeflecht) | {chf(nh['Hornbach'][0])} |",
       f"| OBI Volketswil (Schamott, Platten, Perlit, Zement, Schalung, Blech) | {chf(nh['OBI'][0])} |",
       f"| Kleinmaterial, Plane, Diamantscheibe (ANNAHME) | {chf(nh['Klein'][0])} |",
       f"| Mieten (Mischer 1 Woche, Rüttelplatte 1 Tag) | {chf(S['summe_mieten'])} |",
       f"| **Total Variante B** | **{chf(S['gesamt'])}** |",
       f"| **Reserve bis CHF 2000** | **{chf(S['reserve'])}** |",
       f"| Variante C (mit Sparliste) | ca. {chf(VA['C']['total'])} |"]
s = s.replace('<!--BUDGET-->', '\n'.join(bud) + '\n\nKautionen (werden zurückbezahlt): Mischer CHF 200, Rüttelplatte CHF 250. Nicht im Budget: Werkzeug, das ihr ausleiht, Benzin (~120 km heute, ca. CHF 25–30), Brennholz.')
Q = [
 ('OBI Schweiz – Schamottestein 64 × 124 × 250 mm (Art. 5390067), CHF 8.50, 3.78 kg', 'https://www.obi.ch/grillutensilien/schamottestein-hxbxt-64-x-124-x-250-mm/p/5390067'),
 ('OBI Schweiz – Schamottestein 40 × 200 × 500 mm (Art. 5390026), CHF 18.95, 7.4 kg', 'https://www.obi.ch/grillutensilien/schamottestein-hxbxt-40-x-200-x-500-mm/p/5390026'),
 ('OBI Schweiz – Pflanzen-Perlit 100 l (Art. 3798733), CHF 29.95', 'https://www.obi.ch/perlite-vermiculite/pflanzen-perlit-100-l/p/3798733'),
 ('OBI Schweiz – Zement CEM I 42.5 N (Art. 4793972), CHF 5.50', 'https://www.obi.ch/zemente-kalke/zement-cem-i-42-5-n/p/4793972'),
 ('OBI Schweiz – OSB-Platte N+F 1.8 × 62.5 × 250 cm (Art. 6464333), CHF 17.00', 'https://www.obi.ch/osb-platten-verlegeplatten/osb-platte-nut-und-feder-hxbxt-1-8-x-62-5-x-250-cm/p/6464333'),
 ('OBI Schweiz – Schalbrett 23 × 150 mm 3 m (Art. 2473270), CHF 11.95; Brett 23 × 100 mm 2 m (Art. 4895694), CHF 4.95', 'https://www.obi.ch/search/schaltafel/'),
 ('OBI Schweiz – Glattblech Stahl 500 × 1000 × 0.75 mm (Art. 4983821), CHF 23.50', 'https://www.obi.ch/bleche/glattblech-stahl-500-x-1-000-mm-staerke-0-75-mm/p/4983821'),
 ('OBI Schweiz – Kann Schalungsstein 24 cm, CHF 5.95, 27 kg (Plan B / Gewichtsannahme)', 'https://www.obi.ch/einfassungen-stufen-mauersysteme/kann-schalungsstein-grau-24-cm/p/5047857'),
 ('OBI Schweiz – Sakret Schamottemörtel 5 kg, CHF 17.95 (Plan B)', 'https://www.obi.ch/trockenmoertel/sakret-schamottemoertel-grau-5-kg/p/2925493'),
 ('OBI Schweiz – Preisliste Mietgeräte (Betonmischer, Rüttelplatte, Steintrennmaschine)', 'https://www.obi.ch/public/specials/baumarkt-services/assets/pdf/preisliste-obi-mietgeraete-ch-de.pdf'),
 ('OBI Schweiz – Marktliste (Adressen) und Markt Volketswil (Öffnungszeiten, Tel.)', 'https://www.obi.ch/markt/volketswil'),
 ('HORNBACH Schweiz – Betonschalungsstein 50 × 24 × 25 cm, CHF 4.90 (ab 50: 4.40)', 'https://www.hornbach.ch/de/p/betonschalungsstein-grau-50-x-24-x-25-cm-palette-45-vollsteine-5-endsteine/5242971/'),
 ('HORNBACH Schweiz – Endstein 50 × 24 × 25 cm, CHF 5.40', 'https://www.hornbach.ch/de/p/betonschalungsstein-endstein-grau-50-x-24-x-25-cm/10080612/'),
 ('HORNBACH Schweiz – Portlandkompositzement CEM II/B-M 42.5 N 25 kg, CHF 5.15', 'https://www.hornbach.ch/de/p/portlandkompositzement-cem-ii-b-m-v-ll-42-5-n-25-kg/12415537/'),
 ('HORNBACH Schweiz – CATNIC Baustahlmatte Q188A 2300 × 1500 × 6 mm, CHF 32.50', 'https://www.hornbach.ch/de/p/catnic-baustahlmatte-q188a-2300-x-1500-x-6-mm/5498829/'),
 ('HORNBACH Schweiz – Schamottemörtel 7 kg, CHF 11.50, bis 1000 °C', 'https://www.hornbach.ch/de/p/schamottemoertel-7-kg/5167054/'),
 ('HORNBACH Schweiz – Ofenrohr Ø150 Edelstahl 1 m, CHF 80.40', 'https://www.hornbach.ch/de/p/ofenrohr-o150-mm-edelstahl-1-m/5860137/'),
 ('HORNBACH Schweiz – Regenhut Ø150 Edelstahl, CHF 134.40 (optional)', 'https://www.hornbach.ch/de/p/regenhut-o150-mm-edelstahl/5860174/'),
 ('HORNBACH Schweiz – Drahtgeflecht Sechseck 25 mm 100 cm × 10 m, CHF 29.90', 'https://www.hornbach.ch/de/p/drahtgeflecht-sechseck-25-mm-100-cm-silber-verzinkt/6482865/'),
 ('HORNBACH Schweiz – Baumit Trockenbeton C25/30 25 kg, CHF 7.90 (Plan B)', 'https://www.hornbach.ch/de/p/baumit-trockenbeton-c25-30-25-kg/7798656/'),
 ('HORNBACH Affoltern a. A. – Marktseite (Adresse); Öffnungszeiten/Telefon aus Verzeichnissen', 'https://www.hornbach.ch/mein-markt/baumarkt-hornbach-affoltern-am-albis/'),
 ('Verzeichnis Hornbach Affoltern (Öffnungszeiten Di 07–19 Uhr, Tel. 044 204 40 00)', 'https://www.oeffnungszeitenbuch.de/filiale/Affoltern%2520a.%2520Albis-Hornbach%2520Baumarkt-4387710S.html'),
 ('Bauhaus Schweiz – Schamottsteinplatte 25 × 12.4 × 6.4 cm, CHF 7.95 (nur Suchindex, unbestätigt)', 'https://www.bauhaus.ch/de/bims-schamott/schamottsteinplatte/p/13876956'),
 ('Tägerhard Kies AG – Preisliste 2026 inkl. Bar-/Privatpreise, Öffnungszeiten, Telefon', 'https://taegerhardkies.ch/wp-content/uploads/2025/12/Grundpreisliste-2026.pdf'),
 ('Hug Baustoffe AG – Standorte/Mietmaschinen; Nassfräse S-75 K CHF 100/Tag exkl. MWST', 'https://www.hug-baustoffe.ch/standorte'),
 ('OBI Deutschland – Markt Waldshut-Tiengen (Adresse, Öffnungszeiten, Tel.)', 'https://www.obi.de/markt/waldshut-tiengen'),
 ('OBI Deutschland – Firefix Schamottstein 250 × 124 × 64 mm, €9.49', 'https://www.obi.de/p/2269678/firefix-schamottstein-250-mm-x-124-mm-x-64-mm'),
 ('schamotte-shop.de – Schamottstein NF2 250 × 124 × 64, 1350 °C, 3.9 kg, €4.29 (ab 50 Stk €4.12)', 'https://www.schamotte-shop.de/schamottstein-nf2-250x124x64mm.html'),
 ('schamotte-shop.de – Keramikfasermatte (u. a. 1000 × 610 × 25 mm, 1260 °C, €26.49)', 'https://www.schamotte-shop.de/ofenbaumaterial/hochtemperatur-isolierung/keramikfasermatte.html'),
 ('holz-feuer.shop – CUPPO Pizzaofen-Bausatz 90 cm, €2’220 + €150 Spedition, 375 kg; Abholung Berching (DE)', 'https://holz-feuer.shop/products/cuppo-pizzaofen-bausatz'),
 ('kuppelofen.de – Les Cheminées FD-Serie (FD 100–120), €1’149–1’399, Abholung Ruderatshofen', 'https://www.kuppelofen.de/les-cheminees-fd-serie/'),
 ('pizzaofenbau.ch – Bausätze CHF 3’490–5’490 (Suchindex)', 'https://www.pizzaofenbau.ch/bausatz/'),
 ('TheFiredome (Kiesen BE) – 2026 keine neuen Bausätze', 'https://www.thefiredome.ch/'),
 ('ofenseite.ch – Schamott-Normalstein 250 × 125 × 64, €15.90 (Vergleich)', 'https://www.ofenseite.ch/1151488-schamotte-normalstein-250x125x64mm'),
 ('Bauhaus DE – Schamottstein 250 × 124 × 64, 1200 °C, 3.7 kg, €7.95 (Vergleich)', 'https://www.bauhaus.info/ofenzubehoer/schamottstein/p/33066655'),
 ('BAZG – Wertfreigrenze 150 Franken, MWST 8.1 %, Rückerstattung ausländische MWST', 'https://www.bazg.admin.ch/de/wertfreigrenze-mehrwertsteuer-einreise-150-franken'),
 ('BAZG – App QuickZoll', 'https://www.bazg.admin.ch/de/quickzoll-app-waren-anmelden-private'),
 ('Ratgeber Ausfuhrschein (Bagatellgrenze €50.01, Stand 2025)', 'https://lieferadresse-konstanz.ch/mehrwertsteuer-zurueckholen-so-klappts-fuer-schweizer/'),
 ('Blick – Digitaler Ausfuhrschein Pilot seit 16.6.2026', 'https://www.blick.ch/politik/leichteres-leben-fuer-einkaufstouristen-jetzt-wird-der-ausfuhrschein-digital-id22038001.html'),
 ('EZB – Euro-Referenzkurse (CHF 0.9312 am 12.10.2026)', 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'),
 ('Kanton Aargau – Bauverordnung BauV (SAR 713.121), §§ 19, 49', 'https://gesetzessammlungen.ag.ch/app/de/texts_of_law/713.121'),
 ('Gemeinde Würenlos – Bauverwaltung (Kontakt, Öffnungszeiten)', 'https://www.wuerenlos.ch/verwaltung/bauverwaltung/bauverwaltung/'),
 ('MeteoSchweiz – Klimanormwerte 1991–2020 (Zürich-Affoltern)', 'https://data.geo.admin.ch/ch.meteoschweiz.klima/normwerte/normwerte.zip'),
 ('ADAC Autokatalog – Fiat Talento Kastenwagen L2H2 1.2t (Leergewicht 1965 kg, zGG 3060 kg, Zuladung 1095 kg)', 'https://www.adac.de/rund-ums-fahrzeug/autokatalog/marken-modelle/fiat/talento/296/308458'),
 ('VTS Art. 7 – Leergewicht inkl. Führer 75 kg (via admin.ch)', 'https://www.fedlex.admin.ch/eli/cc/1995/4425_4425_4425/de'),
 ('Kanton Aargau – Merkblatt Führerausweis Kategorie B', 'https://ag.ch/media/kanton-aargau/dvi/dokumente/stva/fuehrerausweise/ausweiskategorien/kategorie-b-03072024.pdf'),
 ('OpenStreetMap Nominatim / OSRM – Distanzen und Fahrzeiten', 'https://router.project-osrm.org/'),
]
s = s.replace('<!--QUELLEN-->', '\n'.join(f'{i}. {a} – <{u}>' for i, (a, u) in enumerate(Q, 1)))
open(os.path.join(H, 'Bauplan_Pizzaofen.md'), 'w').write(s)
print('ok', len(s), 'Zeichen,', len(Q), 'Quellen')
