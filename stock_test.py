import yfinance as yf

# トヨタの株価データを取得
ticker = yf.Ticker("7203.T")
df = ticker.history(period="5y", interval="1d")

# 最初の5行を表示
print(df.head())
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13 -m pip show yfinance
