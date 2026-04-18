import pandas as pd

# Define the user's requested data structure
user_data = [
    {"地點名稱": "大濠公園", "分類": "景點", "地址": "福岡県福岡市中央区大濠公園", "停留時間": "1.5小時", "Lat": 33.5847, "Lon": 130.3764, "Day": 1},
    {"地點名稱": "福岡塔", "分類": "景點", "地址": "福岡県福岡市早良区百道浜2丁目3-26", "停留時間": "1小時", "Lat": 33.5933, "Lon": 130.3515, "Day": 1},
    {"地點名稱": "三井LaLaport福岡", "分類": "購物", "地址": "福岡県福岡市博多区那珂6丁目23-1", "停留時間": "2-3小時", "Lat": 33.5623, "Lon": 130.4431, "Day": 1},
    {"地點名稱": "笑樂牛腸鍋博多車站店", "分類": "美食", "地址": "福岡県福岡市博多区博多駅中央街1-1", "停留時間": "晚餐", "Lat": 33.5898, "Lon": 130.4205, "Day": 1},
    {"地點名稱": "柳川遊船", "分類": "景點", "地址": "福岡県柳川市三橋町下百町1-6", "停留時間": "2小時", "Lat": 33.1648, "Lon": 130.4076, "Day": 2},
    {"地點名稱": "太宰府天滿宮", "分類": "景點", "地址": "福岡県太宰府市宰府4丁目7-1", "停留時間": "2小時", "Lat": 33.5215, "Lon": 130.5348, "Day": 2},
    {"地點名稱": "中洲屋台街", "分類": "美食", "地址": "福岡県福岡市博多區中洲1丁目", "停留時間": "晚餐宵夜", "Lat": 33.5915, "Lon": 130.4065, "Day": 2},
    {"地點名稱": "由布院湯之坪街道", "分類": "景點", "地址": "大分県由布市湯布院町川上", "停留時間": "3-4小時", "Lat": 33.2657, "Lon": 131.3618, "Day": 3},
    {"地點名稱": "博多運河城", "分類": "購物", "地址": "福岡県福岡市博多區住吉1丁目2", "停留時間": "晚餐", "Lat": 33.5898, "Lon": 130.4110, "Day": 3},
    {"地點名稱": "高千穗峽集合點", "分類": "交通", "地址": "福岡県福岡市博多區博多駅中央街1-1", "停留時間": "全天", "Lat": 33.5897, "Lon": 130.4208, "Day": 4},
    {"地點名稱": "元祖博多明太重", "分類": "美食", "地址": "福岡県福岡市中央区西中洲6-15", "停留時間": "晚餐", "Lat": 33.5902, "Lon": 130.4031, "Day": 4}
]

df_full = pd.DataFrame(user_data)

# 1. Generate full_itinerary.csv (requested format)
df_clean = df_full[["地點名稱", "分類", "地址", "停留時間"]]
df_clean.to_csv('full_itinerary.csv', index=False, encoding='utf-8-sig')

# 2. Generate itinerary_map.kml (same logic as before)
kml_header = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>九州 AI 旅遊規劃地圖</name>
    <Style id="red_marker">
      <IconStyle><color>ff0000ff</color><scale>1.2</scale><Icon><href>http://maps.google.com/mapfiles/kml/paddle/red-circle.png</href></Icon></IconStyle>
    </Style>
    <Style id="yellow_marker">
      <IconStyle><color>ff00ffff</color><scale>1.2</scale><Icon><href>http://maps.google.com/mapfiles/kml/paddle/ylw-circle.png</href></Icon></IconStyle>
    </Style>
    <Style id="blue_marker">
      <IconStyle><color>ffff0000</color><scale>1.2</scale><Icon><href>http://maps.google.com/mapfiles/kml/paddle/blu-circle.png</href></Icon></IconStyle>
    </Style>
    <Style id="day1_line"><LineStyle><color>7f500050</color><width>4</width></LineStyle></Style>
    <Style id="day2_line"><LineStyle><color>7fed0000</color><width>4</width></LineStyle></Style>
    <Style id="day3_line"><LineStyle><color>7f00ff00</color><width>4</width></LineStyle></Style>
    <Style id="day4_line"><LineStyle><color>7f0000ff</color><width>4</width></LineStyle></Style>
"""

kml_footer = """  </Document>
</kml>
"""

kml_content = ""

for _, row in df_full.iterrows():
    style = "#blue_marker"
    if row['分類'] == '美食': style = "#red_marker"
    elif row['分類'] == '交通': style = "#yellow_marker"
    
    kml_content += f"""    <Placemark>
      <name>{row['地點名稱']}</name>
      <description>{row['地址']} / {row['停留時間']}</description>
      <styleUrl>{style}</styleUrl>
      <Point><coordinates>{row['Lon']},{row['Lat']},0</coordinates></Point>
    </Placemark>
"""

colors = ["#day1_line", "#day2_line", "#day3_line", "#day4_line"]
for day in range(1, 5):
    day_data = df_full[df_full['Day'] == day]
    if not day_data.empty:
        coords = " ".join([f"{r['Lon']},{r['Lat']},0" for _, r in day_data.iterrows()])
        kml_content += f"""    <Placemark>
      <name>Day {day} 路徑</name>
      <styleUrl>{colors[day-1]}</styleUrl>
      <LineString><coordinates>{coords}</coordinates></LineString>
    </Placemark>
"""

with open('itinerary_map.kml', 'w', encoding='utf-8') as f:
    f.write(kml_header + kml_content + kml_footer)

# 3. Save internal data for st.map
df_full.to_csv('map_internal.csv', index=False, encoding='utf-8-sig')

print("All files updated successfully.")
