import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="AI株価予測", layout="wide")

st.markdown("# 🤖 AI株価予測アドバイザー")
st.write("過去3ヶ月の株価データから、**来週の終値を予測**します。")

# 入力欄を2カラムで整理
col1, col2 = st.columns([3, 1])
with col1:
    ticker = st.text_input("🔍 銘柄コード（例：7203.T）", "7203.T")
with col2:
    go = st.button("📈 予測する")

if go:
    data = yf.download(ticker, period="3mo", interval="1d", progress=False)

    if data.empty:
        st.error("⚠️ データ取得失敗。銘柄コードを確認してください。")
    else:
        close_prices = data["Close"].dropna()
        X = np.arange(len(close_prices)).reshape(-1, 1)
        y = close_prices.values

        model = LinearRegression()
        model.fit(X, y)

        future_X = np.arange(len(close_prices), len(close_prices)+5).reshape(-1, 1)
        predictions = model.predict(future_X)

        st.markdown("## 📊 予測結果")
        current_price = float(y[-1])
        predicted_last = float(predictions[-1])
        diff = predicted_last - current_price

        # AI判断コメント
        if diff > 15:
            comment = "📈 上昇傾向（強）"
        elif diff > 5:
            comment = "📈 上昇傾向"
        elif diff < -15:
            comment = "📉 下落傾向（強）"
        elif diff < -5:
            comment = "📉 下落傾向"
        else:
            comment = "⏳ 横ばい予測"

        # メトリック表示（スマホでも見やすい）
        col1, col2, col3 = st.columns(3)
        col1.metric("現在の株価", f"{current_price:.2f} 円")
        col2.metric("5日後の予測", f"{predicted_last:.2f} 円", f"{diff:+.2f} 円")
        col3.metric("AI判断", comment)

        # 表形式でも予測を表示
        st.markdown("### 🧮 来週の予測一覧")
        table_data = {
            "日数": [f"Day {i+1}（{len(close_prices)+i}日目）" for i in range(5)],
            "予測終値": [f"{float(p):.2f} 円" for p in predictions]
        }
        st.table(pd.DataFrame(table_data))

        # グラフ用データ
        all_days = np.concatenate([X, future_X]).flatten()
        all_prices = np.concatenate([y, predictions]).flatten()
        df_chart = pd.DataFrame({
            "Day": all_days,
            "終値と予測": all_prices
        })
        st.markdown("### 📈 株価チャート（実績＋予測）")
        st.line_chart(df_chart.set_index("Day"))
