import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="月底匯率表產生器", layout="wide")

st.title("月底匯率表產生器")
st.write("正式版 v2（台銀歷史匯率）")

currencies = {
    "USD": "USD",
    "CNY": "CNY",
    "HKD": "HKD",
    "GBP": "GBP",
    "AUD": "AUD",
    "CAD": "CAD",
    "SGD": "SGD",
    "CHF": "CHF",
    "JPY": "JPY",
    "ZAR": "ZAR",
    "SEK": "SEK",
    "NZD": "NZD",
    "THB": "THB",
    "PHP": "PHP",
    "IDR": "IDR",
    "EUR": "EUR",
    "KRW": "KRW",
    "VND": "VND",
    "MYR": "MYR"
}

month = st.text_input("請輸入月份（例如：2026-06）", "2026-06")


def fetch_currency_data(currency, month):
    rows = []

    year, mon = month.split("-")

    url = f"https://rate.bot.com.tw/xrt/flcsv/0/{month}/{currency}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
    except Exception as e:
        st.warning(f"{currency} 下載失敗：{e}")
        return pd.DataFrame()



    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("table")

    if table is None:
        st.warning(f"{currency} 找不到台銀資料表")
        return pd.DataFrame()

    df_list = pd.read_html(str(table))
    if not df_list:
        st.warning(f"{currency} 無法解析資料表")
        return pd.DataFrame()

    raw = df_list[0]

    for _, r in raw.iterrows():
        date_value = str(r.iloc[0]).strip()

        if "/" not in date_value:
            continue

        row = {
            "資料日期": date_value,
            "幣別": currency,
            "匯率（本行買入）": "本行買入",
            "現金": r.iloc[1],
            "即期": r.iloc[3],
            "遠期10天": 0,
            "遠期30天": 0,
            "遠期60天": 0,
            "遠期90天": 0,
            "遠期120天": 0,
            "遠期150天": 0,
            "遠期180天": 0,
            "匯率（本行賣出）": "本行賣出",
            "現金_賣出": r.iloc[2],
            "即期_賣出": r.iloc[4],
            "遠期10天_賣出": 0,
            "遠期30天_賣出": 0,
            "遠期60天_賣出": 0,
            "遠期90天_賣出": 0,
            "遠期120天_賣出": 0,
            "遠期150天_賣出": 0,
            "遠期180天_賣出": 0,
        }
        rows.append(row)

    while len(rows) < 30:
        rows.append({
            "資料日期": "",
            "幣別": "",
            "匯率（本行買入）": "",
            "現金": "",
            "即期": "",
            "遠期10天": "",
            "遠期30天": "",
            "遠期60天": "",
            "遠期90天": "",
            "遠期120天": "",
            "遠期150天": "",
            "遠期180天": "",
            "匯率（本行賣出）": "",
            "現金_賣出": "",
            "即期_賣出": "",
            "遠期10天_賣出": "",
            "遠期30天_賣出": "",
            "遠期60天_賣出": "",
            "遠期90天_賣出": "",
            "遠期120天_賣出": "",
            "遠期150天_賣出": "",
            "遠期180天_賣出": "",
        })

    return pd.DataFrame(rows)


if st.button("產生資料"):
    final_df = pd.DataFrame()

    for currency in currencies:
        df = fetch_currency_data(currency, month)
        final_df = pd.concat([final_df, df], ignore_index=True)

    st.success("成功產生匯率表！")
    st.dataframe(final_df)

    csv = final_df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="下載 CSV",
        data=csv,
        file_name=f"{month}_月底匯率表.csv",
        mime="text/csv"
    )
