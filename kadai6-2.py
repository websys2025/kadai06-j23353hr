import requests
import pandas as pd

# 参照するオープンデータ：OpenWeatherMap API
# 名称：OpenWeatherMap API（https://openweathermap.org/api）
# 概要：世界中の天気情報（現在・予報・過去）を提供するオープンAPI。

# エンドポイント：
#   ・https://api.openweathermap.org/data/2.5/weather
#   ・現在の天気情報を都市名・緯度経度・郵便番号などで取得できる。

# 機能：
#   ・気温（現在・最低・最高）、湿度、天気、風速などの取得。
#   ・「units=metric」で摂氏（°C）に変換。
#   ・「lang=ja」で日本語の天気説明を取得。

# 使い方：
#   ・APIキー（appid）を取得して、q=都市名,JPを指定してGETリクエスト。
#   ・天気情報はJSONで返される。


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
