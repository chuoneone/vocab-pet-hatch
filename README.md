# 魔法寵物孵化屋 Skill（vocab-pet-hatch）

貼上英文單字，AI 就幫你做出一個「唸單字餵寵物」的互動網頁。

學生按 🎤 大聲唸單字，瀏覽器聽懂後會丟食物餵蛋。蛋吃一口就變大一點、裂痕變多，吃飽就破蛋孵出可愛寵物，全部孵完有寵物大合照和分數。

## 使用流程

安裝後，貼上單字並告訴 AI：「幫我把這些單字做成寵物孵蛋朗讀網頁。」它會：

1. **整理單字**：補上中文、例句、圖卡 emoji，以及語音辨識容易聽錯的相似字
2. **產生網頁**：輸出一個 HTML 檔，超過 9 個單字會自動分成幾頁
3. **（選用）配插圖**：在 Codex、Antigravity 等能生圖的環境，可以幫每個單字畫插圖

## 特色

- **單一檔案**：寵物圖片都在檔案裡，雙擊就能開，也能直接寄給學生或放上網站
- **不用帳號、不用伺服器**：成績只存在學生自己的瀏覽器，不會上傳
- **唸得越好餵得越多**：唸對餵 3 個、很接近餵 2 個、有開口餵 1 個，唸不好也能繼續玩
- **老師可以放行**：學生唸兩次都沒被聽到，會出現「👩‍🏫 老師確認通過」
- **不用捲動**：筆電與手機都在同一個畫面完成作答
- **看得出弱點**：完成畫面用紅底標出星星較少的單字

## 安裝

### Claude Code

```bash
git clone https://github.com/chuoneone/vocab-pet-hatch ~/.claude/skills/vocab-pet-hatch
```

### Codex／Antigravity 等其他 AI 工具

把整個資料夾放到該工具的 skills 資料夾，或在對話中請它讀 `SKILL.md`。

需要 Python 3 來執行 `scripts/build.py`（不用安裝套件）。

## 不用 AI 也能用

1. 複製 `examples/words-example.json`，改成你的單字
2. 執行：

```bash
python scripts/build.py words.json -o my-words.html
```

3. 用 Chrome 或 Edge 開啟 `my-words.html`

範例成品：`examples/example.html`

## 需要的環境

- **電腦版 Chrome 或 Edge**：才聽得懂學生唸什麼。Safari、iPad 與部分手機只能判斷有沒有出聲。
- 有麥克風。第一次唸時瀏覽器會詢問權限，請按「允許」。
- 直接雙擊檔案通常就能用；麥克風一直被擋時，請放到 https 網站，或在資料夾內執行 `python -m http.server` 再開啟。

## 單字插圖

預設用 emoji 當圖卡，不需要生圖。想要插圖時：

- 在 **Codex** 或 **Antigravity** 裡使用：AI 會用內建的生圖功能
- 在 **Claude Code** 裡使用：電腦有裝 `codex` 或 `agy` 指令時，AI 會呼叫它們生圖

細節見 `references/image-generation.md`。

## 授權

程式碼與圖片皆採 [MIT](LICENSE)：可以自由使用、修改與分享，請保留授權聲明。
