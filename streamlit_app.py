import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="AI株価予測", layout="wide")

# タイトルと概要
st.title("📈 AI株価予測アプリ")
st.markdown("過去3〜6ヶ月の株価データをもとに、翌週の終値をAIが予測します。")
st.markdown("- 複数銘柄チャートの比較\n- テクニカル分析（移動平均線・RSI）\n- AIによる翌営業日の価格予測と判断表示")

# 株価予測パート
ticker = st.text_input("🔍 銘柄コードを入力\n例: 7203.T (トヨタ自動車)", "7203.T")
if st.button("📊 AI予測する"):
    data = yf.download(ticker, period="6mo", interval="1d", progress=False)
    if data.empty:
        st.error("データ取得に失敗しました。")
    else:
        data["Close_shift"] = data["Close"].shift(1)
        data["MA_5"] = data["Close"].rolling(window=5).mean().shift(1)
        data = data.dropna()
        X = data[["Close_shift", "MA_5"]]
        y = data["Close"]
        model = LinearRegression()
        model.fit(X, y)
        latest_X = X.iloc[-1].values.reshape(1, -1)
        predicted_price = float(model.predict(latest_X)[0])
        current_price = float(data["Close"].iloc[-1])
        diff = predicted_price - current_price
        rate = diff / current_price * 100

        if rate > 1.5:
            comment = "📈 買いのチャンスです！"
        elif rate < -1.5:
            comment = "📉 売却を検討しましょう。"
        else:
            comment = "🟡 様子を見ましょう。"

        st.markdown("## ✅ AIによる予測結果")
        col1, col2, col3 = st.columns(3)
        col1.metric("現在の株価", f"{current_price:.2f} 円")
        col2.metric("予測終値（翌営業日）", f"{predicted_price:.2f} 円", f"{diff:+.2f} 円")
        col3.metric("AI判断", comment)

        st.markdown("### 📈 株価チャート（過去＋予測）")
        chart_series = data["Close"].copy()
        next_date = chart_series.index[-1] + pd.Timedelta(days=1)
        chart_series.loc[next_date] = predicted_price
        chart_df = chart_series.reset_index()
        chart_df.columns = ["日付", "終値"]
        chart_df = chart_df.set_index("日付")
        st.line_chart(chart_df)

# 複数銘柄チャート比較
st.markdown("## 📊 複数銘柄チャート比較")
multi_input = st.text_input("銘柄コードをカンマで区切って入力（例：7203.T,6758.T）", "7203.T,6758.T")
if st.button("📉 チャートを表示"):
    tickers = [x.strip() for x in multi_input.split(",")]
    df_all = pd.DataFrame()
    for t in tickers:
        df = yf.download(t, period="3mo", interval="1d", progress=False)
        if not df.empty:
            df_all[t] = df["Close"]
    if not df_all.empty:
        st.line_chart(df_all)
    else:
        st.warning("有効な株価データが取得できませんでした。")

# テクニカル分析
st.markdown("## 📊 テクニカル分析：RSI & 移動平均線")
tech_ticker = st.text_input("銘柄コード（RSIと移動平均線を表示）", "7203.T")
if st.button("📈 テクニカル分析を表示"):
    df = yf.download(tech_ticker, period="3mo", interval="1d", progress=False)
    if df.empty:
        st.error("テクニカルデータ取得に失敗しました。")
    else:
        df["MA5"] = df["Close"].rolling(window=5).mean()
        df["MA25"] = df["Close"].rolling(window=25).mean()
        delta = df["Close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        df["RSI"] = 100 - (100 / (1 + rs))

        st.markdown("### 📉 株価と移動平均線")
        plot_data = df[["Close", "MA5", "MA25"]].dropna()
        if plot_data.empty:
            st.warning("移動平均線が正しく計算できていません。")
        else:
            st.line_chart(plot_data)

        st.markdown("### 💡 RSI（相対力指数）")
        if df["RSI"].dropna().empty:
            st.warning("RSIの計算に失敗しました。")
        else:
            st.line_chart(df["RSI"])










        


        


       
