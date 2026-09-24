"""pixel-brand-video 混音腳本：產生 audio/mix_filter.txt 與 ffmpeg_mix.sh（BGM 剪輯 + 音效 cue sheet + sidechain + 母帶）。
用法（專案根目錄）：
  1. python scripts/fetch_mixkit.py get-music <ID> ; python scripts/fetch_mixkit.py get-sfx <ID...>
  2. 修改下面「設定」與「CUE SHEET」（秒數 = 影片時間；對照 index.html 最下方的時間軸）
  3. python audio/build_mix.py && bash ffmpeg_mix.sh      -> output_esdesign_sound.mp4 / mix_audio.wav
需求：ffmpeg。音效 ID 都是 Mixkit 免費音效（授權見 references/licensing.md）。
"""
import math, os

AUDIO = os.path.dirname(os.path.abspath(__file__))       # .../audio
ROOT = os.path.dirname(AUDIO)                            # 專案根目錄
VIDEO = "renders/output.mp4"        # 設定：你渲染出來的無聲影片（相對專案根目錄）
OUT = "output_esdesign_sound.mp4"   # 設定：最終輸出檔名
DUR = 30.0                          # 設定：影片秒數
BGM_FILE = "audio/raw/bgm_623.mp3"  # 設定：BGM 檔（範例：Mixkit「Deep Urban」）

# ---- BGM 剪輯：讓原曲的 drop 對齊影片主要轉折 ----
BPM_SRC = 124.0            # 原曲 BPM（用 numpy 自相關估，或看曲目資訊）
BEAT_OFFSET = 0.131        # 原曲第一個 kick 的秒數
BPM_OUT = 128.0            # 變速後 BPM（±3% 內聽不出差異；用來讓小節數剛好填滿影片）
BARS_BEFORE_DROP = 4       # 影片開頭到 drop 之間放幾小節的 build-up
DROP_BAR = 8               # 原曲 drop 出現在第幾小節（從 0 算）
bar_src = 4 * 60.0 / BPM_SRC
bar_out = 4 * 60.0 / BPM_OUT
BGM_SS = BEAT_OFFSET + (DROP_BAR - BARS_BEFORE_DROP) * bar_src   # 從原曲哪一秒開始取
BGM_TEMPO = BPM_OUT / BPM_SRC                                    # atempo 倍率
BGM_LEN = DUR * BGM_TEMPO + 1.0                                  # 取多長（變速前；變速後 = BGM_LEN / BGM_TEMPO ≥ DUR）
DROP = BARS_BEFORE_DROP * bar_out                                # drop 在影片的第幾秒（本範例 7.5）
BGM_GAIN_DB = -9.5         # BGM 基礎音量：讓音效比它高一點
FADE_OUT_AT = DUR - 2.4    # BGM 開始淡出的秒數

SFX = {}
def sfx(i):
    SFX.setdefault(i, len(SFX) + 1)  # input 0 是 BGM
    return i

events = []
def ev(f, t, g=-12, pk=0.0, ss=0.0, d=None, st=0.0, fi=0.005, fo=0.05, pan=0.0, rev=False, echo=False):
    """f=音效ID  t=該音效「峰值」要落在的影片秒數  g=增益dB  pk=峰值在檔案內的秒數  ss/d=裁切起點/長度
    st=升降半音  fi/fo=淡入/淡出秒  pan=-1..1  rev=倒轉  echo=加短回音"""
    events.append(dict(f=f, t=t, g=g, pk=pk, ss=ss, d=d, st=st, fi=fi, fo=fo, pan=pan, rev=rev, echo=echo))

def syn(expr, dur, t, g=-18, st=0.0, fo=0.05, pan=0.0):
    events.append(dict(syn=expr, dur=dur, t=t, g=g, st=st, fo=fo, pan=pan))

def blip(f0, f1, dur, k=22):
    """8-bit 方波 blip（自己合成，無授權問題）：頻率 f0→f1，k 越大衰減越快"""
    return ("aevalsrc='0.45*sgn(sin(2*PI*(%g*t+(%g-%g)*t*t/(2*%g))))*exp(-t*%g)':d=%g:s=48000" % (f0, f1, f0, dur, k, dur))

def crunch(dur):
    """極輕的 bit-crush 噪音，用在像素方塊轉場"""
    return "anoisesrc=d=%g:c=white:a=0.5:s=48000,acrusher=bits=4:mix=1:samples=10,lowpass=f=4500" % dur

# ================= CUE SHEET（對應 assets/template/index.html 的時間軸；換內容時改這裡）=================
# --- 場景 A：舊 → 新（0–7s）
syn(blip(330, 660, 0.16), 0.16, 0.50, g=-15, pan=0.2)                    # 吉祥物出現：8-bit blip
ev(sfx(2356), 0.55, g=-9)                                                # pixel pop
for k, t in enumerate([1.0, 1.5, 2.0]):                                  # 三個痛點貼紙（低音量、音高下降）
    ev(sfx(2569), t + 0.05, g=-17, d=0.30, st=-2 - 2 * k, pan=[-0.3, 0.3, 0][k])
ev(sfx(2580), 3.02, g=-9)                                                # 觸控筆點擊
ev(sfx(2631), 3.15, g=-11, pk=0.25, d=0.8)                               # 掃描換新
ev(sfx(3124), 3.92, g=-11, d=0.4)                                        # 標籤落下
# --- 轉場 → B（7.0）
syn(crunch(0.45), 0.45, 6.75, g=-27, fo=0.25)                            # 像素轉場（極輕）
ev(sfx(1490), 7.0, g=-13, pk=0.55, d=1.2)                                # soft whoosh
ev(sfx(2634), DROP, g=-11, pk=1.45, d=1.8, fo=0.03)                      # riser 衝向 drop
ev(sfx(2600), DROP + 0.05, g=-11, pk=0.55, d=1.6)                        # power up
ev(sfx(2303), DROP, g=-5, d=1.3, fo=0.5)                                 # drop 低頻 impact
ev(sfx(2580), 7.92, g=-11, st=-2)                                        # 點擊
for k in range(6):                                                       # 六個模組依序接上（音高遞增）
    ev(sfx(2568), 8.22 + k * 0.28, g=-13, st=k * 1.5, pan=-0.3 if k % 2 == 0 else 0.3)
ev(sfx(3122), 10.2, g=-13, pk=0.75, d=2.4, fo=0.5)                       # 資料流
ev(sfx(2133), 9.0, g=-24, ss=0.5, d=4.0, fi=0.6, fo=1.0)                 # 低音量科技底噪
for k, t in enumerate([10.2, 11.2, 12.2]):
    ev(sfx(2519), t, g=-17, st=[0, 3, 7][k], d=0.4, pan=[-0.3, 0.3, 0][k])   # digital pulse
# --- 轉場 → C（14.5）
syn(crunch(0.45), 0.45, 14.25, g=-27, fo=0.25)
ev(sfx(3114), 14.5, g=-13, pk=0.3, d=0.9)
ev(sfx(1030), 14.35, g=-20, d=0.28)                                      # 極輕 glitch
for k in range(4):                                                       # 四項費用
    ev(sfx(2568), 14.95 + k * 0.25, g=-13, st=k * 2, d=0.15, pan=-0.3)
for k in range(19):                                                      # 累計數字跳動：漸強 tick
    ev(sfx(2568), 15.1 + k * 0.115, g=-24 + k * 0.2, st=-8 + k * 0.6, d=0.12, pan=0.35)
ev(sfx(2580), 18.02, g=-12)                                              # 點擊
ev(sfx(2577), 18.10, g=-6, d=0.4, fo=0.1)                                # 按下切換按鈕
ev(sfx(2859), 18.24, g=-12, d=0.6, fo=0.2)                               # 切換到新方案
ev(sfx(2634), 18.5, g=-15, pk=0.9, d=1.6, rev=True, fo=0.3)              # 成本下降：倒轉 riser = 下滑掃頻
ev(sfx(3005), 18.55, g=-15, st=2)                                        # 圖表出現
ev(sfx(2568), 18.95, g=-16, st=-5, pan=-0.3)                             # 線條繪製
ev(sfx(2568), 19.35, g=-16, st=-9, pan=0.3)
# --- 轉場 → 結尾（22.5）
syn(crunch(0.45), 0.45, 22.25, g=-25, fo=0.25)
ev(sfx(2634), 22.55, g=-11, pk=1.45, d=1.7, fo=0.03)                     # 鋪陳 Logo 出場
ev(sfx(2303), 22.8, g=-6, d=1.3, fo=0.5)                                 # Logo impact
ev(sfx(2350), 22.85, g=-10, pk=0.25, d=1.8, fo=0.8)                      # sparkle
ev(sfx(3108), 23.05, g=-8, pk=0.25, d=1.5, fo=0.6)                       # 短 chime
for k in range(4):                                                       # 標籤四聲 pop（音高遞增）
    ev(sfx(3005), 23.95 + k * 0.16, g=-19, st=k * 3, pan=-0.3 + k * 0.2)
ev(sfx(3116), 24.85, g=-13, d=1.0)                                       # 標語
ev(sfx(2577), 26.52, g=-9, d=0.35)                                       # 吉祥物點擊
for k, (t, f0, f1) in enumerate([(27.0, 330, 330), (27.2, 440, 440), (27.4, 660, 880)]):   # Logo 三段像素化
    syn(blip(f0, f1, 0.13, k=16), 0.13, t, g=-13)
ev(sfx(2303), 27.4, g=-9, d=1.0, fo=0.5)                                 # 最終 thump
ev(sfx(2870), 27.42, g=-9, d=0.6, fo=0.3, echo=True)                     # success chime
ev(sfx(3108), 27.43, g=-9, pk=0.25, d=1.1, fo=0.6, echo=True)            # chime 尾巴（在淡出下收束）

# ================= build filter graph =================
inputs = ["-i", BGM_FILE]
for i, idx in sorted(SFX.items(), key=lambda kv: kv[1]):
    inputs += ["-i", "audio/sfx/%s.mp3" % i]

lines = []
labels = []
for n, e in enumerate(events):
    lab = "e%d" % n
    delay_t = e["t"]
    if "syn" in e:
        chain = e["syn"]
        st = e.get("st", 0)
        chain += ",aformat=sample_fmts=fltp:channel_layouts=stereo"
        chain += ",afade=t=in:d=0.003,afade=t=out:st=%.3f:d=%.3f" % (max(e["dur"] - e["fo"], 0), e["fo"])
        chain += ",volume=%gdB" % e["g"]
        start = delay_t
    else:
        src = "[%d:a]" % SFX[e["f"]]
        parts = []
        trim = "atrim=start=%.3f" % e["ss"]
        if e["d"]:
            trim += ":duration=%.3f" % e["d"]
        parts.append(trim)
        parts.append("asetpts=PTS-STARTPTS")
        parts.append("aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo")
        if e["rev"]:
            parts.append("areverse")
        if e["st"]:
            r = 2 ** (e["st"] / 12.0)
            parts.append("asetrate=%d,aresample=48000" % round(48000 * r))
        dur = e["d"] or 1.0
        if e["st"]:
            dur = dur / (2 ** (e["st"] / 12.0))
        parts.append("afade=t=in:d=%.3f" % e["fi"])
        parts.append("afade=t=out:st=%.3f:d=%.3f" % (max(dur - e["fo"], 0), e["fo"]))
        if e["echo"]:
            parts.append("aecho=0.8:0.6:90|180:0.35|0.2")
        parts.append("volume=%gdB" % e["g"])
        chain = src + ",".join(parts)
        start = delay_t - e["pk"] / (2 ** (e["st"] / 12.0))
    if e["pan"]:
        p = e["pan"]
        l, r = (1.0 - max(p, 0) * 0.8), (1.0 + min(p, 0) * 0.8)
        chain += ",pan=stereo|c0=%.2f*c0|c1=%.2f*c1" % (l, r)
    ms = max(int(round(start * 1000)), 0)
    chain += ",adelay=%d|%d" % (ms, ms)
    if "syn" in e:
        lines.append("%s[%s]" % (chain, lab))
    else:
        lines.append("%s[%s]" % (chain, lab))
    labels.append("[%s]" % lab)

# SFX bus
lines.append("%samix=inputs=%d:normalize=0:duration=longest,alimiter=limit=0.9:level=false,volume=0dB,apad=whole_dur=%g[sfxbus]" % ("".join(labels), len(labels), DUR))   # 補靜音到影片長度，否則 sidechain 會提早結束
lines.append("[sfxbus]asplit=2[sfxA][sfxSC]")

# BGM edit
bgm = ("[0:a]atrim=start=%.3f:duration=%.3f,asetpts=PTS-STARTPTS,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
       "atempo=%.4f,atrim=duration=%.2f,"
       "equalizer=f=3000:t=q:w=1.0:g=-2.5,equalizer=f=250:t=q:w=1.0:g=-1.5,"
       "volume='if(lt(t,%.3f),0.67,1)':eval=frame,"          # intro ~3.5 dB lower
       "volume=%gdB,"
       "afade=t=in:st=0:d=0.5,afade=t=out:st=%.2f:d=2.4:curve=qsin[bgm0]" % (BGM_SS, BGM_LEN, BGM_TEMPO, DUR, DROP, BGM_GAIN_DB, FADE_OUT_AT))
lines.append(bgm)
lines.append("[bgm0][sfxSC]sidechaincompress=threshold=0.03:ratio=3.5:attack=8:release=280:makeup=1[bgmd]")
lines.append("[bgmd][sfxA]amix=inputs=2:normalize=0:duration=longest,atrim=duration=%.2f,asetpts=PTS-STARTPTS[mix]" % DUR)

with open(os.path.join(AUDIO, "mix_filter.txt"), "w", encoding="utf-8") as f:
    f.write(";\n".join(lines))

sh = r"""#!/usr/bin/env bash
# pixel-brand-video - audio mix + final MP4 (run from the project root)
set -euo pipefail
VIDEO="%(video)s"
OUT="%(out)s"
INPUTS=(%(inputs)s)

# 1) build premaster (float WAV) from mix_filter.txt (BGM edit + %(n)d timed cues + sidechain ducking)
ffmpeg -y -v error "${INPUTS[@]}" -filter_complex_script audio/mix_filter.txt -map "[mix]" -ar 48000 -c:a pcm_f32le audio/premaster.wav

# 2) two-pass loudness normalisation (I=-15 LUFS, TP=-1.5 dBTP) + safety limiter
STATS=$(ffmpeg -hide_banner -nostats -i audio/premaster.wav -af loudnorm=I=-15:TP=-1.5:LRA=9:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g() { echo "$STATS" | grep "\"$1\"" | sed -E 's/.*: "([^"]+)".*/\1/'; }
ffmpeg -y -v error -i audio/premaster.wav -af "loudnorm=I=-15:TP=-1.5:LRA=9:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,alimiter=limit=0.89:level=false,aresample=48000" -c:a pcm_s16le mix_audio.wav

# 3) mux with the original picture (re-encode H.264 CRF 22, AAC 160k, faststart)
ffmpeg -y -v error -i "$VIDEO" -i mix_audio.wav -map 0:v:0 -map 1:a:0 -c:v libx264 -preset slow -crf 22 -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -ar 48000 -movflags +faststart -shortest "$OUT"
echo "done -> $OUT"
""" % dict(out=OUT, video=VIDEO, inputs=" ".join('"%s"' % x if x.startswith("audio") else x for x in inputs), n=len(events))
with open(os.path.join(ROOT, "ffmpeg_mix.sh"), "w", encoding="utf-8", newline="\n") as f:
    f.write(sh)
print("events:", len(events), "inputs:", len(inputs) // 2)
