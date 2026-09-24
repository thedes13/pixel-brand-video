"""從 Mixkit（免費授權）列出／下載背景音樂與音效。只用標準函式庫。
用法（都在專案根目錄執行）：
  python scripts/fetch_mixkit.py music-list technology        # 列出音樂：ID 曲名 曲風 作者 長度
  python scripts/fetch_mixkit.py sfx-list click               # 列出音效：ID 名稱（tag 例：click whoosh technology digital notification interface futuristic sci-fi impact）
  python scripts/fetch_mixkit.py get-music 623                # 下載到 audio/raw/bgm_623.mp3
  python scripts/fetch_mixkit.py get-sfx 2356 2580 2568       # 下載到 audio/sfx/<id>.mp3
下載前請先讀 references/licensing.md，並確認 Mixkit 授權條款仍適用。
"""
import sys, re, json, html, os, urllib.request

UA = {"User-Agent": "Mozilla/5.0"}

def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "ignore")

def music_list(tag):
    page = get("https://mixkit.co/free-stock-music/tag/%s/" % tag)
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)
    for g in json.loads(m.group(1)).get("@graph", []):
        if g.get("@type") == "ItemList":
            for it in g["itemListElement"]:
                mid = it["url"].rstrip("/").split("/")[-1].replace(".mp3", "")
                print(mid, "|", it["name"], "|", it.get("genre"), "|", it.get("byArtist"), "|", it.get("duration"))

def sfx_list(tag):
    page = get("https://mixkit.co/free-sound-effects/%s/" % tag)
    seen = set()
    for m in re.finditer(r'preview-url-value="[^"]*/sfx/(\d+)/\d+-preview\.mp3".*?item-grid-card__title">\s*([^<]*?)\s*</h2>', page, re.S):
        if m.group(1) not in seen:
            seen.add(m.group(1)); print(m.group(1), "|", html.unescape(m.group(2)))

def save(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "wb").write(get(url, binary=True)); print("saved", path)

if __name__ == "__main__":
    cmd, args = (sys.argv[1] if len(sys.argv) > 1 else ""), sys.argv[2:]
    if cmd == "music-list": music_list(args[0] if args else "technology")
    elif cmd == "sfx-list": sfx_list(args[0] if args else "click")
    elif cmd == "get-music":
        for i in args: save("https://assets.mixkit.co/music/%s/%s.mp3" % (i, i), "audio/raw/bgm_%s.mp3" % i)
    elif cmd == "get-sfx":
        for i in args: save("https://assets.mixkit.co/active_storage/sfx/%s/%s-preview.mp3" % (i, i), "audio/sfx/%s.mp3" % i)
    else: print(__doc__)
