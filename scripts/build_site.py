"""Buendelt die Demo-Daten fuer die Webseite in docs/ (GitHub Pages).

Eingabe:  data/script.json, data/transcript.json, data/protokoll.json, audio/meeting.m4a
Ausgabe:  docs/data.js (window.DEMO = {...}), docs/meeting.m4a
"""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
load = lambda p: json.loads((ROOT / p).read_text(encoding="utf-8"))

script = load("data/script.json")
demo = {
    "meta": script["meta"],
    "sprecher": script["sprecher"],
    "transcript": [
        {k: t[k] for k in ("i", "sprecher", "start", "ende", "text")} |
        {"unsicher": [w["w"] for w in t["woerter"] if w["p"] < 0.6]}
        for t in load("data/transcript.json")
    ],
    "protokoll": load("data/protokoll.json"),
}
(ROOT / "docs/data.js").write_text(
    "window.DEMO = " + json.dumps(demo, ensure_ascii=False) + ";\n", encoding="utf-8")
shutil.copy(ROOT / "audio/meeting.m4a", ROOT / "docs/meeting.m4a")
print("docs/data.js und docs/meeting.m4a geschrieben")
