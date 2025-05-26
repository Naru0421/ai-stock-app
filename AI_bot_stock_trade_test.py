import yfinance as yf

ticker = "7203.T"  # トヨタの証券コード
data = yf.download(ticker, period="1mo", interval="1d")

print(data)  # データ確認用

if data.empty:
    print("⚠️ データが取得できませんでした。")
else:
    close_prices = data["Close"]
    current_price = close_prices.iloc[-1].item()  # ← 修正ポイント①
    moving_average_25 = close_prices.rolling(window=25).mean().iloc[-1].item()  # ← 修正ポイント②

    print(f"現在の株価: {current_price:.2f}")
    print(f"25日移動平均: {moving_average_25:.2f}")

    if current_price > moving_average_25 * 1.03:
        print("✅ 買いのチャンスです！")
    elif current_price < moving_average_25 * 0.97:
        print("⚠️ 売却を検討しましょう。")
    else:
        print("⏳ 今は保有して様子を見ましょう。")
