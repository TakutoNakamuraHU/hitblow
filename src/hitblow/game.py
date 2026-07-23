"""ゲームの進行（入力・表示・ループ）。

★ チームで足す機能は **自分の担当の場所**に書く（1機能=1ファイル）。
   下の「ここに足す」場所は3か所（① 開始時 ② 入力コマンド ③ 勝利時）。
   ペアごとに**別の場所**を直すので、並行作業でも衝突しない。
   import も自分の場所の近くに書くこと（ファイル先頭にまとめない＝衝突回避）。
"""

from .core import judge, make_secret

# ===== ② 入力コマンドに足す（ヒント など）: ここに書く（import もここに） =====
from .highlow import highlow

# 入力した数字が含まれているか判定
from .check import check

def play(digits=3):
    secret = make_secret(digits)
    print(f"Hit & Blow（{digits} 桁・重複なし）\n")
    print("【highlowと入力】0-4はL, 5-9はHと表示\n【checkと入力】任意の数字が含まれているか確認，1回のみ")

    # ===== ① 開始時に足す（難易度・あいさつ など）: ここに書く =====
    from .time import start_timer, stop_timer, register_score, display_ranking
    start_time = start_timer()

    tries = 0
    check_used = False
    while True:
        guess = input("予想 > ").strip()

        # 追加部分(highlow)
        if guess == "highlow":
            print("High/Low:", highlow(secret))
            continue
        
        # 追加部分(check)
        if guess == "check":

            if check_used:
                print("checkは1回しか使えません。")
                continue

            number = input("調べたい数字（0～9）> ").strip()

            if len(number) != 1 or not number.isdigit():
                print("0～9の数字を1つ入力してください")
                continue

            check_used = True

            if check(secret, number):
                print(f"{number} は答えに含まれています。")
            else:
                print(f"{number} は答えに含まれていません。")

            continue
        
        if len(guess) != digits or not guess.isdigit():
            print(f"{digits} 桁の数字で入力してね")
            continue
        tries += 1
        hit, blow = judge(secret, guess)
        print(f"  Hit={hit}  Blow={blow}")
        if hit == digits:

            # ===== ③ 勝利時に足す（スコア・履歴 など）: ここに書く =====
            elapsed = stop_timer(start_time)
            print(f"正解！ {tries} 回で当たり（答え {secret}）")
            print(f"クリアタイム: {elapsed:.2f} 秒")

            # スコアの登録とランキング表示
            register_score(elapsed, digits)
            display_ranking()
            break