"""Transkribiert jede Spur lokal mit Whisper (mlx-whisper, laeuft komplett auf dem Mac).

Eingabe:  audio/segments/NNN.wav, data/turns.json
Ausgabe:  data/transcript.json  (Text + Wort-Zeitstempel + Wort-Wahrscheinlichkeit)

Aufruf:   .venv/bin/python scripts/transcribe.py
"""
import json
import time
import wave
from pathlib import Path

import mlx_whisper
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
MODEL = "mlx-community/whisper-large-v3-turbo"

turns = json.loads((ROOT / "data/turns.json").read_text(encoding="utf-8"))
out, t0 = [], time.time()
for turn in turns:
    # 16-kHz-WAV direkt einlesen (spart die ffmpeg-Abhaengigkeit)
    with wave.open(str(ROOT / f"audio/segments/{turn['i']:03d}.wav")) as w:
        audio = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    r = mlx_whisper.transcribe(audio, path_or_hf_repo=MODEL, language="de",
                               word_timestamps=True, condition_on_previous_text=False)
    woerter = [
        {"w": w["word"].strip(), "start": round(turn["start"] + w["start"], 2),
         "ende": round(turn["start"] + w["end"], 2), "p": round(w["probability"], 3)}
        for s in r["segments"] for w in s.get("words", [])
    ]
    out.append({**turn, "text": r["text"].strip(), "woerter": woerter})
    print(f"[{turn['i']:02d}] {r['text'].strip()[:70]}")

(ROOT / "data/transcript.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"Fertig: {len(out)} Spuren in {time.time() - t0:.0f} s, Modell {MODEL}")
