# 全国の市区町村の一覧（診断の「お住まい」の入力候補）を data/munis.js に書き出す
# 使い方: python3 tools/guide/munis.py .            （国土地理院と Wikidata から取り直す。公式サイトのリンク切れも確かめる）
#         python3 tools/guide/munis.py . --no-check  （リンクの確認を省く）
# 出どころ: 市区町村名とコード＝国土地理院 https://maps.gsi.go.jp/js/muni.js
#           公式サイトのトップURL＝Wikidata（P429 全国地方公共団体コード → P856 公式ウェブサイト）。開けないURLは載せない
# 地域記事のある市区（data/areas.js）は、その記事のキーを持たせる
import csv, io, json, re, subprocess, sys, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
CHECK = "--no-check" not in sys.argv
UA = {"User-Agent": "hinata-lp-munis/1.0 (https://hinata.shiokonbu.com/)"}
# 北方領土の6村は受付がないので除く
SKIP = {1695, 1696, 1697, 1698, 1699, 1700}
SPARQL = """SELECT ?code ?url WHERE { ?item wdt:P429 ?code . ?item wdt:P856 ?url .
 FILTER NOT EXISTS { ?item wdt:P576 ?end } }"""


def get(url, timeout=60):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read().decode("utf-8")


def load_gsi():
    mu = {}
    for m in re.finditer(r"= '(\d+),([^,]+),(\d+),([^']+)'", get("https://maps.gsi.go.jp/js/muni.js")):
        c = int(m[3])
        if c not in SKIP:
            mu[c] = (m[2], m[4].replace(" ", "　"))
    return mu


def load_wikidata():
    q = urllib.parse.urlencode({"query": SPARQL})
    req = urllib.request.Request("https://query.wikidata.org/sparql?" + q, headers={**UA, "Accept": "text/csv"})
    txt = urllib.request.urlopen(req, timeout=120).read().decode("utf-8")
    by = {}
    for r in csv.DictReader(io.StringIO(txt)):
        u = r["url"].strip()
        if not re.match(r"https?://", u) or re.search(r"foreign|english|chinese|korean|/en/|/zh|/ko/", u, re.I):
            continue
        by.setdefault(int(r["code"].strip()[:5]), []).append(u)
    # https を先に、短いもの（トップページ）を先に
    return {c: sorted(us, key=lambda u: (not u.startswith("https"), len(u))) for c, us in by.items()}


# 自治体のドメインらしいもの（*.lg.jp か city./town./vill. で始まるもの）だけ使う。古いドメインが別のサイトに変わっているのを避けるため
GOVHOST = re.compile(r"(\.lg\.jp$)|(^(www\.)?(city|town|vill|village)\.)")


def alive(u):
    """開けて、リダイレクトのあとも自治体のドメインのままなら True"""
    if not GOVHOST.search(urllib.parse.urlparse(u).netloc):
        return False
    try:
        req = urllib.request.Request(u, headers={**UA, "User-Agent": "Mozilla/5.0 (compatible; hinata-lp-munis/1.0)"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status < 400 and bool(GOVHOST.search(urllib.parse.urlparse(r.geturl()).netloc))
    except Exception:
        return False


def main():
    mu = load_gsi()
    wd = load_wikidata()
    js = subprocess.run(["node", "-e", 'global.window={};require(process.argv[1]+"/data/areas.js");'
                         'console.log(JSON.stringify(Object.fromEntries(Object.entries(window.HINATA_AREAS).map(([k,v])=>[k,[v.n,v.url||""]]))))', ROOT],
                        capture_output=True, text=True, check=True).stdout
    areas = json.loads(js)
    cities = {c: v for c, v in mu.items() if "　" not in v[1]}
    # 地域記事のキー：名前で探し、同じ名前が2つ以上あるとき（府中市など）は公式ページのドメインで見分ける
    akey = {}
    for k, (n, u) in areas.items():
        cand = [c for c, (p, nn) in cities.items() if nn == n]
        if len(cand) > 1:
            host = urllib.parse.urlparse(u).netloc
            cand = [c for c in cand if any(urllib.parse.urlparse(x).netloc == host for x in wd.get(c, []))] or cand[:1]
        if cand:
            akey[cand[0]] = k
        else:
            print("記事の市区が一覧にない:", k, n)
    # 公式サイト：開けるものを先頭から1つ
    urls = {}
    if CHECK:
        allu = sorted({u for c in cities for u in wd.get(c, [])[:3]})
        with ThreadPoolExecutor(16) as ex:
            ok = dict(zip(allu, ex.map(alive, allu)))
        for c in cities:
            urls[c] = next((u for u in wd.get(c, [])[:3] if ok.get(u)), "")
    else:
        urls = {c: next((u for u in wd.get(c, []) if GOVHOST.search(urllib.parse.urlparse(u).netloc)), "") for c in cities}
    # [コード, 都道府県, 名前, 公式サイト（https:// と末尾の / を省く。http のものは http:// のまま）, 記事のキー, 親の市のコード（政令市の区）]
    rows = []
    for c, (p, n) in sorted(mu.items()):
        if "　" in n:
            par, w = n.split("　")
            pc = next((k for k, (pp, nn) in cities.items() if pp == p and nn == par), 0)
            rows.append([c, p, par + w, "", "", pc])
        else:
            u = re.sub(r"^https://", "", urls.get(c, "")).rstrip("/")
            rows.append([c, p, n, u, akey.get(c, ""), 0])
    miss = sum(1 for r in rows if not r[5] and not r[3])
    out = ("// 自動生成（tools/guide/munis.py）。手で直さない。市区町村名＝国土地理院、公式サイト＝Wikidata（自治体のドメインで、開けたものだけ）\n"
           f"// 取得日 {__import__('datetime').date.today()}。公式サイトは自動で集めたリンクで、粗大ごみのページは各自治体で確かめていない\n"
           "// [コード, 都道府県, 名前, 公式サイト（https:// 省略）, 地域記事のキー, 親の市のコード（政令市の区）]\n"
           "window.HINATA_MUNIS=" + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ";\n")
    open(ROOT + "/data/munis.js", "w", encoding="utf-8").write(out)
    print(f"市区町村 {sum(1 for r in rows if not r[5])}・政令市の区 {sum(1 for r in rows if r[5])}・記事つき {len(akey)}・公式サイトなし {miss}・{len(out.encode())//1024}KB")


main()
