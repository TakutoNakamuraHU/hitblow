"""コマンドの入口。第3回で `hitblow` コマンドがここ（main）を呼ぶ。"""

from .game import play
from .choose_digits import choose_digits 


def main():
    # キーボード入力で 3, 4, 5 のいずれかの桁数を取得する
    digits = choose_digits()
    
    # 取得した桁数を渡してゲームをスタート
    play(digits)