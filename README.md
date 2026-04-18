# 🗾 九州 AI 旅遊規劃

這是一個基於 **Streamlit** 開發的互動式數位旅遊手冊，整合了 AI 視覺藝廊、互動式地圖以及客製化的餐點點餐建議，專門為九州 4 天 3 夜行程所設計。

## 🔗 線上展示

可以在此體驗應用程式：  
👉 **[https://gai-group5-midterm.streamlit.app/](https://gai-group5-midterm.streamlit.app/)**

## 🚀 快速啟動指南

請依照以下步驟在您的本機電腦上執行此應用程式：

### 1. 安裝環境需求

確保您的電腦已安裝 Python，接著打開終端機 (Terminal / PowerShell) 並安裝所需的套件：

```bash
pip install streamlit pandas pydeck
```

### 2. 準備必要檔案

請確認您的專案目錄中包含以下關鍵檔案，程式才能正常運作：

- `app.py`: 主程式邏輯
- `map_internal.csv`: 行程座標與詳細資料
- `itinerary_map.kml`: 供下載的地圖路徑檔
- `all.png` / `day1_new.png`...: 各類 AI 生成的視覺圖片
- `itenerary_new.png`: 行程總覽表
- `example.jpg`: 屋台點餐建議參考菜單

### 3. 執行應用程式

在終端機輸入以下指令：

```bash
streamlit run app.py
```

執行後，程式會自動在瀏覽器中開啟 (`http://localhost:8501`)，即可開始體驗。

---

## ✨ 核心特色

- **📅 詳細行程細節**：動態展示每日行程、通車時間與景點地圖連結。
- **🖼️ AI 視覺藝廊**：展示由 AI 生成的虛擬日系場景，提升旅遊儀式感。
- **🗺️ 互動數位地圖**：整合 Google My Maps，即時查看路線顏色與定點標記。
- **🍱 餐點品項推薦**：提供中洲屋台「零剩食」點餐策略，包含營養與永續分析。

---
*祝您在九州有一段美好的旅程！* 🍂
