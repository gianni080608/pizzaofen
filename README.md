# Pizzaofen Würenlos

Bau- und Beschaffungsplan für einen gemauerten Kuppelofen (neapolitanischer Stil, Ø 80 cm innen, Fassung 3) im Garten in Würenlos AG. Entstanden als Teil einer schulischen Vertiefungsarbeit, Stand 13.10.2026.

| Datei | Inhalt |
|---|---|
| [`dokument/Bauplan_Pizzaofen.md`](dokument/Bauplan_Pizzaofen.md) (+ `.html`, `.pdf`) | Vollständiges Dokument mit allen 10 Punkten: Varianten, Stückliste, Zeichnungen, Route, Transport, Zoll, Bauanleitung, Werkzeug, Recht, Budget |
| [`karte.html`](karte.html) | Abholkarte: Route, Stopps, Ladeliste je Fahrt, Navigation (Google Maps), Phasen Sockel/Ofen, Nutzlast-Rechner |
| [`einkaufsliste.html`](einkaufsliste.html) / [`einkaufsliste.pdf`](einkaufsliste.pdf) | Einkaufsliste zum Abhaken, nach Fahrten gruppiert (Handy) |
| [`zeichnungen/`](zeichnungen/) | Frontansicht, Schnitt A–A, Draufsicht, Kuppelschnitt mit Steinreihen (SVG + PNG) |
| [`berechnung/`](berechnung/) | Python-Skripte für alle Mengen, Gewichte, Kosten, Phasen und Varianten |
| [`karte/`](karte/) | Grundkarte (OSM, OSRM) und Generator für `karte.html` |

**Ergebnis (Fassung 3):** Variante B (Selbstbau Ø 80 cm), CHF 1'961.80 alles inklusive (Material, Kleinmaterial, Schutz, Werkzeug), Lagerbestand aller 39 OBI-Positionen live geprüft, ca. 5.1 t Material in 7 Fahrten à max. 900 kg. Einkauf in zwei Phasen: **Phase 1 Sockel** (Fahrten A, B, K1–K4, CHF 1'282.25, davon CHF 388.95 knappe Ofen-Teile vorgezogen) und **Phase 2 Ofen** (Fahrt C am Mo 19.10., CHF 679.55).

## Neu berechnen

```bash
cd berechnung && python3 berechnung.py && python3 stueckliste.py && python3 varianten_und_zoll.py && python3 obi_bestand.py
cd ../zeichnungen && python3 zeichnungen.py
cd ../dokument && python3 build.py && python3 gen_einkaufsliste.py && python3 gen_bauplan_html.py
cd ../karte && python3 basemap.py cache && python3 gen_karte.py
```

Vor jeder Fahrt `python3 berechnung/obi_bestand.py` (aus dem Ordner `berechnung`) laufen lassen: prüft den OBI-Lagerbestand live.

Preise wurden am 13.10.2026 bei den Händlern abgerufen und können sich ändern. Quellen siehe Anhang A im Dokument.
