#!/usr/bin/env python3
"""Fragt den aktuellen Lagerbestand aller OBI-Artikel der Einkaufsliste ab (oeffentliche Schnittstelle von obi.ch,
dieselbe, die die Website fuer "Verfuegbarkeit im Markt pruefen" nutzt). Aufruf: python3 obi_bestand.py
Schreibt obi_bestand.json mit Zeitstempel."""
import json, urllib.request, datetime, sys
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
MAERKTE = {'022': 'Volketswil', '025': 'Oftringen', '029': 'Winterthur', '021': 'Basel', '032': 'Schaffhausen'}
ART = json.load(open('obi_artikel.json'))
def bestand(a):
    r = urllib.request.Request(f"https://www.obi.ch/article-service/store-availabilities/ch/{a}",
                               headers={"User-Agent": UA, "x-obi-application": "decide-storefinder-adapter"})
    try:
        d = json.load(urllib.request.urlopen(r, timeout=25))
    except Exception as e:
        return {'fehler': str(e)}
    return {MAERKTE[x['storenumber']]: x['stock'] for x in d if x['storenumber'] in MAERKTE}
out = dict(zeit=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='minutes'), artikel={})
ok = True
for a, info in ART.items():
    b = bestand(a.split("@")[0]); out["artikel"][a] = dict(info, bestand=b)
    need = info['menge']; markt = info['markt']; have = b.get(markt, 0)
    flag = 'OK ' if isinstance(have, int) and have >= need else 'ZU WENIG'
    ok &= flag == 'OK '
    print(f"{flag:8} {a} {info['name'][:52]:52} {markt:10} braucht {need:3}  hat {have}")
json.dump(out, open('obi_bestand.json', 'w'), indent=1, ensure_ascii=False)
print('\nALLES VERFUEGBAR' if ok else '\nACHTUNG: mindestens ein Artikel reicht nicht -> Plan B im Dokument (Kap. 10.3)')
sys.exit(0 if ok else 1)
