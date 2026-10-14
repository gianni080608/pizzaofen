#!/usr/bin/env python3
"""Werkzeichnungen (CAD, 2D) und Isometrie-Skizzen fuer die Bauanleitung (Fassung 4).
Koordinaten in cm: x = Breite links->rechts, y = Tiefe (0 = hinten an der Betonwand, 150 = vorne/Tuer), z = Hoehe ueber Terrain.
Alle Masse aus ../berechnung/ergebnis.json bzw. zeichnungen.py (gleiche Konstanten). Ausgabe: <name>.svg + cad.json (Zuschnittlisten)."""
import json, math, os
import zeichnungen as Zg
from zeichnungen import rect, poly, line, text, dim_h, dim_v, svg, COL, A, C, T, ISO, PUTZ, CX, CY, TUN_B, TUN_W, TUN_H, Y_TUER, Y_KAMIN, K, V
HERE = os.path.dirname(os.path.abspath(__file__))
Z_FUND0, Z_FUND1, Z_WAND1, Z_HERD1, Z_DAEMM1, Z_BODEN1 = -10, Zg.Z_FUND1, Zg.Z_WAND1, Zg.Z_HERD1, Zg.Z_DAEMM1, Zg.Z_BODEN1
BRETT = 2.3
OUT = {}
DATA = {}

def head(x, y, title, sub=''):
    return text(x, y, title, 4.4, 'start', COL['line'], 'bold') + (text(x, y + 5.2, sub, 2.8, 'start', '#555') if sub else '')

def note(x, y, lines, size=2.7, fill=COL['line'], lh=4.0):
    return ''.join(text(x, y + i * lh, s, size, 'start', fill) for i, s in enumerate(lines))

def circle(cx, cy, r, fill='none', stroke=COL['line'], sw=0.35, extra=''):
    return f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def path(d, fill='none', stroke=COL['line'], sw=0.35, extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def badge(x, y, s, fill='#a9542a', r=2.6, size=2.6):
    return circle(x, y, r, fill, 'none', 0) + text(x, y + size * 0.36, s, size, 'middle', '#fff', 'bold')

# ================================================================ 1 LAGEPLAN / ABSTECKEN
def lageplan():
    b = []
    b.append(rect(-60, -32, 290, 22, '#9aa1a8', COL['line'], 0.4))
    b.append(text(85, -19, 'bestehende Betonwand', 3.2, 'middle', '#fff', 'bold'))
    b.append(rect(-60, -10, 290, 222, '#eef0ea', 'none', 0))
    for gx in range(-60, 230, 25):
        for gy in range(-10, 212, 25):
            b.append(rect(gx + 0.6, gy + 0.6, 23.8, 23.8, '#e3e6df', '#cfd3cb', 0.2))
    b.append(text(-56, 205, 'alte Gartenplatten (bleiben ausserhalb liegen)', 2.6, 'start', '#666'))
    b.append(rect(-10, -10, 170, 170, 'url(#pKies)', COL['line'], 0.45))
    b.append(rect(0, 0, 150, 150, 'none', COL['dim'], 0.6, 'stroke-dasharray="3 1.5"'))
    b.append(line(-10, -10, 160, 160, COL['hint'], 0.35, 'stroke-dasharray="2 1.2"') + line(160, -10, -10, 160, COL['hint'], 0.35, 'stroke-dasharray="2 1.2"'))
    b.append(text(118, 104, 'Diagonale 240.4', 2.8, 'start', COL['hint'], 'bold', rot=45))
    b.append(text(26, 18, 'Fundament 150 x 150', 3.0, 'start', COL['dim'], 'bold'))
    b.append(text(26, 22.5, 'Diagonale 212.1', 2.6, 'start', COL['dim']))
    for (px, py) in [(-25, 160), (175, 160), (-10, 175), (160, 175)]:
        b.append(rect(px - 1.2, py - 1.2, 2.4, 2.4, '#7a4a20', 'none'))
    b.append(line(-25, 160, 175, 160, '#c0392b', 0.25) + line(-10, -10, -10, 175, '#c0392b', 0.25) + line(160, -10, 160, 175, '#c0392b', 0.25))
    b.append(text(178, 161, 'Schnur', 2.5, 'start', '#c0392b'))
    b.append(dim_v(-30, -10, 0, '10', -1, 2.4))
    b.append(dim_h(-10, 160, 192, 'freilegen 170 (bis auf den Kies)'))
    b.append(dim_h(0, 150, 183, 'Fundament 150'))
    b.append(dim_v(186, -10, 160, '170', 1))
    b.append(text(75, 222, '▼ vorne = Arbeitsseite / Ofentür', 3.2, 'middle', COL['hint'], 'bold'))
    b.append(head(-60, -48, 'LAGEPLAN UND ABSTECKEN  1:25', 'Draufsicht · Betonwand oben · alle Masse in cm'))
    b.append(note(200, 20, ['So steckt ihr ab:', '1. Hinten ist die Wand die Kante:', '   freilegen bis an die Wand.', '2. Fundament-Hinterkante 10 cm', '   vor der Wand (Fuss der Wand', '   kann vorstehen → dort messen).', '3. Schnur links, rechts, vorne:', '   170 x 170 ab Wand.', '4. Diagonalen gleich lang', '   (240.4 cm) = rechtwinklig.', '5. Innen 150 x 150 markieren.', '6. Platten, Sand, Vlies weg;', '   Sand aufheben (Sandform).'], 2.7))
    OUT['lageplan'] = svg(1200, 1000, ''.join(b), 'Lageplan', (-64, -58, 330, 288))

# ================================================================ 2 FUNDAMENT: SCHALUNG, GITTER, STECKEISEN
STECK = [(12.5, 12), (37.5, 12), (62.5, 12), (87.5, 12), (112.5, 12), (137.5, 12),
         (12, 62.5), (12, 112.5), (12, 137), (138, 62.5), (138, 112.5), (138, 137)]

def fundament():
    b = []
    # Grundriss links
    b.append(rect(-10, -10, 170, 170, 'url(#pKies)', COL['line'], 0.3, 'opacity="0.55"'))
    b.append(rect(0, 0, 150, 150, '#dfe3e7', COL['line'], 0.3))
    # Schalbretter
    b.append(rect(-BRETT, -BRETT, 150 + 2 * BRETT, BRETT, '#c9a26b', COL['line'], 0.3))
    b.append(rect(-BRETT, 150, 150 + 2 * BRETT, BRETT, '#c9a26b', COL['line'], 0.3))
    b.append(rect(-BRETT, 0, BRETT, 150, '#d8b47c', COL['line'], 0.3))
    b.append(rect(150, 0, BRETT, 150, '#d8b47c', COL['line'], 0.3))
    b.append(text(75, -5, 'Brett B1  155 cm', 2.5, 'middle', '#7a5523', 'bold'))
    b.append(text(75, 158.5, 'Brett B2  155 cm', 2.5, 'middle', '#7a5523', 'bold'))
    b.append(text(-5, 75, 'Brett B3  150', 2.5, 'middle', '#7a5523', 'bold', rot=-90))
    b.append(text(157, 75, 'Brett B4  150', 2.5, 'middle', '#7a5523', 'bold', rot=-90))
    for (px, py) in [(-6, -6), (156, -6), (-6, 156), (156, 156)]:
        b.append(rect(px - 1.5, py - 1.5, 3, 3, '#7a4a20', 'none'))
    # Estrichgitter 2 Stueck 140 x 75, 10 cm Ueberlappung
    for (y0, op) in [(5, 0.9), (70, 0.9)]:
        for gx in range(0, 141, 5):
            b.append(line(5 + gx, y0, 5 + gx, y0 + 75, COL['stahl'], 0.18, f'opacity="{op}"'))
        for gy in range(0, 76, 5):
            b.append(line(5, y0 + gy, 145, y0 + gy, COL['stahl'], 0.18, f'opacity="{op}"'))
    b.append(rect(5, 70, 140, 10, 'none', '#c0392b', 0.4, 'stroke-dasharray="1.5 1"'))
    b.append(text(75, 85.5, '10 cm überlappt, mit Bindedraht verbinden', 2.3, 'middle', '#c0392b'))
    # Abstandhalter
    for (sx, sy) in [(25, 25), (75, 25), (125, 25), (25, 75), (75, 75), (125, 75), (25, 125), (75, 125), (125, 125)]:
        b.append(rect(sx - 2.5, sy - 2.5, 5, 5, '#9aa1a8', '#555', 0.25))
    # Steckeisen
    for i, (sx, sy) in enumerate(STECK, 1):
        b.append(circle(sx, sy, 1.6, '#c0392b', '#fff', 0.3))
        b.append(text(sx + 2.2, sy + 3.2 if sy < 20 else sy + 1, f'{i}', 2.2, 'start', '#c0392b', 'bold'))
    # spaetere Sockelwaende gestrichelt
    for (x, y, w, h) in [(0, 0, 150, 24), (0, 24, 24, 126), (126, 24, 24, 126)]:
        b.append(rect(x, y, w, h, 'none', '#555', 0.3, 'stroke-dasharray="2 1"'))
    b.append(dim_h(0, 150, 170, '150 (Innenmass Schalung)'))
    b.append(dim_v(167, 0, 150, '150', 1))
    b.append(dim_h(-BRETT, 150 + BRETT, 178, '154.6 ≈ 155 (B1, B2)'))
    b.append(text(-10, 188, 'Legende:  ● Steckeisen (Nr.)   ▪ Abstandhalter 4 cm (Stück alte Gartenplatte)   – – – spätere Sockelwand', 2.5, 'start', '#444'))
    # Schnitt rechts
    ox, oz = 205, 0
    def S(x, z): return (ox + x * 0.9, -(z) * 1.6 + 100)
    b.append(text(ox, 30, 'SCHNITT DURCH DAS FUNDAMENT (überhöht)', 3.0, 'start', COL['line'], 'bold'))
    x0, y0 = S(0, 5); x1, y1 = S(150, -10)
    b.append(rect(S(-12, -10)[0], S(0, -10)[1], (162 + 12) * 0.9 - 9, 12.5 * 1.6, 'url(#pKies)', COL['line'], 0.25))
    b.append(rect(x0, y0, 150 * 0.9, 15 * 1.6, 'url(#pBeton)', COL['line'], 0.35))
    b.append(rect(S(-2.3, 5)[0], S(0, 5)[1], 2.3 * 0.9, 15 * 1.6, '#c9a26b', COL['line'], 0.3))
    b.append(rect(S(150, 5)[0], S(0, 5)[1], 2.3 * 0.9, 15 * 1.6, '#c9a26b', COL['line'], 0.3))
    b.append(line(S(5, -6)[0], S(0, -6)[1], S(145, -6)[0], S(0, -6)[1], COL['stahl'], 0.8))
    for sx in (25, 75, 125):
        b.append(rect(S(sx - 2.5, -6)[0], S(0, -6)[1], 4.5, 4 * 1.6, '#9aa1a8', '#555', 0.2))
    for sx in (12.5, 137.5):
        b.append(line(S(sx, -7)[0], S(0, -7)[1], S(sx, 23)[0], S(0, 23)[1], '#c0392b', 0.7))
    b.append(text(S(140, 25)[0] - 2, S(0, 26)[1], 'Steckeisen 30 cm', 2.4, 'end', '#c0392b'))
    b.append(text(S(140, 25)[0] - 2, S(0, 26)[1] + 3.2, '12 tief, 18 heraus', 2.4, 'end', '#c0392b'))
    b.append(text(S(75, -2)[0], S(0, -2)[1], 'Beton 15 cm (300 kg Zement/m³)', 2.5, 'middle', '#222', 'bold'))
    b.append(text(S(75, -14)[0], S(0, -14)[1], 'bestehender Kies 10–15 cm, genässt + verdichtet', 2.4, 'middle', '#5a4a2a'))
    b.append(text(S(75, 2.5)[0], S(0, 2.5)[1], 'Estrichgitter auf 4 cm Abstandhaltern', 2.3, 'middle', COL['stahl']))
    b.append(line(S(-25, 0)[0], S(0, 0)[1], S(-14, 0)[0], S(0, 0)[1], '#222', 0.4))
    b.append(text(S(-25, 0)[0], S(0, 0)[1] - 1, '±0 Terrain', 2.3, 'start', '#222'))
    b.append(dim_v(S(160, 0)[0] + 4, S(0, -10)[1], S(0, 5)[1], '15', 1, 2.4))
    b.append(dim_v(S(160, 0)[0] + 4, S(0, 5)[1], S(0, 0)[1], '', 1, 2.4))
    b.append(text(S(160, 0)[0] + 7, S(0, 3)[1], 'OK +5', 2.4, 'start', COL['dim']))
    b.append(text(S(160, 0)[0] + 7, S(0, -10)[1] + 1, 'UK −10', 2.4, 'start', COL['dim']))
    b.append(note(ox, 140, ['Steckeisen-Positionen (x / y ab Ecke hinten links):',
                            *[f'{i:>2}:  {x:g} / {y:g}' for i, (x, y) in enumerate(STECK, 1) if i <= 6]], 2.5))
    b.append(note(ox + 62, 144, [f'{i:>2}:  {x:g} / {y:g}' for i, (x, y) in enumerate(STECK, 1) if i > 6], 2.5))
    b.append(note(ox, 172, ['= Mitte der Steinkammern, die durch alle 3 Lagen', '   übereinander liegen (Verlegeplan Sockel).', 'Bretter: 3 m-Schalbrett → 155 + 145, 155 + 145,', '   150 + 150. Die 145er-Reste werden Stützen.'], 2.5))
    b.append(head(-10, -22, 'FUNDAMENT  1:25', 'Schalung, Bewehrung, Steckeisen – Draufsicht links, Schnitt rechts'))
    OUT['fundament'] = svg(1400, 880, ''.join(b), 'Fundament', (-16, -30, 386, 230))

# ================================================================ 3 SOCKEL VERLEGEPLAN
def sockel():
    b = []
    LA = [('1', 0, 0, 50, 24), ('2', 50, 0, 50, 24), ('3', 100, 0, 50, 24),
          ('4', 0, 24, 24, 50), ('5', 0, 74, 24, 50), ('6½', 0, 124, 24, 25),
          ('7', 126, 24, 24, 50), ('8', 126, 74, 24, 50), ('9½', 126, 124, 24, 25)]
    LB = [('1', 0, 0, 24, 50), ('2', 0, 50, 24, 50), ('3', 0, 100, 24, 50),
          ('4', 126, 0, 24, 50), ('5', 126, 50, 24, 50), ('6', 126, 100, 24, 50),
          ('7', 24, 0, 50, 24), ('8', 74, 0, 50, 24)]
    def stone(ox, n, x, y, w, h, half=False):
        o = rect(ox + x + 0.3, y + 0.3, w - 0.6, h - 0.6, '#cfd3d7' if not half else '#e7d3b8', '#444', 0.35)
        # Kammern
        if w > h:
            for k in range(int(round(w / 25))):
                o += rect(ox + x + k * 25 + 3.5, y + 4, 18, h - 8, '#f7f8f9', '#777', 0.2)
        else:
            for k in range(int(round(h / 25))):
                o += rect(ox + x + 4, y + k * 25 + 3.5, w - 8, 18, '#f7f8f9', '#777', 0.2)
        o += text(ox + x + w / 2, y + h / 2 + 1.1, n, 3.0, 'middle', '#a9542a', 'bold')
        return o
    for ox, L, title in [(0, LA, 'LAGE 1 und LAGE 3'), (190, LB, 'LAGE 2')]:
        b.append(rect(ox - 4, -4, 158, 158, '#dfe3e7', 'none', 0))
        b.append(text(ox + 75, -9, title, 3.6, 'middle', COL['line'], 'bold'))
        for st in L:
            b.append(stone(ox, *st, half=st[0].endswith('½')))
        for (sx, sy) in STECK:
            b.append(circle(ox + sx, sy, 1.3, '#c0392b', '#fff', 0.25))
        b.append(dim_h(ox, ox + 150, 162, '150'))
        b.append(dim_v(ox - 8, 0, 150, '150', -1))
        b.append(text(ox + 75, 75, 'Holzlager', 3.0, 'middle', '#777'))
        b.append(text(ox + 75, 80, '(hohl)', 2.6, 'middle', '#777'))
        b.append(text(ox + 75, 156.8, '▼ vorne offen', 2.6, 'middle', COL['hint']))
    b.append(text(190 + 124.6, 30, '2 cm', 2.2, 'middle', '#c0392b', rot=-90))
    b.append(line(190 + 124, 2, 190 + 126, 2, '#c0392b', 0.5))
    b.append(note(0, 176, ['Lage 1 + 3: 7 ganze Steine + 1 Stein halbiert (6½, 9½ = je 25 cm, Schnitt durch den Mittelsteg). Lage 2: 8 ganze Steine.',
                           'Total 24 Steine verbaut, 2 Reserve. Lage 1 im Mörtelbett (Zement : Sand 1 : 4, ca. 2 cm), Lagen 2 und 3 trocken aufsetzen.',
                           'Rote Punkte = Steckeisen-Kammern (durchgehend über alle 3 Lagen). Rückwand Lage 2: 2 cm Lücke bei x = 124–126 bleibt, wird mit Beton gefüllt.',
                           'Offene Kammerenden vorne (Steine 6½, 9½, 3, 6) beim Füllen mit einem Brettrest + Schnur abschalen.'], 2.6))
    b.append(head(-8, -22, 'SOCKEL – VERLEGEPLAN SCHALUNGSSTEINE  1:20', 'Kann Schalungsstein 50 x 24 x 25 cm · Draufsicht, Betonwand oben'))
    OUT['sockel_verlegeplan'] = svg(1400, 920, ''.join(b), 'Sockel Verlegeplan', (-18, -30, 370, 228))

# ================================================================ 4 HERDPLATTEN-SCHALUNG
PROPS = [(x, y) for y in (40, 90, 140) for x in (37, 75, 113)]

def herdplatte():
    b = []
    b.append(rect(0, 0, 150, 150, '#eceef0', 'none', 0))
    for (x, y, w, h) in [(0, 0, 150, 24), (0, 24, 24, 126), (126, 24, 24, 126)]:
        b.append(rect(x, y, w, h, 'url(#pSchal)', '#444', 0.35))
    b.append(rect(24, 24, 102, 62.5, '#e9d9b0', '#7a5523', 0.4))
    b.append(rect(24, 86.5, 102, 62.5, '#efe1bd', '#7a5523', 0.4))
    b.append(text(75, 52, 'OSB 1   102 x 62.5', 2.8, 'middle', '#7a5523', 'bold'))
    b.append(text(75, 117, 'OSB 2   102 x 62.5', 2.8, 'middle', '#7a5523', 'bold'))
    for (px, py) in PROPS:
        b.append(rect(px - 5, py - 1.15, 10, 2.3, '#a07040', '#4a2f14', 0.3))
    b.append(text(75, 94.5, 'Stützen 23 x 100 mm, Länge 73.2', 2.4, 'middle', '#4a2f14'))
    # Matten
    for (y0, col) in [(5, COL['stahl']), (45, '#3d6a99')]:
        b.append(rect(5, y0, 140, 100, 'none', col, 0.55, 'stroke-dasharray="3 1.5"'))
    b.append(text(155, 9, 'Matte 1 (y 5–105)', 2.3, 'start', COL['stahl'], 'bold'))
    b.append(text(155, 141, 'Matte 2 (y 45–145)', 2.3, 'start', '#3d6a99', 'bold'))
    b.append(rect(5, 45, 140, 60, 'none', '#c0392b', 0.4, 'stroke-dasharray="1 1"'))
    b.append(text(155, 74, '60 cm', 2.3, 'start', '#c0392b'))
    b.append(text(155, 77.5, 'Übergriff', 2.3, 'start', '#c0392b'))
    for (sx, sy) in STECK:
        b.append(circle(sx, sy, 1.3, '#c0392b', '#fff', 0.25))
    # Randbretter
    b.append(rect(-BRETT, -BRETT, 150 + 2 * BRETT, BRETT, '#c9a26b', COL['line'], 0.3))
    b.append(rect(-BRETT, 150, 150 + 2 * BRETT, BRETT, '#c9a26b', COL['line'], 0.3))
    b.append(rect(-BRETT, 0, BRETT, 150, '#d8b47c', COL['line'], 0.3))
    b.append(rect(150, 0, BRETT, 150, '#d8b47c', COL['line'], 0.3))
    for yy in (30, 75, 120):
        b.append(line(-BRETT, yy, 150 + BRETT, yy, '#555', 0.25, 'stroke-dasharray="0.8 0.8"'))
    for xx in (37, 75, 113):
        b.append(line(xx, -BRETT, xx, 150 + BRETT, '#555', 0.25, 'stroke-dasharray="0.8 0.8"'))
    b.append(text(75, 155.5, '· · · Drahtanker (Bindedraht)', 2.2, 'middle', '#555'))
    b.append(dim_h(24, 126, 164, 'OSB-Feld 102'))
    b.append(dim_v(-9, 24, 150, '126', -1))
    b.append(dim_h(0, 150, 171, '150'))
    for i, x in enumerate((37, 75, 113)):
        b.append(text(x, -6, f'x={x}', 2.2, 'middle', '#4a2f14'))
    for y in (40, 90, 140):
        b.append(text(118.5, y + 0.8, f'y={y}', 2.2, 'start', '#4a2f14'))
    # Schnitt rechts
    ox = 205
    def S(y, z): return (ox + y * 0.95, 120 - (z - 60) * 1.9)
    b.append(text(ox, 18, 'SCHNITT QUER (x = 75), überhöht', 3.0, 'start', COL['line'], 'bold'))
    # Wand hinten
    b.append(rect(S(0, 80)[0], S(0, 80)[1], 24 * 0.95, 20 * 1.9, 'url(#pSchal)', '#444', 0.3))
    b.append(rect(S(24, 80)[0], S(0, 80)[1], 126 * 0.95, 1.8 * 1.9, '#e9d9b0', '#7a5523', 0.35))
    b.append(rect(S(0, 90)[0], S(0, 90)[1], 150 * 0.95, 10 * 1.9, 'url(#pBeton)', '#333', 0.35, 'opacity="0.9"'))
    b.append(line(S(5, 83)[0], S(0, 83)[1], S(145, 83)[0], S(0, 83)[1], COL['stahl'], 0.7))
    b.append(line(S(45, 83.7)[0], S(0, 83.7)[1], S(145, 83.7)[0], S(0, 83.7)[1], '#3d6a99', 0.7))
    for py in (40, 90, 140):
        b.append(rect(S(py - 1.15, 78.2)[0], S(0, 78.2)[1], 2.3 * 0.95, 18.2 * 1.9, '#a07040', '#4a2f14', 0.3))
    b.append(rect(S(-2.3, 90)[0], S(0, 90)[1], 2.3 * 0.95, 15 * 1.9, '#c9a26b', COL['line'], 0.3))
    b.append(rect(S(150, 90)[0], S(0, 90)[1], 2.3 * 0.95, 15 * 1.9, '#c9a26b', COL['line'], 0.3))
    b.append(line(S(12, 60)[0], S(0, 60)[1], S(12, 85)[0], S(0, 85)[1], '#c0392b', 0.8))
    b.append(line(S(-2.3, 86)[0], S(0, 86)[1], S(152.3, 86)[0], S(0, 86)[1], '#555', 0.3, 'stroke-dasharray="0.8 0.8"'))
    b.append(text(S(75, 87.2)[0], S(0, 87.2)[1], 'Herdplatte 10 cm, 2 x R188A auf 3 cm Abstandhaltern', 2.4, 'middle', '#222', 'bold'))
    b.append(text(S(65, 75.5)[0], S(0, 75.5)[1], 'OSB 18 mm, Oberkante = Oberkante Sockel', 2.4, 'middle', '#7a5523'))
    b.append(text(S(75, 66)[0], S(0, 66)[1], 'Stützen bis aufs Fundament', 2.4, 'middle', '#4a2f14'))
    b.append(text(S(12, 61)[0] + 2, S(0, 61)[1], 'Stab 80 cm in Kammer', 2.3, 'start', '#c0392b'))
    b.append(text(S(152, 92)[0], S(0, 92)[1] - 1, 'Randbrett 15 cm, 5 cm über Wandkopf', 2.3, 'end', '#7a5523'))
    b.append(text(S(0, 70)[0] + 1, S(0, 70)[1], 'Wand', 2.4, 'start', '#fff', 'bold'))
    b.append(text(S(150, 55)[0], S(0, 55)[1], 'vorne →', 2.4, 'end', COL['hint']))
    b.append(note(ox, 170, ['Stützen: 9 Stück auf einem 3 x 3-Raster (Werte links).', 'Oben mit je 1 Schraube 4 x 40 durchs OSB fixieren.',
                            'Drahtanker: 3 x quer + 3 x längs, Bindedraht doppelt,', 'durch 3-mm-Löcher in den Randbrettern, aussen verdrillen.',
                            'Nach dem Betonieren bleiben sie drin, Enden abzwicken.'], 2.5))
    b.append(head(-10, -20, 'HERDPLATTE – SCHALUNG UND BEWEHRUNG  1:20', 'Draufsicht links (Betonwand oben), Schnitt rechts · Stützen frühestens nach 10 Tagen entfernen'))
    OUT['herdplatte_schalung'] = svg(1400, 880, ''.join(b), 'Herdplatte Schalung', (-14, -28, 378, 222))

# ================================================================ 5 BODENDAEMMUNG
def bodendaemmung():
    b = []
    R = A + T + 5
    b.append(rect(0, 0, 150, 150, 'url(#pBeton)', '#333', 0.35))
    hx = TUN_B / 2 + TUN_W + 5
    n = 16
    pts = []
    for i in range(n + 1):
        ang = math.pi / 2 + math.radians(30) + i * (2 * math.pi - math.radians(60)) / n
        pts.append((CX + R * math.cos(ang), CY + R * math.sin(ang)))
    th = math.asin(hx / R)
    y_cut = CY + R * math.cos(th)
    outline = [(CX - hx, 150), (CX - hx, y_cut)]
    m = 60
    a0 = math.pi / 2 + th
    a1 = math.pi / 2 - th + 2 * math.pi
    for i in range(m + 1):
        ang = a0 + (a1 - a0) * i / m
        outline.append((CX + R * math.cos(ang), CY + R * math.sin(ang)))
    outline += [(CX + hx, y_cut), (CX + hx, 150)]
    b.append(poly(outline, 'url(#pPerlit)', '#9c8a3f', 0.5))
    # OSB-Randstreifen als 16-Eck
    seg = []
    for i in range(n + 1):
        ang = a0 + (a1 - a0) * i / n
        seg.append((CX + (R + 0.9) * math.cos(ang), CY + (R + 0.9) * math.sin(ang)))
    for i in range(n):
        b.append(line(*seg[i], *seg[i + 1], '#7a5523', 1.4))
    b.append(line(CX - hx - 0.9, y_cut, CX - hx - 0.9, 150, '#7a5523', 1.4) + line(CX + hx + 0.9, y_cut, CX + hx + 0.9, 150, '#7a5523', 1.4))
    seglen = 2 * (R + 0.9) * math.sin((a1 - a0) / n / 2)
    b.append(circle(CX, CY, A + T, 'none', '#7a3d1c', 0.35, 'stroke-dasharray="2 1"'))
    b.append(circle(CX, CY, A, 'none', '#7a3d1c', 0.25, 'stroke-dasharray="1 1"'))
    b.append(circle(CX, CY, 0.9, '#c0392b', 'none'))
    b.append(text(CX + 2, CY - 1.5, 'Mittelpunkt M', 2.4, 'start', '#c0392b', 'bold'))
    b.append(dim_h(CX - R, CX + R, CY + 3, f'Ø {2 * R:.1f}', 0, 2.6))
    b.append(dim_h(CX - hx, CX + hx, 145, f'{2 * hx:.0f}', 0, 2.6))
    b.append(dim_v(-6, 0, CY, f'{CY:g}', -1, 2.6))
    b.append(dim_h(0, CX, -6, '75', 0, 2.6))
    b.append(text(CX, CY + 14, 'Perlit-Zement 10 cm', 3.0, 'middle', '#6d5f20', 'bold'))
    b.append(text(CX, CY + 19, '(Kuppel-Aussenrand + 5 cm)', 2.5, 'middle', '#6d5f20'))
    b.append(note(170, 10, ['Randschalung:', f'16 OSB-Streifen 10 x {seglen:.1f} cm', 'als 16-Eck um M, Ecken', 'mit Klebeband/Draht zusammen,', 'aussen mit Steinen gestützt.', '', 'Vorne 2 gerade Streifen bis', 'zur Plattenkante.', '', 'So zeichnet ihr den Kreis:', 'Nagel in M (75 / 73.4),', f'Schnur {R:.1f} cm + Bleistift.', '', 'Mischung 5 : 1 erdfeucht,', 'nur andrücken, nicht stampfen.', 'Oberfläche mit Brett', 'auf den Rand abziehen.'], 2.6))
    b.append(text(75, 158, '▼ vorne', 2.8, 'middle', COL['hint'], 'bold'))
    b.append(head(-10, -16, 'BODENDÄMMUNG  1:20', 'Draufsicht auf die Herdplatte (Betonwand oben)'))
    OUT['bodendaemmung'] = svg(1200, 820, ''.join(b), 'Bodendaemmung', (-16, -26, 250, 192))
    DATA['daemm_ring'] = dict(R=round(R, 1), segment=round(seglen, 1), n=n)

# ================================================================ 6 BACKBODEN VERLEGEPLAN + ZUSCHNITT
def backboden():
    Rb = A + T
    hx = TUN_B / 2 + TUN_W
    y0 = CY - Rb
    rows, y = [], y0
    while y < 150 - 0.01:
        rows.append((round(y, 2), round(min(y + 20, 150), 2)))
        y += 20
    def need(ya, yb):
        xs = []
        for k in range(41):
            yy = ya + (yb - ya) * k / 40
            d = yy - CY
            if abs(d) <= Rb:
                h = math.sqrt(Rb * Rb - d * d); xs += [CX - h, CX + h]
            if yy >= CY:
                xs += [CX - hx, CX + hx]
        return (min(xs), max(xs))
    layout = []
    for i, (ya, yb) in enumerate(rows):
        xa, xb = need(ya, yb)
        xa, xb = math.floor(xa), math.ceil(xb)
        W = round(yb - ya, 1)
        L = xb - xa
        if W >= 19.9:
            first = 50 if L > 50 else L
            segs = [(xb - first, first)] + ([(xa, L - first)] if L > first else []) if i % 2 else [(xa, first)] + ([(xa + first, L - first)] if L > first else [])
        else:
            segs = [(xa, L / 2), (xa + L / 2, L / 2)]
        for (sx, sl) in segs:
            layout.append(dict(reihe=i + 1, x=sx, y=ya, l=sl, w=W, ganz=(abs(sl - 50) < 0.01 and W >= 19.9)))
    # Herkunft: ganze Platten zuerst, Zuschnitte nach First-Fit-Decreasing (0.5 cm Schnittverlust)
    plates = 0
    for p in layout:
        if p['ganz']:
            plates += 1; p['quelle'] = f'P{plates}'
    narrow = [p for p in layout if p['w'] < 19.9]
    cuts = sorted([p for p in layout if not p['ganz'] and p['w'] >= 19.9], key=lambda p: -p['l'])
    if narrow:   # schmale Streifen: aus einem 20 cm breiten Stueck der Laenge max(l) laengs geschnitten
        cuts.append(dict(l=max(p['l'] for p in narrow), streifen=narrow))
        cuts.sort(key=lambda p: -p['l'])
    bins = []
    for p in cuts:
        for bn in bins:
            if bn['rest'] >= p['l'] + 0.5:
                bn['rest'] -= p['l'] + 0.5; src = bn['name']; break
        else:
            plates += 1; src = f'P{plates}'; bins.append(dict(name=src, rest=50 - p['l'] - 0.5))
        for q in p.get('streifen', [p]):
            q['quelle'] = src
    DATA['backboden'] = dict(platten=plates, stuecke=layout)
    b = []
    b.append(rect(0, 0, 150, 150, 'url(#pPerlit)', '#9c8a3f', 0.3, 'opacity="0.5"'))
    for p in layout:
        fill = '#d9844f' if p['ganz'] else '#e8a77f'
        b.append(rect(p['x'], p['y'], p['l'], p['w'], fill, '#5a2a12', 0.35))
        if p['w'] > 6:
            b.append(text(p['x'] + p['l'] / 2, p['y'] + p['w'] / 2 - 0.6, f"{p['l']:g}", 2.6, 'middle', '#fff', 'bold'))
            b.append(text(p['x'] + p['l'] / 2, p['y'] + p['w'] / 2 + 3.0, p['quelle'], 2.2, 'middle', '#fff'))
    # Schnittlinie Kreis + Tunnel
    th = math.asin(hx / Rb)
    yc = CY + Rb * math.cos(th)
    d = f'M {CX - hx:.2f} 150 L {CX - hx:.2f} {yc:.2f} '
    m = 80
    a0, a1 = math.pi / 2 + th, math.pi / 2 - th + 2 * math.pi
    for k in range(m + 1):
        ang = a0 + (a1 - a0) * k / m
        d += f'L {CX + Rb * math.cos(ang):.2f} {CY + Rb * math.sin(ang):.2f} '
    d += f'L {CX + hx:.2f} {yc:.2f} L {CX + hx:.2f} 150'
    b.append(path(d, 'none', '#c0392b', 0.7, 'stroke-dasharray="2.5 1.2"'))
    b.append(circle(CX, CY, A, 'none', '#222', 0.3, 'stroke-dasharray="1 1"'))
    b.append(circle(CX, CY, 0.9, '#c0392b', 'none'))
    for i, (ya, yb) in enumerate(rows):
        b.append(text(-3, (ya + yb) / 2 + 1, f'R{i + 1}', 2.4, 'end', '#5a2a12', 'bold'))
    b.append(dim_h(CX - Rb, CX + Rb, 160, f'Schnittkreis Ø {2 * Rb:.1f} (Kuppel aussen)', 0, 2.5))
    b.append(dim_v(155, rows[0][0], 150, f'{150 - rows[0][0]:.1f}', 1, 2.5))
    b.append(dim_h(CX - hx, CX + hx, 153.5, f'Tunnel {2 * hx:.0f}', 0, 2.3))
    b.append(note(170, 6, [f'{plates} Platten 50 x 20 x 4 nötig', '(P1 … = Herkunftsplatte;', 'Reststücke werden weiter-', 'verwendet).', '', 'Zahl im Stück = Länge in cm.', 'dunkel = ganze Platte', 'hell = zugeschnitten', '', 'Rot gestrichelt = Schnittlinie.', 'Erst rechteckig auslegen,', 'Kreis mit Schnur (46.4 cm)', 'anzeichnen, Stücke einzeln', 'herausnehmen, nass schneiden,', 'wieder einlegen.', '', 'Fugen dicht gestossen,', 'ohne Mörtel, auf 5 mm', 'trockenem Sand.'], 2.6))
    b.append(head(-10, -16, 'BACKBODEN – VERLEGE- UND ZUSCHNITTPLAN  1:20', 'Schamottplatten 40 x 200 x 500 mm · Draufsicht (Betonwand oben)'))
    OUT['backboden'] = svg(1200, 860, ''.join(b), 'Backboden', (-16, -26, 260, 196))

# ================================================================ 7 SANDFORM-SCHABLONE
def schablone():
    b = []
    S = 2.4
    def P(x, z): return (24 + x * S, 150 - z * S)
    W, Hh = 48, 44
    curve = [P(A * math.cos(math.pi / 2 * i / 60), C * math.sin(math.pi / 2 * i / 60)) for i in range(61)]   # von (40,0) bis (0,36)
    # Schablone = Negativ: OSB-Rechteck minus Viertel-Ellipse
    board = [P(0, Hh), P(W, Hh), P(W, 0), P(A, 0)] + curve + [P(0, C)]
    b.append(poly([P(0, 0), P(A, 0)] + curve, '#fbf3e6', '#bbb', 0.3, 'stroke-dasharray="1.5 1"'))
    b.append(poly(board, '#e9d9b0', '#7a5523', 0.5))
    b.append(path('M ' + ' L '.join(f'{x:.2f} {y:.2f}' for x, y in curve), 'none', '#c0392b', 0.9))
    b.append(text(*P(14, 12), 'wegschneiden', 2.8, 'middle', '#999', 'bold'))
    b.append(text(*P(14, 8), '(hier entsteht die Sandform)', 2.4, 'middle', '#999'))
    b.append(text(*P(38, 38), 'SCHABLONE (OSB)', 3.0, 'middle', '#7a5523', 'bold'))
    b.append(line(*P(-2, -8), *P(-2, Hh + 10), '#333', 0.9))
    b.append(text(*P(0, Hh + 6), 'Drehachse (Rundholz/Rohr senkrecht im Mittelpunkt M)', 2.6, 'start', '#333', 'bold'))
    for zz in (C + 3, Hh - 3):
        b.append(circle(*P(1.5, zz), 0.8, '#333', 'none'))
    b.append(text(*P(3, Hh - 1), '2 Schrauben', 2.3, 'start', '#333'))
    b.append(line(*P(-6, 0), *P(W + 4, 0), '#555', 0.4))
    b.append(text(*P(W + 4, 1), 'Backboden (Zeitung)', 2.3, 'end', '#555'))
    tab = []
    for xx in range(0, 41, 5):
        zz = C * math.sqrt(max(0, 1 - (xx / A) ** 2))
        tab.append((xx, round(zz, 1)))
        b.append(line(*P(xx, 0), *P(xx, zz), '#bbb', 0.2, 'stroke-dasharray="0.8 0.8"'))
        b.append(circle(*P(xx, zz), 0.8, '#c0392b', 'none'))
        b.append(text(P(xx, 0)[0], P(0, -3.6)[1], f'{xx}', 2.4, 'middle', '#333'))
    b.append(text(P(20, 0)[0], P(0, -8)[1], 'Abstand von der Achse (cm)', 2.6, 'middle', '#333'))
    b.append(dim_v(P(-9, 0)[0], P(0, 0)[1], P(0, C)[1], f'{C:g}', -1, 2.6))
    b.append(note(150, 52, ['Höhe der Kurve über dem Boden:'] + [f'  {x:>2} cm → {z:>4} cm' for x, z in tab], 2.8, lh=4.3))
    b.append(note(150, 102, ['1. Punkte auf das OSB übertragen, mit einer', '   Latte zur Kurve verbinden, aussägen.', '2. Schablone so an die Achse schrauben, dass', '   ihre Unterkante den Boden gerade berührt.', '3. Feuchten Sand lagenweise andrücken,', '   Schablone ringsum drehen, Sand ergänzen.', '4. Mit nassem Zeitungspapier belegen.',
                        f'Sandmenge ca. {2 / 3 * math.pi * A * A * C / 1e6:.2f} m³ (alter Bettungssand).'], 2.7))
    b.append(head(5, 10, 'SANDFORM-SCHABLONE  1:10', 'Viertel-Ellipse = Innenform der Kuppel (Radius 40, Höhe 36) · die Schablone ist das Negativ'))
    OUT['schablone'] = svg(1200, 800, ''.join(b), 'Schablone', (0, 0, 262, 176))
    DATA['schablone'] = tab

# ================================================================ 8 KUPPEL REIHE 1 (Draufsicht)
def kuppel_reihen():
    b = []
    S = 1.5
    def P(x, y): return (95 + x * S, 95 + y * S)
    b.append(circle(*P(0, 0), (A + T + 1) * S, '#efe2d6', 'none', 0))
    reihen = K['reihen']
    rad = [(r['r_innen'], r['halbsteine'] + r['tuerabzug'], r['tuerabzug'], r['reihe']) for r in reihen]
    # Reihe 1 in voller Darstellung
    r1 = reihen[0]
    n = r1['halbsteine'] + r1['tuerabzug']
    step = 2 * math.pi / n
    ri, ro = A, A + T
    for k in range(n):
        a0 = math.pi / 2 + (k - (r1['tuerabzug'] - 1) / 2) * step - step / 2 + 0.015
        a1 = a0 + step - 0.03
        is_door = k < r1['tuerabzug']
        q = [P(ri * math.cos(a0), ri * math.sin(a0)), P(ro * math.cos(a0), ro * math.sin(a0)), P(ro * math.cos(a1), ro * math.sin(a1)), P(ri * math.cos(a1), ri * math.sin(a1))]
        if is_door:
            b.append(poly(q, 'none', '#999', 0.3, 'stroke-dasharray="1 1"'))
        else:
            b.append(poly(q, '#d9844f', '#5a2a12', 0.35))
            am = (a0 + a1) / 2
            b.append(text(*P((ri + T / 2) * math.cos(am), (ri + T / 2) * math.sin(am) + 0.8), f'{k - r1["tuerabzug"] + 1}', 2.2, 'middle', '#fff', 'bold'))
    b.append(circle(*P(0, 0), A * S, 'none', '#7a3d1c', 0.3, 'stroke-dasharray="1.5 1"'))
    b.append(circle(*P(0, 0), 0.8, '#c0392b', 'none'))
    # Tunnelwaende
    b.append(rect(P(-TUN_B / 2 - TUN_W, 37)[0], P(0, 37)[1], TUN_W * S, (150 - CY - 37) * S, '#e8a77f', '#5a2a12', 0.35))
    b.append(rect(P(TUN_B / 2, 37)[0], P(0, 37)[1], TUN_W * S, (150 - CY - 37) * S, '#e8a77f', '#5a2a12', 0.35))
    b.append(text(*P(0, 62), 'Tür / Tunnel 40 breit', 2.6, 'middle', '#5a2a12', 'bold'))
    b.append(dim_h(P(-TUN_B / 2, 0)[0], P(TUN_B / 2, 0)[0], P(0, 54)[1], '40', 0, 2.4))
    b.append(text(*P(0, -A - 12), 'hinten (Betonwand)', 2.6, 'middle', COL['hint']))
    b.append(head(5, 6, 'KUPPEL – REIHE 1 IN DER DRAUFSICHT  1:15', f'{r1["halbsteine"]} Halbsteine + Türlücke ({r1["tuerabzug"]} Plätze), Teilung {360 / n:.1f}°'))
    # Tabelle aller Reihen rechts
    tx, ty = 190, 30
    b.append(text(tx, ty, 'Alle Reihen', 3.2, 'start', COL['line'], 'bold'))
    hdr = ['Reihe', 'Höhe innen', 'Radius innen', 'Neigung', 'Steine', 'Teilung']
    for j, h in enumerate(hdr):
        b.append(text(tx + j * 22, ty + 7, h, 2.4, 'start', '#555', 'bold'))
    for i, r in enumerate(reihen):
        nn = r['halbsteine'] + r['tuerabzug']
        row = [f'R{r["reihe"]}', f'{r["z_innen_von"]}–{r["z_innen_bis"]}', f'{r["r_innen"]}', f'{r["neigung_grad"]:.0f}°',
               f'{r["halbsteine"]}' + (f' (+{r["tuerabzug"]} Tür)' if r['tuerabzug'] else ''), f'{360 / nn:.1f}°']
        for j, c in enumerate(row):
            b.append(text(tx + j * 22, ty + 13 + i * 6, c, 2.6))
    b.append(text(tx, ty + 13 + len(reihen) * 6, f'Schluss: {K["schluss_halbsteine"]} zugeschnittene Halbsteine', 2.6, 'start', COL['line'], 'bold'))
    b.append(note(tx, ty + 30 + len(reihen) * 6, ['Reihenfolge je Reihe:', '1. Mitte gegenüber der Tür beginnen,', '2. abwechselnd links/rechts setzen,', '3. letzter Stein = Schlussstein der Reihe,', '   bei Bedarf schmaler schneiden.', 'Stossfugen gegenüber der Reihe darunter', 'um eine halbe Steinbreite versetzen.', 'Fuge innen 3–6 mm, aussen keilförmig voll.'], 2.6))
    OUT['kuppel_reihe1'] = svg(1300, 840, ''.join(b), 'Kuppel Reihe 1', (0, -6, 340, 222))

# ================================================================ 9 EINGANG, STURZ, DECKPLATTEN, KAMIN
def eingang():
    b = []
    # Ansicht von vorne (links)
    S = 1.6
    def P(x, z): return (40 + (x - 40) * S, 130 - (z - Z_BODEN1) * S)
    b.append(rect(*P(40, Z_BODEN1), 70 * S, 4 * S, '#d9844f', '#5a2a12', 0.35))
    for k in range(V['tunnel_lagen']):
        z0 = Z_BODEN1 + k * 4.6
        for x0 in (CX - TUN_B / 2 - TUN_W, CX + TUN_B / 2):
            b.append(rect(P(x0, z0 + 4)[0], P(0, z0 + 4)[1], TUN_W * S, 4 * S, '#e8a77f', '#5a2a12', 0.35))
    zt = Z_BODEN1 + TUN_H
    for (x0, lab) in [(CX - 25, 'Sturz-/Deckplatte 50 x 20')]:
        b.append(rect(P(x0, zt + 4)[0], P(0, zt + 4)[1], 50 * S, 4 * S, '#c8693f', '#5a2a12', 0.4))
        b.append(text(P(CX, zt + 2)[0], P(0, zt + 2)[1] + 0.9, lab, 2.4, 'middle', '#fff', 'bold'))
    b.append(rect(P(CX - 7.5, zt + 4 + 30)[0], P(0, zt + 4 + 30)[1], 15 * S, 30 * S, '#c7ccd1', '#333', 0.4, 'opacity="0.85"'))
    b.append(text(P(CX, zt + 20)[0], P(0, zt + 20)[1], 'Kaminrohr', 2.3, 'middle', '#222', rot=-90))
    b.append(dim_h(P(CX - TUN_B / 2, 0)[0], P(CX + TUN_B / 2, 0)[0], P(0, Z_BODEN1 - 6)[1], '40 (Türöffnung)', 0, 2.4))
    b.append(dim_v(P(CX + 27, 0)[0], P(0, Z_BODEN1)[1], P(0, zt)[1], f'{TUN_H}', 1, 2.4))
    b.append(dim_h(P(CX - 30, 0)[0], P(CX - 20, 0)[0], P(0, Z_BODEN1 - 12)[1], '10', 0, 2.2))
    b.append(text(P(CX - 32, Z_BODEN1 + 12)[0], P(0, Z_BODEN1 + 12)[1], f'{V["tunnel_lagen"]} Lagen Streifen', 2.3, 'end', '#5a2a12'))
    b.append(text(P(CX - 32, Z_BODEN1 + 8.5)[0], P(0, Z_BODEN1 + 8.5)[1], '50 x 10 x 4, Fuge 6 mm', 2.3, 'end', '#5a2a12'))
    b.append(text(10, 30, 'ANSICHT VON VORNE (ohne Dämmung/Putz)', 3.0, 'start', COL['line'], 'bold'))
    # Deckplatten Draufsicht (rechts)
    ox, oy = 175, 54
    S2 = 1.4
    def Q(x, y): return (ox + (x - 40) * S2, oy + (y - 100) * S2)
    for x0 in (CX - TUN_B / 2 - TUN_W, CX + TUN_B / 2):
        b.append(rect(*Q(x0, 108.8), TUN_W * S2, (150 - 108.8) * S2, '#e8a77f', '#5a2a12', 0.3, 'opacity="0.6"'))
    rr = 7.75
    for (ya, yb, notch_at, lab) in [(Y_TUER, Y_TUER + 20, Y_TUER + 20, 'Platte D1 (Sturz)'), (Y_TUER + 21, Y_TUER + 41, Y_TUER + 21, 'Platte D2')]:
        x0, x1 = CX - 25, CX + 25
        if notch_at == yb:
            d = (f'M {Q(x0, ya)[0]:.2f} {Q(x0, ya)[1]:.2f} L {Q(x1, ya)[0]:.2f} {Q(x1, ya)[1]:.2f} L {Q(x1, yb)[0]:.2f} {Q(x1, yb)[1]:.2f} '
                 f'L {Q(CX + rr, yb)[0]:.2f} {Q(CX + rr, yb)[1]:.2f} A {rr * S2:.2f} {rr * S2:.2f} 0 0 0 {Q(CX - rr, yb)[0]:.2f} {Q(CX - rr, yb)[1]:.2f} '
                 f'L {Q(x0, yb)[0]:.2f} {Q(x0, yb)[1]:.2f} Z')
        else:
            d = (f'M {Q(x0, ya)[0]:.2f} {Q(x0, ya)[1]:.2f} L {Q(CX - rr, ya)[0]:.2f} {Q(CX - rr, ya)[1]:.2f} A {rr * S2:.2f} {rr * S2:.2f} 0 0 0 {Q(CX + rr, ya)[0]:.2f} {Q(CX + rr, ya)[1]:.2f} '
                 f'L {Q(x1, ya)[0]:.2f} {Q(x1, ya)[1]:.2f} L {Q(x1, yb)[0]:.2f} {Q(x1, yb)[1]:.2f} L {Q(x0, yb)[0]:.2f} {Q(x0, yb)[1]:.2f} Z')
        b.append(path(d, '#c8693f', '#5a2a12', 0.45))
        b.append(text(Q(CX + 16, 0)[0], Q(0, (ya + yb) / 2)[1] + 1, lab, 2.3, 'middle', '#fff', 'bold'))
    b.append(circle(*Q(CX, Y_KAMIN), rr * S2, 'none', '#222', 0.4, 'stroke-dasharray="1 0.8"'))
    b.append(text(Q(CX, 0)[0], Q(0, Y_KAMIN)[1] + 1, 'Ø 15.5', 2.3, 'middle', '#222', 'bold'))
    b.append(dim_h(Q(CX - 25, 0)[0], Q(CX + 25, 0)[0], Q(0, 154)[1], '50', 0, 2.4))
    b.append(dim_v(Q(CX + 33, 0)[0], Q(0, Y_TUER)[1], Q(0, Y_TUER + 20)[1], '20', 1, 2.3))
    b.append(dim_v(Q(CX + 33, 0)[0], Q(0, Y_TUER + 21)[1], Q(0, Y_TUER + 41)[1], '20', 1, 2.3))
    b.append(text(Q(CX + 36, 0)[0], Q(0, Y_TUER + 20.8)[1], '1 cm Fuge', 2.2, 'start', '#555'))
    b.append(text(Q(40, 0)[0], Q(0, Y_TUER - 4)[1], f'Kuppel-Türlinie y = {Y_TUER:g}', 2.3, 'start', '#7a3d1c'))
    b.append(text(ox - 6, 30, 'DECKPLATTEN VON OBEN', 3.0, 'start', COL['line'], 'bold'))
    b.append(note(ox - 6, 150, [f'Halbkreis-Ausschnitt r = {rr} cm in beide Platten', '(Winkelschleifer, mehrere flache Schnitte, dann', 'ausbrechen). Rohr sitzt zwischen D1 und D2.', 'Auflager: 5 cm je Seite auf den Tunnelwänden.',
                                 'Hat das Rohr des Kollegen einen anderen Ø:', 'Ausschnitt = Rohr-Ø + 5 mm.'], 2.5))
    b.append(head(5, 6, 'EINGANG, STURZ, DECKPLATTEN, KAMIN  1:10', 'Tunnel 40 x 22.4 cm · Wände aus längs halbierten Schamottplatten'))
    OUT['eingang'] = svg(1300, 800, ''.join(b), 'Eingang', (0, -2, 305, 182))

# ================================================================ 10 ZUSCHNITT STEINE
def zuschnitt():
    b = []
    def box3(x, y, w, d, h, fill, lab=''):
        # einfache Kavalierperspektive
        k = 0.5
        top = [(x, y), (x + w, y), (x + w + d * k, y - d * k), (x + d * k, y - d * k)]
        front = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        side = [(x + w, y), (x + w + d * k, y - d * k), (x + w + d * k, y + h - d * k), (x + w, y + h)]
        o = poly(front, fill, '#333', 0.35) + poly(top, '#f2c4a4' if fill == '#d9844f' else '#e6e8ea', '#333', 0.35) + poly(side, '#b86a3c' if fill == '#d9844f' else '#b8bec4', '#333', 0.35)
        if lab: o += text(x + w / 2, y + h + 5, lab, 2.5, 'middle')
        return o
    # NF-Stein halbieren
    b.append(text(5, 18, '① Schamottstein NF halbieren (35 Stück → 70 Halbsteine)', 3.0, 'start', COL['line'], 'bold'))
    b.append(box3(10, 40, 50, 25, 12.8, '#d9844f', '250 x 124 x 64 mm'))
    b.append(line(35, 40, 35, 52.8, '#c0392b', 0.6, 'stroke-dasharray="1.5 1"') + line(35, 40, 41.2, 33.8, '#c0392b', 0.6, 'stroke-dasharray="1.5 1"'))
    b.append(text(70, 46, '→', 6, 'middle', '#555'))
    b.append(box3(80, 40, 25, 25, 12.8, '#d9844f') + box3(112, 40, 25, 25, 12.8, '#d9844f'))
    b.append(text(108, 63.5, '2 x 125 x 124 x 64', 2.5, 'middle'))
    b.append(note(150, 30, ['Schnitt quer in der Mitte (125 mm).', 'Winkelschleifer 125 schneidet nur 33 mm tief:', '→ ringsum 4 Seiten anschneiden, dann mit', '   Gummihammer auf Kante brechen.', 'Steine vorher 5 min wässern = weniger Staub.', 'FFP2/FFP3, Brille, Gehörschutz, draussen, Wind', 'im Rücken. Nie trocken in geschlossenen Räumen.'], 2.6))
    # Platte laengs halbieren
    b.append(text(5, 85, '② Schamottplatte längs halbieren (5 Platten → 10 Streifen 500 x 100 x 40)', 3.0, 'start', COL['line'], 'bold'))
    b.append(box3(10, 105, 100, 20, 8, '#d9844f', '500 x 200 x 40 mm'))
    b.append(line(10, 109, 110, 109, '#c0392b', 0.6, 'stroke-dasharray="1.5 1"'))
    b.append(note(150, 98, ['Mit Bleistift + Brett als Lineal anzeichnen.', '40 mm dick: von oben 33 mm, dann umdrehen', 'und von unten fertig schneiden.', 'Schnittkante innen in den Tunnel legen,', 'Werkskante nach aussen.'], 2.6))
    # Kann-Stein halbieren
    b.append(text(5, 145, '③ Schalungsstein halbieren (1 Stück → 2 x 25 cm, Steine 6½ und 9½)', 3.0, 'start', COL['line'], 'bold'))
    b.append(box3(10, 165, 50, 24, 25, '#cfd3d7', '500 x 240 x 250 mm'))
    b.append(line(35, 165, 35, 190, '#c0392b', 0.6, 'stroke-dasharray="1.5 1"'))
    b.append(note(150, 160, ['Schnitt durch den Mittelsteg.', 'Aussenwände (ca. 3 cm) mit Diamantscheibe', 'durchtrennen, Steg mit Hammer + Meissel brechen.'], 2.6))
    b.append(head(5, 4, 'ZUSCHNITT  (Skizze, nicht massstäblich)', ''))
    OUT['zuschnitt'] = svg(1200, 880, ''.join(b), 'Zuschnitt', (0, -4, 255, 212))

# ================================================================ 11 TUER UND KAMINABDECKUNG
def tuer():
    b = []
    S = 0.22
    ox, oy = 10, 25
    b.append(rect(ox, oy, 1000 * S, 500 * S, '#e6e8ea', '#333', 0.4))
    b.append(text(ox + 500 * S, oy - 2, 'Glattblech 1000 x 500 x 0.75 mm', 2.6, 'middle', '#333', 'bold'))
    b.append(rect(ox + 10 * S, oy + 10 * S, 490 * S, 310 * S, '#c7ccd1', '#c0392b', 0.5))
    b.append(rect(ox + 25 * S, oy + 25 * S, 460 * S, 280 * S, 'none', '#555', 0.3, 'stroke-dasharray="1.5 1"'))
    b.append(text(ox + 255 * S, oy + 170 * S, 'Tür: zuschneiden 490 x 310', 2.6, 'middle', '#222', 'bold'))
    b.append(text(ox + 255 * S, oy + 205 * S, 'Rand 15 mm rundum abkanten → 460 x 280', 2.3, 'middle', '#222'))
    for (x, y) in [(10, 10), (500, 10), (10, 320), (500, 320)]:
        b.append(rect(ox + x * S - 15 * S if x > 10 else ox + x * S, oy + y * S - 15 * S if y > 10 else oy + y * S, 15 * S, 15 * S, '#fff', '#c0392b', 0.3))
    b.append(circle(ox + 750 * S, oy + 165 * S, 100 * S, '#c7ccd1', '#c0392b', 0.5))
    b.append(text(ox + 750 * S, oy + 166 * S, 'Kaminabdeckung Ø 200', 2.4, 'middle', '#222', 'bold'))
    b.append(text(ox + 750 * S, oy + 166 * S + 3.4, '(nur auf kalten Ofen)', 2.2, 'middle', '#222'))
    b.append(text(ox + 255 * S, oy + 420 * S, 'Rest', 2.6, 'middle', '#777'))
    b.append(note(ox, oy + 500 * S + 10, ['Ecken 15 x 15 mm ausschneiden (Kästchen), dann die 4 Ränder über eine Tischkante', 'mit Gummihammer + Holzklotz 90° abkanten → steife Tür 46 x 28 cm (Öffnung 40 x 22.4,', 'Überdeckung 3 cm seitlich, 2.8 cm oben/unten). Griff mit 2 Schrauben M4 + 3-cm-Holzklotz', 'als Abstand mittig anschrauben. Aussen 2 x Thermolack. Tür lehnt vor der Tunnelöffnung.'], 2.6))
    # Seitenansicht Tuer
    sx, sy = 175, 140
    b.append(rect(sx, sy, 2, 28 * 1.6, '#555', '#333', 0.3))
    b.append(rect(sx + 2, sy, 1.5 * 1.6, 0.8, '#555') + rect(sx + 2, sy + 28 * 1.6 - 0.8, 1.5 * 1.6, 0.8, '#555'))
    b.append(rect(sx - 4.8, sy + 18, 4.8, 9, '#c9a26b', '#7a5523', 0.3))
    b.append(rect(sx - 9.5, sy + 14, 4.7, 17, '#d8b47c', '#7a5523', 0.3))
    b.append(text(sx - 12, sy + 40, 'Griff + Holzklotz', 2.3, 'end', '#7a5523'))
    b.append(text(sx + 6, sy + 48, 'Seitenansicht', 2.3, 'start', '#333'))
    b.append(head(5, 6, 'TÜR UND KAMINABDECKUNG  1:5 / Zuschnitt 1:10', 'aus dem Glattblech 500 x 1000 x 0.75 mm (OBI 4983821)'))
    OUT['tuer'] = svg(1100, 720, ''.join(b), 'Tuer', (0, -2, 240, 200))

# ================================================================ 12 DETAIL WANDAUFBAU KUPPEL
def detail():
    b = []
    S = 5
    def P(r, z): return (20 + r * S, 150 - z * S)
    layers = [(0, 6.4, '#d9844f', 'Schamott-Halbstein 6.4 cm'), (6.4, 14.4, 'url(#pIso)', 'Perlit-Zement 5:1, 8 cm (3 Lagen)'),
              (14.4, 14.8, 'none', 'Sechseckgeflecht, mit Draht verankert'), (14.8, 17.4, COL['putz'], 'Zementputz 1:4, 2 Lagen = ca. 3 cm')]
    for r0, r1, f, lab in layers:
        if f != 'none':
            b.append(rect(P(r0, 0)[0], P(0, 22)[1], (r1 - r0) * S, 22 * S, f, '#333', 0.3))
    b.append(line(P(14.6, 0)[0], P(0, 22)[1], P(14.6, 0)[0], P(0, 0)[1], '#2c5f8a', 0.9, 'stroke-dasharray="1.2 0.8"'))
    for z in (4, 11, 18):
        b.append(line(P(6.4, z)[0], P(0, z)[1], P(15.2, z)[0], P(0, z - 0.6)[1], '#2c5f8a', 0.5))
        b.append(f'<path d="M {P(15.2, z)[0]:.1f} {P(0, z - 0.6)[1]:.1f} q 2 -2 0 -4" fill="none" stroke="#2c5f8a" stroke-width="0.5"/>')
    b.append(text(P(-1, 0)[0], P(0, 23)[1] - 2, 'innen (Feuerraum)', 2.8, 'end', COL['hint'], 'bold'))
    b.append(text(P(18, 0)[0], P(0, 23)[1] - 2, 'aussen', 2.8, 'start', COL['hint'], 'bold'))
    for i, (r0, r1, f, lab) in enumerate(layers):
        b.append(line(P((r0 + r1) / 2, 0)[0], P(0, 2 + i * 5)[1], P(20, 0)[0] + 4, P(0, 2 + i * 5)[1], '#888', 0.25))
        b.append(text(P(20, 0)[0] + 6, P(0, 2 + i * 5)[1] + 1, lab, 2.8))
    b.append(text(P(20, 0)[0] + 6, P(0, 22)[1] + 1, 'Drahtanker: Bindedraht-Haken in die 1. Perlitlage', 2.6, 'start', '#2c5f8a'))
    b.append(text(P(20, 0)[0] + 6, P(0, 22)[1] + 5, 'stecken, ca. alle 25 cm; später ums Geflecht drehen.', 2.6, 'start', '#2c5f8a'))
    b.append(dim_h(P(0, 0)[0], P(17.4, 0)[0], P(0, -4)[1], 'Wandstärke total 17.4 cm', 0, 2.6))
    b.append(head(5, 8, 'DETAIL WANDAUFBAU KUPPEL  1:2', 'Schnitt durch die Kuppelwand'))
    OUT['detail_wand'] = svg(1100, 620, ''.join(b), 'Detail Wand', (0, -2, 230, 178))

# ================================================================ 13 ISOMETRIE
COS30, SIN30 = math.cos(math.radians(30)), 0.5

def iso(x, y, z, s=1.0, ox=0, oy=0):
    return (ox + (x - y) * COS30 * s, oy + ((x + y) * SIN30 - z) * s)

def iso_box(x, y, z, w, d, h, col, s, ox, oy, sw=0.3):
    top, front, right = col
    P = lambda a, b_, c: iso(a, b_, c, s, ox, oy)
    t = [P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)]
    f = [P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x, y + d, z + h)]
    r = [P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x + w, y, z + h)]
    return poly(f, front, '#333', sw) + poly(r, right, '#333', sw) + poly(t, top, '#333', sw)

def hull(pts):
    pts = sorted(set((round(p[0], 2), round(p[1], 2)) for p in pts))
    if len(pts) < 3: return pts
    def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]

def iso_cyl(cx, cy, z, r, h, col, s, ox, oy, front=None):
    top, side, _ = col
    n = 72
    ring = lambda zz: [iso(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n), zz, s, ox, oy) for i in range(n)]
    lo, hi = ring(z), ring(z + h)
    o = poly(hull(lo + hi), side, '#333', 0.3)
    o += poly(hi, top, '#333', 0.3)
    if front:
        fx0, fx1, fy0, fy1 = front
        o += iso_box(fx0, fy0, z, fx1 - fx0, fy1 - fy0, h, col, s, ox, oy)
        o += poly([iso(fx0, fy0, z + h, s, ox, oy), iso(fx1, fy0, z + h, s, ox, oy), iso(fx1, fy1 - 0.01, z + h, s, ox, oy), iso(fx0, fy1 - 0.01, z + h, s, ox, oy)], top, 'none', 0)
    return o

def iso_dome(cx, cy, z0, a, c, col, s, ox, oy, lines=None, door=None):
    pts = [iso(cx + a * math.cos(th) * math.cos(ph), cy + a * math.cos(th) * math.sin(ph), z0 + c * math.sin(th), s, ox, oy)
           for th in [i * math.pi / 2 / 12 for i in range(13)] for ph in [j * 2 * math.pi / 48 for j in range(48)]]
    o = poly(hull(pts), col, '#333', 0.35)
    for (zz, rr) in (lines or []):
        seg = []
        for j in range(0, 97):
            ph = math.radians(-45) + j * math.radians(180) / 96
            seg.append(iso(cx + rr * math.cos(ph), cy + rr * math.sin(ph), zz, s, ox, oy))
        o += '<polyline points="' + ' '.join(f'{p[0]:.2f},{p[1]:.2f}' for p in seg) + '" fill="none" stroke="#7a3d1c" stroke-width="0.25"/>'
    return o

C_BETON = ('#d6dadf', '#b7bdc4', '#c6ccd2')
C_STEIN = ('#dfe2e5', '#aeb4bb', '#c2c8ce')
C_SCHAM = ('#e8a77f', '#c8693f', '#d9844f')
C_PERL = ('#f6edc9', '#e3d49a', '#ecdfae')
C_KIES = ('#d8cfb8', '#bfb397', '#cbc0a6')
C_PUTZ = ('#f1eee8', '#d8d3c9', '#e5e1d8')

def stage_parts(stage):
    """Bauteile bis zur Etappe (Liste von ('box', args) / ('dome', args))."""
    P = []
    P.append(('box', (-10, -10, -22.5, 170, 170, 12.5, C_KIES)))
    if stage >= 2:
        P.append(('box', (0, 0, -10, 150, 150, 15, C_BETON)))
    if stage >= 3:
        P.append(('box', (0, 0, 5, 150, 24, 75, C_STEIN)))
        P.append(('box', (0, 24, 5, 24, 126, 75, C_STEIN)))
        P.append(('box', (126, 24, 5, 24, 126, 75, C_STEIN)))
    if stage >= 4:
        P.append(('box', (0, 0, 80, 150, 150, 10, C_BETON)))
    if stage >= 5:
        P.append(('cyl', (CX, CY, 90, 51.4, 10, C_PERL, (CX - 35, CX + 35, CY + 30, 150))))
        P.append(('cyl', (CX, CY, 100, 46.4, 4.5, C_SCHAM, (CX - 30, CX + 30, CY + 30, 150))))
    if stage == 6:
        P.append(('box', (CX - 30, Y_TUER + 2, Z_BODEN1, 10, 150 - Y_TUER - 2, TUN_H, C_SCHAM)))
        P.append(('dome', (CX, CY, Z_BODEN1, A + T, C + T, '#d9844f', [(Z_BODEN1 + r['z_innen_bis'] + 0.3, A * math.cos(math.asin(min(1, r['z_innen_bis'] / C))) + T) for r in K['reihen']])))
        P.append(('box', (CX + 20, Y_TUER + 2, Z_BODEN1, 10, 150 - Y_TUER - 2, TUN_H, C_SCHAM)))
        P.append(('box', (CX - 25, Y_TUER, Z_BODEN1 + TUN_H, 50, 41, 4, C_SCHAM)))
        P.append(('box', (CX - 7.5, Y_KAMIN - 7.5, Z_BODEN1 + TUN_H + 4, 15, 15, 60, ('#d5d9dd', '#9da4ab', '#b9c0c6'))))
    if stage >= 7:
        P.append(('dome', (CX, CY, Z_BODEN1, A + T + ISO + PUTZ, C + T + ISO + PUTZ, '#ece8e0', [])))
        P.append(('box', (CX - 33, Y_TUER - 4, Zg.Z_HERD1, 66, 150 - Y_TUER + 4 + 3, Z_BODEN1 + TUN_H + 4 + ISO + PUTZ - Zg.Z_HERD1, C_PUTZ)))
        P.append(('box', (CX - 7.5, Y_KAMIN - 7.5, Z_BODEN1 + TUN_H + 4 + ISO + PUTZ, 15, 15, 85, ('#4d5257', '#2e3236', '#3d4146'))))
        P.append(('box', (CX - 23, 150 + 3, Z_BODEN1 - 2, 46, 0.8, 28, ('#555', '#3a3a3a', '#444'))))
    return P

def draw_parts(parts, s, ox, oy):
    o = ''
    for kind, a in parts:
        if kind == 'box':
            x, y, z, w, d, h, col = a
            o += iso_box(x, y, z, w, d, h, col, s, ox, oy)
        elif kind == 'cyl':
            cx, cy, z, r, h, col, fr = a
            o += iso_cyl(cx, cy, z, r, h, col, s, ox, oy, fr)
        else:
            cx, cy, z0, aa, cc, col, ln = a
            o += iso_dome(cx, cy, z0, aa, cc, col, s, ox, oy, ln)
    return o

def iso_etappen():
    b = []
    titles = ['1  Freilegen: Platten, Sand, Vlies weg', '2  Fundament 150 x 150 x 15', '3  Sockel: 3 Lagen Schalungssteine',
              '4  Herdplatte 10 cm', '5  Bodendämmung + Backboden', '6  Eingang, Kuppel, Deckplatten, Kamin', '7  Dämmung, Putz, Tür: fertig']
    s = 0.36
    for i, t in enumerate(titles):
        col, row = i % 4, i // 4
        ox, oy = 50 + col * 118, 82 + row * 122
        stage = i + 1
        b.append(draw_parts(stage_parts(stage if stage != 6 else 6), s, ox, oy))
        b.append(text(ox - 40, oy + 52, t, 3.0, 'start', COL['line'], 'bold'))
    # Legende im 8. Feld
    lx, ly = 50 + 3 * 118 - 40, 82 + 122 - 48
    leg = [(C_KIES[0], 'bestehender Kies'), (C_BETON[0], 'Beton'), (C_STEIN[0], 'Schalungsstein (gefüllt)'), (C_PERL[0], 'Perlit-Zement (Dämmung)'),
           (C_SCHAM[2], 'Schamott'), (C_PUTZ[0], 'Putz'), ('#3d4146', 'Stahl (Rohr, Tür)')]
    b.append(text(lx, ly - 6, 'Legende', 3.2, 'start', COL['line'], 'bold'))
    for j, (c, l) in enumerate(leg):
        b.append(rect(lx, ly + j * 7, 6, 4.5, c, '#333', 0.3) + text(lx + 9, ly + j * 7 + 3.8, l, 2.9))
    b.append(text(lx, ly + 58, 'Blick von vorne rechts,', 2.7, 'start', '#555'))
    b.append(text(lx, ly + 62, 'Betonwand hinten (nicht gezeichnet).', 2.7, 'start', '#555'))
    b.append(head(8, 10, 'BAUETAPPEN – ISOMETRISCHE SKIZZEN', 'von unten nach oben, jede Etappe baut auf der vorherigen auf'))
    OUT['iso_etappen'] = svg(1500, 860, ''.join(b), 'Bauetappen', (0, 0, 480, 266))

def iso_explosion():
    b = []
    s = 0.62
    ox, oy = 150, 210
    layers = [
        ([('box', (-10, -10, -22.5, 170, 170, 12.5, C_KIES))], 0, 'bestehender Kies 10–15 cm'),
        ([('box', (0, 0, -10, 150, 150, 15, C_BETON))], 25, 'Fundament 15 cm, Estrichgitter'),
        ([('box', (0, 0, 5, 150, 24, 75, C_STEIN)), ('box', (0, 24, 5, 24, 126, 75, C_STEIN)), ('box', (126, 24, 5, 24, 126, 75, C_STEIN))], 50, 'Sockel 75 cm (24 Schalungssteine)'),
        ([('box', (0, 0, 80, 150, 150, 10, C_BETON))], 80, 'Herdplatte 10 cm, 2 x R188A'),
        ([('cyl', (CX, CY, 90, 51.4, 10, C_PERL, (CX - 35, CX + 35, CY + 30, 150)))], 105, 'Bodendämmung Perlit 10 cm'),
        ([('cyl', (CX, CY, 100, 46.4, 4.5, C_SCHAM, (CX - 30, CX + 30, CY + 30, 150)))], 125, 'Backboden Schamott 4 cm'),
        (stage_parts(6)[-5:], 150, 'Kuppel, Eingang, Deckplatten, Rohr'),
    ]
    for parts, dz, lab in layers:
        shifted = []
        for kind, a in parts:
            if kind == 'box':
                x, y, z, w, d, h, col = a; shifted.append(('box', (x, y, z + dz, w, d, h, col)))
            elif kind == 'cyl':
                cx, cy, z, r, h, col, fr = a; shifted.append(('cyl', (cx, cy, z + dz, r, h, col, fr)))
            else:
                cx, cy, z0, aa, cc, col, ln = a; shifted.append(('dome', (cx, cy, z0 + dz, aa, cc, col, [(zz + dz, rr) for zz, rr in ln])))
        b.append(draw_parts(shifted, s, ox, oy))
        px, py = iso(150, 0, (parts[0][1][2] if parts[0][0] == 'box' else parts[0][1][2]) + dz, s, ox, oy)
        b.append(line(px + 2, py, px + 40, py, '#888', 0.25) + text(px + 42, py + 1, lab, 3.2))
    b.append(head(8, 10, 'EXPLOSIONSZEICHNUNG – SCHICHTEN DES OFENS', 'auseinandergezogen, damit jede Schicht sichtbar ist'))
    OUT['iso_explosion'] = svg(1300, 1150, ''.join(b), 'Explosionszeichnung', (0, 0, 400, 355))

def iso_fertig():
    b = []
    s = 0.75
    ox, oy = 122, 205
    b.append(iso_box(-40, -32, -10, 230, 22, 200, ('#b9bec3', '#a2a8ae', '#acb2b8'), s, ox, oy))
    parts = stage_parts(4)[1:] + stage_parts(7)[-4:]
    b.append(draw_parts(parts, s, ox, oy))
    for i in range(5):
        for j in range(2):
            px, py = iso(40 + i * 16, 148, 12 + j * 13, s, ox, oy)
            b.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{6 * s:.1f}" fill="{"#9c7a55" if j else "#8b6b4a"}" stroke="#4a3a2a" stroke-width="0.3"/>')
    hx, hy = iso(150, 150, 0, s, ox, oy)
    b.append(line(hx + 6, hy, hx + 6, iso(150, 150, Z_BODEN1, s, ox, oy)[1], COL['dim'], 0.4, 'marker-start="url(#arr)" marker-end="url(#arr)"'))
    b.append(text(hx + 9, (hy + iso(150, 150, Z_BODEN1, s, ox, oy)[1]) / 2, 'Arbeitshöhe 104.5', 3.4, 'start', COL['dim'], 'bold'))
    b.append(head(8, 12, 'SO SIEHT ER FERTIG AUS', 'Isometrie, Blick von vorne rechts · Gesamthöhe mit Kaminrohr ca. 231 cm'))
    OUT['iso_fertig'] = svg(1000, 1100, ''.join(b), 'Fertiger Ofen', (0, 0, 300, 330))

if __name__ == '__main__':
    for f in (lageplan, fundament, sockel, herdplatte, bodendaemmung, backboden, schablone, kuppel_reihen, eingang, zuschnitt, tuer, detail, iso_etappen, iso_explosion, iso_fertig):
        f()
    for k, v in OUT.items():
        open(os.path.join(HERE, f'{k}.svg'), 'w').write(v)
    json.dump(DATA, open(os.path.join(HERE, 'cad.json'), 'w'), indent=1, ensure_ascii=False)
    print(len(OUT), 'Zeichnungen', 'Backboden-Platten:', DATA['backboden']['platten'], 'Ring:', DATA['daemm_ring'])
