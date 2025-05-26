
import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📋 複数銘柄のAI株式アドバイザー")
st.write("日本株の証券コードをカンマ区切りで最大10社以上入力してください（例：7203.T, 6758.T, 9984.T, ...）")

# ユーザー入力（複数銘柄）
code_input = st.text_area("銘柄コード入力", "7203.T, 6758.T, 9984.T, 8306.T, 9434.T, 4502.T, 2914.T, 7974.T, 6098.T, 9433.T")

if st.button("一括分析を開始"):
    tickers = [code.strip() for code in code_input.split(",") if code.strip()]
    results = []

    for ticker in tickers:
        try:
            data = yf.download(ticker, period="3mo", interval="1d", progress=False)

            if data.empty:
                results.append({
                    "銘柄コード": ticker,
                    "現在価格": "取得失敗",
                    "25日移動平均": "-",
                    "判断": "⚠️ データなし"
                })
                continue

            close_prices = data["Close"]
            moving_avg_25 = close_prices.rolling(window=25).mean()

            current_price = close_prices.iloc[-1].item()
            moving_avg_value = moving_avg_25.iloc[-1].item()

            # 売買判断ロジック
            if current_price > moving_avg_value * 1.03:
                judgement = "✅ 買い"
            elif current_price < moving_avg_value * 0.97:
                judgement = "⚠️ 売り"
            else:
                judgement = "⏳ 保有"

            results.append({
                "銘柄コード": ticker,
                "現在価格": f"{current_price:.2f} 円",
                "25日移動平均": f"{moving_avg_value:.2f} 円",
                "判断": judgement
            })

        except Exception as e:
            results.append({
                "銘柄コード": ticker,
                "現在価格": "エラー",
                "25日移動平均": "-",
                "判断": f"❌ {str(e)[:30]}"
            })

    # 表を表示
    st.subheader("📊 分析結果（最大10社以上対応）")
    df = pd.DataFrame(results)
    st.dataframe(df)

    # オプションでCSVダウンロード
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 CSVとしてダウンロード", data=csv, file_name="stock_analysis.csv", mime='text/csv')
