"""Erzeugt die Demo-Aufnahme aus data/script.json mit macOS-Stimmen (say).

Jede Zeile wird als eigene Spur gesprochen (wie eine Mehrspur-Aufnahme in Teams/Zoom).
Ausgabe:
  audio/segments/NNN.wav   einzelne Spuren (16 kHz, mono)
  audio/meeting.wav        alle Spuren hintereinander mit kurzen Pausen
  audio/meeting.m4a        komprimierte Fassung fuer die Webseite
  data/turns.json          Start/Ende jeder Spur in Sekunden
"""
import json
import random
import subprocess
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RATE = 16000
random.seed(7)  # gleiche Pausen bei jedem Lauf

script = json.loads((ROOT / "data/script.json").read_text(encoding="utf-8"))
seg_dir = ROOT / "audio/segments"
seg_dir.mkdir(parents=True, exist_ok=True)

turns, frames_all, t = [], [], 0.0
for i, (sid, text) in enumerate(script["zeilen"]):
    voice = script["sprecher"][sid]["stimme"]
    seg = seg_dir / f"{i:03d}.wav"
    subprocess.run(["say", "-v", voice, "-r", "175", "-o", str(seg),
                    f"--data-format=LEI16@{RATE}", text], check=True)
    with wave.open(str(seg)) as w:
        assert w.getframerate() == RATE and w.getnchannels() == 1
        data = w.readframes(w.getnframes())
    dur = len(data) / 2 / RATE
    pause = round(random.uniform(0.45, 0.9), 2)
    turns.append({"i": i, "sprecher": sid, "start": round(t, 2), "ende": round(t + dur, 2)})
    frames_all.append(data + b"\x00\x00" * int(pause * RATE))
    t += dur + pause

out = ROOT / "audio/meeting.wav"
with wave.open(str(out), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
    w.writeframes(b"".join(frames_all))

subprocess.run(["afconvert", "-f", "m4af", "-d", "aac",
                str(out), str(ROOT / "audio/meeting.m4a")], check=True)
(ROOT / "data/turns.json").write_text(json.dumps(turns, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(turns)} Spuren, Gesamtdauer {t:.1f} s")
