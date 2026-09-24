# 素材授權：Mixkit（本 skill 預設來源）

> 本文整理自 Mixkit 網站授權頁（2026-09-24 讀取），**不是法律意見**，條款可能更新。使用前請自行到 https://mixkit.co/license/ 再確認一次。

## Stock Music Free License（背景音樂）
- 商業與非商業專案皆可免費使用，**不需署名**
- 允許：Podcast、社群媒體影片、線上行銷廣告、教育用途、YouTube 影片（*若收到版權申訴，把詳情寄給 team@mixkit.co 由 Mixkit 協助）；可在任何網站／社群平台下載、複製、修改、散布與公開播放
- **不允許**：CD／DVD、電視與廣播、電玩遊戲；不可重混成純音樂曲目；不可宣稱是自己的創作；不可登記到任何版權管理服務（例如 YouTube Content ID）

## Sound Effects Free License（音效）
- 商業與非商業專案皆可免費使用，**不需署名**
- 可用於 YouTube、社群、廣告、電影、電視／廣播、電玩、DVD 等；可修改、散布、公開播放
- **不允許**：單獨轉售或轉散布音效本身；放進工具／模板／原始檔案包散布；宣稱是自己的創作；登記到版權管理服務

## 對這個 skill 的實際影響
1. **只交付成品 MP4。** `audio/raw/`、`audio/sfx/` 的原檔僅供內部混音，不要放進公開 repo、模板或素材包（本專案的 `.gitignore` 已排除）。
2. **不要把 BGM 登記到 Content ID。** 若影片放 YouTube 又被第三方誤判，依授權寄信給 Mixkit。
3. **BGM 不可用於電視／廣播、遊戲。** 要投放電視廣告請改用他曲或另購授權。
4. 剪輯、變速、EQ、淡出、ducking 都屬「修改」，允許；但不要把音樂做成「純音樂混音曲」。

## 讀取授權全文的方法（授權文字在彈窗裡，靜態 HTML 抓不到）
用瀏覽器開 `https://mixkit.co/license/`，在頁面執行：
```js
document.querySelectorAll('[data-license="musicFree"]').forEach(b => b.click());   // 音樂；音效改 "sfxFree"
await new Promise(r => setTimeout(r, 800));
document.querySelector('dialog,[role=dialog],[class*=modal]').innerText
```

## 授權不確定時
不要用。換另一個來源或另一首曲子。也不要用：YouTube 轉 MP3、來源不明音樂、標示 Personal Use Only 的素材、有明顯 Content ID 風險的來源。

## 其他免費來源（本 skill 沒有自動化，使用前要各自確認授權）
Pixabay Music／Sound Effects 等其他來源，本 skill 沒有測試過。若下載時遇到登入、Captcha、Cloudflare 等阻擋，直接放棄該來源、換別的，不要嘗試繞過。
