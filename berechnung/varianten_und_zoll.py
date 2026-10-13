#!/usr/bin/env python3
"""Variantenvergleich A/B/C, Groessenvergleich 80/90/100, Deutschland-Rechnung, Waermebedarf (Stand 13.10.2026)."""
import json, math
K = 0.9312                                    # EZB 12.10.2026
S = json.load(open('stueckliste.json')); E = json.load(open('ergebnis.json'))
r2 = lambda x: round(x, 2)
B = S['summen']['gesamt_mit_werkzeug']
row = {r['id']: r for r in S['rows']}
out = {'B_80': B}
# --- Groessenvergleich: Mehr-/Minderkosten gegenueber 80 cm (gleiche Stueckliste, nur mengenabhaengige Positionen)
def kosten(k):
    v = E[k]
    nf = v['nf_kuppel'] + 4
    return nf * 8.50 + v['platten_total'] * 18.95 + math.ceil(v['moertel_kg'] / 5) * 17.95 + math.ceil(v['perlit_l'] / 100) * 29.95
base = kosten('D80')
for k in ('D80', 'D90', 'D100'):
    v = E[k]; m = v['masse_kuppel_kg'] + v['masse_boden_kg']; kwh = m * 0.9 * 330 / 3600
    out[k] = dict(nf=v['nf_kuppel'], nf_kauf=v['nf_kuppel'] + 4, platten=v['platten_total'], masse=r2(m), kwh=r2(kwh),
                  backflaeche=r2(math.pi * (v['D'] / 200) ** 2), aussen=v['aussendurchmesser'], tunnel=v['tunnel_laenge'],
                  mehrkosten=r2(kosten(k) - base), total=r2(B + kosten(k) - base), tuer=v['tuer_h'])
out['nf_bestand_umkreis'] = dict(Volketswil=24, Oftringen=25, Basel=21, Schaffhausen=9, Winterthur=3)
# --- Variante A: Bausatz Les Cheminees FD 100 (kleinster Bausatz) + Daemmpaket lt. kuppelofen.de + Unterbau aus B
kit_eur = 1149 + 3 * 60 + 4 * 80 + 45          # FD-Serie ab 1149, 3 CS-Platten a 60, 4 Keramikfaser a 80, Moertel 45
kit_chf = kit_eur / 1.19 * K * 1.081            # mit DE-MWST-Rueckerstattung, + 8.1 % CH
entfallen = sum(row[i]['gp'] for i in ('O07', 'O08', 'O09', 'O10', 'O13'))
out['A'] = dict(kit_eur=kit_eur, kit_chf=r2(kit_chf), entfallen=r2(entfallen), total=r2(B - entfallen + kit_chf),
                cuppo90_eur=2220 + 150, cuppo90_chf=r2((2220 / 1.19) * K * 1.081 + 150 * K))
# --- Variante C: B (80 cm) + Werkzeug ausleihen statt kaufen (Ruehrwerk, Stampfer, Kellen) + Betrieb spaeter
c_minus = sum(row[i]['gp'] for i in ('O31', 'O32', 'O33', 'O34', 'O35', 'O36'))
out['C'] = dict(minus=r2(c_minus), total=r2(B - c_minus))
# --- Deutschland a) OBI Waldshut Firefix NF 9.49 EUR
n = S['nf_kauf']
brutto = n * 9.49; netto = brutto / 1.19
out['DE_Waldshut'] = dict(stk=n, brutto_eur=r2(brutto), netto_eur=r2(netto), chf=r2(netto * K), mwst_ch=r2(netto * K * 0.081),
                          mit=r2(netto * K * 1.081), ohne=r2(brutto * K * 1.081), ch=r2(n * 8.50))
# --- b) schamotte-shop.de online an Lieferadresse Konstanz (35 Stk a 4.20, Paketversand max 79.90, 7 Pakete a 7.00 Annahme)
m = E['D80']['nf_kuppel']
ware = m * 4.20; versand = 79.90; annahme = 7 * 7.00
wert_ch = ware / 1.19 * K                          # massgebend fuer Wertfreigrenze (MWST ausgewiesen)
mwst_ch = 0 if wert_ch <= 150 else wert_ch * 0.081
out['DE_online'] = dict(stk=m, ware_eur=r2(ware), versand_eur=versand, annahme_eur=annahme, total_chf=r2((ware + versand + annahme) * K + mwst_ch),
                        wert_ch=r2(wert_ch), mwst_ch=r2(mwst_ch), ch=r2(m * 8.50), fahrt_km=150)
json.dump(out, open('varianten.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
