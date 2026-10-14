# Pizzaofen Würenlos

Bau- und Beschaffungsplan für einen gemauerten Kuppelofen (neapolitanischer Stil, Ø 80 cm innen, Fassung 4) im Garten in Würenlos AG. Entstanden als Teil einer schulischen Vertiefungsarbeit, Stand 14.10.2026.

| Datei | Inhalt |
|---|---|
| [`dokument/Bauplan_Pizzaofen.md`](dokument/Bauplan_Pizzaofen.md) (+ `.html`, `.pdf`) | **Bauanleitung Fassung 4**: Stand Material, Terminplan nach neuer Wetterprognose, Mischungen, 17 Bauschritte mit Kontrollen, 19 Zeichnungen |
| [`zeichnungen/Zeichnungsmappe_A4.pdf`](zeichnungen/Zeichnungsmappe_A4.pdf) | Alle 19 Werkzeichnungen und Skizzen, je eine A4-Seite quer, zum Ausdrucken für die Baustelle |
| [`dokument/archiv/`](dokument/archiv/) | Fassung 3 (Bau- und Beschaffungsplan mit Varianten, Route, Zoll, Recht) |
| [`karte.html`](karte.html) | Abholkarte: Route, Stopps, Ladeliste je Fahrt, Navigation (Google Maps), Phasen Sockel/Ofen, Nutzlast-Rechner |
| [`einkaufsliste.html`](einkaufsliste.html) / [`einkaufsliste.pdf`](einkaufsliste.pdf) | Einkaufsliste zum Abhaken, nach Fahrten gruppiert (Handy) |
| [`zeichnungen/`](zeichnungen/) | `zeichnungen.py` (Ansicht, Schnitt, Draufsicht, Kuppelschnitt) und `cad.py` (Lageplan, Fundament, Sockel-Verlegeplan, Herdplattenschalung, Bodendämmung, Backboden-Zuschnitt, Schablone, Kuppel Reihe 1, Eingang, Zuschnitt, Tür, Detail, Isometrien) |
| [`berechnung/`](berechnung/) | Python-Skripte für alle Mengen, Gewichte, Kosten, Phasen und Varianten |
| [`karte/`](karte/) | Grundkarte (OSM, OSRM) und Generator für `karte.html` |

**Ergebnis Fassung 4 (14.10.):** Einkäufe B und C erledigt, der alte Kies unter den Gartenplatten wird wiederverwendet, Kosten CHF 1'604.35 bis 1'730.30. Bau: Fundament Do 15.10., Sockel Fr 16.10., Herdplatte Mo 19.10., Kuppel So 25.10.

**Ergebnis Fassung 3:** Variante B (Selbstbau Ø 80 cm), CHF 1'961.80 alles inklusive (Material, Kleinmaterial, Schutz, Werkzeug), Lagerbestand aller 39 OBI-Positionen live geprüft, ca. 5.1 t Material in 7 Fahrten à max. 900 kg. Einkauf in zwei Phasen: **Phase 1 Sockel** (Fahrten A, B, K1–K4, CHF 1'282.25, davon CHF 388.95 knappe Ofen-Teile vorgezogen) und **Phase 2 Ofen** (Fahrt C am Mo 19.10., CHF 679.55).

## Neu berechnen

```bash
cd berechnung && python3 berechnung.py && python3 stueckliste.py && python3 varianten_und_zoll.py && python3 obi_bestand.py
cd ../zeichnungen && python3 zeichnungen.py && python3 cad.py
cd ../dokument && python3 build_v4.py && python3 gen_einkaufsliste.py && python3 gen_bauplan_html.py
cd ../karte && python3 basemap.py cache && python3 gen_karte.py
```

Vor jeder Fahrt `python3 berechnung/obi_bestand.py` (aus dem Ordner `berechnung`) laufen lassen: prüft den OBI-Lagerbestand live.

Preise wurden am 13.10.2026 bei den Händlern abgerufen und können sich ändern. Quellen siehe Anhang A im Dokument.
