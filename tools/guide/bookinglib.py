"""地域記事の「申し込み方法」欄からウェブ予約の状態・予約サイト・電話を取り出す（areas.py と gencity.py で共通）。"""
import html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKING = json.load(open(os.path.join(HERE, "booking.json"), encoding="utf-8"))

def txt(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()

def safe_html(s):
    # 記事の中の <a> だけ残す
    s = re.sub(r"<(?!/?a\b)[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()

def booking(key, s):
    """記事の「申し込み方法」欄から、予約サイトのリンクと電話の行を取り出し、booking.json の状態を足す。
    bk = {web: open|cond|stop|none, w: [[名前, URL]], t: [電話の行（tel リンクつき）], note, mail}"""
    sec = re.search(r"<h2>[^<]*申し込み[^<]*</h2>(.*?)<h2>", s, re.S)
    sec = sec.group(1) if sec else ""
    w, t = [], []
    for li in re.findall(r"<li>(.*?)</li>", sec, re.S):
        head = txt((re.match(r"\s*<b>(.*?)</b>", li, re.S) or [None, ""])[1])
        if re.search(r"インターネット|LINE", head):
            for u, label in re.findall(r'<a href="(https?://[^"]+)"[^>]*>(.*?)</a>', li, re.S):
                label = txt(label)
                if "LINE" in head and "インターネット" not in head and "LINE" not in label:
                    label = f"{re.sub(r'（.*?）', '', head)}で申し込む（{label}）"
                elif re.search(r"変更|取消|品目|収集日|一覧|ページ", label):
                    continue
                w.append([label, html.unescape(u)])
        elif "電話" in head and "tel:" in li:
            t.append(safe_html(re.sub(r"^\s*<b>(.*?)</b>：?", r"\1：", li)))
    b = dict(BOOKING.get(key, {}))
    b.setdefault("web", "open" if w else "none")
    if w and b["web"] != "stop":
        b["w"] = w
    if t:
        b["t"] = t
    return b
