# KI-Protokoll mit Belegen · Demo

**Live:** https://hackersmz.github.io/ki-protokoll-demo/

Aus einer Besprechungsaufnahme wird ein Protokoll, in dem jeder Beschluss und jede Aufgabe per Klick auf die Stelle in der Aufnahme verweist.

- Firma und Personen sind erfunden; die Stimmen sind synthetisch (macOS-Sprachausgabe).
- Die Transkription läuft lokal mit Whisper large-v3-turbo (mlx-whisper) – die Aufnahme verlässt den Rechner nicht.
- Der Protokollentwurf wurde von Claude (Anthropic) ausschließlich aus dem Transkript erstellt und anschließend geprüft.

## Ergebnisse dieser Demo

| | |
|---|---|
| Länge der Aufnahme | 3:37 min, 4 Sprecher, 26 Wortbeiträge |
| Transkriptionszeit | 47 s auf einem MacBook (M1 Pro) |
| Hörfehler | 5 bei 476 Wörtern, z. B. „DM50“ statt „DN 50“ |
| Davon vom Modell als unsicher markiert | 0 – deshalb Fachbegriffliste und menschliche Prüfung |

## Selbst nachbauen

Voraussetzung: macOS mit Apple Silicon, Python 3.12.

```bash
python3.12 -m venv .venv && .venv/bin/pip install mlx-whisper
python3 scripts/synth.py              # Aufnahme aus data/script.json erzeugen
.venv/bin/python scripts/transcribe.py  # lokal transkribieren -> data/transcript.json
.venv/bin/python scripts/build_site.py  # Webseite in docs/ aktualisieren
```

Das Protokoll selbst liegt in `data/protokoll.json`; jeder Eintrag verweist über `beleg` auf die Nummer des Wortbeitrags im Transkript.

## Aufbau

```
data/script.json      Drehbuch der fiktiven Besprechung
data/turns.json       Start/Ende jedes Wortbeitrags in der Aufnahme
data/transcript.json  Whisper-Ergebnis mit Wort-Zeitstempeln und Wahrscheinlichkeiten
data/protokoll.json   Protokollentwurf mit Belegen
docs/                 Webseite (GitHub Pages)
```

---

Mingzhe Sun · KI-Umsetzung für den Mittelstand · [LinkedIn](https://www.linkedin.com/in/mingzhe-sun)
