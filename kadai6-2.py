import requests
import pandas as pd

# OpenWeatherMap用のAPIキー
APP_ID = "b17dfaab66f9ca5e5953afd04ad7fa94"

# エンドポイント（現在の天気）
API_URL = "https://api.openweathermap.org/data/2.5/weather"

# 対象都市（日本国内）
cities = [
    "Sapporo", "Kushiro", "Sendai", "Niigata", "Tokyo",
    "Kanazawa", "Hiroshima", "Nagoya", "Osaka",
    "Kochi", "Fukushima", "Kagoshima", "Naha"
]


# 結果を格納するリスト
weather_data = []

# 各都市についてループでデータを取得
for city in cities:
    params = {
        "q": f"{city},JP",
        "appid": APP_ID,
        "units": "metric",  # 摂氏
        "lang": "ja"
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        city_name = data["name"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        weather = data["weather"][0]["description"]

        weather_data.append({
            "地域": city_name,
            "最低気温(°C)": temp_min,
            "最高気温(°C)": temp_max,
            "天気": weather
        })

    except requests.RequestException as e:
        print(f"Failed to get data for {city}: {e}")
        weather_data.append({
            "地域": city,
            "最低気温(°C)": "Error",
            "最高気温(°C)": "Error",
            "天気": "Error"
        })

# DataFrame表示
df = pd.DataFrame(weather_data)
print(df)