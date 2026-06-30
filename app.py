import pandas as pd
import streamlit as st

st.set_page_config(page_title="月底匯率表產生器")

st.title("月底匯率表產生器")
st.write("第一版測試：先確認 Streamlit 可以正常跑")

currencies = [
    "USD","CNY","HKD","GBP","AUD","CAD","SGD","CHF","JPY",
    "ZAR","SEK","NZD","THB","PHP","IDR","EUR","KRW","VND","MYR"
]

month = st.text_input("請輸入月份（例如：2026-06）", "2026-06")

if st.button("產生測試資料"):
    rows = []

    for c in currencies:
        for i in range(30):
            rows.append({
                "資料日期": f"{month}-{i+1:02d}",
                "幣別": c,
                "來源": "台灣銀行"
            })

    df = pd.DataFrame(rows)

    st.success("成功！")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="下載 CSV",
        data=csv,
        file_name=f"exchange_rate_{month}.csv",
        mime="text/csv",
    )
