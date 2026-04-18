import streamlit as st
import pandas as pd
from pathlib import Path

# --- PAGE CONFIG ---
st.set_page_config(page_title="九州 AI 旅遊高效規劃", page_icon="🗾", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def get_itinerary():
    try:
        # Use map_internal.csv for app logic as it contains Day, lat, lon
        df = pd.read_csv('map_internal.csv')
        df = df.rename(columns={'Lat': 'lat', 'Lon': 'lon'})
        return df
    except:
        return pd.DataFrame()

df_full = get_itinerary()

# --- HEADER SECTION ---
st.markdown('<div style="text-align: left; padding: 1rem 0;">', unsafe_allow_html=True)
st.title("🍂 九州 AI 旅遊規劃")
st.subheader("核心概念：打造具備「智慧排程」、「飲食控管」與「高質感視覺」的全新旅遊規劃模式")
st.markdown('</div>', unsafe_allow_html=True)

# # --- HERO AREA (IMAGE + COLORFUL MAP) ---
# if Path("all.png").exists():
#     # 調整欄位比例，讓地圖所在的欄位變窄 (1.5:1)
#     col_img, col_map = st.columns([1.5, 1])
#     with col_img:
#         st.image("all.png", width=350, caption="九州 AI 繪製封面")
#     with col_map:
#         if not df_full.empty:
#             st.markdown("### 🗺️ 福岡景點探索")
#             import pydeck as pdk
            
#             # 使用不需要 Token 的開源彩色風格 (Voyager)
#             st.pydeck_chart(pdk.Deck(
#                 map_style='https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json', 
#                 initial_view_state=pdk.ViewState(
#                     latitude=df_full['lat'].mean(),
#                     longitude=df_full['lon'].mean(),
#                     zoom=10,
#                     pitch=0,
#                 ),
#                 height=200, 
#                 layers=[
#                     pdk.Layer(
#                         'ScatterplotLayer',
#                         data=df_full,
#                         get_position='[lon, lat]',
#                         get_color='[255, 0, 0, 200]', # Bright Red for pins
#                         get_radius=300,
#                         pickable=True
#                     ),
#                 ],
#                 tooltip={"text": "{地點名稱}\n分類: {分類}"}
#             ), use_container_width=True)

st.markdown("---")

# --- MAIN CONTENT TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["📅 詳細行程細節", "🖼️ AI 視覺藝廊", "🗺️ 互動數位地圖", "🍱 餐點品項推薦"])

with tab1:
    st.markdown('<h2 style="color: #ffaa00;">九州行程總覽與細節</h2>', unsafe_allow_html=True)
    
    # Split into two columns as requested: Image left, Text Itinerary right
    tab1_col_img, tab1_col_text = st.columns([1.2, 1])
    
    with tab1_col_img:
        if Path("itenerary_new.png").exists():
            st.image("itenerary_new.png", caption="KYUSHU TOUR OVERVIEW", width='stretch')
    
    with tab1_col_text:
        st.markdown("### 🗒️ 每日行程安排")
        
        # 恢復區域性的日期選擇器
        day_selection_t1 = st.selectbox("選擇查看日期", ["第一天", "第二天", "第三天", "第四天"], key="tab1_day")
        day_num_t1 = {"第一天": 1, "第二天": 2, "第三天": 3, "第四天": 4}[day_selection_t1]
        
        current_day_df = df_full[df_full['Day'] == day_num_t1]
        
        if current_day_df.empty:
            st.warning("尚無此日期的行程資料。")
        else:
            for _, r in current_day_df.iterrows():
                icon = "📍" if r['分類'] == '景點' else "🍴" if r['分類'] == '美食' else "🚩"
                st.markdown(f"{icon} **[{r['地點名稱']}](https://www.google.com/maps/search/?api=1&query={r['lat']},{r['lon']})**")
                # Show travel time if it exists
                if '通車時間' in r and pd.notna(r['通車時間']):
                    st.caption(f"🚌 {r['通車時間']}")
                st.write(f"  └ {r['地址']}")
                st.caption(f"  停留時間：{r['停留時間']}")

with tab2:
    st.markdown("## 🖼️ AI 視覺藝廊")
    # 加入藝廊專用的天數選擇器
    gallery_day = st.radio("選擇要查看的天數：", ["第一天", "第二天", "第三天", "第四天"], horizontal=True, key="tab2_day")
    
    # 定義圖片資料映射
    gallery_data = {
        "第一天": ("day1_new.png", "Day 1: 福岡風情 - 都市與鋼彈的融合"),
        "第二天": ("day2_new.png", "Day 2: 柳川之美 - 西鐵文化與水鄉漫遊"),
        "第三天": ("day3_new.png", "Day 3: 由布院慢步 - 溫泉小鎮的寧靜"),
        "第四天": ("day4_new.png", "Day 4: 高千穗秘境 - 神話之鄉的壯闊")
    }
    
    img_path, img_caption = gallery_data.get(gallery_day, (None, None))
    
    if img_path and Path(img_path).exists():
        st.image(img_path, caption=img_caption, width='stretch')
    else:
        st.warning(f"目前尚無 {gallery_day} 的圖片素材。")

with tab3:
    st.markdown("## 🗺️ 互動數位地圖")
    
    # --- 美化後的圖例說明區塊 ---
    st.markdown("""
    <div style="background-color: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; margin-bottom: 20px; border-left: 6px solid #4285F4;">
        <h4 style="margin-top: 0; color: #4285F4;">ℹ️ 地圖圖例</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <p style="font-weight: bold; margin-bottom: 10px;">📍 定點標記</p>
                <ul style="list-style: none; padding: 0; font-size: 0.95rem;">
                    <li style="margin-bottom: 5px;"><span style="color: #FF0000; font-size: 1.2rem;">●</span> <b>紅色</b>：必吃美食餐廳</li>
                    <li style="margin-bottom: 5px;"><span style="color: #FFFF00; font-size: 1.2rem;">●</span> <b>黃色</b>：Klook / 交通集合點</li>
                    <li style="margin-bottom: 5px;"><span style="color: #4285F4; font-size: 1.2rem;">●</span> <b>藍色</b>：一般觀光景點</li>
                </ul>
            </div>
            <div>
                <p style="font-weight: bold; margin-bottom: 10px;">🛣️ 路線顏色</p>
                <ul style="list-style: none; padding: 0; font-size: 0.95rem;">
                    <li style="margin-bottom: 5px;"><span style="color: #7f007f; font-weight: bold;">▬</span> <b>紫色</b>：第一天行程路徑</li>
                    <li style="margin-bottom: 5px;"><span style="color: #007aff; font-weight: bold;">▬</span> <b>藍色</b>：第二天行程路徑</li>
                    <li style="margin-bottom: 5px;"><span style="color: #34c759; font-weight: bold;">▬</span> <b>綠色</b>：第三天行程路徑</li>
                    <li style="margin-bottom: 5px;"><span style="color: #ff3b30; font-weight: bold;">▬</span> <b>紅色</b>：第四天行程路徑</li>
                </ul>
            </div>
        </div>
        <p style="font-size: 0.8rem; color: #888; margin-top: 10px;">※ 路線與座標均依據行程順序標示，點擊地圖中的圖示可查看詳細資訊。</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Keep the user's provided Iframe here as a 100% reliable backup
    map_html = '<iframe src="https://www.google.com/maps/d/u/0/embed?mid=1ky2nFWjXYt12xuniqzW0fbIno-ILWTc&ehbc=2E312F" width="100%" height="600"></iframe>'
    st.components.v1.html(map_html, height=620)

with tab4:
    st.markdown("## 🍢 中洲屋台客製化點餐建議")
    st.info("💡 針對兩位旅客量身打造的：零剩食・完美 8 分飽方案")
    
    # --- Part 1: Overeating Warning ---
    st.markdown("""
    <div style="background-color: rgba(255, 75, 75, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid #FF4B4B; margin-bottom: 20px;">
        <h4 style="color: #FF4B4B; margin-top: 0;">⚠️ 【過量警告】高熱量組合風險</h4>
        <p style="font-size: 0.95rem; margin-bottom: 0;">
            屋台料理多為重口味與高碳水化合物。若兩位旅客各自點一碗「長濱豚骨拉麵」，再加上「牛舌」或「牛腹肉牛排」等大份量肉類，極高機率會過飽並造成剩餘浪費。
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- Part 2: Layout: Image & Recommendations ---
    col_menu, col_advice = st.columns([1, 1.2])
    
    with col_menu:
        if Path("example.jpg").exists():
            st.image("example.jpg", caption="屋台風味菜單參考 (example.jpg)", use_container_width=True)
            st.markdown("""
            > **營養平衡建議**：目前菜單單品多偏向肉類與澱粉。為增加纖維量並解膩，系統已預選「關東煮拼盤」中的大根來平衡飽足感。
            """)
    
    with col_advice:
        st.markdown("### 🍃 完美 8 分飽點餐建議")
        
        st.markdown("""
        1. **長浜豚骨ラーメン (長濱豚骨拉麵)**  
           `¥1,000 × 1 碗`  
           *🧑‍⚕️ 營養師點評：兩人分食剛好品嚐口味道，避免攝取過量碳水化合物。*
        
        2. **おでん盛り合わせ (關東煮拼盤)**  
           `¥1,200 × 1 盤`  
           *🧑‍⚕️ 營養師點評：包含大根、玉子與魚漿製品。提供優質蛋白與纖維，中和濃郁湯頭。*
        
        3. **焼き鳥 お好み4本セット (烤鳥串 4 支套餐)**  
           `¥1,200 × 1 份`  
           *🚩 導遊點評：建議從菜單右上方選明太子豬五花、雞皮等，份量精準適中。*
        """)
        
        st.warning("💡 **貼心提醒**：本店有「每人低消 1 杯飲料與 1 道餐點」限制。以上方案已達食物低消，請記得再各點 1 杯飲品喔！")

    # --- Part 3: Metrics & Feedback ---
    st.markdown("---")
    m1, m2 = st.columns(2)
    with m1:
        st.metric("📊 總熱量估算 (每人)", "約 600 kcal", delta="達成 8 分飽目標", delta_color="normal")
    with m2:
        st.metric("🌍 永續指標", "100% 完食", delta="實踐零剩食旅遊", delta_color="normal")
    
    st.success("✨ 採「共享小份」策略，不僅能品嚐多元口味，更能實踐永續旅遊目標！")
    
    

# with tab5:
#     st.markdown("## 📦 旅遊數據下載")
#     d1, d2 = st.columns(2)
#     with d1:
#         if Path("itinerary_map.kml").exists():
#             with open("itinerary_map.kml", "rb") as f:
#                 st.download_button("📥 下載 KML 地圖檔", f, file_name="itinerary_map.kml")
#         if Path("attreaction.csv").exists():
#             with open("attreaction.csv", "rb") as f:
#                 st.download_button("📥 下載行程資料 CSV", f, file_name="attreaction.csv")
#     with d2:
#         st.markdown("### 🔗 交通參考連結")
#         st.markdown("- [JR 九州官網](https://train.yoyaku.jrkyushu.co.jp/)")

# st.markdown("---")
