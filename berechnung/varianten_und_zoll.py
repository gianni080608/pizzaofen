#!/usr/bin/env python3
"""Variantenvergleich (A/B/C), Deutschland-Rechnung (MWST/Zoll) und Waermebedarf. Kurs EZB 12.10.2026."""
import json, math
K = 0.9312
S = json.load(open('stueckliste.json')); E = json.load(open('ergebnis.json'))
B = S['gesamt']
r = lambda x: round(x, 2)
out = {}
# --- Variante C: 80 cm + NF online an DE-Lieferadresse + Mischer geliehen + Handstampfer
d80, d90 = E['D80'], E['D90']
minus_80 = (d90['nf_total'] - d80['nf_total']) * 8.50 + (d90['platten_total'] - d80['platten_total']) * 18.95 + (math.ceil(d90['perlit_l']/100) - math.ceil(d80['perlit_l']/100)) * 29.95
nf_de_eur = d80['nf_total'] * 4.12                     # schamotte-shop.de Staffelpreis ab 50 Stk
nf_de_netto_chf = nf_de_eur / 1.19 * K
versand_eur, adresse_eur = 60.0, 10.0                 # ANNAHMEN (unbestaetigt)
nf_de_total = (nf_de_netto_chf + versand_eur * K) * 1.081 + adresse_eur * K
nf_ch_80 = d80['nf_total'] * 8.50
C = B - minus_80 - (nf_ch_80 - nf_de_total) - 147 - 77
out['C'] = dict(minus_80=r(minus_80), nf_de_eur=r(nf_de_eur), nf_de_total_chf=r(nf_de_total), nf_ch_80=r(nf_ch_80), total=r(C))
# --- Variante A: Les Cheminees FD 100 + Unterbau aus B
fd_eur, iso_eur = 1149.0, 350.0                        # iso = ANNAHME (3 CS-Platten + 3-4 Pakete Keramikfaser + Moertel)
fd_chf = (fd_eur + iso_eur) / 1.19 * K * 1.081
ofenteile_B = sum(x['gp'] for x in S['rows'] if x['pos'] in ('11', '12', '13', '17')) + 3 * 29.95   # entfallen bei Bausatz (3 von 4 Perlitsaecken)
A = B - ofenteile_B + fd_chf
out['A'] = dict(bausatz_chf_netto_import=r(fd_chf), entfallen=r(ofenteile_B), total=r(A),
               cuppo90_chf=r((2220 + 150) * K), cuppo_import=r((2220 / 1.19 + 150) * K * 1.081))
# --- Deutschland: NF bei OBI Waldshut (Firefix 9.49 EUR) vs OBI CH 8.50
n = d90['nf_total']
brutto = n * 9.49; netto = brutto / 1.19
mit_rueck = netto * K * 1.081
ohne_rueck = brutto * K * 1.081
out['DE_OBI_Waldshut'] = dict(stk=n, brutto_eur=r(brutto), netto_eur=r(netto), chf_netto=r(netto*K), ch_mwst=r(netto*K*0.081),
                              total_mit_rueckerstattung=r(mit_rueck), total_ohne_rueckerstattung=r(ohne_rueck), obi_ch=r(n*8.50))
nf90_de = n * 4.12
out['DE_online_90'] = dict(eur=r(nf90_de), netto_chf=r(nf90_de/1.19*K), total_chf=r((nf90_de/1.19*K + versand_eur*K)*1.081 + adresse_eur*K), obi_ch=r(n*8.5))
# --- Waermebedarf Aufheizen (Kuppel + Boden auf Mittel 350 C, dT 330 K, c = 0.9 kJ/kgK)
for k in ('D80', 'D90', 'D100'):
    m = E[k]['masse_kuppel_kg'] + E[k]['masse_boden_kg']
    kwh = m * 0.9 * 330 / 3600
    out[k] = dict(masse=r(m), kwh=r(kwh), holz_kg_bei_35pct=r(kwh / 0.35 / 4.0), backflaeche_m2=r(math.pi*(E[k]['D']/200)**2))
json.dump(out, open('varianten.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
