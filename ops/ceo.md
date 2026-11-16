# 旅遊通｜CEO 營運手冊

## 三大目標與指標
| 目標 | 負責 AG | 北極星指標 | 30 天目標 |
|---|---|---|---|
| 養帳號 | 養號AG | 帳號無警告、每篇觸及穩定成長 | 0 次限流警告、Reels 平均觸及 > 500 |
| 增加粉絲 | 內容AG＋美術AG＋互動AG | IG＋Threads 新增粉絲 | IG 300、Threads 500 |
| 轉換 | 轉換AG | 新增 LINE 好友、私訊→LINE 轉換率 | LINE 好友 100、轉換率 ≥ 20% |

## AG 編制（定義檔：/home/claude/.claude/agents/lyt-*.md）
- 養號AG（lyt-yanghao）：活躍度、限動、追蹤同領域、帳號健康
- 內容AG（lyt-content）：週計畫、Reels 腳本、封面文案、說明文字、Threads 短文
- 美術AG（lyt-visual）：GPT 雜誌封面、Grok 動態影片
- 發佈AG（lyt-publish）：IG／Threads 上架（晚上 19:30–21:00）
- 互動AG（lyt-engage）：留言、回覆、Threads 熱門串
- 轉換AG（lyt-convert）：私訊、精選、LINE 漏斗、網站 CTA
- 數據品管AG（lyt-data）：去 AI 味＋合規審稿、每週數據檢討

## 每日營運（19:00 開始）
1. 數據品管AG：昨天的觸及、粉絲、留言、LINE 新好友 → 寫 ops/daily/日期.md
2. CEO 開會：依數據決定今天重點（觸及低→加強互動；留言多→加強轉換）
3. 內容AG 出稿 → 美術AG 出圖／影片 → 數據品管AG 審稿
4. 發佈AG 19:30 發佈；互動AG 發佈後 60 分鐘內回覆所有留言
5. 養號AG 全天分散執行養號動作
6. CEO 裁決記錄＋排下一天的營運（send_later），用繁體中文回報經紀人

## 每週一
數據品管AG：ig-profile、ig-audit、ig-viral → ops/weekly/；內容AG 用 ig-plan 排下週；CEO 裁決。

## 紅線
不保證理賠、保費一律「預估」、不用他牌商標、不買粉不互粉、不碰帳密、AI 影片開標籤、經紀人本名不公開。

## 只能由經紀人本人做的事
手機端：置頂貼文、IG 連結、精選動態、封存舊文、帳密與驗證碼、真人接 LINE 客人。

## 營運看板（每日必做）
- 看板：https://claude.ai/artifact/XfYQ9MBWsZMSTVcqxdthmo （artifact slug f853c5fd-a353-49f8-83c4-28bd8fa2e8de，只有老闆看得到）
- 原始檔：/home/claude/office/（index.html、data.json、img/）
- 每天營運跑完最後一步：更新 data.json（updated、day、focus、kpi 真實數字、每位成員 status/doing/progress、timeline、next），用 publish_files mode patch 只送 data.json 上去。
- KPI 只填實際查到的數字，查不到寫「—」，不准編。

## 內容方向更新（2026-11-16 經紀人指示）
- IG Reels：改做「搞笑共鳴＋最後反轉到旅平險／旅平卡」，腳本庫在 ig/reels_funny.md，爆款觀察在 /root/.claude/instagram/swipe.md。每週至少 2 支搞笑型，其餘照雜誌封面動態。不要一開頭就講保險。
- Threads：不只純文字，每週 2～3 篇要帶圖或影片（可重用 IG 封面、Reels 影片、手機實拍感照片），其他天發短文。
- 留言安全：照 lyt-engage.md「避免留言被刪」規則；一週被刪 2 次以上要向經紀人提建議。
