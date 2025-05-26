import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

st.title("🤖 AI株価予測アドバイザー")
st.write("過去3ヶ月の株価データから、来週の終値を予測します。")

ticker = st.text_input("銘柄コードを入力（例：7203.T）", "7203.T")

if st.button("予測する"):
    data = yf.download(ticker, period="3mo", interval="1d", progress=False)

    if data.empty:
        st.error("⚠️ データが取得できませんでした。")
    else:
        close_prices = data["Close"].dropna().reset_index()

        # 日数でXを作成（0,1,2,...）
        close_prices["Day"] = np.arange(len(close_prices))

        # 学習データ
        X = close_prices[["Day"]]   # 特徴量（日にち）
        y = close_prices["Close"]   # 目的変数（終値）

        # モデル作成と学習
        model = LinearRegression()
        model.fit(X, y)

        # 予測：次の5営業日（未来のX）
        future_days = np.arange(len(close_prices), len(close_prices) + 5).reshape(-1, 1)
        predictions = model.predict(future_days)

        # 予測結果表示
        st.subheader("📈 来週の予測株価（終値）")
        for i, pred in enumerate(predictions):
            st.write(f"📅 Day {i+1}（{len(close_prices)+i}日目）: {pred:.2f} 円")

        # 予測グラフ表示
        st.subheader("🔮 株価と予測線")
        all_days = np.concatenate([X.values, future_days])
        all_prices = np.concatenate([y.values, predictions])
        full_df = pd.DataFrame({
            "Day": all_days.flatten(),
            "予測終値": all_prices
        })
        st.line_chart(full_df.set_index("Day"))
