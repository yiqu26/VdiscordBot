# VdiscordBot 使用說明

這是一個 Discord 機器人，當使用者貼上 IG 或 Bilibili 影片連結時，會自動轉換為可在 Discord 播放的版本。

---

## 🔧 支援功能

| 平台     | 轉換對象                  | 說明 |
|----------|---------------------------|------|
| Instagram | `reel/` 與 `p/` 貼文     | 轉為 `ddinstagram.com`，支援短網址與分享連結 |
| Bilibili  | 原始連結 `/video/`      | 轉為 `vxbilibili.com` |
| Bilibili  | 短連結 `b23.tv`          | 自動展開並轉換 |
| 所有連結 | 清除 URL 中多餘參數      | 保留主體網址，避免網址過長 |

---

## ⚙️ 權限需求

- ✅ Read Message History
- ✅ Send Messages
- ✅ Embed Links
- ✅ Manage Messages（如需刪除使用者原始訊息）

---

## 🧪 使用方式

1. 建立 `.env` 或設定系統變數 `TOKEN=你的 Discord Bot Token`
2. 執行：

```bash
pip install -r requirements.txt
python bot.py
```

---

## 📁 檔案結構

- `bot.py`：主程式
- `README.md`：使用說明文件

---
