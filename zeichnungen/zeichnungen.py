#!/usr/bin/env python3
"""Erzeugt die Bauzeichnungen (SVG) aus den Werten in ../berechnung/ergebnis.json.
Koordinaten in cm. x = Breite (links->rechts), y = Tiefe (0 = hinten/Mauer), z = Hoehe ueber Terrain."""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(HERE, '..', 'berechnung', 'ergebnis.json')))
WAHL = json.load(open(os.path.join(HERE, '..', 'berechnung', 'stueckliste.json')))['d']
V = E[WAHL]; K = V['kuppel']

# ------------------------------------------------------------ Hoehen
Z_KIES0, Z_KIES1 = -30, -10
Z_FUND1 = 5
Z_WAND1 = Z_FUND1 + 75
Z_HERD1 = Z_WAND1 + 10
Z_DAEMM1 = Z_HERD1 + 10
Z_BODEN0 = Z_DAEMM1 + 0.5
Z_BODEN1 = Z_BODEN0 + 4.0                 # Arbeitshoehe
A, C, T = V['D'] / 2, float(V['h']), 6.4
ISO, PUTZ = 8.0, 3.0
CY, CX = V['cy'], 75.0
TUN_B, TUN_W = 40.0, 10.0
TUN_H = V['tuer_h']
Y_TUER = V['y_tuer']
Z_TUN1 = Z_BODEN1 + TUN_H
Z_PLATTE1 = Z_TUN1 + 4
ROHR_L = 100
Z_ROHR1 = Z_PLATTE1 + ROHR_L
Y_KAMIN = round(Y_TUER + 20.5, 1)
Z_KUPPEL_IN = Z_BODEN1 + C
Z_KUPPEL_AUS = Z_BODEN1 + C + T + ISO + PUTZ
HOEHEN = dict(kies=(Z_KIES0, Z_KIES1), fundament=(Z_KIES1, Z_FUND1), sockel=(Z_FUND1, Z_WAND1), herdplatte=(Z_WAND1, Z_HERD1),
              daemmung=(Z_HERD1, Z_DAEMM1), boden=(Z_BODEN0, Z_BODEN1), kuppel_innen_scheitel=Z_KUPPEL_IN,
              kuppel_aussen=Z_KUPPEL_AUS, tunnel_oben=Z_TUN1, platte_oben=Z_PLATTE1, kamin_oben=Z_ROHR1)

COL = dict(kies='#d8cfb8', beton='#c9cdd2', schal='#aeb4bb', herd='#b7bec6', perlit='#f3e7b3', boden='#c8693f',
           stein='#d9844f', iso='#f6edc9', putz='#e7e3dc', stahl='#5b7fa6', mauer='#9aa1a8', erde='#b59b74',
           line='#222', dim='#1c4f8a', hint='#8a3b12')

DEFS = '''<defs>
<pattern id="pKies" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="#d8cfb8"/><circle cx="1" cy="1" r="0.55" fill="#8f8060"/><circle cx="3" cy="2.8" r="0.7" fill="#a8977a"/></pattern>
<pattern id="pBeton" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#c9cdd2"/><circle cx="1.5" cy="2" r="0.35" fill="#7d838b"/><circle cx="4.3" cy="4.5" r="0.5" fill="#8c929a"/><path d="M3.5 1 l0.7 0.6 l-0.9 0.2z" fill="#7d838b"/></pattern>
<pattern id="pSchal" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="5" height="5" fill="#b9bfc6"/><line x1="0" y1="0" x2="0" y2="5" stroke="#6d747c" stroke-width="0.5"/></pattern>
<pattern id="pPerlit" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="#f3e7b3"/><circle cx="2" cy="2" r="0.45" fill="#fffaf0" stroke="#c8b46a" stroke-width="0.15"/></pattern>
<pattern id="pIso" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="#f6edc9"/><circle cx="1" cy="3" r="0.4" fill="#fffaf0" stroke="#c8b46a" stroke-width="0.12"/><circle cx="3" cy="1" r="0.4" fill="#fffaf0" stroke="#c8b46a" stroke-width="0.12"/></pattern>
<pattern id="pErde" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#cdb48f"/><path d="M0 6 L6 0" stroke="#a0855f" stroke-width="0.4"/></pattern>
<marker id="arr" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#1c4f8a"/></marker>
</defs>'''

def svg(w, h, body, title, vb):
    x0, y0, vw, vh = vb
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{x0} {y0} {vw} {vh}" '
            f'font-family="DejaVu Sans, Arial, sans-serif"><title>{title}</title>{DEFS}'
            f'<rect x="{x0}" y="{y0}" width="{vw}" height="{vh}" fill="#ffffff"/>{body}</svg>')

def rect(x, y, w, h, fill, stroke=COL['line'], sw=0.35, extra=''):
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def poly(pts, fill, stroke=COL['line'], sw=0.3, extra=''):
    p = ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts)
    return f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def line(x1, y1, x2, y2, stroke=COL['line'], sw=0.3, extra=''):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def text(x, y, s, size=3.2, anchor='start', fill=COL['line'], weight='normal', rot=None):
    tr = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot is not None else ''
    return f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{weight}"{tr}>{s}</text>'

def dim_h(x1, x2, y, label, off=0, size=3.0):
    return (line(x1, y, x2, y, COL['dim'], 0.25, 'marker-start="url(#arr)" marker-end="url(#arr)"') +
            line(x1, y - 2, x1, y + 2, COL['dim'], 0.2) + line(x2, y - 2, x2, y + 2, COL['dim'], 0.2) +
            text((x1 + x2) / 2, y - 1.2 + off, label, size, 'middle', COL['dim']))

def dim_v(x, y1, y2, label, side=-1, size=3.0):
    tx = x + side * 1.6
    return (line(x, y1, x, y2, COL['dim'], 0.25, 'marker-start="url(#arr)" marker-end="url(#arr)"') +
            line(x - 2, y1, x + 2, y1, COL['dim'], 0.2) + line(x - 2, y2, x + 2, y2, COL['dim'], 0.2) +
            text(tx, (y1 + y2) / 2, label, size, 'middle', COL['dim'], rot=-90))

def half_ellipse(cx, z0, a, c, n=90, sign=1):
    """obere Halbellipse (in SVG-Koordinaten, z nach oben = -y). Rueckgabe Liste (x, svg_y)."""
    return [(cx + a * math.cos(math.pi * i / n), -(z0 + c * math.sin(math.pi * i / n))) for i in range(n + 1)]

def ring(cx, z0, a_in, c_in, a_out, c_out, fill, extra='', clip=None):
    outer = half_ellipse(cx, z0, a_out, c_out)
    inner = list(reversed(half_ellipse(cx, z0, a_in, c_in)))
    return poly(outer + inner, fill, sw=0.3, extra=extra)

def Z(z):
    return -z

# ============================================================== FRONTANSICHT
def frontansicht():
    b = []
    # Terrain + Kies (gestrichelt, im Boden)
    b.append(rect(-35, Z(0), 220, 33, 'url(#pErde)', 'none', 0))
    b.append(line(-35, 0, 185, 0, COL['line'], 0.5))
    b.append(rect(-10, Z(Z_KIES1), 170, 20, 'url(#pKies)', COL['line'], 0.3, 'stroke-dasharray="1.5 1"'))
    b.append(rect(0, Z(Z_FUND1), 150, 15, 'url(#pBeton)'))
    # Sockel: Seitenwaende + Rueckwand sichtbar durch Oeffnung
    b.append(rect(24, Z(Z_WAND1), 102, 75, '#5b5148', COL['line'], 0.3))            # Holzlager (dunkel)
    for i in range(6):                                                                 # Holzscheite angedeutet
        b.append(f'<circle cx="{34 + i * 16:.1f}" cy="{Z(Z_FUND1 + 8):.1f}" r="6.5" fill="#8b6b4a" stroke="#4a3a2a" stroke-width="0.3"/>')
        b.append(f'<circle cx="{42 + i * 16:.1f}" cy="{Z(Z_FUND1 + 20):.1f}" r="6.5" fill="#9c7a55" stroke="#4a3a2a" stroke-width="0.3"/>')
    for x0 in (0, 126):
        b.append(rect(x0, Z(Z_WAND1), 24, 75, 'url(#pSchal)'))
        for k in (1, 2):
            b.append(line(x0, Z(Z_FUND1 + 25 * k), x0 + 24, Z(Z_FUND1 + 25 * k), COL['line'], 0.25))
    b.append(rect(0, Z(Z_HERD1), 150, 10, 'url(#pBeton)'))
    # Daemmung + Boden (sichtbar als Putzband vorne)
    b.append(rect(CX - TUN_B / 2 - TUN_W - PUTZ, Z(Z_TUN1 + 4 + ISO + PUTZ), TUN_B + 2 * (TUN_W + PUTZ), Z_TUN1 + 4 + ISO + PUTZ - Z_HERD1, COL['putz']))
    # Kuppel aussen (verputzt)
    Ra = A + T + ISO + PUTZ
    b.append(poly(half_ellipse(CX, Z_HERD1, Ra, Z_KUPPEL_AUS - Z_HERD1), COL['putz'], sw=0.5))
    # Tunnelvorbau vor die Kuppel zeichnen
    tx0 = CX - TUN_B / 2 - TUN_W - PUTZ
    tw = TUN_B + 2 * (TUN_W + PUTZ)
    b.append(rect(tx0, Z(Z_PLATTE1 + ISO + PUTZ), tw, Z_PLATTE1 + ISO + PUTZ - Z_HERD1, COL['putz'], COL['line'], 0.5))
    # Ziegelbogen-Optik um Oeffnung
    b.append(rect(CX - TUN_B / 2 - 6.4, Z(Z_TUN1 + 4), TUN_B + 12.8, TUN_H + 4 + (Z_BODEN1 - Z_HERD1), COL['stein'], COL['line'], 0.3))
    b.append(rect(CX - TUN_B / 2, Z(Z_TUN1), TUN_B, TUN_H, '#2b1d14', COL['line'], 0.4))
    b.append(rect(CX - TUN_B / 2, Z(Z_TUN1 + 4), TUN_B, 4, COL['boden'], COL['line'], 0.3))
    # Boden-Kante
    b.append(rect(CX - TUN_B / 2, Z(Z_BODEN1), TUN_B, 4, COL['boden'], COL['line'], 0.3))
    # Kamin
    b.append(rect(CX - 7.5, Z(Z_ROHR1), 15, ROHR_L - ISO - PUTZ, '#c7ccd1', COL['line'], 0.4))
    b.append(rect(CX - 10, Z(Z_ROHR1 + 4), 20, 0.8, '#e5e8eb', COL['line'], 0.3, 'stroke-dasharray="1.2 0.8"'))
    b.append(text(CX + 16, Z(Z_ROHR1 + 9), 'Abdeckblech nur bei kaltem Ofen (aus Türblech-Rest)', 2.6, 'start', COL['hint']))
    # Masse
    b.append(dim_h(0, 150, Z(-38), 'Fundament 150', 0))
    b.append(dim_h(-10, 160, Z(-47), 'Kieskoffer 170 (20 cm verdichtet, UK -30)', 0))
    b.append(dim_h(CX - Ra, CX + Ra, Z(Z_KUPPEL_AUS + 8), ''))
    b.append(text(CX - Ra + 2, Z(Z_KUPPEL_AUS + 10), f'Kuppel aussen Ø {2 * Ra:.1f}', 3.0, 'start', COL['dim']))
    b.append(dim_h(CX - TUN_B / 2, CX + TUN_B / 2, Z(Z_BODEN1 + 6), 'Tür 40'))
    b.append(dim_h(24, 126, Z(Z_FUND1 + 66), 'Holzlager 102 x 75'))
    x = 170
    for z0, z1, lab in [(0, Z_FUND1, '5'), (Z_FUND1, Z_WAND1, '75'), (Z_WAND1, Z_HERD1, '10'), (Z_HERD1, Z_BODEN1, '14.5'),
                        (Z_BODEN1, Z_KUPPEL_AUS, f'{Z_KUPPEL_AUS - Z_BODEN1:.1f}'), (Z_KUPPEL_AUS, Z_ROHR1, f'{Z_ROHR1 - Z_KUPPEL_AUS:.1f}')]:
        b.append(dim_v(x, Z(z0), Z(z1), lab, 1, 2.6))
    b.append(dim_v(190, Z(0), Z(Z_ROHR1), f'Gesamthöhe {Z_ROHR1:.0f}', 1, 3.0))
    b.append(dim_v(-20, Z(0), Z(Z_BODEN1), f'Arbeitshöhe {Z_BODEN1:.1f}', -1, 3.0))
    b.append(dim_v(-6, Z(Z_BODEN1), Z(Z_TUN1), f'{TUN_H}', -1, 2.6))
    b.append(text(-35, Z(Z_ROHR1 + 22), 'FRONTANSICHT  1:20 (Masse in cm)', 4.5, 'start', COL['line'], 'bold'))
    b.append(text(-35, Z(Z_ROHR1 + 16), f'Kuppelofen Ø {V["D"]} innen – Würenlos – Variante B', 3, 'start', '#555'))
    b.append(text(-33, Z(2), '±0 = Terrain / Plattenbelag', 2.6, 'start', COL['hint']))
    return svg(900, 1200, ''.join(b), 'Frontansicht', (-40, Z(Z_ROHR1 + 28), 245, Z_ROHR1 + 28 + 54))

# ============================================================== SCHNITT A-A (Laengsschnitt durch Mitte)
def schnitt():
    b = []
    # Mauer hinten (y<0), Abstand 10
    b.append(rect(-35, Z(200), 20, 240, '#9aa1a8', COL['line'], 0.4))
    b.append(text(-24, Z(120), 'Betonmauer', 3, 'middle', '#fff', 'bold', rot=-90))
    b.append(rect(-15, Z(0), 175, 40, 'url(#pErde)', 'none', 0))
    b.append(line(-15, 0, 160, 0, COL['line'], 0.5))
    b.append(rect(-10, Z(Z_KIES1), 170, 20, 'url(#pKies)'))
    b.append(rect(0, Z(Z_FUND1), 150, 15, 'url(#pBeton)'))
    # Bewehrung Fundament
    b.append(line(5, Z(Z_KIES1 + 5), 145, Z(Z_KIES1 + 5), COL['stahl'], 0.7))
    # Sockel: Rueckwand y0..24 (Schnitt), Seitenwand dahinter als Ansicht
    b.append(rect(24, Z(Z_WAND1), 126, 75, '#e9ecef', COL['line'], 0.25))  # Seitenwand in Ansicht
    for k in (1, 2):
        b.append(line(24, Z(Z_FUND1 + 25 * k), 150, Z(Z_FUND1 + 25 * k), '#999', 0.2))
    for s in range(1, 3):
        b.append(line(24 + 50 * s - 12, Z(Z_FUND1), 24 + 50 * s - 12, Z(Z_FUND1 + 25), '#999', 0.2))
    b.append(rect(0, Z(Z_WAND1), 24, 75, 'url(#pSchal)'))
    b.append(rect(5, Z(Z_WAND1), 14, 75, 'url(#pBeton)', COL['line'], 0.2))
    b.append(line(12, Z(Z_FUND1 - 8), 12, Z(Z_HERD1 - 3), COL['stahl'], 0.6))
    b.append(text(87, Z(Z_FUND1 + 40), 'Holzlager (Seitenwand in Ansicht)', 3, 'middle', '#666'))
    b.append(rect(0, Z(Z_HERD1), 150, 10, 'url(#pBeton)'))
    b.append(line(4, Z(Z_WAND1 + 3), 146, Z(Z_WAND1 + 3), COL['stahl'], 0.7))
    # Perlit-Daemmung unter Boden
    y_d0 = CY - (A + T + ISO)
    b.append(rect(y_d0, Z(Z_DAEMM1), 150 - y_d0, 10, 'url(#pPerlit)'))
    b.append(rect(y_d0, Z(Z_BODEN1), CY - (A + T) - y_d0, Z_BODEN1 - Z_DAEMM1, 'url(#pIso)'))
    b.append(rect(y_d0 - PUTZ, Z(Z_BODEN1), PUTZ, Z_BODEN1 - Z_HERD1, COL['putz']))
    # Boden
    y_b0 = CY - (A + T)
    b.append(rect(y_b0, Z(Z_BODEN1), 150 - y_b0, 4, COL['boden']))
    for yy in range(int(y_b0) + 20, 150, 20):
        b.append(line(yy, Z(Z_BODEN1), yy, Z(Z_BODEN0), COL['line'], 0.2))
    # Kuppel: Ring Stein, Iso, Putz  (Schnitt in y-Richtung; Tunnel vorne rechts)
    z0 = Z_BODEN1
    def ell(a, c, t0, t1, n=120):
        return [(CY + a * math.cos(t0 + (t1 - t0) * i / n), Z(z0 + c * math.sin(t0 + (t1 - t0) * i / n))) for i in range(n + 1)]
    # Tueroeffnung: vorne (rechts) Kuppel bis Hoehe TUN_H offen -> Winkel
    th_t = math.asin(min(1, TUN_H / C))
    for (ai, ci, ao, co, fill) in [(A, C, A + T, C + T, COL['stein']), (A + T, C + T, A + T + ISO, C + T + ISO, 'url(#pIso)'),
                                   (A + T + ISO, C + T + ISO, A + T + ISO + PUTZ, C + T + ISO + PUTZ, COL['putz'])]:
        th_o = math.asin(min(1, (TUN_H + 4) / co)) if fill == COL['stein'] else math.asin(min(1, (TUN_H + 4 + (ISO if fill != 'url(#pIso)' else 0)) / co))
        th_i = math.asin(min(1, (TUN_H + 4) / ci)) if fill == COL['stein'] else th_o
        outer = ell(ao, co, th_o, math.pi)
        inner = list(reversed(ell(ai, ci, th_i, math.pi)))
        b.append(poly(outer + inner, fill, sw=0.3))
    # Reihenfugen in Kuppel (Schnitt)
    for r in K['reihen']:
        th = math.asin(min(1, r['z_innen_von'] / C)) if r['z_innen_von'] > 0 else 0
        for side in (-1,):
            xi = CY + side * A * math.cos(th); zi = z0 + C * math.sin(th)
            nx, nz = side * (C * math.cos(th)), A * math.sin(th)
            nn = math.hypot(nx, nz) or 1
            b.append(line(xi, Z(zi), xi + T * nx / nn, Z(zi + T * nz / nn), COL['line'], 0.3))
    # Tunnel: Seitenwand in Ansicht (Steinlagen), Deckplatten, Kamin
    yt0 = Y_TUER
    b.append(rect(yt0, Z(Z_TUN1), 150 - yt0, TUN_H, '#f1d7c4', COL['line'], 0.25))
    for k in range(1, V['tunnel_lagen']):
        b.append(line(yt0, Z(Z_BODEN1 + k * 4.6), 150, Z(Z_BODEN1 + k * 4.6), '#b06a40', 0.2))
    b.append(text((yt0 + 150) / 2, Z(Z_BODEN1 + 13), 'Tunnelwand', 2.4, 'middle', '#7a3d1c'))
    b.append(text((yt0 + 150) / 2, Z(Z_BODEN1 + 10.3), 'Plattenstreifen 10 cm', 2.0, 'middle', '#7a3d1c'))
    b.append(rect(Y_TUER, Z(Z_PLATTE1), 20, 4, COL['boden']))
    b.append(rect(Y_TUER + 21, Z(Z_PLATTE1), 150 - Y_TUER - 21, 4, COL['boden']))
    b.append(rect(Y_TUER, Z(Z_PLATTE1 + ISO), 150 - Y_TUER, ISO, 'url(#pIso)'))
    b.append(rect(Y_TUER, Z(Z_PLATTE1 + ISO + PUTZ), 150 - Y_TUER, PUTZ, COL['putz']))
    b.append(rect(150, Z(Z_PLATTE1 + ISO + PUTZ), 3, Z_PLATTE1 + ISO + PUTZ - Z_HERD1, COL['putz']))
    b.append(rect(Y_KAMIN - 7.5, Z(Z_ROHR1), 15, ROHR_L, '#c7ccd1', COL['line'], 0.4))
    b.append(rect(Y_KAMIN - 7.5, Z(Z_PLATTE1), 15, 4, '#2b1d14', 'none', 0))
    # Rauchweg
    b.append(f'<path d="M {CY + 10} {Z(z0 + 30)} Q {Y_KAMIN - 5} {Z(Z_TUN1 - 2)} {Y_KAMIN} {Z(Z_PLATTE1 + 20)}" fill="none" stroke="#888" stroke-width="0.8" stroke-dasharray="2 1.5" marker-end="url(#arr)"/>')
    b.append(text(Y_KAMIN + 9, Z(Z_PLATTE1 + 30), 'Rauch', 2.6, 'start', '#666'))
    # Tuer
    b.append(rect(150.5, Z(Z_TUN1 + 2), 1.2, TUN_H + 4, '#333', '#333', 0.2))
    # Beschriftung Schichten
    labs = [
        (Z_KIES0 + 10, '① Kieskoffer 0/31.5, 20 cm verdichtet (170 x 170)'),
        (Z_KIES1 + 7, '② Fundamentplatte C25/30, 15 cm, Estrichgitter'),
        (Z_FUND1 + 37, '③ Sockel Schalungssteine 24 cm, 3 Lagen, gefüllt'),
        (Z_WAND1 + 5, '④ Herdplatte Stahlbeton 10 cm, 2 x R188A'),
        (Z_HERD1 + 5, '⑤ Perlit-Zement 5:1, 10 cm (Bodendämmung)'),
        (Z_BODEN0 + 2, '⑥ Backboden Schamottplatten 40 mm auf 5 mm Sandbett'),
        (Z_BODEN1 + 22, f'⑦ Kuppel Schamott-Halbsteine 6.4 cm, {len(K["reihen"])} Reihen + Schluss'),
        (Z_BODEN1 + C + T + 4, '⑧ Perlit-Zement 8 cm (Kuppeldämmung)'),
        (Z_KUPPEL_AUS - 1, '⑨ Drahtgeflecht + Aussenputz 3 cm'),
        (Z_PLATTE1 + 50, '⑩ Kaminrohr Stahl Ø150 (Firefix), 1.0 m'),
    ]
    for zz, lab in labs:
        b.append(line(160, Z(zz), 172, Z(zz), '#888', 0.2))
        b.append(text(173, Z(zz) + 1, lab, 2.8))
    b.append(dim_h(0, 150, Z(-36), 'Fundament 150'))
    b.append(dim_h(CY - A, CY + A, Z(z0 + 8), f'Ø innen {V["D"]}'))
    b.append(dim_h(0, CY, Z(Z_ROHR1 - 20), f'Achse Kuppel {CY:.0f}'))
    b.append(dim_h(Y_TUER, 150, Z(Z_ROHR1 - 20), f'Tunnel {150 - Y_TUER:.1f}'))
    b.append(dim_v(-8, Z(Z_BODEN1), Z(Z_KUPPEL_IN), f'h innen {V["h"]}', 1, 2.6))
    b.append(dim_v(155, Z(Z_BODEN1), Z(Z_TUN1), f'Tür {TUN_H}', 1, 2.4))
    b.append(text(-35, Z(Z_ROHR1 + 14), 'SCHNITT A–A (Längsschnitt Mitte)  1:20', 4.5, 'start', COL['line'], 'bold'))
    b.append(text(-35, Z(Z_ROHR1 + 8), 'Schichtaufbau von unten nach oben ① – ⑩, Masse in cm, ±0 = Terrain', 3, 'start', '#555'))
    b.append(text(-13, Z(-26), 'Abstand Mauer ≥ 10 cm (ANNAHME)', 2.2, 'start', COL['hint']))
    return svg(1400, 1100, ''.join(b), 'Schnitt A-A', (-40, Z(Z_ROHR1 + 20), 330, Z_ROHR1 + 20 + 45))

# ============================================================== DRAUFSICHT
def draufsicht():
    b = []
    b.append(rect(-30, -38, 210, 22, '#9aa1a8', COL['line'], 0.4))
    b.append(text(75, -25, 'Betonmauer (Abstand Fundament ≥ 10 cm)', 3.2, 'middle', '#fff', 'bold'))
    b.append(rect(-10, -10, 170, 170, 'url(#pKies)', COL['line'], 0.3, 'stroke-dasharray="1.5 1" opacity="0.7"'))
    b.append(rect(0, 0, 150, 150, 'url(#pBeton)'))
    # Sockelwaende (gestrichelt, verdeckt)
    for (x, y, w, h) in [(0, 0, 150, 24), (0, 24, 24, 126), (126, 24, 24, 126)]:
        b.append(rect(x, y, w, h, 'none', '#555', 0.35, 'stroke-dasharray="2 1"'))
    Ra = A + T + ISO + PUTZ
    tx0 = CX - TUN_B / 2 - TUN_W - PUTZ
    b.append(rect(tx0, CY + 20, TUN_B + 2 * (TUN_W + PUTZ), 150 - CY - 20 + 3, COL['putz'], COL['line'], 0.5))
    b.append(f'<circle cx="{CX}" cy="{CY}" r="{Ra}" fill="{COL["putz"]}" stroke="{COL["line"]}" stroke-width="0.5"/>')
    yi = CY + math.sqrt(Ra ** 2 - (TUN_B / 2 + TUN_W + PUTZ) ** 2)
    tw_ = TUN_B + 2 * (TUN_W + PUTZ)
    b.append(rect(tx0 + 0.25, yi, tw_ - 0.5, 153 - yi, COL['putz'], 'none', 0))
    b.append(line(tx0, yi, tx0, 153, COL['line'], 0.5) + line(tx0 + tw_, yi, tx0 + tw_, 153, COL['line'], 0.5) + line(tx0, 153, tx0 + tw_, 153, COL['line'], 0.5))
    for r, st in [(A + T + ISO, '2 1'), (A + T, '2 1'), (A, '0')]:
        b.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="#7a3d1c" stroke-width="{0.45 if r == A else 0.25}" stroke-dasharray="{st}"/>')
    b.append(rect(CX - TUN_B / 2, Y_TUER, TUN_B, 150 - Y_TUER, 'none', '#7a3d1c', 0.45, 'stroke-dasharray="2 1"'))
    b.append(f'<circle cx="{CX}" cy="{Y_KAMIN}" r="7.5" fill="#c7ccd1" stroke="{COL["line"]}" stroke-width="0.5"/>')
    b.append(text(CX, Y_KAMIN + 1, 'Ø15', 2.6, 'middle'))
    b.append(text(CX, CY, f'Backraum Ø {V["D"]}', 3.4, 'middle', '#7a3d1c', 'bold'))
    b.append(text(CX, CY + 5, f'Kuppel aussen Ø {2 * Ra:.1f}', 2.8, 'middle', '#7a3d1c'))
    # Masse
    b.append(dim_h(0, 150, 168, 'Fundament 150'))
    b.append(dim_h(-10, 160, 178, 'Kieskoffer 170'))
    b.append(dim_v(162, 0, 150, '150', 1))
    b.append(dim_v(-5, 0, CY, f'{CY:.0f}', -1, 2.6))
    b.append(text(150, -3, f'Kuppel bis Hinterkante: {CY - Ra:.1f} cm', 2.6, 'end', COL['hint']))
    b.append(dim_h(CX - TUN_B / 2, CX + TUN_B / 2, 145, 'Tür 40', 0, 2.6))
    b.append(dim_h(tx0, tx0 + TUN_B + 2 * (TUN_W + PUTZ), 159, f'Vorbau {TUN_B + 2 * (TUN_W + PUTZ):.1f}', 0, 2.6))
    b.append(text(75, 190, '▼ Arbeitsseite / Rasen', 3.2, 'middle', COL['hint'], 'bold'))
    b.append(text(-40, -53, 'DRAUFSICHT  1:20', 4.5, 'start', COL['line'], 'bold'))
    b.append(text(-40, -47, 'gestrichelt = verdeckte Kanten (Sockel, Steinlage, Dämmung)', 3, 'start', '#555'))
    b.append(text(190, 10, 'Abstände (Empfehlung):', 3, 'start', COL['line'], 'bold'))
    for i, s in enumerate(['Mauer (nicht brennbar): ≥ 10 cm', 'Rasen: 50 cm Kies-/Plattenstreifen', 'Feigenbaum: Krone ≥ 3 m vom Kamin', 'Nachbargrenze: ≥ 2 m (BauV AG § 19)', 'Brennbares (Holz, Möbel): ≥ 1.5 m vor Tür']):
        b.append(text(190, 17 + i * 6, '• ' + s, 2.8))
    return svg(1300, 1000, ''.join(b), 'Draufsicht', (-45, -62, 330, 262))

# ============================================================== KUPPELSCHNITT MIT STEINREIHEN
def kuppelschnitt():
    b = []
    am, cm = A + T / 2, C + T / 2
    def point(th, a, c): return (a * math.cos(th), c * math.sin(th))
    # Theta-Lookup ueber Bogenlaenge Mittelflaeche
    n = 4000; pts = [(0.0, 0.0)]; s = 0; prev = point(0, am, cm)
    for i in range(1, n + 1):
        th = math.pi / 2 * i / n; p = point(th, am, cm); s += math.dist(p, prev); prev = p; pts.append((th, s))
    def th_at(sv):
        for th, ss in pts:
            if ss >= sv: return th
        return math.pi / 2
    S = 2.2   # Skalierung -> grosser Massstab
    ox, oz = 30, 10
    def P(x, z): return (ox + x * S, -(oz + z * S))
    # Boden
    bx0, bx1 = P(-5, 0), P(A + T + 8, 0)
    b.append(rect(bx0[0], bx0[1], bx1[0] - bx0[0], 4 * S, COL['boden']))
    b.append(text(P(10, -2)[0], P(10, -2)[1] + 1, 'Backboden (Schamottplatte 40 mm)', 2.8, 'start', '#fff'))
    b.append(line(*P(0, -4), *P(0, C + 12), '#999', 0.3, 'stroke-dasharray="2 1.5"'))
    b.append(text(*P(1, C + 10), 'Kuppelachse', 2.6, 'start', '#777'))
    pitch = 12.4 + 0.6
    s0 = 0.0
    for r in K['reihen']:
        t0, t1 = th_at(s0), th_at(s0 + 12.4)
        def corners(th):
            mx, mz = point(th, am, cm)
            nx, nz = cm * math.cos(th), am * math.sin(th); nn = math.hypot(nx, nz)
            return (mx - T / 2 * nx / nn, mz - T / 2 * nz / nn), (mx + T / 2 * nx / nn, mz + T / 2 * nz / nn)
        i0, o0 = corners(t0); i1, o1 = corners(t1)
        quad = [P(*i0), P(*o0), P(*o1), P(*i1)]
        b.append(poly(quad, COL['stein'], sw=0.4))
        cxm = sum(q[0] for q in quad) / 4; czm = sum(q[1] for q in quad) / 4
        b.append(text(cxm, czm + 1, f'R{r["reihe"]}', 2.8, 'middle', '#fff', 'bold'))
        # Label nach aussen
        lx, lz = point((t0 + t1) / 2, am + 22, cm + 22)
        L = P(lx, lz)
        b.append(line(*P(*point((t0 + t1) / 2, am + T / 2, cm + T / 2)), *L, '#888', 0.25))
        anchor = 'start'
        b.append(text(L[0] + 1, L[1] - 1.5, f'Reihe {r["reihe"]}: {r["halbsteine"]} Halbsteine' + (f' (−{r["tuerabzug"]} Tür)' if r['tuerabzug'] else ''), 2.9, anchor, COL['line'], 'bold'))
        b.append(text(L[0] + 1, L[1] + 2.2, f'Lagerfuge {r["neigung_grad"]:.0f}° geneigt · z = {r["z_innen_von"]:.1f}–{r["z_innen_bis"]:.1f} cm · r = {r["r_innen"]:.1f}', 2.5, anchor, '#444'))
        s0 += pitch
    # Schlussstein
    t0 = th_at(s0)
    mx, mz = point(t0, am, cm)
    cap = [P(0, C), P(0, C + T), P(mx + T / 2 * 0.3, mz + T / 2), P(mx - T / 2 * 0.3, mz - T / 2)]
    b.append(poly(cap, '#b5653a', sw=0.4))
    Lc = P(15, C + 30)
    b.append(line(*P(4, C + T), *Lc, '#888', 0.25))
    b.append(text(Lc[0] + 1, Lc[1] - 1.5, f'Schluss: {K["schluss_halbsteine"]} zugeschnittene Halbsteine (Restöffnung Ø ca. {2 * am * math.cos(t0):.0f} cm)', 2.9, 'start', COL['line'], 'bold'))
    # Innenkontur + Daemmung angedeutet
    inner = [P(A * math.cos(math.pi / 2 * i / 60), C * math.sin(math.pi / 2 * i / 60)) for i in range(61)]
    b.append('<polyline points="' + ' '.join(f'{x:.2f},{y:.2f}' for x, y in inner) + '" fill="none" stroke="#7a3d1c" stroke-width="0.4" stroke-dasharray="1.5 1"/>')
    iso_o = [P((A + T + ISO) * math.cos(math.pi / 2 * i / 60), (C + T + ISO) * math.sin(math.pi / 2 * i / 60)) for i in range(61)]
    b.append('<polyline points="' + ' '.join(f'{x:.2f},{y:.2f}' for x, y in iso_o) + '" fill="none" stroke="#c8b46a" stroke-width="0.6" stroke-dasharray="3 1.5"/>')
    b.append(text(*P(A + T + ISO + 1, 3), 'Aussenkante Dämmung', 2.5, 'start', '#9c8a3f'))
    # Masse
    b.append(dim_h(P(0, 0)[0], P(A, 0)[0], P(0, -9)[1], f'r innen {A:g}'))
    b.append(dim_v(P(-6, 0)[0], P(0, 0)[1], P(0, C)[1], f'h innen {C:g}', -1))
    b.append(dim_h(P(A, 0)[0], P(A + T, 0)[0], P(0, -14)[1], '6.4', 0, 2.4))
    b.append(text(ox - 10, -(oz + (C + 52) * S), 'KUPPELSCHNITT MIT STEINREIHEN  (halber Schnitt, Massstab ca. 1:10)', 4, 'start', COL['line'], 'bold'))
    b.append(text(ox - 10, -(oz + (C + 52) * S) + 5, 'Halber NF-Stein 125 x 124 x 64 mm, flach verlegt: Fläche 125 x 124 zeigt nach innen, 6.4 cm = Kuppelstärke. Fuge 6 mm.', 2.8, 'start', '#555'))
    b.append(text(ox - 10, -(oz + (C + 52) * S) + 9, f'Total: {K["halbsteine_reihen"]} Halbsteine + 10 % Verschnitt = {V["halbsteine_mit_verschnitt"]} = {V["nf_kuppel"]} ganze NF-Steine. Tunnelwände aus Schamottplatten-Streifen.', 2.8, 'start', '#555'))
    b.append(text(ox - 10, -(oz + (C + 52) * S) + 13, 'Neigung = Winkel der Lagerfuge gegen die Waagrechte; jede Reihe auf Sandform/Lehre setzen, Fugen innen eng, aussen keilförmig.', 2.8, 'start', '#555'))
    return svg(1300, 860, ''.join(b), 'Kuppelschnitt Steinreihen', (ox - 15, -(oz + (C + 58) * S), 260, (C + 58) * S + oz + 18 * S))

if __name__ == '__main__':
    out = dict(frontansicht=frontansicht(), schnitt_A_A=schnitt(), draufsicht=draufsicht(), kuppelschnitt_steinreihen=kuppelschnitt())
    for k, v in out.items():
        open(os.path.join(HERE, f'{k}.svg'), 'w').write(v)
    json.dump(HOEHEN, open(os.path.join(HERE, 'hoehen.json'), 'w'), indent=1)
    print(json.dumps(HOEHEN, indent=1))
