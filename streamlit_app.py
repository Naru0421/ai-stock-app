import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="AI株価予測", layout="wide")
st.title("📈 AI株価予測アプリ")
st.markdown("過去3〜6ヶ月の株価データをもとに、翌週の終値をAIが予測します。")

# ユーザー入力
col1, col2 = st.columns([3, 1])
with col1:
    ticker = st.text_input("🔍 銘柄コード（例：7203.T）", "7203.T")
with col2:
    go = st.button("📊 予測する")

if go:
    # 株価データ取得
    data = yf.download(ticker, period="6mo", interval="1d", progress=False)

    if data.empty:
        st.error("⚠️ データ取得に失敗しました。銘柄コードを確認してください。")
    else:
        # 特徴量の生成
        data = data.dropna()
        data["Close_shift"] = data["Close"].shift(1)
        data["MA_5"] = data["Close"].rolling(window=5).mean().shift(1)
        data = data.dropna()

        # 入力・出力
        X = data[["Close_shift", "MA_5"]]
        y = data["Close"]

        # 学習
        model = LinearRegression()
        model.fit(X, y)

        # 予測
        latest_X = X.iloc[-1].values.reshape(1, -1)
        predicted_price = model.predict(latest_X)[0]

        current_price = float(data["Close"].iloc[-1])
        predicted_price = float(predicted_price)
        diff = predicted_price - current_price
        rate = diff / current_price * 100

        st.markdown("## 📊 複数銘柄チャート比較")

ticker_input = st.text_input("複数銘柄コードをカンマ区切りで入力（例：7203.T,6758.T,9984.T）", "7203.T,6758.T")
if st.button("📊 チャートを表示"):
    tickers = [t.strip() for t in ticker_input.split(",")]
    chart_data = pd.DataFrame()

    for ticker in tickers:
        try:
            df = yf.download(ticker, period="3mo", interval="1d", progress=False)
            if not df.empty:
                chart_data[ticker] = df["Close"]
        except:
            st.warning(f"{ticker} のデータ取得に失敗しました。")

    if not chart_data.empty:
        st.line_chart(chart_data)
    else:
        st.error("📉 有効な株価データが取得できませんでした。")


        # -----------------------------------------
# 📈 テクニカル指標（RSI & 移動平均線）表示機能
# -----------------------------------------
st.markdown("## 📊 テクニカル分析：RSI & 移動平均線")

selected_ticker = st.text_input("銘柄コード（RSIと移動平均線を表示）", "7203.T")
if st.button("📉 テクニカル分析を表示"):

    tech_data = yf.download(selected_ticker, period="3mo", interval="1d", progress=False)

    if tech_data.empty:
        st.warning("データ取得に失敗しました。")
    else:
        # 移動平均線（MA5, MA25）
        tech_data["MA5"] = tech_data["Close"].rolling(window=5).mean()
        tech_data["MA25"] = tech_data["Close"].rolling(window=25).mean()

        # RSI（相対力指数）の計算
        delta = tech_data["Close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        tech_data["RSI"] = 100 - (100 / (1 + rs))

        # グラフ表示（NaNを含む行は削除）
st.markdown("### 📉 株価と移動平均線")

# 必要な列が揃っている行だけ使う
plot_data = tech_data[["Close", "MA5", "MA25"]].dropna()
st.line_chart(plot_data)




        # 判断
        if rate > 1.5:
            comment = "📈 買いのチャンスです！"
        elif rate < -1.5:
            comment = "📉 売却を検討しましょう。"
        else:
            comment = "⏳ 様子を見ましょう。"

        # メトリック表示
        col1, col2, col3 = st.columns(3)
        col1.metric("現在の株価", f"{current_price:.2f} 円")
        col2.metric("予測終値（翌営業日）", f"{predicted_price:.2f} 円", f"{diff:+.2f} 円")
        col3.metric("AI判断", comment)

        # 📈 チャート表示（ここも if go の中に入れる！）
        st.markdown("### 📉 株価チャート（過去＋予測）")
        next_date = data.index[-1] + pd.Timedelta(days=1)
        chart_series = data["Close"].copy()
        chart_series.loc[next_date] = predicted_price
        chart_df = chart_series.reset_index()
        chart_df.columns = ["日付", "終値"]
        chart_df = chart_df.set_index("日付")
        st.line_chart(chart_df)









        


        


       
