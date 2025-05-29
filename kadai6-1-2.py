import requests
import pandas as pd


# 新規就農者調査の統計データをe-Stat APIから取得し、農業に就職した人の年代別人数などを分析・表示する。
# 自分が農業に興味を持っているため、年代別の就農者数を知りたくて作成。

# - APIエンドポイント: https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData
# - 機能: 指定した統計表IDに基づく統計データの取得
# - 取得データ形式: JSON

# ....プログラムの使い方....
# 1. APIキー（APP_ID）を取得し、変数にセットする。
# 2. statsDataIdに任意の統計表IDを指定することで取得対象のデータを選択可能。
#    →今回は「0002110241」（新規就農者調査）を使用。
# 3. パラメータを設定しAPIを呼び出してJSONを取得。
# 4. データ本体を抽出して表形式のDataFrameに変換。
# 5. コード値を意味のある名称に置換して見やすくする。
# 6. 必要に応じて列名も日本語に変更。
# 7. 最終的に年代別の就農者数などを確認できる表を表示。



# 定数：APIキーとURL
API_KEY = "f4d64065649092f863973c568f17b7efdd64e636"
API_ENDPOINT = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

def fetch_stats_data(stats_data_id: str, limit: int = 60) -> dict:
    """
    指定した統計データIDでe-Stat APIから統計データを取得する。
    成功したらJSONデータ（辞書）を返す。失敗時はNoneを返す。
    """
    params = {
        "appId": API_KEY,
        "statsDataId": stats_data_id,
        "metaGetFlg": "Y",
        "cntGetFlg": "N",
        "explanationGetFlg": "Y",
        "annotationGetFlg": "Y",
        "sectionHeaderFlg": "1",
        "replaceSpChars": "0",
        "limit": limit,
        "lang": "J"
    }

    try:
        response = requests.get(API_ENDPOINT, params=params)
        response.raise_for_status()  # HTTPエラーを例外化
        return response.json()
    except requests.RequestException as e:
        print(f"APIリクエスト失敗: {e}")
        return None

def parse_values(data: dict) -> pd.DataFrame:
    """
    JSONデータから統計値の部分を抽出し、PandasのDataFrameに変換する。
    """
    values = data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']
    return pd.DataFrame(values)

def replace_codes_with_names(df: pd.DataFrame, meta_info: list) -> pd.DataFrame:
    """
    DataFrame内のコードを対応する名称に置換する。
    meta_infoはAPIから取得した分類ラベル情報のリスト。
    """
    for class_obj in meta_info:
        column_name = '@' + class_obj['@id']
        id_to_name = {}

        classes = class_obj['CLASS']
        if isinstance(classes, list):
            for c in classes:
                id_to_name[c['@code']] = c['@name']
        else:
            id_to_name[classes['@code']] = classes['@name']

        # 置換処理（辞書を用いてコードを名称に）
        df[column_name] = df[column_name].replace(id_to_name)
    return df

def rename_columns_to_japanese(df: pd.DataFrame, meta_info: list) -> pd.DataFrame:
    """
    DataFrameの列名を日本語に置き換える。
    """
    rename_dict = {'@unit': '単位', '$': '値'}
    for class_obj in meta_info:
        original = '@' + class_obj['@id']
        japanese = class_obj['@name']
        rename_dict[original] = japanese

    df = df.rename(columns=rename_dict)
    return df

def main():
    # 統計表ID（新規就農者調査）
    stats_data_id = "0002110241"

    # APIからデータ取得
    data = fetch_stats_data(stats_data_id)
    if data is None:
        return

    # データ本体をDataFrame化
    df = parse_values(data)

    # メタ情報（コード対応表）を取得
    meta_info = data['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ']

    # コードを名称に置換
    df = replace_codes_with_names(df, meta_info)

    # 列名を日本語に置換
    df = rename_columns_to_japanese(df, meta_info)

    # 結果表示
    print(df)

if __name__ == "__main__":
    main()
