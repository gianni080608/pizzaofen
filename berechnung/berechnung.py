#!/usr/bin/env python3
"""Mengen-, Gewichts- und Kostenberechnung Pizzaofen Wuerenlos.
Alle Masse in cm, Volumen in m3, Gewichte in kg, Preise in CHF.
Aufruf: python3 berechnung.py  -> schreibt ergebnis.json und gibt Tabellen aus.
"""
import json, math

# ---------------------------------------------------------------- Konstanten
NF = dict(l=25.0, b=12.4, h=6.4, kg=3.78)          # OBI Art. 5390067
HALB = dict(w=12.5, h=12.4, t=6.4)                  # halber NF, flach verbaut
FUGE = 0.6                                          # Fugendicke Kuppel/Tunnel [cm]
PLATTE = dict(l=50.0, b=20.0, d=4.0, kg=7.4)        # OBI Art. 5390026
SOCKEL_B = SOCKEL_T = 150.0                         # Grundflaeche Sockel
WAND = 24.0                                          # Schalungsstein 50x24x25
TUNNEL_INNEN_B = 40.0
STREIFEN = dict(l=50.0, b=10.0, d=4.0)               # Plattenstreifen 500 x 100 x 40 (Platte laengs halbiert)
TUNNEL_W = STREIFEN['b']                            # Tunnelwand 10 cm
TUNNEL_LAGEN = 6
TUNNEL_H = TUNNEL_LAGEN * STREIFEN['d'] + (TUNNEL_LAGEN - 1) * FUGE   # 6 Lagen = 27.0 cm
DAEMM_KUPPEL = 8.0                                   # Perlit-Zement auf Kuppel
PUTZ = 3.0
DAEMM_BODEN = 10.0                                   # Perlit-Zement unter Boden


def ellipse_arc(a, c, n=20000):
    """Bogenlaenge Viertelellipse, liefert Liste (theta, s)."""
    pts, s, prev = [(0.0, 0.0)], 0.0, (a, 0.0)
    for i in range(1, n + 1):
        th = math.pi / 2 * i / n
        p = (a * math.cos(th), c * math.sin(th))
        s += math.dist(p, prev); prev = p
        pts.append((th, s))
    return pts


def theta_at(pts, s):
    for th, ss in pts:
        if ss >= s:
            return th
    return math.pi / 2


def kuppel(D_innen, h_innen, tuer_b=TUNNEL_INNEN_B, tuer_h=TUNNEL_H):
    """Fassung 5: Reihen auf der INNENflaeche (dort beruehren sich die Steine, die Fugen oeffnen sich nach aussen).
    Reihenhoehe = Halbstein 12.4 + Lagerfuge innen 0.4. Steinzahl pro Reihe so, dass die 12.5 cm breiten Steine
    an der Unterkante innen Platz haben (Stossfuge innen min. 3 mm). Oben ist der Ring enger -> Steine keilfoermig
    zuschneiden (Breite oben). Tuer: Reihen, die unterhalb der Tuerhoehe beginnen, haben eine Luecke von 40 cm."""
    a, c = D_innen / 2, h_innen
    B, H = HALB['w'], HALB['h']
    FI, FS = 0.4, 0.3                                 # Lagerfuge innen, Stossfuge innen (min.)
    pts = ellipse_arc(a, c)
    L = pts[-1][1]
    def pos(sv):
        th = theta_at(pts, sv)
        return th, a * math.cos(th), c * math.sin(th)
    def avail(r, tuer):
        u = 2 * math.pi * r
        if tuer:
            u -= 2 * math.asin(min(1.0, (tuer_b / 2) / r)) * r
        return u
    reihen, s0, total = [], 0.0, 0
    while s0 + H <= L - 6:
        th0, r0, z0 = pos(s0)
        th1, r1, z1 = pos(s0 + H)
        thm, rm, zm = pos(s0 + H / 2)
        neigung = math.degrees(math.atan2(zm / c ** 2, rm / a ** 2))
        tuer = z0 < tuer_h - 1
        n = math.floor(avail(r0, tuer) / (B + FS))
        b_oben = avail(r1, tuer) / n - FS
        fuge_unten = avail(r0, tuer) / n - B
        abzug = round((2 * math.pi * r0 - avail(r0, tuer)) / (B + FS)) if tuer else 0
        reihen.append(dict(reihe=len(reihen) + 1, s_von=round(s0, 1), z_innen_von=round(z0, 1), z_innen_bis=round(z1, 1),
                           r_innen=round(rm, 1), r_unten=round(r0, 1), r_oben=round(r1, 1), neigung_grad=round(neigung, 1),
                           halbsteine=n, tuerabzug=abzug, tuer=tuer, breite_oben=round(min(B, b_oben), 1),
                           zuschnitt_seite=round(max(0.0, (B - b_oben) / 2), 1), fuge_unten=round(fuge_unten, 1)))
        total += n
        s0 += H + FI
    rest = L - s0
    th_r, r_rest, z_rest = pos(s0)
    schluss = 4                                       # 4 Viertelkreis-Stuecke (je 1 Halbstein)
    total += schluss
    e = math.sqrt(1 - (c / a) ** 2) if c < a else 0.0
    A_full = 2 * math.pi * a ** 2 + (math.pi * c ** 2 / e) * math.log((1 + e) / (1 - e)) if e > 0 else 4 * math.pi * a ** 2
    A_half = A_full / 2 / 1e4
    A_tuer = tuer_b * tuer_h / 1e4
    halbe_flaeche = (A_half - A_tuer) / ((B + FS) * (H + FI) / 1e4)
    return dict(D=D_innen, h=h_innen, meridian_cm=round(L, 1), reihen=reihen, schluss_halbsteine=schluss,
                rest_bogen_cm=round(rest, 1), rest_radius_cm=round(r_rest, 1), rest_z_cm=round(z_rest, 1),
                halbsteine_reihen=total, kontrolle_flaeche_m2=round(A_half, 3), halbsteine_flaechenkontrolle=round(halbe_flaeche, 1))


def flaeche_union(cx, cy, R, xl, xr, y0, y1, step=0.5):
    n = 0
    y = 0.25
    while y < SOCKEL_T:
        x = 0.25
        while x < SOCKEL_B:
            if (x - cx) ** 2 + (y - cy) ** 2 <= R * R or (xl <= x <= xr and y0 <= y <= y1):
                n += 1
            x += step
        y += step
    return n * step * step / 1e4                    # m2


def variante(D, h, cy=None):
    a = D / 2
    lagen = max(4, round((0.63 * h + FUGE) / (STREIFEN['d'] + FUGE)))   # Tuerhoehe ~63 % der Kuppelhoehe (neapolitanisch)
    tuer_h = lagen * STREIFEN['d'] + (lagen - 1) * FUGE
    k = kuppel(D, h, tuer_h=tuer_h)
    halbe = k['halbsteine_reihen']
    halbe_mit_verschnitt = math.ceil(halbe * 1.10)
    nf_kuppel = math.ceil(halbe_mit_verschnitt / 2)
    # Lage: Kuppel mittig in x, so weit hinten wie moeglich (Aussenkante >= 5 cm vom Rand)
    R_aussen = a + HALB['t'] + DAEMM_KUPPEL + PUTZ
    if cy is None:
        cy = R_aussen + 5.6
    cx = SOCKEL_B / 2
    R_boden = a + HALB['t']
    halb_tunnel = TUNNEL_INNEN_B / 2 + TUNNEL_W      # Tunnelwand 10 cm (Plattenstreifen)
    y_tuer = cy + math.sqrt(a ** 2 - (TUNNEL_INNEN_B / 2) ** 2)
    tunnel_laenge = SOCKEL_T - y_tuer                # an der Tuerkante gemessen
    # Tunnelwaende: je 6 Lagen Plattenstreifen 500 x 100 x 40 (1 Streifen pro Lage, an Kuppelrundung angepasst)
    y_wand_aussen = cy + math.sqrt(max(a ** 2 - halb_tunnel ** 2, 0))
    wandlaenge_mittel = SOCKEL_T - (y_tuer + y_wand_aussen) / 2
    streifen = 2 * lagen
    platten_tunnelwand = math.ceil(streifen / 2)        # 2 Streifen pro Platte
    nf_tunnel = 0
    # Boden
    A_boden = flaeche_union(cx, cy, R_boden, cx - halb_tunnel, cx + halb_tunnel, cy, SOCKEL_T)
    platten_boden = math.ceil(A_boden / (PLATTE['l'] * PLATTE['b'] / 1e4) * 1.15)
    platten_tunneldecke = 2
    platten_tunnel = platten_tunneldecke + platten_tunnelwand
    # Moertel (Schamott): Fugenvolumen
    v_halb = (HALB['w'] * HALB['t'] + HALB['h'] * HALB['t']) * FUGE          # cm3 pro Halbstein
    v_streifen = (STREIFEN['l'] * STREIFEN['b'] + STREIFEN['b'] * STREIFEN['d']) * FUGE   # cm3 pro Streifen
    v_platten = platten_tunneldecke * 2 * (PLATTE['b'] * NF['b']) * 1.0      # Auflager 1 cm
    v_moertel_l = (halbe * v_halb + streifen * v_streifen + v_platten) / 1000
    kg_moertel = v_moertel_l * 1.6 * 1.30                                       # 1.6 kg Trockenmoertel/l, +30 % Verlust
    # Perlit-Zement
    A_daemm_boden = flaeche_union(cx, cy, R_boden + 5, cx - halb_tunnel - 5, cx + halb_tunnel + 5, cy, SOCKEL_T)
    V_boden = A_daemm_boden * DAEMM_BODEN / 100
    a1, c1 = a + HALB['t'], h + HALB['t']
    a2, c2 = a1 + DAEMM_KUPPEL, c1 + DAEMM_KUPPEL
    V_kuppel = (2 / 3) * math.pi * (a2 ** 2 * c2 - a1 ** 2 * c1) / 1e6
    V_tunneldecke = (2 * halb_tunnel) * tunnel_laenge * DAEMM_KUPPEL / 1e6
    # Fassung 5: Daemmring am Kuppelfuss (unter Bodenniveau bis auf die Herdplatte) + Tunnelseiten
    R_iso, R_bd = a1 + DAEMM_KUPPEL, a1 + 5
    V_fussring = (math.pi * (R_iso ** 2 - R_bd ** 2) * (DAEMM_BODEN + 4.5) + math.pi * (R_bd ** 2 - a1 ** 2) * 4.5) / 1e6
    V_tunnelseiten = 2 * DAEMM_KUPPEL * (tuer_h + 4 + DAEMM_BODEN + 4.5) * tunnel_laenge / 1e6
    V_perlit_mix = V_boden + V_kuppel + V_tunneldecke + V_fussring + V_tunnelseiten
    perlit_l = V_perlit_mix * 1000 * 1.10
    zement_perlit_kg = perlit_l / 5 * 1.3
    # Aussenputz
    a3, c3 = a2 + PUTZ / 2, c2 + PUTZ / 2
    e3 = math.sqrt(1 - (c3 / a3) ** 2) if c3 < a3 else 0
    A3 = (2 * math.pi * a3 ** 2 + (math.pi * c3 ** 2 / e3) * math.log((1 + e3) / (1 - e3))) / 2 / 1e4 if e3 else 2 * math.pi * a3 ** 2 / 1e4
    A_putz = A3 + 0.45                                                    # + Tunnel/Front ca. 0.45 m2
    V_putz = A_putz * PUTZ / 100 * 1.1
    zement_putz = V_putz * 350
    sand_putz_m3 = V_putz * 1.25
    return dict(D=D, h=h, cy=round(cy, 1), kuppel=k, tunnel_lagen=lagen, tuer_h=round(tuer_h, 1), tuer_anteil=round(tuer_h / h, 2), halbsteine_mit_verschnitt=halbe_mit_verschnitt,
                nf_kuppel=nf_kuppel, nf_tunnel=nf_tunnel, nf_total=nf_kuppel + nf_tunnel,
                y_tuer=round(y_tuer, 1), tunnel_laenge=round(tunnel_laenge, 1),
                boden_m2=round(A_boden, 3), platten_boden=platten_boden, platten_tunnel=platten_tunnel, streifen=streifen, wandlaenge_mittel=round(wandlaenge_mittel, 1), platten_total=platten_boden + platten_tunnel,
                moertel_liter=round(v_moertel_l, 1), moertel_kg=round(kg_moertel, 1),
                perlit_mix_m3=dict(boden=round(V_boden, 3), kuppel=round(V_kuppel, 3), tunnel=round(V_tunneldecke, 3), fussring=round(V_fussring, 3), tunnelseiten=round(V_tunnelseiten, 3), total=round(V_perlit_mix, 3)),
                perlit_l=round(perlit_l), zement_perlit_kg=round(zement_perlit_kg, 1),
                putz_m2=round(A_putz, 2), putz_m3=round(V_putz, 3), zement_putz_kg=round(zement_putz, 1), sand_putz_m3=round(sand_putz_m3, 3),
                R_aussen=round(R_aussen, 1), aussendurchmesser=round(2 * R_aussen, 1),
                masse_kuppel_kg=round(halbe * NF['kg'] / 2, 1), masse_boden_kg=round(platten_boden / 1.15 * PLATTE['kg'], 1))


def unterbau():
    fund = 1.5 * 1.5 * 0.15
    wandlaenge = SOCKEL_B + 2 * (SOCKEL_T - WAND)          # U-Form, vorne offen
    wandflaeche = wandlaenge / 100 * 0.75                   # 3 Lagen a 25 cm
    fuell = wandflaeche * 0.121                             # 121 l/m2 Fuellbeton (KANN-Datenblatt, Schalungsstein 24 cm)
    herd = 1.5 * 1.5 * 0.10
    beton = (fund + fuell + herd) * 1.05
    steine_pro_lage = SOCKEL_B / 50 + 2 * (SOCKEL_T - WAND) / 50
    kies_verdichtet = 1.7 * 1.7 * 0.15                     # Fassung 5: Kieskoffer 15 cm (Aushub -25 bis -10)
    return dict(fundament_m3=round(fund, 4), wandlaenge_cm=wandlaenge, wandflaeche_m2=round(wandflaeche, 3),
                fuellbeton_m3=round(fuell, 3), herdplatte_m3=herd, beton_total_m3=round(beton, 3),
                zement_beton_kg=round(beton * 300, 1), betonkies_kg=round(beton * 1900),
                betonkies_m3_lose=round(beton * 1900 / 1800, 3),
                steine_pro_lage=round(steine_pro_lage, 2), steine_3_lagen=round(3 * steine_pro_lage, 1),
                kies_verdichtet_m3=round(kies_verdichtet, 3), kies_lose_m3=round(kies_verdichtet * 1.25, 3),
                kies_kg=round(kies_verdichtet * 1.25 * 1600))


if __name__ == '__main__':
    out = {}
    for D, h, cy in [(80, 36, 73.4), (90, 40, None), (100, 44, None)]:
        out[f'D{D}'] = variante(D, h, cy)
    out['unterbau'] = unterbau()
    json.dump(out, open('ergebnis.json', 'w'), indent=1, ensure_ascii=False)
    for key in ['D80', 'D90', 'D100']:
        v = out[key]; k = v['kuppel']
        print(f"\n=== Kuppel {v['D']} cm innen, {v['h']} cm hoch ===")
        print(f"Meridianlaenge innen {k['meridian_cm']} cm, Reihen {len(k['reihen'])}, Restbogen {k['rest_bogen_cm']} cm, Restoeffnung r {k['rest_radius_cm']} ab z {k['rest_z_cm']} -> Schluss {k['schluss_halbsteine']} Stuecke")
        for r in k['reihen']:
            print(f"  Reihe {r['reihe']}: z {r['z_innen_von']:5.1f}-{r['z_innen_bis']:5.1f} cm, r unten {r['r_unten']:5.1f} oben {r['r_oben']:5.1f}, Lagerfuge {r['neigung_grad']:5.1f} Grad, {r['halbsteine']} Halbsteine{' + Tuer' if r['tuer'] else ''}, Breite oben {r['breite_oben']} (je Seite {r['zuschnitt_seite']} weg), Stossfuge unten {r['fuge_unten']}")
        print(f"Halbsteine Reihen+Schluss: {k['halbsteine_reihen']} | Flaechenkontrolle: {k['halbsteine_flaechenkontrolle']} | +10% -> {v['halbsteine_mit_verschnitt']} -> NF Kuppel {v['nf_kuppel']}")
        print(f"NF Tunnel {v['nf_tunnel']} | NF total {v['nf_total']} | Boden {v['boden_m2']} m2 -> Platten {v['platten_boden']} + 2 Tunneldecke")
        print(f"Moertel {v['moertel_liter']} l -> {v['moertel_kg']} kg | Perlit {v['perlit_l']} l, Zement Perlit {v['zement_perlit_kg']} kg | Putz {v['putz_m2']} m2, {v['putz_m3']} m3")
        print(f"Aussendurchmesser {v['aussendurchmesser']} cm, Kuppelmasse {v['masse_kuppel_kg']} kg, Bodenmasse {v['masse_boden_kg']} kg, Tuerlinie y={v['y_tuer']} Tunnel {v['tunnel_laenge']} cm, cy={v['cy']}")
    print('\n=== Unterbau ===')
    for kk, vv in out['unterbau'].items():
        print(f'  {kk}: {vv}')
