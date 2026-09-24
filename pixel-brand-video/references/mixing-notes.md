# 混音筆記（為什麼這樣做）

## 選曲與對拍
- 目標 110～130 BPM、無人聲、有「build-up → drop」結構。`python scripts/estimate_bpm.py <mp3>` 會印出 BPM、第一拍位置（BEAT_OFFSET）與每小節能量，能量突然變大的小節就是 drop。
- 影片的最大轉折（本範例是「核心＋模組」場景進場）放在 drop：`BARS_BEFORE_DROP` 決定開頭放幾小節 build-up。
- 為了讓整數小節剛好填滿影片，把 BPM 變速 ≤ 3%（124 → 128）；用 `atempo` 聽不出差異。30 秒 @128 BPM = 16 小節。

## 音效 cue sheet 的寫法
- `ev(id, t, ...)` 的 `t` 是**音效峰值**要落在的影片秒數；`pk` 是峰值在音效檔內的位置，腳本會自動往前推起點。用 RMS 包絡找峰值（每 0.25 秒一格）。
- 一連串相似事件（模組接上、數字跳動、標籤 pop）用迴圈，逐次 `st=+n` 半音、`g` 漸強，聽起來才有「往上」的感覺；成本下降類用負半音、倒轉（`rev=True`）riser。
- 聲音層次：低頻 impact 只給 2～4 個關鍵時刻；UI tick 很輕；轉場用「極輕 bit-crush 噪音 + soft whoosh」，glitch 一律很小聲。
- 不要每個動畫都配音，留白讓關鍵音效有份量。

## 母帶與避免踩雷
- 全部音效先合成一條 SFX bus，再當 sidechain 訊號壓 BGM（ratio 3.5、attack 8 ms、release 280 ms）。
- **SFX bus 必須 `apad` 到影片長度**（腳本已處理）：sidechaincompress 輸出長度是兩條輸入的較短者，最後一個音效若早於影片結尾，整條混音會被截短、結尾不會淡出。
- BGM 變速前要取 `DUR × tempo + 1` 秒（不是除）；否則音樂不夠長。
- 兩段式 loudnorm（I=-15、TP=-1.5、線性）+ alimiter；混音後檢查：`ebur128` 的 LUFS 與 true peak、最後 0.1 秒 RMS（應 < -35 dBFS）。
- 判斷平衡：輸出「只有 BGM」與「只有 SFX」兩個 stem，看 LUFS；音效應略高於 BGM。
