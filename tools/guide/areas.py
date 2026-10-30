"""地域記事（tools/guide/city と /guide/<key>/）から、診断ページで使う data/areas.js を作る。

python3 tools/guide/areas.py .

診断ページ（index.html）は data/areas.js を読み込んで、品目ごとの料金と「新居の自治体を調べる」に使う。
数字は記事に書いた公式の数字をそのまま使う（記事を直したら、これも実行し直す）。
"""
import glob, html, json, os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
HERE = os.path.dirname(os.path.abspath(__file__))
CHECKED = "2026-10-30"

def txt(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()

def safe_html(s):
    # 記事の中の <a> だけ残す
    s = re.sub(r"<(?!/?a\b)[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()

def name_of(key):
    m = os.path.join(HERE, "meta", key + ".json")
    if os.path.exists(m):
        return json.load(open(m, encoding="utf-8"))["name"]
    g = open(os.path.join(ROOT, "guide", key, "index.html"), encoding="utf-8").read()
    return re.search(r"<h2>(.+?)に引っ越してきた人へ</h2>", g).group(1)

def fee_rows(s):
    rows = []
    for tb in re.findall(r"<table>(.*?)</table>", s, re.S):
        ths = [txt(x) for x in re.findall(r"<th[^>]*>(.*?)</th>", tb, re.S)]
        for tr in re.findall(r"<tr>(.*?)</tr>", tb, re.S):
            tds = [txt(x) for x in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
            if not tds:
                continue
            fee = drop = None; items = []
            for i, t in enumerate(tds):
                h = ths[i] if i < len(ths) else ""
                if "処理券" in h or "大きさ" in h:
                    continue
                if "持" in h:
                    drop = t
                elif "円" in t or t == "無料":
                    if fee is None:
                        fee = t
                else:
                    items.append(t)
            if fee and items and "円" in fee:
                rows.append([("、".join(items)), fee] + ([drop] if drop else []))
    return rows

areas = {}
for f in sorted(glob.glob(os.path.join(HERE, "city", "*.html"))):
    key = os.path.basename(f)[:-5]
    s = open(f, encoding="utf-8").read()
    g = open(os.path.join(ROOT, "guide", key, "index.html"), encoding="utf-8").read()
    a = {"n": name_of(key), "g": f"/guide/{key}/"}
    src = re.search(r'<p class="src">[^\n]*?href="(https://[^"]+)"', s)
    if src:
        a["url"] = src.group(1)
    # 記事の「〇〇のポイント」（対象・申し込み・料金・持ち込みなど）を [見出し, 本文] で
    pt = re.search(r'<div class="point">(.*?)</div>', s, re.S)
    if pt:
        a["pt"] = [txt(li).split("：", 1) for li in re.findall(r"<li>(.*?)</li>", pt.group(1), re.S) if "：" in txt(li)]
    # 「〇〇に引っ越してきた人へ」。どの地域にも同じ3行（申し込みは新しい住所で・券は自治体ごと・段ボール）は診断ページ側で出す
    mv = re.search(r"に引っ越してきた人へ</h2>\s*<p>(.*?)</p>\s*<ul>(.*?)</ul>", g, re.S)
    if mv:
        lead = safe_html(mv.group(1))
        a["mv0"] = 1 if "特に書かれていませんでした" in lead else lead
        a["mv"] = [safe_html(x) for x in re.findall(r"<li>(.*?)</li>", mv.group(2), re.S)
                   if not re.match(r"(申し込みは、住み始めてから|処理券やシールは自治体ごと|段ボールや梱包材は)", txt(x))]
    # 家電4品目を市が条件つきで収集すると記事に書いた地域（広島・相模原・岡山）は、その一文を残す
    kp = re.search(r"<h2>出せない物と家電4品目</h2>.*?<p>(家電4品目は.*?)</p>", s, re.S)
    if kp:
        ks = [x + "。" for x in txt(kp.group(1)).split("。") if re.search(r"大型ごみ収集|市へ頼む|市の戸別収集", x)]
        if ks:
            a["kaden"] = "".join(ks)
    rows = fee_rows(s)
    if rows:
        a["items"] = rows
    areas[key] = a

os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
out = os.path.join(ROOT, "data", "areas.js")
with open(out, "w", encoding="utf-8") as w:
    w.write(f"// 自動生成（tools/guide/areas.py）。手で直さず、記事の元データを直して作り直す。数字は {CHECKED} に各公式ページで確認したもの\n")
    w.write("window.HINATA_AREAS=" + json.dumps(areas, ensure_ascii=False, separators=(",", ":")) + ";\n")
print(out, len(areas), "areas,", sum(1 for a in areas.values() if a.get("items")), "with item fees")
