---
name: pixel-brand-video
description: 用 HyperFrames（HTML→MP4）製作 8-bit 像素風品牌／產品宣傳短影片，並用 Mixkit 免費授權的 BGM 與音效經 FFmpeg 混音，輸出含聲音的 MP4 與授權紀錄。內含可直接改字改色的 30 秒 16:9 範本（舊→新對比、核心＋模組、成本對比、Logo 像素化結尾）、吉祥物與 Logo 佔位圖、音效 cue sheet 混音腳本、Mixkit 下載腳本。只要使用者想做品牌宣傳片、產品介紹短片、像素風／8-bit／遊戲感的影片、Reels／Shorts／官網形象影片、影片加配樂或音效、影片混音，或要整理影片用的免費音樂授權紀錄，就使用這個 skill，即使沒有說出 skill 名稱。
---

# 像素風品牌短影片

把「品牌 + 主題 + 重點文字」變成一支有畫面、有配樂音效、授權乾淨的短影片。分兩段：**畫面**（HyperFrames）與**聲音**（Mixkit + FFmpeg）。

## 開始前確認（一次問完，其餘自己決定）
1. 品牌：名稱、Logo 圖（建議透明背景 PNG）、吉祥物圖（可省略）、主色 3～5 個
2. 主題與 3～4 個重點（每個重點對應一個場景）
3. 長度與比例：範本是 30 秒、16:9；其他長度改時間軸，9:16 需要重排版面
4. 聲音：純畫面，或要配樂＋音效

使用者說「不要問我、直接做」時，就用合理預設做完，最後說明假設。

## 範本（`assets/template/index.html`）
30 秒、1920×1080，結構：HUD（世界名／關卡／進度條）→ 場景 A 舊→新對比 → 場景 B 核心＋六個模組 → 場景 C 成本對比 → 結尾 Logo＋標語＋像素化收尾。吉祥物固定右下，關鍵操作時「觸控筆點擊」，換場時跳過像素方塊轉場。

- 搜尋檔案中的 `EDIT:` 註解，改文字、色票（`:root` 的 CSS 變數）、關卡名稱即可
- 場景數量不同時，要同步改 `STAGES`、`.hud-name` 數量、時間軸的 `stage(n, t)` 與 `cover2(...)`
- 場景 A/B/C 是三種可重用的版型（前後對比／中心輻射／數字對比圖表）；內容不適合時，換成別的版型但保留 HUD、轉場、吉祥物的一致語言
- 圖檔放專案根目錄：`logo.png`、`mascot.png`、`logo_px1~3.png`（`python scripts/pixelate_logo.py logo.png` 由 Logo 產生）。`assets/placeholders/` 有佔位圖可先測試

風格原則（為什麼）：像素風要靠「粗黑框＋硬陰影＋方塊裝飾」建立質感，大字只用 3～5 組，其餘留白，觀眾才記得住重點；不要宣稱具體省多少錢或百分比，改用圖表視覺表達。

## 畫面製作步驟
1. 先讀 `/hyperframes` skill（規則以它為準），用 `npx hyperframes init <名稱> --example blank --non-interactive` 建專案
2. 把範本複製成 `index.html`，圖檔放進根目錄，依上面說明改內容
3. `npx hyperframes check`（等同 lint + validate + inspect）→ 全部處理完；裝飾用的巨大數字已標 `data-layout-ignore`
4. `npx hyperframes render --quality draft --output renders/draft.mp4`，用 ffmpeg 每個場景擷一張圖確認版面；沒問題再 `--quality high --output renders/output.mp4`（30 秒約 2 分鐘）
5. 傳給使用者看

踩過的坑：
- 不要 tween `letterSpacing`、`className`、`textContent`（lint 會擋或不生效）；用位移／透明度代替
- 系統字型（如 PMingLiU）要加 `@font-face { src: local(...) }`
- 隨機用 mulberry32 種子，不可 `Math.random()`；動畫都掛在同一條 paused timeline
- 對比度警告：小字用深一點的藍（範本 `#1a4fbf`）

## 聲音製作步驟
詳細授權規則在 `references/licensing.md`，動手前先讀。
1. **分析**：`ffprobe` 取長度／FPS／解析度／是否有音軌；畫面時間以 HTML 時間軸為準，寫 `timeline.md`
2. **選 BGM**：`python scripts/fetch_mixkit.py music-list technology` 列表，挑 110～130 BPM、無人聲、有 build-up 與 drop 的曲子，`get-music <ID>` 下載；用 numpy 自相關估 BPM 與第一拍位置（見 `references/mixing-notes.md`）
3. **選音效**：`sfx-list <tag>`（click、whoosh、technology、digital、notification、interface、futuristic、sci-fi、impact）→ `get-sfx <ID...>`。避開 Mario／紅白機金幣類（arcade coin、retro casino）
4. **確認授權**：Mixkit 的授權全文要用瀏覽器開 `https://mixkit.co/license/` 點 View License 才讀得到（做法見 `references/licensing.md`）。授權不明或下載被擋（登入、Captcha、Cloudflare、403）就放棄該來源換別的，不要繞過
5. **混音**：複製 `assets/audio-pipeline/build_mix.py` 到專案 `audio/`，改「設定」（BGM 檔、BPM、drop 對齊）與「CUE SHEET」，執行 `python audio/build_mix.py && bash ffmpeg_mix.sh`
   - 比例約 80% 現代科技音效 + 20% 8-bit（`syn(blip(...))` 方波 blip、`crunch()` bit-crush 噪音，自己合成，無授權問題）
   - 不要每個動畫都配音；UI 音效略高於 BGM，Impact 明顯但不爆，Logo 最突出
   - 母帶：BGM 降 9.5 dB、被音效 sidechain 壓、兩段式 loudnorm 到 -15 LUFS / TP -1.5、alimiter；結尾淡出＋短 echo 自然收束
6. **寫 `audio/LICENSES.md`**：每個實際用到的素材記錄名稱、作者、來源、網址、License、Commercial、Attribution、下載日期（範本見 `references/licenses-template.md`）
7. **QA（自己做，不要問使用者）**：`ffprobe`（長度與原片一致、解析度、FPS、有音軌）；`ebur128` 看 LUFS 與 true peak；最後 0.1 秒要明顯淡出、無 clipping；分別輸出只有 BGM／只有 SFX 的 stem 比較平衡；擷取關鍵時間點畫面核對音畫同步。有問題自己修

## 交付回報
成品 MP4 路徑、使用的 BGM、主要音效、`LICENSES.md` 路徑、授權注意事項。沒辦法親耳聽就老實說「只做了數據與畫面對位檢查」。

## 環境注意
- Windows：含中文的檔案用 `PYTHONIOENCODING=utf-8`；路徑加引號；ffmpeg 濾鏡過長時用 `-filter_complex_script`（腳本已處理）
- 需要：Node.js 22+、FFmpeg、Python 3（pillow 用於 Logo 像素化、numpy 用於估 BPM）
