#!/usr/bin/env python3
"""Stueckliste, Kosten, Gewichte und Fahrtenplan (Variante B, Kuppel 90 cm).
Mengen kommen aus berechnung.py (ergebnis.json). Preise: siehe Quelle je Position, abgerufen 13.10.2026.
"""
import json, math
E = json.load(open('ergebnis.json'))
V, U = E['D90'], E['unterbau']
ABRUF = '13.10.2026'
EUR_CHF = 0.9312   # EZB-Referenzkurs 12.10.2026

zement_total = U['zement_beton_kg'] + V['zement_perlit_kg'] + V['zement_putz_kg']
zement_sack = math.ceil(zement_total / 25)

items = [
 # pos, gruppe, bezeichnung, spezifikation, menge, einheit, ep, kg_einheit, haendler, url, verfuegbarkeit, fahrt, preisstatus
 ('1','Fundament','Kiesgemisch UG22 0/31.5 (Art. 60201) fuer Kieskoffer','ungebundenes Gemisch, RG 1.60 t/m3; 1.70 x 1.70 x 0.20 m verdichtet = 0.578 m3, lose x1.25',0.75,'m³',60.00,1600,'Taegerhard Kies AG, Wettingen','https://taegerhardkies.ch/wp-content/uploads/2025/12/Grundpreisliste-2026.pdf','Kieswerk, Bar-/Privatverkauf waehrend Oeffnungszeiten','K1+K2','Privatpreis inkl. MWST lt. Preisliste 2026 (S. 10) - telefonisch bestaetigen'),
 ('2','Fundament','Betonkies gewaschen 0-16 (Art. 20001)','EN 12620, RG 1.80 t/m3; 1.018 m3 Beton x 1900 kg/m3',1.10,'m³',60.00,1800,'Taegerhard Kies AG, Wettingen','https://taegerhardkies.ch/wp-content/uploads/2025/12/Grundpreisliste-2026.pdf','Kieswerk','K2-K4','Privatpreis inkl. MWST lt. Preisliste 2026 - telefonisch bestaetigen'),
 ('3','Ofen','Sand gewaschen 0-4 (Art. 40001)','RG 1.50 t/m3; Sandform Kuppel (0.17 m3), danach Putz + Bodenbett',0.25,'m³',60.00,1500,'Taegerhard Kies AG, Wettingen','https://taegerhardkies.ch/wp-content/uploads/2025/12/Grundpreisliste-2026.pdf','Kieswerk','K4','Privatpreis inkl. MWST lt. Preisliste 2026 - telefonisch bestaetigen'),
 ('4','Fundament','Zement CEM II/B-M (V-LL) 42.5 N, 25 kg (Art. 12415537)','fuer Fundamentbeton (0.354 m3 x 300 kg = 106 kg)',5,'Sack',5.15,25,'HORNBACH Affoltern a. A.','https://www.hornbach.ch/de/p/portlandkompositzement-cem-ii-b-m-v-ll-42-5-n-25-kg/12415537/','Marktsortiment','H','Preis lt. hornbach.ch (Seitenstand Aug. 2026)'),
 ('5','Sockel/Ofen','Zement CEM I 42.5 N, 25 kg (OBI Art. 4793972)',f'Sockelfuellung + Herdplatte (199 kg), Perlit-Daemmung ({V["zement_perlit_kg"]:.0f} kg), Putz ({V["zement_putz_kg"]:.0f} kg)',zement_sack-5,'Sack',5.50,25,'OBI Volketswil','https://www.obi.ch/zemente-kalke/zement-cem-i-42-5-n/p/4793972','online n.v. -> Marktbestand telefonisch pruefen','O','Online-Preis obi.ch; Ersatz: Hornbach Art. 12415537 (5.15)'),
 ('6','Sockel','Betonschalungsstein grau 50x24x25 cm, Vollstein (Art. 5242971)','3 Lagen U-Form, 8.04 Steine/Lage -> 18 Voll + 6 End + 2 Reserve',20,'Stk',4.90,27,'HORNBACH Affoltern a. A.','https://www.hornbach.ch/de/p/betonschalungsstein-grau-50-x-24-x-25-cm-palette-45-vollsteine-5-endsteine/5242971/','Marktsortiment','H','Preis lt. hornbach.ch; Gewicht ANNAHME (27 kg wie OBI Kann 24 cm)'),
 ('7','Sockel','Betonschalungsstein Endstein grau 50x24x25 cm (Art. 10080612)','offene Wandenden vorne, 2 pro Lage',6,'Stk',5.40,27,'HORNBACH Affoltern a. A.','https://www.hornbach.ch/de/p/betonschalungsstein-endstein-grau-50-x-24-x-25-cm/10080612/','Marktsortiment','H','Preis lt. hornbach.ch; Gewicht ANNAHME'),
 ('8','Fundament/Sockel','CATNIC Baustahlmatte Q188A 2300 x 1500 x 6 mm (Art. 5498829)','je 1 Matte Fundament + Herdplatte, zugeschnitten 140 x 140 cm; Reststreifen = Steckeisen',2,'Stk',32.50,10.4,'HORNBACH Affoltern a. A.','https://www.hornbach.ch/de/p/catnic-baustahlmatte-q188a-2300-x-1500-x-6-mm/5498829/','Marktsortiment','H','Preis lt. hornbach.ch; Gewicht berechnet 3.0 kg/m2'),
 ('9','Sockel','OSB-3 Verlegeplatte N+F 250 x 62.5 cm, 18 mm (OBI Art. 6464333)','verlorene/abnehmbare Schalung Herdplatte, Feld 102 x 126 cm',2,'Stk',17.00,16.9,'OBI Volketswil','https://www.obi.ch/osb-platten-verlegeplatten/osb-platte-nut-und-feder-hxbxt-1-8-x-62-5-x-250-cm/p/6464333','online verfuegbar','O','Online-Preis obi.ch'),
 ('10','Fundament/Sockel','Schalbrett saegerau Fichte/Tanne 23 x 150 mm, 3 m (OBI Art. 2473270)','Fundamentrand (2x155 + 2x150 cm), Herdplattenrand, Stuetzen; im Markt halbieren lassen',3,'Stk',11.95,4.7,'OBI Volketswil','https://www.obi.ch/saegeraue-ware/schalbrett-saegerau-fichte-tanne-23-x-150-mm-laenge-3-m/p/2473270','online verfuegbar','O','Online-Preis obi.ch'),
 ('10b','Sockel','Brett saegerau Fichte/Tanne 23 x 100 mm, 2 m (OBI Art. 4895694)','8 Stuetzen a 75 cm (je 2 Bretter verschraubt) unter der Herdplatten-Schalung',4,'Stk',4.95,2.1,'OBI Volketswil','https://www.obi.ch/saegeraue-ware/brett-saegerau-fichte-tanne-23-x-100-mm-laenge-2-m/p/4895694','Marktsortiment','O','Online-Preis obi.ch (Suchliste)'),
 ('11','Ofen','Schamottestein 64 x 124 x 250 mm (NF2) (OBI Art. 5390067)',f'Kuppel {V["nf_kuppel"]} NF (= {V["halbsteine_mit_verschnitt"]} Halbsteine inkl. 10 %) + Tunnel {V["nf_tunnel"]} NF; Qualitaet am Etikett pruefen: >= 1200 C, Al2O3 >= 30 %',V['nf_total'],'Stk',8.50,3.78,'OBI Volketswil','https://www.obi.ch/grillutensilien/schamottestein-hxbxt-64-x-124-x-250-mm/p/5390067','online verfuegbar; Reservieren & Abholen ca. 4 h','O','Online-Preis obi.ch (Marktpreis kann abweichen)'),
 ('12','Ofen','Schamottestein 40 x 200 x 500 mm (OBI Art. 5390026)',f'Backboden {V["boden_m2"]} m2 -> {V["platten_boden"]} Platten (inkl. 15 % Verschnitt) + 2 Tunneldecke/Kaminauflager',V['platten_total'],'Stk',18.95,7.4,'OBI Volketswil','https://www.obi.ch/grillutensilien/schamottestein-hxbxt-40-x-200-x-500-mm/p/5390026','online verfuegbar','O','Online-Preis obi.ch; Temperaturklasse nicht angegeben -> Etikett pruefen'),
 ('13','Ofen','HORNBACH Schamottemoertel 7 kg (Art. 5167054)',f'feuerbestaendig bis 1000 C; Bedarf {V["moertel_kg"]} kg (Fugen 6 mm, +30 %)',math.ceil(V['moertel_kg']/7),'Eimer',11.50,7,'HORNBACH Affoltern a. A.','https://www.hornbach.ch/de/p/schamottemoertel-7-kg/5167054/','Marktsortiment','H','Preis lt. hornbach.ch (Seitenstand 02.09.2026)'),
 ('14','Ofen','Pflanzen-Perlit 100 l, Koernung bis 10 mm (OBI Art. 3798733)',f'Perlit-Zement 5:1 - Boden 10 cm, Kuppel 8 cm; Bedarf {V["perlit_l"]} l',math.ceil(V['perlit_l']/100),'Sack',29.95,9.4,'OBI Volketswil','https://www.obi.ch/perlite-vermiculite/pflanzen-perlit-100-l/p/3798733','online verfuegbar','O','Online-Preis obi.ch'),
 ('15','Ofen','Ofenrohr Ø150 mm Edelstahl, einwandig 0.6 mm, 1 m (Art. 5860137)','Kaminrohr, steckt im Ø15-Loch zwischen den Tunneldeckplatten',1,'Stk',80.40,2.3,'HORNBACH Affoltern a. A.','https://www.hornbach.ch/de/p/ofenrohr-o150-mm-edelstahl-1-m/5860137/','Marktsortiment / evtl. Lieferzeit -> telefonisch pruefen','H','Preis lt. hornbach.ch (Seitenstand 29.07.2026)'),
 ('16','Ofen','Drahtgeflecht Sechseck 25 mm, 100 cm x 10 m, verzinkt silber (Art. 6482865)',f'Putztraeger fuer Aussenputz {V["putz_m2"]} m2',1,'Rolle',29.90,5,'HORNBACH Affoltern a. A.','https://www.hornbach.ch/de/p/drahtgeflecht-sechseck-25-mm-100-cm-silber-verzinkt/6482865/','Marktsortiment','H','Preis lt. hornbach.ch (Seitenstand 05.08.2026); Gewicht ANNAHME'),
 ('17','Ofen','Glattblech Stahl 500 x 1000 x 0.75 mm (OBI Art. 4983821)','Ofentuer DIY 46 x 33 cm (Rand 2x abgekantet) + Holzgriff',1,'Stk',23.50,2.9,'OBI Volketswil','https://www.obi.ch/bleche/glattblech-stahl-500-x-1-000-mm-staerke-0-75-mm/p/4983821','online verfuegbar','O','Online-Preis obi.ch'),
 ('18','Klein','Kleinmaterial: Bindedraht, Schrauben, Holzgriff, Ofenlack, Abstandhalter, Zeitungen','-',1,'Pausch.',40.00,8,'Hornbach/OBI','-','Marktsortiment','H/O','Preis unbestaetigt - ANNAHME'),
 ('19','Klein','Abdeckplane ca. 4 x 5 m (Regen-/Frostschutz)','-',1,'Stk',20.00,3,'Hornbach/OBI','-','Marktsortiment','H/O','Preis unbestaetigt - ANNAHME'),
 ('20','Klein','Diamanttrennscheibe 125 mm fuer Stein (eigener Winkelschleifer)','-',1,'Stk',25.00,0.2,'Hornbach/OBI','-','Marktsortiment','H/O','Preis unbestaetigt - ANNAHME'),
]
mieten = [
 ('M1','Betonmischer (OBI Mietgeraet 513905)','Wochentarif, Kaution CHF 200',1,'Woche',147.00,65,'OBI Volketswil (oder naeher: Hug Baustoffe, Preis telefonisch pruefen)','https://www.obi.ch/public/specials/baumarkt-services/assets/pdf/preisliste-obi-mietgeraete-ch-de.pdf','O'),
 ('M2','Ruettelplatte Benzin 11 kN (OBI Mietgeraet 513961)','Tagestarif, Kaution CHF 250',1,'Tag',77.00,75,'OBI Volketswil','https://www.obi.ch/public/specials/baumarkt-services/assets/pdf/preisliste-obi-mietgeraete-ch-de.pdf','O'),
]
optional = [
 ('O1','Steintrennmaschine 600 mm (OBI Mietgeraet 525983)','nur falls kein Winkelschleifer: Tagestarif',120.00,'https://www.obi.ch/public/specials/baumarkt-services/assets/pdf/preisliste-obi-mietgeraete-ch-de.pdf'),
 ('O2','Regenhut Ø150 mm Edelstahl (Hornbach Art. 5860174)','Lieferzeit ca. 8 Arbeitstage -> spaeter',134.40,'https://www.hornbach.ch/de/p/regenhut-o150-mm-edelstahl/5860174/'),
 ('O4','Deponie Aushub sauber (Taegerhard, Privatpreis)','ca. 1.1 m3 lose; gratis, wenn im Garten verteilt',22.00,'https://taegerhardkies.ch/wp-content/uploads/2025/12/Grundpreisliste-2026.pdf'),
 ('O3','Keramikfasermatte 1000 x 610 x 25 mm, 1260 C (schamotte-shop.de)','erste Daemmlage auf Kuppel statt 2.5 cm Perlit; 7 Stk x 26.49 EUR (Versand)',round(7*26.49*EUR_CHF,2),'https://www.schamotte-shop.de/ofenbaumaterial/hochtemperatur-isolierung/keramikfasermatte.html'),
]

rows = []
for p in items:
    pos,gr,bez,spez,menge,eh,ep,kg,h,url,verf,fahrt,status = p
    gp = round(menge*ep,2); kgt = round(menge*kg,1)
    rows.append(dict(pos=pos,gruppe=gr,bez=bez,spez=spez,menge=menge,eh=eh,ep=ep,gp=gp,kg_einheit=kg,kg=kgt,haendler=h,url=url,verf=verf,fahrt=fahrt,status=status))
mrows = [dict(pos=m[0],bez=m[1],spez=m[2],menge=m[3],eh=m[4],ep=m[5],gp=m[3]*m[5],kg=m[6],haendler=m[7],url=m[8],fahrt=m[9]) for m in mieten]
summe_mat = round(sum(r['gp'] for r in rows),2)
summe_miet = round(sum(r['gp'] for r in mrows),2)
gesamt = round(summe_mat+summe_miet,2)
by_h = {}
for r in rows:
    key = 'Taegerhard' if 'Taegerhard' in r['haendler'] else ('Hornbach' if r['haendler'].startswith('HORNBACH') else ('OBI' if r['haendler'].startswith('OBI') else 'Klein'))
    by_h.setdefault(key,[0,0]); by_h[key][0]+=r['gp']; by_h[key][1]+=r['kg']
gewicht_total = round(sum(r['kg'] for r in rows),1)

# ------------------------------------------------ Fahrtenplan
NUTZLAST = dict(gesamtgewicht=3060, leergewicht=1965, beifahrer=75, ausruestung=20)
nutz = NUTZLAST['gesamtgewicht']-NUTZLAST['leergewicht']
verfuegbar = nutz-NUTZLAST['beifahrer']-NUTZLAST['ausruestung']
planung = 900
def g(pos): return next(r for r in rows if r['pos']==pos)
fahrten = {
 'F1 HORNBACH Affoltern': [('6',20),('7',6),('4',5),('8',2),('13',4),('15',1),('16',1)],
 'F2 OBI Volketswil': [('11',V['nf_total']),('12',V['platten_total']),('14',math.ceil(V['perlit_l']/100)),('5',zement_sack-5),('9',2),('10',3),('10b',4),('17',1),('18',1),('19',1),('20',1)],
}
fplan = {}
for f,lst in fahrten.items():
    kg = sum(g(p)['kg_einheit']*m for p,m in lst)
    if f.startswith('F2'): kg += sum(m['kg'] for m in mrows)
    fplan[f]=round(kg,1)
kies = [('K1 Kies','Kiesgemisch 0/31.5', 0.56, 1600),('K2 Kies','Kiesgemisch 0/31.5 Rest 0.19 m3 + Betonkies 0.33 m3', None, None),
        ('K3 Kies','Betonkies 0/16 0.50 m3', 0.50, 1800),('K4 Kies','Betonkies 0/16 0.27 m3 + Sand 0.25 m3', None, None)]
fplan['K1 Taegerhard'] = round(0.56*1600)
fplan['K2 Taegerhard'] = round(0.19*1600+0.33*1800)
fplan['K3 Taegerhard'] = round(0.50*1800)
fplan['K4 Taegerhard'] = round(0.27*1800+0.25*1500)

out = dict(abruf=ABRUF, kurs=EUR_CHF, zement_total_kg=round(zement_total,1), zement_sack=zement_sack,
           rows=rows, mieten=mrows, optional=[dict(pos=o[0],bez=o[1],spez=o[2],gp=o[3],url=o[4]) for o in optional],
           summe_material=summe_mat, summe_mieten=summe_miet, gesamt=gesamt, reserve=round(2000-gesamt,2),
           nach_haendler={k:[round(v[0],2),round(v[1],1)] for k,v in by_h.items()}, gewicht_material=gewicht_total,
           nutzlast=dict(**NUTZLAST, nutzlast=nutz, verfuegbar=verfuegbar, planungsgrenze=planung), fahrten=fplan)
json.dump(out, open('stueckliste.json','w'), indent=1, ensure_ascii=False)
if __name__=='__main__':
    for r in rows: print(f"{r['pos']:>3} {r['bez'][:60]:60} {r['menge']:>6} {r['eh']:5} {r['ep']:7.2f} {r['gp']:8.2f} {r['kg']:7.1f} kg  [{r['fahrt']}]")
    for m in mrows: print(f"{m['pos']:>3} {m['bez'][:60]:60} {m['menge']:>6} {m['eh']:5} {m['ep']:7.2f} {m['gp']:8.2f} {m['kg']:7.1f} kg")
    print('Zement total', round(zement_total,1),'kg ->',zement_sack,'Sack')
    print('Material',summe_mat,'Mieten',summe_miet,'GESAMT',gesamt,'Reserve',round(2000-gesamt,2))
    print('nach Haendler',out['nach_haendler'])
    print('Gewicht Material total',gewicht_total,'kg')
    print('Nutzlast',nutz,'verfuegbar',verfuegbar)
    for k,v in fplan.items(): print(' ',k,v,'kg')
