#!/usr/bin/env python3
"""Grundkarte fuer karte.html: OSM-Daten holen (Overpass, Nominatim, OSRM), vereinfachen, in lokale Koordinaten projizieren -> basemap.json.
Aufruf: python3 basemap.py <cache-ordner>   (vorhandene Dateien im Cache werden nicht neu geladen)
Daten: (c) OpenStreetMap-Mitwirkende, ODbL. Routen: OSRM Demo-Server (router.project-osrm.org)."""
import json, math, os, sys, time, urllib.parse, urllib.request
C = sys.argv[1] if len(sys.argv) > 1 else 'cache'; os.makedirs(C, exist_ok=True)
H = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'pizzaofen-plan/1.0 (privat)'}
OVERPASS = 'https://maps.mail.ru/osm/tools/overpass/api/interpreter'   # overpass-api.de lief am 13.10. in Timeouts
BBOX = (47.24, 7.84, 47.62, 8.80)
ORTE = {  # lon, lat (Nominatim, 13.10.2026)
 'home': (8.366084, 47.4428612), 'kies': (8.3408231, 47.4540442), 'oftringen': (7.9286324, 47.3085811),
 'volketswil': (8.6749119, 47.3798843), 'winterthur': (8.761635, 47.4969019)}
LAT0, LON0, K = 47.45, 8.30, 1000.0     # 1 Einheit = 1/1000 Grad Breite = 111 m
COS = math.cos(math.radians(LAT0))
def P(lon, lat): return (round((lon - LON0) * COS * K, 1), round((LAT0 - lat) * K, 1))
def get(url, data=None, fn=None):
    f = os.path.join(C, fn)
    if os.path.exists(f) and os.path.getsize(f) > 500: return json.load(open(f))
    req = urllib.request.Request(url, data=data.encode() if data else None, headers=UA)
    d = json.load(urllib.request.urlopen(req, timeout=180)); json.dump(d, open(f, 'w')); time.sleep(1); return d
def dp(pts, tol):  # Douglas-Peucker
    if len(pts) < 3: return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]; dx, dy = x2 - x1, y2 - y1; n = math.hypot(dx, dy)
    if n < 1e-6:   # Anfang = Ende (Rundfahrt, Ring): am entferntesten Punkt teilen
        i = max(range(len(pts)), key=lambda k: math.hypot(pts[k][0] - x1, pts[k][1] - y1))
        return pts if i == 0 else dp(pts[:i + 1], tol)[:-1] + dp(pts[i:], tol)
    i, dm = 0, -1
    for k in range(1, len(pts) - 1):
        d = abs(dy * pts[k][0] - dx * pts[k][1] + x2 * y1 - y2 * x1) / n
        if d > dm: i, dm = k, d
    if dm <= tol: return [pts[0], pts[-1]]
    return dp(pts[:i + 1], tol)[:-1] + dp(pts[i:], tol)
def path(lines, tol, closed=False):
    out = []
    for ln in lines:
        pp = [P(*p) for p in ln]
        q = dp(pp, tol)
        if len(q) < 2: continue
        out.append('M' + ' '.join(f'{x:g},{y:g}' for x, y in q) + ('Z' if closed else ''))
    return ''.join(out)
b = ','.join(map(str, BBOX))
mw = get(OVERPASS, 'data=' + urllib.parse.quote(f'[out:json][timeout:120];(way["highway"="motorway"]({b});node["place"~"^(city|town)$"]({b}););out geom;'), 'mw.json')
rv = get(OVERPASS, 'data=' + urllib.parse.quote(f'[out:json][timeout:120];relation["waterway"="river"]["name"~"^(Limmat|Aare|Reuss|Rhein|Glatt|Töss)$"]({b});out geom;'), 'rivers.json')
lakes = []
for n in ['Zürichsee', 'Greifensee', 'Hallwilersee', 'Pfäffikersee', 'Baldeggersee', 'Sempachersee', 'Türlersee']:
    d = get('https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode(dict(q=n, format='json', polygon_geojson=1, polygon_threshold=0.001, limit=1, countrycodes='ch')), fn=f'lake_{n}.json')
    g = d[0]['geojson']; rings = g['coordinates'] if g['type'] == 'Polygon' else [r for poly in g['coordinates'] for r in poly]
    lakes += [rings[0]] if g['type'] == 'Polygon' else rings
def route(name, pts):
    co = ';'.join(f'{ORTE[p][0]},{ORTE[p][1]}' for p in pts)
    d = get(f'https://router.project-osrm.org/route/v1/driving/{co}?overview=full&geometries=geojson', fn=f'route_{name}.json')
    r = d['routes'][0]
    return dict(km=round(r['distance'] / 1000, 1), min=round(r['duration'] / 60), legs=[[round(l['distance'] / 1000, 1), round(l['duration'] / 60)] for l in r['legs']],
                d=path([r['geometry']['coordinates']], 0.04 if name == 'kies' else 0.12))
routes = {'oftringen': route('oftringen', ['home', 'oftringen', 'home']), 'volketswil': route('volketswil', ['home', 'volketswil', 'home']),
          'kies': route('kies', ['home', 'kies', 'home']), 'winterthur': route('winterthur', ['home', 'volketswil', 'winterthur', 'home'])}
mways = [[(p['lon'], p['lat']) for p in e['geometry']] for e in mw['elements'] if e['type'] == 'way']
rivers = [[(p['lon'], p['lat']) for p in m['geometry']] for e in rv['elements'] for m in e.get('members', []) if m['type'] == 'way' and 'geometry' in m]
inb = lambda ln: [p for p in ln if BBOX[1] - .05 <= p[0] <= BBOX[3] + .05 and BBOX[0] - .05 <= p[1] <= BBOX[2] + .05]
rivers = [r for r in (inb(x) for x in rivers) if len(r) > 1]
places = [dict(n=e['tags']['name'].replace(' ZH', '').replace(' AG', ''), t=e['tags']['place'], p=P(e['lon'], e['lat'])) for e in mw['elements'] if e['type'] == 'node']
x0, y0 = P(BBOX[1], BBOX[2]); x1, y1 = P(BBOX[3], BBOX[0])
out = dict(quelle='© OpenStreetMap-Mitwirkende (ODbL) · Routen OSRM · abgerufen 13.10.2026', bbox=[x0, y0, x1, y1],
           orte={k: P(*v) for k, v in ORTE.items()}, ll={k: [v[1], v[0]] for k, v in ORTE.items()},
           lakes=path(lakes, 0.3, True), rivers=path(rivers, 0.5), motorways=path(mways, 0.5), places=places, routes=routes)
json.dump(out, open(os.path.join(H, 'basemap.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
print({k: len(v) if isinstance(v, str) else '' for k, v in out.items()}, {k: (v['km'], v['min'], v['legs']) for k, v in routes.items()}, os.path.getsize(os.path.join(H, 'basemap.json')))
