"""入力した数字が答えに含まれているか判定する"""

def check(secret, number):
    """
    secret : 答え（例: "582"）
    number : 調べる数字（例: "5"）

    戻り値:
        True  : 含まれている
        False : 含まれていない
    """
    return number in secret