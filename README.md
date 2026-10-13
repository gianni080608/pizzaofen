# Pizzaofen Würenlos

Bau- und Beschaffungsplan für einen gemauerten Kuppelofen (neapolitanischer Stil, Ø 80 cm innen, Fassung 2) im Garten in Würenlos AG. Entstanden als Teil einer schulischen Vertiefungsarbeit, Stand 13.10.2026.

| Datei | Inhalt |
|---|---|
| [`dokument/Bauplan_Pizzaofen.md`](dokument/Bauplan_Pizzaofen.md) (+ `.html`, `.pdf`) | Vollständiges Dokument mit allen 10 Punkten: Varianten, Stückliste, Zeichnungen, Route, Transport, Zoll, Bauanleitung, Werkzeug, Recht, Budget |
| [`einkaufsliste.html`](einkaufsliste.html) / [`einkaufsliste.pdf`](einkaufsliste.pdf) | Einkaufsliste zum Abhaken, nach Fahrten gruppiert (Handy) |
| [`zeichnungen/`](zeichnungen/) | Frontansicht, Schnitt A–A, Draufsicht, Kuppelschnitt mit Steinreihen (SVG + PNG) |
| [`berechnung/`](berechnung/) | Python-Skripte für alle Mengen, Gewichte, Kosten und Varianten |

**Ergebnis (Fassung 2):** Variante B (Selbstbau Ø 80 cm), CHF 1'961.80 alles inklusive (Material, Kleinmaterial, Schutz, Werkzeug), Lagerbestand aller 39 OBI-Positionen live geprüft, ca. 5.1 t Material in 6 Fahrten à max. 900 kg.

## Neu berechnen

```bash
cd berechnung && python3 berechnung.py && python3 stueckliste.py && python3 varianten_und_zoll.py && python3 obi_bestand.py
cd ../zeichnungen && python3 zeichnungen.py
cd ../dokument && python3 build.py && python3 gen_einkaufsliste.py && python3 gen_bauplan_html.py
```

Vor jeder Fahrt `python3 berechnung/obi_bestand.py` (aus dem Ordner `berechnung`) laufen lassen: prüft den OBI-Lagerbestand live.

Preise wurden am 13.10.2026 bei den Händlern abgerufen und können sich ändern. Quellen siehe Anhang A im Dokument.
