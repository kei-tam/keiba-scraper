from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
import time
import csv
from io import StringIO

# ヘッドレスモードで起動
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/chromium"

driver = webdriver.Chrome(
    executable_path="/usr/bin/chromedriver",
    options=chrome_options
)

odds_data_all = []
odds_data_all.append(["日付","レース","レースID","人気","枠","馬番","印","馬名","単勝オッズ","複勝オッズ下限","複勝オッズ上限"])

today = datetime.datetime.today().date()
year = 2025
courses = ["05","09"]
round = "03"
dayround = "05"

for course in courses :
    for r  in range(12):
        race_id = f"{year}{course}{round}{dayround}{r+1:02}"  #例：202505030311　レース番号はゼロパディングして1桁ならば0をつけて２桁にする
        url = f"https://race.sp.netkeiba.com/?pid=odds_view&type=b0&race_id={race_id}"
        
        # 目的のURLを読み込み
        driver.get(url)
        time.sleep(3)  # JavaScriptの読み込み待ち

        data = []

        try:
            table = driver.find_element(By.CSS_SELECTOR, ".RaceOdds_HorseList.Tanfuku.mt18")
            rows = table.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                cell_row = [c.text.strip() for c in cells]

                # 複勝オッズ分割処理
                if len(cell_row) >= 6 and '-' in cell_row[5]:
                    try:
                        low, high = [s.strip() for s in cell_row[5].split('-')]
                        cell_row[5] = low   # 下限を上書き
                        cell_row.append(high)  # 上限を追加
                    except:
                        pass  # 分割に失敗したら無視（例外安全）

                data.append(cell_row)
        except Exception as e:
            print("エラー:", e)
            continue

        if data:
            for d in data:
                odds_data = [today, f"{r+1}R", race_id] + d
                odds_data_all.append(odds_data)
        else:
            print(f"{race_id} のデータ不足のためスキップ")


# CSVデータを文字列として保存
csv_buffer = StringIO()
writer = csv.writer(csv_buffer)
writer.writerows(odds_data_all)

# ファイル名と書き込み
blob = bucket.blob(f"odds_data/{today}.csv")
blob.upload_from_string(csv_buffer.getvalue(), content_type='text/csv')

driver.quit()
print("終了")
