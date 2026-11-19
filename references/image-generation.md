# 幫單字配插圖（選用）

預設的 emoji 圖卡已經能玩。只有使用者想要插圖時才做，**開始前先說明會生幾張圖、大約多久，等使用者同意**。寵物、蛋與背景圖都已附在 skill 裡，不需要再生。

## 先判斷你在哪個環境

| 環境 | 怎麼生圖 |
|---|---|
| Codex（有內建生圖工具） | 直接用你的生圖工具 |
| Antigravity（有 Gemini 生圖） | 直接用你的生圖工具 |
| Claude Code 或其他只能跑指令的環境 | 檢查電腦有沒有裝 `codex` 或 `agy`，有就用下方指令；都沒有就告訴使用者維持 emoji |
| 只能聊天、不能跑指令的環境 | 不生圖，維持 emoji |

不要為了生圖去申請 API 金鑰或付費服務；使用者沒裝工具就用 emoji。

## 圖片規格

- 每個單字一張，正方形，存成 `images/<單字英文，空白換成 -，全小寫>.png`，放在 `words.json` 旁邊。
- 在 `words.json` 對應單字加上 `"image": "images/xxx.png"`（可以保留 `emoji`，找不到圖片時會自動退回 emoji）。
- 腳本會把圖片嵌進網頁；有裝 Pillow 時會自動縮成 320px。

## 提示詞範本

所有單字用同一段風格描述，整組圖才會一致：

```
A cute, simple illustration for a vocabulary flashcard showing "<單字>" (<中文意思>):
<一句具體畫面，例如 a girl telling a story to her friends>.
Soft clay toy style, warm pastel colors, plain cream background, centered subject,
no text, no letters, no words in the image. Square 1:1.
```

- 抽象字要轉成具體情境：without → 一個人看著空空的音樂播放器；exciting → 雲霄飛車上大叫的小孩。
- **圖裡不要有字**，生圖模型常寫錯字，而且會洩漏答案。
- 圖片裡不要有真實人物、品牌或學生資料。

## 用指令呼叫（Claude Code 等環境）

**Codex CLI**（需要已登入 ChatGPT 帳號）：

```bash
codex exec "Generate an image and save it as images/plan.png: <提示詞>"
```

**Antigravity CLI（agy）**：

```bash
agy -p "Generate an image: <提示詞>"
```

- 在一個空的資料夾執行，不要在含有私人檔案的資料夾執行。
- agy 可能不照你指定的檔名存檔，生完要找出新產生的圖片（例如 `~/.gemini/antigravity-cli/` 底下），再複製並改名到 `images/`。
- 一張大約 30～60 秒。逐張生，生完打開圖片檢查：主體對不對、有沒有出現文字。有問題就重生那一張。
- 指令失敗（未登入、額度用完、逾時）時，把錯誤告訴使用者，該單字維持 emoji，不要改用其他付費方式。

## 生完之後

重新執行 `scripts/build.py`，開啟網頁檢查圖卡有沒有正確顯示。
