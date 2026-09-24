"""估計 BGM 的 BPM、第一拍位置與每小節能量（找 drop 用）。
用法：python scripts/estimate_bpm.py audio/raw/bgm_623.mp3
輸出：bpm（0.25 精度）、第一個 kick 的秒數（BEAT_OFFSET）、每小節 RMS（數字突然變大的小節 = drop）
需求：pip install numpy；ffmpeg 在 PATH。
"""
import sys, subprocess
import numpy as np

def load(path, lowpass=None):
    af = ["-af", "lowpass=f=%d" % lowpass] if lowpass else []
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path] + af + ["-ac", "1", "-ar", "11025", "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)

path = sys.argv[1]
fs = 11025
x_low = load(path, 140)          # 低頻 = kick，拿來抓拍點
x = load(path)
hop = 64; f = fs / hop
n = len(x_low) // hop
e = np.abs(x_low[: n * hop]).reshape(n, hop).mean(1)
o = np.maximum(np.diff(e), 0)
best = (0, 0, 0)
for bpm in np.arange(90, 141, 0.25):
    per = f * 60 / bpm
    for ph in np.arange(0, per, 0.5):
        idx = (ph + np.arange(0, int((len(o) - ph) / per)) * per).astype(int)
        sc = o[idx].sum()
        if sc > best[0]: best = (sc, bpm, ph / f)
_, bpm, offset = best
print("BPM ~ %.2f   BEAT_OFFSET ~ %.3f s" % (bpm, offset))
bar = 4 * 60 / bpm
rms = [np.sqrt((x[int((offset + i * bar) * fs): int((offset + (i + 1) * bar) * fs)] ** 2).mean()) for i in range(int((len(x) / fs - offset) / bar))]
print("bar length %.3f s; RMS per bar (x10) - a sudden jump = the drop:" % bar)
print(" ".join("%d:%.1f" % (i, r * 10) for i, r in enumerate(rms)))
