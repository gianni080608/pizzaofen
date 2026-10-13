#!/usr/bin/env python3
"""Stueckliste v3 (13.10.2026, Phasen Sockel/Ofen): nur Haendler mit online bestaetigtem Lagerbestand (OBI-Schnittstelle) + Kieswerk Taegerhard.
Mengen aus ergebnis.json. Preise: OBI-Produktseiten/Suchliste, Taegerhard Preisliste 2026. Abruf 13.10.2026."""
import json, math
E = json.load(open('ergebnis.json'))
D = 'D80'
V, U = E[D], E['unterbau']
EUR_CHF = 0.9312
OBI = 'https://www.obi.ch'
TAEG = 'https://taegerhardkies.ch/wp-content/uploads/2025/12/Grundpreisliste-2026.pdf'
zement_total = U['zement_beton_kg'] + V['zement_perlit_kg'] + V['zement_putz_kg']
zement_sack = math.ceil(zement_total / 25)
NF_KAUF = 39                       # Oftringen 25 (ganzer Bestand) + Volketswil 14; Bedarf 35 inkl. 10 % -> 4 Reserve
assert V['nf_kuppel'] <= NF_KAUF
PL = V['platten_total']
# kat: M=Material, K=Kleinmaterial/Verbrauch, G=Gebinde/Transport, S=Schutz, W=Werkzeug (bleibt), B=Betrieb/Sicherheit
# (id, kat, name, spez, menge, eh, chf, kg, quelle, url, art, bezug{markt:menge}, bestand_snapshot)
R = [
 ('K1','M','Kiesgemisch UG22 0/31.5 (Art. 60201)','Kieskoffer 1.70 x 1.70 x 0.20 m verdichtet = 0.578 m³; lose x 1.25',0.75,'m³',60.00,1600,'Kieswerk Tägerhard',TAEG,'60201',{'Tägerhard':0.75},'Kieswerk, Bezug immer möglich'),
 ('K2','M','Betonkies gewaschen 0/16 (Art. 20001)',f"{U['beton_total_m3']} m³ Beton x 1900 kg/m³",1.10,'m³',60.00,1800,'Kieswerk Tägerhard',TAEG,'20001',{'Tägerhard':1.10},'Kieswerk'),
 ('K3','M','Sand gewaschen 0/4 (Art. 40001)','Sandform Kuppel 0.17 m³, danach Putz + Bodenbett',0.25,'m³',60.00,1500,'Kieswerk Tägerhard',TAEG,'40001',{'Tägerhard':0.25},'Kieswerk'),
 ('O01','M','Zement CEM I 42.5 N, 25 kg',f'Beton {U["zement_beton_kg"]:.0f} + Perlit {V["zement_perlit_kg"]:.0f} + Putz {V["zement_putz_kg"]:.0f} = {zement_total:.0f} kg',zement_sack,'Sack',5.50,25,'OBI',OBI+'/zemente-kalke/zement-cem-i-42-5-n/p/4793972','4793972',{'Oftringen':zement_sack},'Oftringen 191'),
 ('O02','M','Kann Schalungsstein grau 24 cm (50 x 25 x 24)','U-Sockel 3 Lagen à 8.04 Stk = 24.1 + 2 Reserve',26,'Stk',5.95,27.0,'OBI',OBI+'/einfassungen-stufen-mauersysteme/kann-schalungsstein-grau-24-cm/p/5047857','5047857',{'Volketswil':26},'Volketswil 36'),
 ('O03','M','Catnic Baustahlmatte R188A 230 x 100 cm (Stäbe 6 mm)','Herdplatte (trägt frei über 102 cm): 2 Matten à 140 x 100, 60 cm überlappt = 140 x 140, Hauptstäbe quer zur Öffnung; Reste = Steckeisen',2,'Stk',22.95,5.6,'OBI',OBI+'/baustahl-baugitter/baustahlmatte-r188a-230-x-100-cm/p/5031802','5031802',{'Volketswil':2},'Volketswil 26'),
 ('O03b','M','Catnic Estrichgitter verzinkt 200 x 100 cm','Fundament (vollflächig auf Kies, nur Schwindriss-Bewehrung): 2 Stück nebeneinander, auf 140 x 140 schneiden',2,'Stk',6.50,3.0,'OBI',OBI+'/baustahl-baugitter/estrichgitter-verzinkt-200-x-100-cm/p/5031687','5031687',{'Volketswil':2},'Volketswil 85'),
 ('O04','M','OSB-Platte N+F 1.8 x 62.5 x 250 cm','Schalung Herdplatte, Feld 102 x 126 cm',2,'Stk',17.00,16.9,'OBI',OBI+'/osb-platten-verlegeplatten/osb-platte-nut-und-feder-hxbxt-1-8-x-62-5-x-250-cm/p/6464333','6464333',{'Volketswil':2},'Volketswil 107'),
 ('O05','M','Schalbrett sägerau 23 x 150 mm, 3 m','Fundamentrand 2 x 155 + 2 x 150 cm, Rest Herdplattenrand; im Markt halbieren lassen',3,'Stk',11.95,4.7,'OBI',OBI+'/saegeraue-ware/schalbrett-saegerau-fichte-tanne-23-x-150-mm-laenge-3-m/p/2473270','2473270',{'Volketswil':3},'Volketswil 63'),
 ('O06','M','Brett sägerau 23 x 100 mm, 2 m','8 Stützen à 75 cm (je 2 Bretter verschraubt) unter Herdplattenschalung',4,'Stk',4.95,2.1,'OBI',OBI+'/saegeraue-ware/brett-saegerau-fichte-tanne-23-x-100-mm-laenge-2-m/p/4895694','4895694',{'Volketswil':4},'Volketswil 23'),
 ('O07','M','Schamottestein 64 x 124 x 250 mm (NF)',f'Kuppel: {V["halbsteine_mit_verschnitt"]} Halbsteine = {V["nf_kuppel"]} NF (inkl. 10 % Verschnitt) + 4 Reserve',NF_KAUF,'Stk',8.50,3.78,'OBI',OBI+'/grillutensilien/schamottestein-hxbxt-64-x-124-x-250-mm/p/5390067','5390067',{'Oftringen':25,'Volketswil':14},'Oftringen 25, Volketswil 24'),
 ('O08','M','Schamottestein 40 x 200 x 500 mm',f'Boden {V["platten_boden"]} + Tunneldecke 2 + Tunnelwände {V["platten_tunnel"]-2} (längs halbiert = {V["streifen"]} Streifen)',PL,'Stk',18.95,7.4,'OBI',OBI+'/grillutensilien/schamottestein-hxbxt-40-x-200-x-500-mm/p/5390026','5390026',{'Oftringen':PL-17,'Volketswil':17},'Volketswil 17, Oftringen 12'),
 ('O09','M','Sakret Schamottemörtel 5 kg (feuerbeständig bis 1100 °C)',f'Bedarf {V["moertel_kg"]} kg',math.ceil(V['moertel_kg']/5),'Sack',17.95,5.0,'OBI',OBI+'/trockenmoertel/sakret-schamottemoertel-grau-5-kg/p/2925493','2925493',{'Volketswil':math.ceil(V['moertel_kg']/5)},'Volketswil 15'),
 ('O10','M','Pflanzen-Perlit 100 l',f'Perlit-Zement 5:1, Boden 10 cm + Kuppel 8 cm; Bedarf {V["perlit_l"]} l',math.ceil(V['perlit_l']/100),'Sack',29.95,9.4,'OBI',OBI+'/perlite-vermiculite/pflanzen-perlit-100-l/p/3798733','3798733',{'Volketswil':math.ceil(V['perlit_l']/100)},'Volketswil 8'),
 ('O11','M','Firefix Rauchrohr schwarz Ø 150 mm, 1 m (Stahl, Senotherm-Lack)','Kaminrohr, im Ø15.5-Loch der Tunneldeckplatten eingemörtelt',1,'Stk',59.95,7.8,'OBI',OBI+'/zubehoer-fuer-cheminees-und-schwedenoefen/firefix-rauchrohr-schwarz-15-cm/p/2480333','2480333',{'Volketswil':1},'Volketswil 2'),
 ('O12','M','Gah Alberts Sechseck-Geflecht verzinkt 25 mm, 1 m x 10 m','Putzträger Aussenschale 2.65 m²',1,'Rolle',27.95,3.5,'OBI',OBI+'/draht-zaungeflecht/gah-alberts-sechseck-geflecht-verzinkt-hoehe-1-m-laenge-10-m/p/4915658','4915658',{'Volketswil':1},'Volketswil 4'),
 ('O13','M','Glattblech Stahl 500 x 1000 x 0.75 mm','Ofentür 46 x 28 cm (Öffnung 40 x 22.4); Rest = Kaminabdeckung Ø 20 cm',1,'Stk',23.50,2.9,'OBI',OBI+'/bleche/glattblech-stahl-500-x-1-000-mm-staerke-0-75-mm/p/4983821','4983821',{'Oftringen':1},'Oftringen 3'),
 ('O14','K','Siro Möbelgriff S113 Kiefer roh, Lochabstand 96 mm','Türgriff (mit 2 Schrauben + Holzklötzchen als Abstand)',1,'Stk',6.95,0.1,'OBI','https://www.obi.ch/moebelgriffe-moebelknoepfe/siro-moebelgriff-s113-kiefer-roh-lochabstand-96-mm/p/5786116','5786116',{'Volketswil':1},'Volketswil 6'),
 ('O15','K','Albrecht Thermolack schwarz matt 125 ml','Tür + Kaminrohr-Ausbesserung',1,'Stk',12.50,0.2,'OBI','https://www.obi.ch/metallschutzlacke/albrecht-thermolack-schwarz-matt-125-ml/p/5756416','5756416',{'Volketswil':1},'Volketswil 9'),
 ('O16','K','LUX Universalschraube Senkkopf 4 x 40 mm, 200 Stk','Schalung, Stützen, Griff',1,'Pack',9.95,0.6,'OBI','https://www.obi.ch/spanplattenschrauben-universalschrauben/lux-universalschraube-senkkopf-4-x-40-mm-tx-antrieb-200-stk-/p/4048450','4048450',{'Volketswil':1},'Volketswil 2'),
 ('O17','K','OBI Bindedraht verzinkt 1.4 mm x 20 m','Matten, Geflecht verankern',1,'Rolle',5.95,0.3,'OBI','https://www.obi.ch/weitere-gartenhelfer/obi-bindedraht-verzinkt-1-4-mm-x-20-m/p/4582912','4582912',{'Volketswil':1},'Volketswil 7'),
 ('O18','K','LUX Gewebeplane grün 4 x 5 m','1 x Ofen (Regen/Frost), 1 x Zement/Material',2,'Stk',12.95,1.5,'OBI','https://www.obi.ch/baufolien-planen/lux-gewebeplane-gruen-4-x-5-m/p/2435469','2435469',{'Oftringen':2},'Oftringen 9'),
 ('O19','K','LUX Diamant-Trennscheibe Universal 125 mm','Schamott schneiden (54 Schnitte)',1,'Stk',21.50,0.2,'OBI','https://www.obi.ch/zubehoer-fuer-winkelschleifer/lux-diamant-trennscheibe-universal-125-mm/p/1755560','1755560',{'Volketswil':1},'Volketswil 2'),
 ('O20','K','LUX Trennscheiben-Sparpack Metall 125 mm','Matten + Türblech schneiden',1,'Pack',8.35,0.4,'OBI','https://www.obi.ch/zubehoer-fuer-winkelschleifer/lux-trennscheiben-sparpack-metall-125-mm/p/1206051','1206051',{'Volketswil':1},'Volketswil 9'),
 ('O21','K','LUX Maurerschnur rot 20 m','Abstecken, Fluchten',1,'Stk',3.65,0.1,'OBI','https://www.obi.ch/pruefwerkzeuge-messwerkzeuge/lux-maurerschnur-classic-rot-20-m/p/1240837','1240837',{'Volketswil':1},'Volketswil 5'),
 ('O22','K','LUX Zimmermannsbleistift 24 cm','Anzeichnen',2,'Stk',2.25,0.02,'OBI','https://www.obi.ch/pruefwerkzeuge-messwerkzeuge/lux-zimmermannsbleistift-classic-24-cm/p/1237163','1237163',{'Volketswil':2},'Volketswil 63'),
 ('O23','G','Jopa Mörtelkasten schwarz 90 l','Mischen + Kiestransport (im Wagen befüllen)',4,'Stk',7.95,2.0,'OBI','https://www.obi.ch/baueimer-moertelkuebel/jopa-moertelkasten-schwarz-fassungsvermoegen-90-l/p/5799150','5799150',{'Oftringen':4},'Oftringen 25'),
 ('O24','G','Jopa Mörteleimer mit Bügel 20 l','Kiestransport (max. 15 l füllen = 25 kg), Wasser',10,'Stk',3.50,0.68,'OBI','https://www.obi.ch/baueimer-moertelkuebel/jopa-moerteleimer-mit-buegel-fassungsvermoegen-20-l/p/5799200','5799200',{'Oftringen':10},'Oftringen 31'),
 ('O25','G','Spanngurt Unitec mit Klemmverschluss 3 m, 400 kg','Ladungssicherung, 4 Stück',4,'Stk',8.95,0.3,'OBI','https://www.obi.ch/spanngurte-zurrgurte/spanngurt-unitec-mit-klemmverschluss-3-m-400-kg/p/4904546','4904546',{'Oftringen':4},'Oftringen 5'),
 ('O26','G','Antirutschunterlage schwarz 30 x 150 cm','unter die Ladung',3,'Stk',5.50,0.4,'OBI','https://www.obi.ch/teppichgleitschutz/antirutschunterlage-schwarz-30-x-150-cm/p/5102272','5102272',{'Oftringen':3},'Oftringen 18'),
 ('O27','S','LUX Feinstaubmaske FFP3 mit Ventil, 2 Stk','Steine schneiden (Quarzstaub), Perlit, Zement',1,'Pack',19.50,0.1,'OBI','https://www.obi.ch/atemschutz-zubehoer/lux-feinstaubmaske-ffp3-2-stueck/p/3084563','3084563',{'Volketswil':1},'Volketswil 12'),
 ('O28','S','Schutzbrille mit Bügeln','2 Personen',2,'Stk',6.50,0.05,'OBI','https://www.obi.ch/augenschutz/schutzbrille-mit-buegeln/p/3084571','3084571',{'Volketswil':2},'Volketswil 11'),
 ('O29','S','3M Gehörschutzstöpsel mit Kordel 1271','Winkelschleifer',1,'Pack',8.95,0.05,'OBI','https://www.obi.ch/gehoerschutz/3m-gehoerschutzstoepsel-mit-kordel-1271/p/5087713','5087713',{'Volketswil':1},'Volketswil 4'),
 ('O30','S','PU-Handschuh Gr. 8','Zement ist ätzend: immer Handschuhe',4,'Paar',0.95,0.05,'OBI','https://www.obi.ch/arbeitshandschuhe/pu-handschuh-gr-8/p/6608442','6608442',{'Oftringen':4},'Oftringen 107'),
 ('O31','W','Betonstampfer 13 x 20 cm, Stiel 105 cm (7.5 kg)','Kieskoffer verdichten (ersetzt Mietrüttelplatte)',1,'Stk',43.95,7.5,'OBI','https://www.obi.ch/baugeraete/betonstampfer-13-x-20-cm-stiellaenge-105-cm/p/5474523','5474523',{'Oftringen':1},'Oftringen 1 (Volketswil 1)'),
 ('O32','W','Einhell Farb-Mörtelrührer TE-MX 1600-2 CE (1600 W)','Beton in 40-l-Chargen, Perlit, Mörtel, Putz (ersetzt Mietmischer)',1,'Stk',106.95,5.2,'OBI','https://www.obi.ch/multitools-spezialwerkzeuge/einhell-farb-moertelruehrer-te-mx-1600-2-ce/p/5047022','5047022',{'Volketswil':1},'Volketswil 4'),
 ('O33','W','LUX Kellenset 3-tlg.','Maurer-/Putzkelle',1,'Set',17.50,1.04,'OBI','https://www.obi.ch/maurer-fliesenleger-verlegewerkzeuge/lux-kellenset-3-tlg-/p/5907696','5907696',{'Volketswil':1},'Volketswil 5'),
 ('O34','W','LUX Fugenkelle Classic 10 mm','Fugen Kuppel',1,'Stk',7.50,0.1,'OBI','https://www.obi.ch/maurer-fliesenleger-verlegewerkzeuge/lux-fugenkelle-classic-10-mm/p/1240233','1240233',{'Volketswil':1},'Volketswil 6'),
 ('O35','B','Abus Löschdecke LD1118','Brandschutz Betrieb (+ Gartenschlauch)',1,'Stk',16.50,0.5,'OBI','https://www.obi.ch/brandschutz/abus-loeschdecke-ld1118/p/5295126','5295126',{'Volketswil':1},'Volketswil 18'),
 ('O36','B','Valo Ascheeimer oval mit Deckel schwarz 24 l','Glut/Asche 24 h auskühlen',1,'Stk',24.95,1.6,'OBI','https://www.obi.ch/zubehoer-fuer-cheminees-und-schwedenoefen/valo-ascheeimer-oval-mit-deckel-schwarz-hxbxt-42-x-31-x-61-cm-24-l/p/6003131','6003131',{'Volketswil':1},'Volketswil 20'),
]
HAUS = [  # nur kaufen, wenn nicht vorhanden (Volketswil, Bestand 13.10.)
 ('H1','Holsteiner Schaufel eingestielt 245 mm (2 Stk)',2,13.95,'1261262','Volketswil 9'),
 ('H2','LUX Gärtnerspaten T-Griff 85 cm',1,9.95,'1262013','Volketswil 25'),
 ('H3','LUX Kreuzhacke 1.5 kg (Aushub harter Boden)',1,35.95,'4498705','Volketswil 5'),
 ('H4','OBI Gartenschubkarre 85 l',1,29.95,'6539670','Volketswil 18'),
 ('H5','LUX Alu-Wasserwaage Classic 100 cm',1,20.95,'3085115','Volketswil 6'),
 ('H6','Sola Rollbandmass 5 m',1,27.95,'5832332','Volketswil 1'),
 ('H7','LUX Gummihammer Classic 54 mm',1,7.95,'1397025','Volketswil 12'),
 ('H8','LUX Handsäge Classic Holz 450 mm',1,16.50,'1222538','Volketswil 2'),
 ('H9','Einhell Winkelschleifer TC-AG 125/850',1,42.95,'5537113','Volketswil 3'),
 ('H10','Bosch Akku-Bohrschrauber EasyDrill 18V-38 inkl. Akku',1,59.95,'6257802','Volketswil 19'),
]
rows = []
for r in R:
    i,k,n,sp,m,eh,ep,kg,q,url,art,bez,best = r
    rows.append(dict(id=i,kat=k,name=n,spez=sp,menge=m,eh=eh,ep=ep,gp=round(m*ep,2),kg_einheit=kg,kg=round(m*kg,1),quelle=q,url=url,art=art,bezug=bez,bestand=best))
URLS = {'4793972': 'https://www.obi.ch/zemente-kalke/zement-cem-i-42-5-n/p/4793972', '5047857': 'https://www.obi.ch/einfassungen-stufen-mauersysteme/kann-schalungsstein-grau-24-cm/p/5047857', '5031802': 'https://www.obi.ch/baustahl-baugitter/baustahlmatte-r188a-230-x-100-cm/p/5031802', '5031687': 'https://www.obi.ch/baustahl-baugitter/estrichgitter-verzinkt-200-x-100-cm/p/5031687', '6464333': 'https://www.obi.ch/osb-platten-verlegeplatten/osb-platte-nut-und-feder-hxbxt-1-8-x-62-5-x-250-cm/p/6464333', '2473270': 'https://www.obi.ch/saegeraue-ware/schalbrett-saegerau-fichte-tanne-23-x-150-mm-laenge-3-m/p/2473270', '4895694': 'https://www.obi.ch/saegeraue-ware/brett-saegerau-fichte-tanne-23-x-100-mm-laenge-2-m/p/4895694', '5390067': 'https://www.obi.ch/grillutensilien/schamottestein-hxbxt-64-x-124-x-250-mm/p/5390067', '5390026': 'https://www.obi.ch/grillutensilien/schamottestein-hxbxt-40-x-200-x-500-mm/p/5390026', '2925493': 'https://www.obi.ch/trockenmoertel/sakret-schamottemoertel-grau-5-kg/p/2925493', '3798733': 'https://www.obi.ch/perlite-vermiculite/pflanzen-perlit-100-l/p/3798733', '2480333': 'https://www.obi.ch/zubehoer-fuer-cheminees-und-schwedenoefen/firefix-rauchrohr-schwarz-15-cm/p/2480333', '4915658': 'https://www.obi.ch/draht-zaungeflecht/gah-alberts-sechseck-geflecht-verzinkt-hoehe-1-m-laenge-10-m/p/4915658', '4983821': 'https://www.obi.ch/bleche/glattblech-stahl-500-x-1-000-mm-staerke-0-75-mm/p/4983821', '5786116': 'https://www.obi.ch/moebelgriffe-moebelknoepfe/siro-moebelgriff-s113-kiefer-roh-lochabstand-96-mm/p/5786116', '5756416': 'https://www.obi.ch/metallschutzlacke/albrecht-thermolack-schwarz-matt-125-ml/p/5756416', '4048450': 'https://www.obi.ch/spanplattenschrauben-universalschrauben/lux-universalschraube-senkkopf-4-x-40-mm-tx-antrieb-200-stk-/p/4048450', '4582912': 'https://www.obi.ch/weitere-gartenhelfer/obi-bindedraht-verzinkt-1-4-mm-x-20-m/p/4582912', '2435469': 'https://www.obi.ch/baufolien-planen/lux-gewebeplane-gruen-4-x-5-m/p/2435469', '1755560': 'https://www.obi.ch/zubehoer-fuer-winkelschleifer/lux-diamant-trennscheibe-universal-125-mm/p/1755560', '1206051': 'https://www.obi.ch/zubehoer-fuer-winkelschleifer/lux-trennscheiben-sparpack-metall-125-mm/p/1206051', '1240837': 'https://www.obi.ch/pruefwerkzeuge-messwerkzeuge/lux-maurerschnur-classic-rot-20-m/p/1240837', '1237163': 'https://www.obi.ch/pruefwerkzeuge-messwerkzeuge/lux-zimmermannsbleistift-classic-24-cm/p/1237163', '5799150': 'https://www.obi.ch/baueimer-moertelkuebel/jopa-moertelkasten-schwarz-fassungsvermoegen-90-l/p/5799150', '5799200': 'https://www.obi.ch/baueimer-moertelkuebel/jopa-moerteleimer-mit-buegel-fassungsvermoegen-20-l/p/5799200', '4904546': 'https://www.obi.ch/spanngurte-zurrgurte/spanngurt-unitec-mit-klemmverschluss-3-m-400-kg/p/4904546', '5102272': 'https://www.obi.ch/teppichgleitschutz/antirutschunterlage-schwarz-30-x-150-cm/p/5102272', '3084563': 'https://www.obi.ch/atemschutz-zubehoer/lux-feinstaubmaske-ffp3-2-stueck/p/3084563', '3084571': 'https://www.obi.ch/augenschutz/schutzbrille-mit-buegeln/p/3084571', '5087713': 'https://www.obi.ch/gehoerschutz/3m-gehoerschutzstoepsel-mit-kordel-1271/p/5087713', '6608442': 'https://www.obi.ch/arbeitshandschuhe/pu-handschuh-gr-8/p/6608442', '5474523': 'https://www.obi.ch/baugeraete/betonstampfer-13-x-20-cm-stiellaenge-105-cm/p/5474523', '5047022': 'https://www.obi.ch/multitools-spezialwerkzeuge/einhell-farb-moertelruehrer-te-mx-1600-2-ce/p/5047022', '5907696': 'https://www.obi.ch/maurer-fliesenleger-verlegewerkzeuge/lux-kellenset-3-tlg-/p/5907696', '1240233': 'https://www.obi.ch/maurer-fliesenleger-verlegewerkzeuge/lux-fugenkelle-classic-10-mm/p/1240233', '5295126': 'https://www.obi.ch/brandschutz/abus-loeschdecke-ld1118/p/5295126', '6003131': 'https://www.obi.ch/zubehoer-fuer-cheminees-und-schwedenoefen/valo-ascheeimer-oval-mit-deckel-schwarz-hxbxt-42-x-31-x-61-cm-24-l/p/6003131', '1261262': 'https://www.obi.ch/spaten-gabel-schaufel/lux-holsteiner-schaufel-eingestielt-breite-245-mm/p/1261262', '1262013': 'https://www.obi.ch/spaten-gabel-schaufel/lux-gaertnerspaten-mit-t-griff-eingestielt-85-cm/p/1262013', '4498705': 'https://www.obi.ch/bodenbearbeitung/lux-kreuzhacke-1-5-kg-mit-90-cm-stiel-und-huelse/p/4498705', '6539670': 'https://www.obi.ch/baugeraete/obi-gartenschubkarre-85-l-luftrad-mit-kugellager-120-kg-tragkraft/p/6539670', '3085115': 'https://www.obi.ch/pruefwerkzeuge-messwerkzeuge/lux-alu-wasserwaage-classic-100-cm/p/3085115', '5832332': 'https://www.obi.ch/pruefwerkzeuge-messwerkzeuge/sola-rollbandmass-popular-laenge-5-m/p/5832332', '1397025': 'https://www.obi.ch/haemmer/lux-gummihammer-classic-54-mm/p/1397025', '1222538': 'https://www.obi.ch/handsaegen-feilen/lux-handsaege-classic-holz-450-mm/p/1222538', '5537113': 'https://www.obi.ch/schleifmaschinen/einhell-winkelschleifer-tc-ag-125-850/p/5537113', '6257802': 'https://www.obi.ch/akkuschrauber/bosch-akku-bohrschrauber-easydrill-18v-38-inkl-akku-2-5-ah-und-koffer/p/6257802'}
haus = [dict(id=h[0],name=h[1],menge=h[2],ep=h[3],gp=round(h[2]*h[3],2),art=h[4],bestand=h[5],url=URLS.get(h[4], f'{OBI}/p/{h[4]}')) for h in HAUS]
def summe(kats): return round(sum(r['gp'] for r in rows if r['kat'] in kats),2)
S = dict(material=summe('M'), klein=summe('K'), gebinde=summe('G'), schutz=summe('S'), werkzeug=summe('W'), betrieb=summe('B'))
S['budget_2000'] = round(S['material']+S['klein']+S['gebinde']+S['schutz'],2)        # was die Vorgabe "ALLES inkl. Kleinmaterial" umfasst
S['gesamt_mit_werkzeug'] = round(S['budget_2000']+S['werkzeug']+S['betrieb'],2)
S['haus_falls_fehlend'] = round(sum(h['gp'] for h in haus),2)
S['worst_case'] = round(S['gesamt_mit_werkzeug']+S['haus_falls_fehlend'],2)
gewicht = round(sum(r['kg'] for r in rows),1)
# ------------------------------------------------ Phasen und Fahrten (Fassung 3, 13.10.2026 15:15)
# Phase 1 = Sockel/Unterbau (Fundament, Sockel, Herdplatte), Phase 2 = Ofen (Kuppel, Dämmung, Kamin, Tür, Betrieb).
PHASE2 = {'K3','O07','O08','O09','O10','O11','O12','O13','O14','O15','O19','O34','O35','O36'}
for r in rows: r['phase'] = 2 if r['id'] in PHASE2 else 1
RID = {r['id']: r for r in rows}
OFT_ADR = 'OBI Oftringen, Ackerweg 2, 4665 Oftringen'; VOL_ADR = 'OBI Volketswil, Industriestrasse 20, 8604 Volketswil'
KIES_ADR = 'Tägerhard Kies AG, Tägerhardstrasse 151, 5430 Wettingen'
# Oeffnungszeiten: obi.ch/markt/<ort> (schema.org openingHours, abgerufen 13.10.2026), Taegerhard: Preisliste 2026
OFT_H = 'Mo–Do 08–19, Fr 08–20, Sa 08–18'; VOL_H = 'Mo–Fr 08–20, Sa 08–18'; KIES_H = 'Mo–Fr 07:00–12:00, 13:00–16:45'
def obi(markt, ids): return {i: RID[i]['bezug'][markt] for i in ids}
P1_VOL = [r['id'] for r in rows if r['phase']==1 and 'Volketswil' in r['bezug']]
P2_VOL = [r['id'] for r in rows if r['phase']==2 and 'Volketswil' in r['bezug'] and r['id'] != 'O07']   # O07: die 14 Steine faehrt B schon am Mi mit
TOUREN = [
 dict(key='A', phase=1, ort='oftringen', tag='Di 13.10.', zeit='heute, Abfahrt spätestens 17:30 (Markt offen bis 19:00)', adr=OFT_ADR, oeffnung=OFT_H, tel='058 329 15 00',
      items={i: RID[i]['bezug']['Oftringen'] for i in RID if 'Oftringen' in RID[i]['bezug']},
      warum='Zement gibt es nur hier (Volketswil 0). Gurte, Matten und Mörtelkästen braucht ihr schon für diese Fahrt und für K1 morgen um 07:00. Die 25 Schamottsteine, 1 Platte und das Türblech sind Ofen-Material, das ihr jetzt mitnehmt: Oftringen hat nur 25 Steine, nirgends sonst gibt es genug.'),
 dict(key='K1', phase=1, ort='kies', tag='Mi 14.10.', zeit='07:00', adr=KIES_ADR, oeffnung=KIES_H, tel='056 426 70 45', kies=[('K1',0.56)], warum='Kieskoffer, Lagen 1–3'),
 dict(key='B', phase=1, ort='volketswil', tag='Mi 14.10.', zeit='08:15', adr=VOL_ADR, oeffnung=VOL_H, tel='058 329 12 00', items=obi('Volketswil', P1_VOL + ['O07']),
      warum='Alles für Fundament, Sockel und Herdplatte: Schalungssteine, Bewehrung, Schalung, Rührwerk, Kellen, Schutz. Dazu die restlichen 14 Schamottsteine (Ofen-Material): Damit habt ihr alle 39 Steine sicher, bevor sie jemand anderes kauft.'),
 dict(key='K2', phase=1, ort='kies', tag='Mi 14.10.', zeit='13:00', adr=KIES_ADR, oeffnung=KIES_H, tel='056 426 70 45', kies=[('K1',0.19),('K2',0.33)], warum='Rest Kieskoffer + erster Betonkies'),
 dict(key='K3', phase=1, ort='kies', tag='Do 15.10.', zeit='07:00', adr=KIES_ADR, oeffnung=KIES_H, tel='056 426 70 45', kies=[('K2',0.50)], warum='Betonkies Fundament'),
 dict(key='K4', phase=1, ort='kies', tag='Do 15.10.', zeit='08:00', adr=KIES_ADR, oeffnung=KIES_H, tel='056 426 70 45', kies=[('K2',0.27),('K3',0.25)],
      warum='Rest Betonkies (Sockelfüllung + Herdplatte am So). Der Sand ist Ofen-Material und fährt mit, weil die Fahrt ohnehin stattfindet.'),
 dict(key='C', phase=2, ort='volketswil', tag='Mo 19.10.', zeit='08:00 (spätestens Di 20.10. – Perlit wird am Mi 21.10. gebraucht)', adr=VOL_ADR, oeffnung=VOL_H, tel='058 329 12 00',
      items=obi('Volketswil', P2_VOL), warum='Der Ofen: 17 Schamottplatten, Mörtel, Perlit, Kaminrohr, Putzträger, Tür, Brandschutz. Am Vorabend den Bestand prüfen (Regel unten).'),
]
for t in TOUREN:
    pos = []
    for i, m in t.get('items', {}).items():
        r = RID[i]; pos.append(dict(id=i, name=r['name'], art=r['art'], menge=m, eh=r['eh'], kg=round(m*r['kg_einheit'],1), chf=round(m*r['ep'],2), phase=r['phase'], url=r['url']))
    for i, m3 in t.get('kies', []):
        r = RID[i]; pos.append(dict(id=i, name=r['name'], art=r['art'], menge=m3, eh='m³', kg=round(m3*r['kg_einheit']), chf=round(m3*r['ep'],2), phase=r['phase'], url=r['url']))
    t['pos'] = pos; t['kg'] = round(sum(p['kg'] for p in pos)); t['chf'] = round(sum(p['chf'] for p in pos), 2)
    t['vorgezogen_chf'] = round(sum(p['chf'] for p in pos if p['phase'] > t['phase']), 2)
    t.pop('items', None); t.pop('kies', None)
# Kontrolle: jede Position genau einmal vollstaendig verteilt
for r in rows:
    tot = sum(p['menge'] for t in TOUREN for p in t['pos'] if p['id'] == r['id'])
    assert abs(tot - r['menge']) < 1e-9, (r['id'], tot, r['menge'])
assert abs(sum(t['chf'] for t in TOUREN) - sum(r['gp'] for r in rows)) < 0.05
PHASEN = {p: dict(chf=round(sum(r['gp'] for r in rows if r['phase']==p),2), kg=round(sum(r['kg'] for r in rows if r['phase']==p))) for p in (1,2)}
fahrten = {f"{t['key']} {t['tag']}": t['kg'] for t in TOUREN}
NUTZ = dict(gesamtgewicht=3060, leergewicht=1965, beifahrer=75, ausruestung=20)
out = dict(abruf='13.10.2026', kurs=EUR_CHF, d=D, nf_kauf=NF_KAUF, zement_total_kg=round(zement_total,1), zement_sack=zement_sack,
           rows=rows, haus=haus, summen=S, gewicht=gewicht, fahrten=fahrten, touren=TOUREN, phasen=PHASEN,
           nutzlast=dict(**NUTZ, nutzlast=NUTZ['gesamtgewicht']-NUTZ['leergewicht'], verfuegbar=NUTZ['gesamtgewicht']-NUTZ['leergewicht']-95, planungsgrenze=900))
json.dump(out, open('stueckliste.json','w'), indent=1, ensure_ascii=False)
art = {r['art']: dict(name=r['name'], menge=m, markt=mk) for r in rows if r['quelle']=='OBI' for mk,m in r['bezug'].items()}
# Artikel mit Bezug in 2 Maerkten: getrennte Pruefung
art = {}
for r in rows:
    if r['quelle']!='OBI': continue
    for mk,m in r['bezug'].items(): art[f"{r['art']}" if len(r['bezug'])==1 else r['art']+'@'+mk] = dict(name=r['name'], menge=m, markt=mk)
json.dump({k.split('@')[0] if '@' not in k else k: v for k,v in art.items()}, open('obi_artikel.json','w'), indent=1, ensure_ascii=False)
if __name__=='__main__':
    for r in rows: print(f"{r['id']:4} {r['kat']} {r['name'][:55]:55} {r['menge']:>5} {r['eh']:5} {r['ep']:7.2f} {r['gp']:8.2f} {r['kg']:7.1f} {r['bezug']}")
    print(S); print('Gewicht', gewicht, PHASEN)
    for t in TOUREN: print(t['key'], t['tag'], t['kg'], 'kg', t['chf'], 'CHF', 'davon vorgezogen', t['vorgezogen_chf'])
