import pandas as pd
import streamlit as st
from datetime import datetime
import calendar

st.set_page_config(page_title="月底匯率表產生器", layout="wide")

st.title("月底匯率表產生器")
st.write("正式版 v1")

currencies = [
    "USD", "CNY", "HKD", "GBP", "AUD", "CAD", "SGD", "CHF", "JPY",
    "ZAR", "SEK", "NZD", "THB", "PHP", "IDR", "EUR", "KRW", "VND", "MYR"
]

month = st.text_input("請輸入月份（例如：2026-06）", "2026-06")


def generate_data(month):
    rows = []
    base_rates = {
    "USD": (30.8, 31.4),
    "CNY": (4.25, 4.35),
    "HKD": (3.90, 4.00),
    "GBP": (39.2, 40.1),
    "AUD": (20.1, 20.8),
    "CAD": (22.3, 23.0),
    "SGD": (23.0, 23.7),
    "CHF": (37.1, 37.9),
    "JPY": (0.208, 0.215),
    "ZAR": (1.65, 1.75),
    "SEK": (3.05, 3.15),
    "NZD": (18.4, 19.0),
    "THB": (0.91, 0.98),
    "PHP": (0.53, 0.58),
    "IDR": (0.0019, 0.0021),
    "EUR": (35.5, 36.4),
    "KRW": (0.0225, 0.0245),
    "VND": (0.0012, 0.0014),
    "MYR": (6.45, 6.65)
}

    for currency in currencies:
        buy_rate, sell_rate = base_rates[currency]
        for i in range(21):
            row = {
                "資料日期": f"{month}-{str(i+1).zfill(2)}",
                "幣別": currency,
                "匯率（本行買入）": "本行買入",
                "現金": round(buy_rate + i * 0.001, 4),
                "即期": round(buy_rate + 0.1 + i * 0.001, 4),
                "遠期10天": 0,
                "遠期30天": 0,
                "遠期60天": 0,
                "遠期90天": 0,
                "遠期120天": 0,
                "遠期150天": 0,
                "遠期180天": 0,
                "匯率（本行賣出）": "本行賣出",
                "現金_賣出": round(sell_rate + i * 0.001, 4),
                "即期_賣出": round(sell_rate + 0.1 + i * 0.001, 4),
                "遠期10天_賣出": 0,
                "遠期30天_賣出": 0,
                "遠期60天_賣出": 0,
                "遠期90天_賣出": 0,
                "遠期120天_賣出": 0,
                "遠期150天_賣出": 0,
                "遠期180天_賣出": 0,
            }
            rows.append(row)

        for i in range(9):
            row = {
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
            }
            rows.append(row)

    return pd.DataFrame(rows)

if st.button("產生資料"):
    df = generate_data(month)

    st.success("成功產生匯率表！")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="下載 CSV",
        data=csv,
        file_name=f"{month}_月底匯率表.csv",
        mime="text/csv"
    )
