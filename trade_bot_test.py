# 例：シンプルな移動平均による売買判断
# ルール：
# - 株価 > 25日移動平均 → 買い
# - 株価 < 25日移動平均 → 売り
# - 株価 ≒ 移動平均 → 保有

current_price = 1050  # 現在の株価
moving_average_25 = 1000  # 25日移動平均

if current_price > moving_average_25 * 1.03:
    print("買いのチャンスです！")
elif current_price < moving_average_25 * 0.97:
    print("売却を検討しましょう。")
else:
    print("今は保有して様子を見ましょう。")
