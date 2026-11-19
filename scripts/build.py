#!/usr/bin/env python3
"""把單字資料（JSON）套進寵物孵化屋模板，輸出單一獨立 HTML。

用法：
    python scripts/build.py words.json -o pet-hatch.html

- 只用 Python 標準函式庫，不需要安裝套件。
- 寵物、蛋、背景圖片會直接嵌進 HTML，產出的檔案可以單獨寄給學生或放上任何網站。
- 單字超過 9 個時，自動拆成多個檔案（-1.html、-2.html…），每個檔案最多 9 顆蛋。
"""
import argparse
import base64
import json
import math
import mimetypes
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "assets" / "template.html"
PET_DIR = SKILL_DIR / "assets" / "pets"
PET_KEYS = ["shiba", "calico", "bunny", "hedgehog", "chick", "owl", "corgi", "red-panda", "penguin"]
MAX_WORDS = len(PET_KEYS)
PLACEHOLDER = "/*__GAME_DATA__*/null"
CJK = re.compile(r"[぀-ヿ㐀-鿿豈-﫿가-힯]")

mimetypes.add_type("image/webp", ".webp")


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def check_words(words):
    errors = []
    for n, w in enumerate(words, 1):
        word = str(w.get("en") or w.get("word") or "").strip()
        if not word:
            errors.append(f"第 {n} 個字詞缺少要唸的內容（\"word\" 或 \"en\"）")
        elif not CJK.search(word) and not str(w.get("zh", "")).strip():
            errors.append(f"第 {n} 個字詞（{word}）缺少中文意思 \"zh\"")
        if w.get("sent") and "<mark>" not in w["sent"]:
            errors.append(f"第 {n} 個字詞（{word}）的例句沒有用 <mark> 標出字詞")
    return errors


def build_page(template: str, data: dict, words: list) -> str:
    images = {"egg": data_uri(PET_DIR / "egg.webp"), "bg": data_uri(PET_DIR / "bg.webp")}
    for key in PET_KEYS[: len(words)]:
        images[key] = data_uri(PET_DIR / f"{key}.webp")
    game = {k: v for k, v in data.items() if k != "words"}
    game["words"] = words
    game["images"] = images
    payload = json.dumps(game, ensure_ascii=False).replace("</", "<\\/")
    title = data.get("title", "魔法寵物孵化屋") + ("：" + data["subtitle"] if data.get("subtitle") else "")
    html = template.replace(PLACEHOLDER, payload, 1)
    return html.replace("__PAGE_TITLE__", title.replace("<", "&lt;"), 1)


def main():
    for stream in (sys.stdout, sys.stderr):  # Windows 終端機預設編碼會讓中文變亂碼
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap =argparse.ArgumentParser(description="產生魔法寵物孵化屋單字朗讀網頁")
    ap.add_argument("words_json", help="單字資料 JSON 檔")
    ap.add_argument("-o", "--output", default="pet-hatch.html", help="輸出的 HTML 檔名")
    args = ap.parse_args()

    src = Path(args.words_json)
    data = json.loads(src.read_text(encoding="utf-8"))
    words = data.get("words") or []
    if not words:
        sys.exit("錯誤：JSON 裡沒有 words。")
    errors = check_words(words)
    if errors:
        sys.exit("資料有問題：\n- " + "\n- ".join(errors))

    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        sys.exit("錯誤：模板裡找不到資料位置，模板可能被改壞了。")

    out = Path(args.output)
    groups = math.ceil(len(words) / MAX_WORDS)
    size = math.ceil(len(words) / groups)  # 平均分組，避免最後一組只剩一兩個字
    written = []
    for g in range(groups):
        chunk = [dict(w) for w in words[g * size:(g + 1) * size]]
        page = dict(data)
        if groups > 1:
            page["subtitle"] = (data.get("subtitle", "") + f" 第 {g + 1} 組").strip()
            page["id"] = (data.get("id") or data.get("title", "")) + f"#{g + 1}"
            target = out.with_name(f"{out.stem}-{g + 1}{out.suffix}")
        else:
            target = out
        target.write_text(build_page(template, page, chunk), encoding="utf-8")
        written.append(target)

    for t in written:
        print(f"完成：{t}（{t.stat().st_size // 1024} KB）")


if __name__ == "__main__":
    main()
