"""High / Low ヒント機能"""

def highlow(secret):
    """答えの各数字が High(5～9) か Low(0～4) かを返す。"""
    return "".join("H" if int(d) >= 5 else "L" for d in secret)