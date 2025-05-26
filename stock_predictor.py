import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

st.title("🤖 AI株価予測アドバイザー")
st.write("過去3ヶ月の株価データから、来週の終値を予測します。")

# 🔸 銘柄コード入力欄
ticker = st.text_input("銘柄コードを入力（例：7203.T）", "7203.T")

if st.button("予測する"):
    # 🔸 株価データ取得
    data = yf.download(ticker, period="3mo", interval="1d", progress=False)

    if data.empty:
        st.error("⚠️ データが取得できませんでした。銘柄コードを確認してください。")
    else:
        # 🔸 終値のSeriesを取得
        close_prices = data["Close"].dropna()

        # 🔸 特徴量（日数）と目的変数（終値）を準備
        X = np.arange(len(close_prices)).reshape(-1, 1)
        y = close_prices.values

        # 🔸 線形回帰モデルで学習
        model = LinearRegression()
        model.fit(X, y)

        # 🔸 来週5営業日分のXを作成し予測
        future_X = np.arange(len(close_prices), len(close_prices) + 5).reshape(-1, 1)
        predictions = model.predict(future_X)

        # 🔸 数値を整えて出力
        st.subheader("📈 来週の予測株価（終値）")
        for i, price in enumerate(predictions):
            st.write(f"Day {i+1}（{len(close_prices)+i}日目）: {float(price):.2f} 円")

        # 🔸 グラフ用のデータ整形（1次元に変換）
        all_days = np.concatenate([X, future_X]).flatten()
        all_prices = np.concatenate([y, predictions]).flatten()

        df_chart = pd.DataFrame({
            "Day": all_days,
            "終値と予測": all_prices
        })

        # 🔸 グラフ表示
        st.subheader("🔮 株価チャート（実績＋予測）")
        st.line_chart(df_chart.set_index("Day"))
