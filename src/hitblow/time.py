"""タイムアタック機能およびオンライン共有ランキング管理（APIキーなし・URL指定版）"""

import json
import time as std_time
import urllib.error
import urllib.request

# =========================================================
# ⚙️ 設定項目（URLのみを指定）
# =========================================================
# ※ JSONBinをご利用の場合は、対象のBinを「Public（公開）」に設定してください
# ※ npoint.io や その他のパブリックJSON APIサービスでもそのまま利用可能です
SHARED_API_URL = "https://api.jsonbin.io/v3/b/6a616576f5f4af5e29b36bcd"


def start_timer():
    """計測開始時のタイムスタンプを返す。"""
    return std_time.time()


def stop_timer(start_time):
    """開始時刻からの経過時間（秒）を計算して返す。"""
    return round(std_time.time() - start_time, 2)


def load_ranking(api_url=SHARED_API_URL):
    """URLから【最新】のランキングデータを取得する。"""
    try:
        # JSONBin等のAPIで最新データを取得するためのURL成形
        base_url = api_url.rstrip("/")
        if not base_url.endswith("/latest"):
            fetch_url = f"{base_url}/latest"
        else:
            fetch_url = base_url

        # キャッシュ対策：URL末尾にタイムスタンプ (?t=...) を付与
        fetch_url = f"{fetch_url}?t={int(std_time.time())}"

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        }

        req = urllib.request.Request(fetch_url, headers=headers)

        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))

                # 配列が直接返ってきた場合
                if isinstance(data, list):
                    return data
                # オブジェクト（{"record": [...]}）形式で返ってきた場合
                elif isinstance(data, dict) and "record" in data:
                    if isinstance(data["record"], list):
                        return data["record"]

    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
        print(f"\n[注意] ランキングの取得に失敗しました: {e}")

    return []


def save_ranking(ranking, api_url=SHARED_API_URL):
    """URLへランキングデータを上書き保存する。"""
    try:
        # 保存先URL（/latest が付いていれば除外する）
        save_url = api_url.replace("/latest", "")

        data = json.dumps(ranking).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
        }

        req = urllib.request.Request(
            save_url,
            data=data,
            headers=headers,
            method="PUT",
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status in (200, 201):
                return True
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"\n[注意] ランキングの更新に失敗しました: {e}")

    return False


def register_score(elapsed_time, digits, api_url=SHARED_API_URL):
    """スコアをオンラインランキングに登録し、上位10件を保持する。"""
    name = input("ランキング用の名前を入力してください > ").strip()
    if not name:
        name = "名無し"

    # 最新のランキングを取得
    ranking = load_ranking(api_url)
    ranking.append({"name": name, "time": elapsed_time, "digits": digits})

    # タイムが短い順（昇順）にソートして上位10件を残す
    ranking.sort(key=lambda x: x["time"])
    ranking = ranking[:10]

    # サーバーへ保存
    save_ranking(ranking, api_url)


def display_ranking(api_url=SHARED_API_URL):
    """TOP 10 ランキングを表示する。"""
    ranking = load_ranking(api_url)
    print("\n===== 🏆 共通タイムアタック TOP 10 🏆 =====")
    if not ranking:
        print("まだ記録がないか、ランキングを取得できませんでした。")
    else:
        for rank, record in enumerate(ranking, 1):
            print(
                f"{rank:>2}位 | {record['time']:>6.2f}秒 | "
                f"{record['name']} ({record['digits']}桁)"
            )
    print("============================================\n")