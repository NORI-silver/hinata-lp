#!/usr/bin/env python3
"""SEOの自動チェック（Python 3 の標準ライブラリだけで動く）。

使い方: python3 tools/seo_check.py [リポジトリのフォルダ] [--external]
NG があれば終了コード 1。--external を付けると、自治体の公式ページなど外部リンクが
開けるかも確かめる（開けないものは WARN。週1回の定期実行で使う）。GitHub Actions（.github/workflows/seo-check.yml）と、
定期のSEOエージェント（docs/seo-playbook.md）が毎回これを実行する。
ルールの元は AGENTS.md の「SEO」と「文言・表示のルール」。
"""
import html
import json
import os
import re
import sys
import urllib.request
from html.parser import HTMLParser

SITE = "https://hinata.shiokonbu.com/"
TITLE_RANGE = (28, 35)   # AGENTS.md: タイトル28〜35字目安
DESC_RANGE = (80, 120)   # AGENTS.md: description 80〜120字
# 本文に必ず残すもの（AGENTS.md の文言ルール）
MUST_TEXT = ["目安", "家電リサイクル法"]
# 出してはいけない言い方（課金方針が決まるまで・根拠のない数字）
NG_TEXT = ["通知します", "申し込む¥", "実績", "件の実績", "No.1", "業界最安"]
KEYWORDS = ["粗大ごみ", "引越し", "間に合"]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta = {}
        self.links = {}
        self.ld = []
        self.h1 = []
        self.summaries = []
        self.hrefs = []
        self.imgs_no_alt = 0
        self._in = None
        self._buf = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link" and a.get("rel"):
            self.links[a["rel"]] = a.get("href", "")
        elif tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        elif tag == "img" and not a.get("alt"):
            self.imgs_no_alt += 1
        if tag in ("title", "h1", "summary") or (tag == "script" and a.get("type") == "application/ld+json"):
            self._in = "ld" if tag == "script" else tag
            self._buf = []
        elif tag in ("script", "style"):
            self._in = "skip"

    def handle_endtag(self, tag):
        if self._in is None:
            return
        done = {"ld": "script", "skip": None}.get(self._in, self._in)
        if done and tag != done:
            return
        if self._in == "skip" and tag not in ("script", "style"):
            return
        s = "".join(self._buf).strip()
        if self._in == "title":
            self.title = s
        elif self._in == "h1":
            self.h1.append(s)
        elif self._in == "summary":
            self.summaries.append(s)
        elif self._in == "ld":
            self.ld.append(s)
        self._in = None

    def handle_data(self, data):
        if self._in in ("title", "h1", "summary", "ld"):
            self._buf.append(data)
        if self._in not in ("skip", "ld"):
            self.text.append(data)


def check_external(src, warn, ok):
    urls = sorted(set(re.findall(r"https://[^\"'`\s<>)]+", src)))
    urls = [u for u in urls if not u.startswith(SITE) and "fonts.g" not in u and "schema.org" not in u]
    bad = 0
    for u in urls:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (seo_check)"})
            with urllib.request.urlopen(req, timeout=20) as r:
                if r.status >= 400:
                    raise OSError(r.status)
        except Exception as e:  # 自治体サイトは一時的に落ちることもあるので WARN 止まり
            bad += 1
            warn.append(f"外部リンクが開けない: {u}（{e}）")
    ok.append(f"外部リンク {len(urls) - bad}/{len(urls)} 件が開けた")


def main(root, external=False):
    ng, warn, ok = [], [], []
    path = os.path.join(root, "index.html")
    src = open(path, encoding="utf-8").read()
    p = Page()
    p.feed(src)
    body = "".join(p.text)

    # タイトル
    n = len(p.title)
    (ok if TITLE_RANGE[0] <= n <= TITLE_RANGE[1] else warn).append(f"title {n}字（目安{TITLE_RANGE[0]}〜{TITLE_RANGE[1]}）: {p.title}")
    for kw in KEYWORDS[:2]:
        if kw not in p.title:
            warn.append(f"title にメインキーワード「{kw}」がない")

    # description
    d = p.meta.get("description", "")
    n = len(d)
    if not d:
        ng.append("meta description がない")
    else:
        (ok if DESC_RANGE[0] <= n <= DESC_RANGE[1] else warn).append(f"description {n}字（目安{DESC_RANGE[0]}〜{DESC_RANGE[1]}）")

    # canonical / OGP
    if p.links.get("canonical") != SITE:
        ng.append(f"canonical が {SITE} でない: {p.links.get('canonical')}")
    for k in ("og:title", "og:description", "og:url", "og:image"):
        if not p.meta.get(k):
            ng.append(f"{k} がない")
    if p.meta.get("og:image", "").startswith(SITE):
        img = os.path.join(root, p.meta["og:image"][len(SITE):])
        if not os.path.exists(img):
            ng.append(f"og:image のファイルがない: {img}")
    if len(p.h1) != 1:
        warn.append(f"h1 が {len(p.h1)} 個（1個が基本）")
    if p.imgs_no_alt:
        warn.append(f"alt のない img が {p.imgs_no_alt} 個")

    # 構造化データ
    types = {}
    for raw in p.ld:
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as e:
            ng.append(f"ld+json が壊れている: {e}")
            continue
        types[obj.get("@type")] = obj
    for t in ("WebApplication", "FAQPage"):
        (ok if t in types else ng).append(f"構造化データ {t}" + ("" if t in types else " がない"))
    if "FAQPage" in types:
        ld_q = [html.unescape(q["name"]).strip() for q in types["FAQPage"].get("mainEntity", [])]
        vis_q = [s for s in p.summaries if s]
        missing = [q for q in vis_q if q not in ld_q]
        extra = [q for q in ld_q if q not in vis_q]
        if missing:
            ng.append("FAQ本文にあって FAQPage にない質問: " + " / ".join(missing))
        if extra:
            ng.append("FAQPage にあって本文にない質問: " + " / ".join(extra))
        if not missing and not extra:
            ok.append(f"FAQPage と本文のFAQが一致（{len(ld_q)}問）")

    # 文言ルール
    for w in MUST_TEXT:
        if w not in body:
            ng.append(f"本文に「{w}」がない（AGENTS.md の文言ルール）")
    for w in NG_TEXT:
        if w in body:
            ng.append(f"本文に出してはいけない言い方「{w}」がある")
    m = re.findall(r"(20\d\d)年(\d{1,2})月(\d{1,2})日", body)
    if not m:
        ng.append("自治体情報の確認日（YYYY年M月D日）が本文にない")
    else:
        ok.append("確認日: " + ", ".join(sorted({f"{y}-{int(mo):02d}-{int(da):02d}" for y, mo, da in m})))

    # サイト内リンク
    for h in p.hrefs:
        if h.startswith("/") and not h.startswith("//"):
            f = h.split("#")[0].split("?")[0]
            f = f.lstrip("/") or "index.html"
            if f.endswith("/"):
                f += "index.html"
            if not os.path.exists(os.path.join(root, f)):
                ng.append(f"リンク切れ（サイト内）: {h}")

    # sitemap / robots
    sm = open(os.path.join(root, "sitemap.xml"), encoding="utf-8").read()
    locs = re.findall(r"<loc>(.*?)</loc>", sm)
    mods = re.findall(r"<lastmod>(.*?)</lastmod>", sm)
    if SITE not in locs:
        ng.append("sitemap.xml にトップページがない")
    if len(mods) != len(locs) or any(not re.fullmatch(r"\d{4}-\d\d-\d\d", x) for x in mods):
        ng.append("sitemap.xml の lastmod が欠けているか形式違い")
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if not x.startswith(".") and x not in ("docs", "tools", "tests")]
        for fn in files:
            if fn != "index.html":
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), root)
            url = SITE + ("" if rel == "index.html" else rel[: -len("index.html")])
            if url not in locs:
                ng.append(f"sitemap.xml に入っていないページ: {url}")
    robots = open(os.path.join(root, "robots.txt"), encoding="utf-8").read()
    if SITE + "sitemap.xml" not in robots:
        ng.append("robots.txt に Sitemap の行がない")

    if external:
        check_external(src, warn, ok)

    for x in ok:
        print("OK  ", x)
    for x in warn:
        print("WARN", x)
    for x in ng:
        print("NG  ", x)
    print(f"\nNG {len(ng)} / WARN {len(warn)} / OK {len(ok)}")
    return 1 if ng else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sys.exit(main(args[0] if args else ".", "--external" in sys.argv))
