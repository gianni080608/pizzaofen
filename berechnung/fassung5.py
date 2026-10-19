#!/usr/bin/env python3
"""Fassung 5 (19.10.2026): Was ist gekauft, was fehlt, wo gibt es es heute.
Liest stueckliste.json (Preise, Gewichte, Links aus Fassung 3), ergebnis.json (Mengen, neu gerechnet)
und fragt den OBI-Lagerbestand live ab. Schreibt fassung5.json fuer Bauplan und Einkaufsliste.
Aufruf: python3 fassung5.py            (live)
        python3 fassung5.py --offline  (letzten Bestand aus fassung5.json weiterverwenden)"""
import json, math, sys, datetime, urllib.request, os

H = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(H, 'stueckliste.json')))
E = json.load(open(os.path.join(H, 'ergebnis.json')))
R = {r['id']: r for r in S['rows']}
V = E['D80']; U = E['unterbau']
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
MARKT = {'021': 'Basel', '022': 'Volketswil', '023': 'Renens', '024': 'Carouge', '025': 'Oftringen', '026': 'S. Antonino',
         '027': 'Agno', '028': 'Schönbühl', '029': 'Winterthur', '030': 'St. Gallen', '031': 'Thun', '032': 'Schaffhausen',
         '033': 'Nyon', '034': 'Stans', '035': 'Steinhausen'}

# ------------------------------------------------------------------ gekauft (laut Fassung 4, bezahlt bis 14.10. morgens)
GEKAUFT = {
    'B': dict(ort='OBI Volketswil', pos={'O02': 26, 'O03': 2, 'O03b': 2, 'O04': 2, 'O05': 3, 'O06': 4, 'O16': 1, 'O17': 1,
                                          'O20': 1, 'O22': 2, 'O32': 1, 'O33': 1, 'O07': 14}),
    'C': dict(ort='OBI Volketswil', pos={'O08': 17, 'O09': 5, 'O10': 3, 'O12': 1, 'O14': 1, 'O15': 1, 'O19': 1, 'O34': 1}),
}
# bewusst nicht gekauft (von zuhause): Maurerschnur, FFP3, Brillen, Gehoerschutz, Loeschdecke, Ascheeimer
ZUHAUSE = ['O21', 'O27', 'O28', 'O29', 'O35', 'O36']

# ------------------------------------------------------------------ Bedarf Fassung 5 (aus ergebnis.json)
k = V['kuppel']
halbe = k['halbsteine_reihen']
nf_bedarf = math.ceil(halbe / 2)                            # 30 NF ohne Reserve
NF_KAUF_TOTAL = 35                                           # 14 + 21: 10 Halbsteine Reserve fuer Keilzuschnitt/Bruch
platten_bedarf = V['platten_total']                         # 11 Boden + 2 Deckplatten + 5 fuer 10 Tunnelstreifen
BETON_MIX_L = 39                                             # 1/2 Sack + 3 Eimer a 14 l Betonkies + 5.5 l Wasser
mix_fund = math.ceil(U['fundament_m3'] * 1000 / BETON_MIX_L)
mix_herd = math.ceil((U['fuellbeton_m3'] + U['herdplatte_m3']) * 1000 / BETON_MIX_L)
perlit_sack = math.ceil(V['perlit_l'] / 100)
PERLIT_MIX = perlit_sack * 2                               # Mischungen a 1/2 Sack Perlit (50 l) + 10 l Zement (13 kg)
zement = dict(beton=(mix_fund + mix_herd) * 12.5, moertelbett=6.25, perlit=PERLIT_MIX * 13.0, putz=V['zement_putz_kg'])
zement['total_kg'] = round(sum(zement.values()), 1)
zement['sack'] = math.ceil(zement['total_kg'] / 25)
ZEMENT_KAUF = zement['sack'] + (1 if zement['sack'] * 25 - zement['total_kg'] < 10 else 0)   # mind. 10 kg Reserve
zement['reserve_kg'] = round(ZEMENT_KAUF * 25 - zement['total_kg'], 1)
betonkies_m3 = round((mix_fund + mix_herd) * 3 * 14 / 1000, 2)
BEDARF = dict(nf=nf_bedarf, halbsteine=halbe, platten=platten_bedarf, zement_sack=zement['sack'], perlit_sack=perlit_sack,
              mischungen_fundament=mix_fund, mischungen_herdplatte=mix_herd, mischungen_perlit=PERLIT_MIX, betonkies_m3=betonkies_m3,
              kiesgemisch_m3=round(U['kies_lose_m3'], 2), sand_m3=round(V['sand_putz_m3'] + 0.02 + 0.005, 3))

# ------------------------------------------------------------------ noch kaufen
def pos(id_, menge, markt, pflicht=True, warum=''):
    r = R[id_]
    return dict(id=id_, art=r['art'], name=r['name'], menge=menge, eh=r['eh'], ep=r['ep'], chf=round(r['ep'] * menge, 2),
                kg=round(r['kg'] / r['menge'] * menge, 1), markt=markt, pflicht=pflicht, warum=warum, url=r.get('url', ''))

FAHRT_A = [
    dict(key='A1', ort='OBI Oftringen', adr='OBI Oftringen, Ackerweg 2, 4665 Oftringen', tel='058 329 15 00',
         oeffnung='Mo–Do 08–19, Fr 08–20, Sa 08–18', weg='42 km · ca. 35 min ab Würenlos', pos=[
        pos('O01', ZEMENT_KAUF, 'Oftringen', warum=f"Bedarf {zement['total_kg']:.0f} kg, Reserve {zement['reserve_kg']:.0f} kg"),
        pos('O08', 2, 'Oftringen', warum='18 nötig, 17 gekauft: 1 fehlt + 1 Reserve'),
        pos('O10', 1, 'Oftringen', warum=f"Bedarf {V['perlit_l']} l = {perlit_sack} Sack, 3 gekauft"),
        pos('O13', 1, 'Oftringen', warum='Tür und Kaminabdeckung'),
        pos('O24', 10, 'Oftringen', warum='Kies holen, Mischungen abmessen'),
        pos('O11', 1, 'Oftringen', warum='Kaminrohr (stand schon in Fassung 3 auf der Liste). Habt ihr doch eins vom Kollegen: weglassen'),
        pos('O31', 1, 'Oftringen', warum='Pflicht: neuer Kieskoffer muss verdichtet werden (sonst Basel, 4 Stk.)'),
        pos('O18', 2, 'Oftringen', False, 'nur wenn zuhause keine 3 grossen Planen'),
        pos('O25', 4, 'Oftringen', False, 'nur wenn keine Spanngurte zuhause'),
        pos('O26', 3, 'Oftringen', False, 'nur wenn keine Antirutschmatten zuhause'),
        pos('O30', 4, 'Oftringen', False, 'nur wenn keine Arbeitshandschuhe zuhause'),
    ]),
    dict(key='A2', ort='OBI Basel Dreispitz', adr='OBI Basel, Reinacherstrasse 29, 4053 Basel', tel='058 329 11 00',
         oeffnung='Mo–Fr 08–20, Sa 08–18', weg='55 km ab Oftringen · 66 km zurück nach Würenlos', pos=[
        pos('O07', 21, 'Basel', warum='nur Basel hat genug (Oftringen 0, Volketswil 9, Winterthur 3)'),
        pos('O23', 6, 'Basel', warum='4 zum Kies holen und Mischen + 2, damit eine Fahrt ins Kieswerk 900 kg fasst'),
    ]),
]
KIES = [
    dict(key='K1', zweck='Kieskoffer (S2)', pos=[('Kiesgemisch 0/31.5', '60201', 0.55, 1600)]),
    dict(key='K2', zweck='Fundament (S4)', pos=[('Betonkies gewaschen 0/16', '20001', 0.50, 1800)]),
    dict(key='K3', zweck='Mörtelbett Sockel (S5), Herdplatte, Putz', pos=[('Betonkies gewaschen 0/16', '20001', 0.36, 1800), ('Sand gewaschen 0/4', '40001', 0.15, 1500)]),
    dict(key='K4', zweck='Herdplatte (S6)', pos=[('Betonkies gewaschen 0/16', '20001', 0.24, 1800)]),
]
for t in KIES:
    t['kg'] = round(sum(m * d for _, _, m, d in t['pos']))
    t['chf'] = round(sum(m * 60 for _, _, m, _ in t['pos']), 2)
    assert t['kg'] <= 900, t

# ------------------------------------------------------------------ Lagerbestand live
def bestand(art):
    r = urllib.request.Request(f"https://www.obi.ch/article-service/store-availabilities/ch/{art}",
                               headers={"User-Agent": UA, "x-obi-application": "decide-storefinder-adapter"})
    d = json.load(urllib.request.urlopen(r, timeout=25))
    return {MARKT[x['storenumber']]: x['stock'] for x in d if x['storenumber'] in MARKT}

offline = '--offline' in sys.argv
alt = json.load(open(os.path.join(H, 'fassung5.json'))) if offline else None
zeit = alt['bestand_zeit'] if offline else datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))).strftime('%d.%m.%Y %H:%M')
BEST = alt['bestand'] if offline else {}
ok = True
for t in FAHRT_A:
    for p in t['pos']:
        if not offline and p['art'] not in BEST:
            BEST[p['art']] = bestand(p['art'])
        b = BEST[p['art']]
        p['bestand'] = b.get(p['markt'], 0)
        p['ok'] = p['bestand'] >= p['menge']
        ok &= p['ok'] or not p['pflicht']
        p['alternativ'] = ', '.join(f'{m} {n}' for m, n in sorted(b.items(), key=lambda x: -x[1]) if m != p['markt'] and n >= p['menge'])[:80]
for art in ['5390067']:
    if not offline and art not in BEST:
        BEST[art] = bestand(art)
for t in FAHRT_A:
    t['chf_pflicht'] = round(sum(p['chf'] for p in t['pos'] if p['pflicht']), 2)
    t['chf_alles'] = round(sum(p['chf'] for p in t['pos']), 2)
    t['kg'] = round(sum(p['kg'] for p in t['pos']))

# ------------------------------------------------------------------ Summen
def summe(posd):
    return round(sum(R[i]['ep'] * m for i, m in posd.items()), 2)
bezahlt = {k_: summe(v['pos']) for k_, v in GEKAUFT.items()}
assert abs(bezahlt['B'] - 575.45) < 0.01 and abs(bezahlt['C'] - 578.15) < 0.01, bezahlt
a_min = round(sum(t['chf_pflicht'] for t in FAHRT_A), 2)
a_max = round(sum(t['chf_alles'] for t in FAHRT_A), 2)
kies = round(sum(t['chf'] for t in KIES), 2)
SUM = dict(bezahlt_B=bezahlt['B'], bezahlt_C=bezahlt['C'], bezahlt=round(bezahlt['B'] + bezahlt['C'], 2),
           fahrt_a_min=a_min, fahrt_a_max=a_max, kies=kies,
           offen_min=round(a_min + kies, 2), offen_max=round(a_max + kies, 2))
SUM['total_min'] = round(SUM['bezahlt'] + SUM['offen_min'], 2)
SUM['total_max'] = round(SUM['bezahlt'] + SUM['offen_max'], 2)

out = dict(stand='Mo 19.10.2026', bestand_zeit=zeit, bestand=BEST, alles_da=ok, bedarf=BEDARF, zement=zement,
           zement_kauf=ZEMENT_KAUF, nf_kauf_total=NF_KAUF_TOTAL,
           gekauft={k_: dict(ort=v['ort'], chf=bezahlt[k_], pos=[dict(id=i, art=R[i]['art'], name=R[i]['name'], menge=m, eh=R[i]['eh'], chf=round(R[i]['ep'] * m, 2)) for i, m in v['pos'].items()]) for k_, v in GEKAUFT.items()},
           zuhause=[dict(id=i, art=R[i]['art'], name=R[i]['name'], menge=R[i]['menge'], eh=R[i]['eh'], chf=R[i]['gp']) for i in ZUHAUSE],
           fahrt_a=FAHRT_A, kies=KIES, summen=SUM)
json.dump(out, open(os.path.join(H, 'fassung5.json'), 'w'), indent=1, ensure_ascii=False)

print(f"Bestand {zeit}  ->  {'ALLES DA' if ok else 'ACHTUNG: etwas fehlt'}")
print('Bedarf:', BEDARF)
print('Zement:', zement, '-> kaufen', ZEMENT_KAUF)
for t in FAHRT_A:
    print(f"\n{t['key']} {t['ort']}  Pflicht CHF {t['chf_pflicht']:.2f}  alles CHF {t['chf_alles']:.2f}  {t['kg']} kg")
    for p in t['pos']:
        print(f"  {'OK ' if p['ok'] else '!! '} {p['menge']:>3} {p['eh']:<5} {p['name'][:48]:48} Bestand {p['bestand']:>4}  {p['chf']:8.2f}  {'' if p['pflicht'] else '(optional)'}")
for t in KIES:
    print(t['key'], t['zweck'], t['pos'], t['kg'], 'kg', t['chf'])
print('\nSummen:', SUM)
