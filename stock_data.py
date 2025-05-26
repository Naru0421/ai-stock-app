import yfinance as yf
import matplotlib.pyplot as plt

ticker = yf.Ticker("7203.T")  # トヨタ
df = ticker.history(period="5y", interval="1d")

# 株価を確認
print(df.head())

# 終値のグラフを表示
df["Close"].plot(title="Toyota Stock Price")
plt.xlabel("Date")
plt.ylabel("Close Price (JPY)")
plt.show()
