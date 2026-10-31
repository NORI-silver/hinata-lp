#!/usr/bin/env python3
"""記事チェックの機械的な下調べ（Python 3 の標準ライブラリだけで動く。サイトに依存しない）。

使い方:
  python3 tools/article_review/review.py <サイト設定.json> [--root DIR] [--external] [--out DIR] [--today YYYY-MM-DD]

サイトごとの違いは sites/<site>.json に書く（記事の場所・ルール・必要な情報・キーワード表など）。
記事は「ローカルのHTMLファイル」か「sitemap.xml の URL」から読む（WordPress は AGENT.md の手順で
HTML をフォルダに書き出してから local で読む）。

7つの観点ごとに、機械でわかる問題だけを拾う。事実が公式と合っているか・ありきたりか・
他サイトより親切か、の最終判断は AGENT.md の手順でAI（と批判役）がする。この出力はその下調べ。
結果は <out>/<site>-<日付>.json と .md（人とAIが読む）。
"""
import datetime as dt
import glob
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from html.parser import HTMLParser

CHECKS = {
    "accuracy": "1. 情報の正確さ",
    "links": "2. リンク",
    "seo": "3. SEO",
    "originality": "4. ありきたりでないか",
    "needs": "5. 困ったときに必要な情報",
    "visual": "6. 画像・図での説明",
    "freshness": "7. 最新の情報か",
}
SEV = {"high": 0, "mid": 1, "low": 2}


class Doc(HTMLParser):
    """1ページ分。本文（main/article の中）とリンク・見出し・画像を集める。"""

    def __init__(self, body_tags):
        super().__init__(convert_charrefs=True)
        self.body_tags = set(body_tags)
        self.title, self.meta, self.canon = "", {}, ""
        self.h = []          # (level, text)
        self.links = []      # (href, text)
        self.imgs = []       # alt
        self.figures = 0     # svg / figure / table（図表）
        self.tables = 0
        self.ld = []
        self.text, self.all_text = [], []
        self._stack, self._cap, self._a, self._depth = [], None, None, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in self.body_tags:
            self._depth += 1
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k:
                self.meta[k] = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canon = a.get("href", "")
        elif tag == "img" and self._depth > 0:
            self.imgs.append(a.get("alt") or "")
        elif tag in ("svg", "figure", "picture", "video") and self._depth > 0:
            self.figures += 1
        elif tag == "table" and self._depth > 0:
            self.tables += 1
        elif tag == "a" and a.get("href"):
            self._a = [a["href"], []]
        if tag in ("title", "h1", "h2", "h3") or (tag == "script" and a.get("type") == "application/ld+json"):
            self._cap = [tag, []]
        elif tag in ("script", "style", "noscript"):
            self._cap = ["skip", []]

    def handle_endtag(self, tag):
        if tag in self.body_tags:
            self._depth -= 1
        if tag == "a" and self._a:
            self.links.append((self._a[0], "".join(self._a[1]).strip()))
            self._a = None
        if self._cap and (tag == self._cap[0] or (self._cap[0] in ("skip", "script") and tag in ("script", "style", "noscript"))):
            kind, buf = self._cap
            s = "".join(buf).strip()
            if kind == "title":
                self.title = s
            elif kind in ("h1", "h2", "h3"):
                self.h.append((int(kind[1]), s))
            elif kind == "script":
                self.ld.append(s)
            self._cap = None

    def handle_data(self, d):
        if self._cap:
            self._cap[1].append(d)
            if self._cap[0] in ("skip", "script"):
                return
        if self._a:
            self._a[1].append(d)
        self.all_text.append(d)
        if self._depth > 0:
            self.text.append(d)


# ---------- 読み込み ----------

def load_pages(cfg, root):
    src = cfg["source"]
    pages = []
    if src["type"] in ("local", "wordpress"):
        # wordpress: AGENT.md の手順で <dump_dir>/<slug>.html に書き出したものを読む（canonical を URL に使う）
        base = os.path.join(root, src.get("root", src.get("dump_dir", ".")))
        files = sorted({f for g in src["include"] for f in glob.glob(os.path.join(base, g))})
        ex = [re.compile(x) for x in src.get("exclude", [])]
        for f in files:
            rel = os.path.relpath(f, base).replace(os.sep, "/")
            if any(x.search(rel) for x in ex):
                continue
            path = re.sub(r"(^|/)index\.html$", r"\1", rel)
            text = open(f, encoding="utf-8").read()
            m = re.search(r'<link rel="canonical" href="([^"]+)"', text)
            url = m[1] if src["type"] == "wordpress" and m else urllib.parse.urljoin(cfg["base_url"], path)
            pages.append({"file": rel, "url": url, "html": text})
    elif src["type"] == "sitemap":
        locs = re.findall(r"<loc>(.*?)</loc>", fetch(src["url"]))
        inc = [re.compile(x) for x in src.get("include", [".*"])]
        ex = [re.compile(x) for x in src.get("exclude", [])]
        for u in locs:
            if any(x.search(u) for x in inc) and not any(x.search(u) for x in ex):
                try:
                    pages.append({"file": u, "url": u, "html": fetch(u)})
                except Exception as e:
                    print("読めない:", u, e, file=sys.stderr)
    else:
        sys.exit(f"source.type が不明: {src['type']}")
    return pages


def fetch(u, timeout=20):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (article_review)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


# ---------- 日付 ----------

ERA = {"令和": 2018, "平成": 1988}


def find_dates(text):
    """本文中の年月（YYYY年M月、令和N年M月、令和N年度）を (date, 文脈) で返す。"""
    out = []
    for m in re.finditer(r"(20\d\d)年(\d{1,2})月(?:(\d{1,2})日)?", text):
        y, mo, d = int(m[1]), int(m[2]), int(m[3] or 1)
        if 1 <= mo <= 12:
            out.append((dt.date(y, mo, min(d, 28)), m.group(0), ctx(text, m)))
    for m in re.finditer(r"(令和|平成)(\d+|元)年(?:度|(\d{1,2})月)?", text):
        n = 1 if m[2] == "元" else int(m[2])
        y = ERA[m[1]] + n
        mo = int(m[3]) if m[3] else 4
        if 1 <= mo <= 12:
            out.append((dt.date(y, mo, 1), m.group(0), ctx(text, m)))
    return out


def ctx(text, m, w=40):
    return re.sub(r"\s+", " ", text[max(0, m.start() - w): m.end() + w]).strip()


# ---------- チェック本体 ----------

def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[。！？])|\n", text) if len(s.strip()) >= 12]


def norm_sentence(s, entity):
    if entity:
        s = s.replace(entity, "〇〇")
    return re.sub(r"[0-9０-９,，]+", "#", s)


def digits(s):
    return re.sub(r"\D", "", s)


def review(cfg, root, today, external=False):
    body_tags = cfg.get("body_tags", ["main", "article"])
    ent_re = re.compile(cfg["entity"]["regex"]) if cfg.get("entity") else None
    pages = load_pages(cfg, root)
    docs = []
    for p in pages:
        d = Doc(body_tags)
        d.feed(p["html"])
        body = "".join(d.text) or "".join(d.all_text)
        h1 = [t for lv, t in d.h if lv == 1]
        ent = None
        if ent_re and h1:
            m = ent_re.search(h1[0])
            ent = m.group(1) if m else None
        typ = "other"
        for t in cfg.get("types", []):
            if re.search(t["match"], p["file"]):
                typ = t["name"]
                break
        docs.append({**p, "doc": d, "body": body, "h1": h1, "entity": ent, "type": typ, "issues": []})

    entities = {x["entity"] for x in docs if x["entity"]}
    # 地域（entity）ごとの公式サイトのホスト：その地域名を文字に含むリンク先のホスト
    host_owner = defaultdict(Counter)
    for x in docs:
        if not x["entity"]:
            continue
        for href, txt in x["doc"].links:
            if href.startswith("http") and x["entity"] in txt:
                host_owner[urllib.parse.urlparse(href).netloc][x["entity"]] += 1
    # 電話番号 → それを載せている地域
    tel_owner = defaultdict(set)
    for x in docs:
        for href, _ in x["doc"].links:
            if href.startswith("tel:") and x["entity"]:
                tel_owner[digits(href)].add(x["entity"])
    # 文の出現回数（ありきたり判定）
    sent_count = Counter()
    for x in docs:
        x["sents"] = {norm_sentence(s, x["entity"]) for s in sentences(x["body"])}
        sent_count.update(x["sents"])
    desc_count = Counter(norm_sentence(x["doc"].meta.get("description", ""), x["entity"]) for x in docs)
    n_docs = len(docs)
    prio = load_priority(cfg, root)
    ext_cache = {}
    if external:  # 外部リンクはまとめて並列に確かめる（同じホストへは少しずつ）
        from concurrent.futures import ThreadPoolExecutor
        urls = sorted({h for x in docs for h, _ in x["doc"].links if h.startswith("http") and urllib.parse.urlparse(h).netloc != urllib.parse.urlparse(cfg["base_url"]).netloc})
        with ThreadPoolExecutor(8) as ex:
            ext_cache = dict(zip(urls, ex.map(check_url, urls)))

    for x in docs:
        d, body, ent, iss = x["doc"], x["body"], x["entity"], x["issues"]
        tcfg = next((t for t in cfg.get("types", []) if t["name"] == x["type"]), {})

        def add(check, sev, msg, hint=""):
            iss.append({"check": check, "sev": sev, "msg": msg, "hint": hint})

        # 1. 正確さ（機械でわかる食い違い）
        for href, txt in d.links:
            if href.startswith("tel:"):
                if digits(txt) and digits(txt) != digits(href):
                    add("accuracy", "high", f"電話番号の表示とリンク先が違う: 「{txt}」→ {href}")
                owners = tel_owner[digits(href)] - {ent}
                if ent and owners and not cfg.get("shared_tel_ok", {}).get(digits(href)):
                    add("accuracy", "mid", f"同じ電話番号が別の地域の記事にもある: {txt}（{'・'.join(sorted(owners))}）", "どちらかの写し間違いでないか、公式で確かめる")
        desc = d.meta.get("description", "")
        for num in set(re.findall(r"[\d,]+円", desc)):
            if num not in body:
                add("accuracy", "mid", f"description の金額「{num}」が本文にない", "本文と description のどちらが正しいか確かめる")
        for w in cfg.get("ng_text", []):
            if w in body:
                add("accuracy", "high", f"出してはいけない言い方「{w}」がある", "サイトのルール（rules）を見る")
        for rule in tcfg.get("must_text", cfg.get("must_text", [])):
            if rule not in "".join(d.all_text):
                add("accuracy", "mid", f"本文に「{rule}」がない", "サイトのルールで必ず書くことになっている")

        # 2. リンク
        seen_off = set()
        for href, txt in d.links:
            u = urllib.parse.urlparse(href)
            if href.startswith(("tel:", "mailto:", "#", "javascript:")):
                continue
            if href.startswith("/") or u.netloc == urllib.parse.urlparse(cfg["base_url"]).netloc:
                if cfg["source"]["type"] == "local" and not internal_exists(root, cfg, u.path):
                    add("links", "high", f"サイト内のリンク切れ: {href}")
                continue
            if u.scheme == "http":
                add("links", "low", f"http のリンク（https にできないか）: {href}")
            if not txt:
                add("links", "low", f"文字のないリンク: {href}")
            # 別の地域の名前がリンクの文字にある / 別の地域の公式ホストに飛ぶ
            if ent:
                others = [e for e in entities if e != ent and e in txt and ent not in txt and not (e in ent)]
                if others and x["type"] in cfg.get("entity_link_check_types", [x["type"]]):
                    add("links", "mid", f"リンクの文字が別の地域「{others[0]}」: {txt} → {href}", "引用として正しいか確かめる")
                owner = host_owner.get(u.netloc)
                if owner and ent not in owner and is_official(u.netloc, cfg) and x["type"] in cfg.get("entity_link_check_types", [x["type"]]):
                    top = owner.most_common(1)[0][0]
                    add("links", "high", f"別の地域（{top}）の公式サイトに飛ぶリンク: {txt} → {href}", "コピーしたまま直し忘れていないか")
            if is_official(u.netloc, cfg):
                seen_off.add(href)
            if external:
                if href not in ext_cache:
                    ext_cache[href] = check_url(href)
                st = ext_cache[href]
                if st:
                    add("links", "high" if st.startswith(("404", "410")) else "mid", f"外部リンクが開けない（{st}）: {txt} → {href}")
        if tcfg.get("need_official_link") and not seen_off:
            add("links", "high", "公式サイトへのリンクが1つもない")

        # 3. SEO
        title = d.title
        tr, dr = cfg.get("title_range", [28, 35]), cfg.get("desc_range", [80, 120])
        if not (tr[0] <= len(title) <= tr[1] + 5):
            add("seo", "low", f"title {len(title)}字（目安{tr[0]}〜{tr[1]}）: {title}")
        if not desc:
            add("seo", "high", "description がない")
        elif not (dr[0] <= len(desc) <= dr[1] + 20):
            add("seo", "low", f"description {len(desc)}字（目安{dr[0]}〜{dr[1]}）")
        if desc and desc_count[norm_sentence(desc, ent)] > 1:
            add("seo", "mid", f"description が他の{desc_count[norm_sentence(desc, ent)] - 1}記事と地名以外同じ", "その地域だけの数字や特徴を入れる")
        if len(x["h1"]) != 1:
            add("seo", "mid", f"h1 が {len(x['h1'])} 個")
        for kw in tcfg.get("title_keywords", []):
            kw = kw.replace("{entity}", ent or "")
            if kw and kw not in title:
                add("seo", "mid", f"title に「{kw}」がない")
        if d.canon and d.canon != x["url"]:
            add("seo", "high", f"canonical が違う: {d.canon}（この記事は {x['url']}）")
        for raw in d.ld:
            try:
                json.loads(raw)
            except json.JSONDecodeError as e:
                add("seo", "high", f"構造化データ（ld+json）が壊れている: {e}")
        h2 = [t for lv, t in d.h if lv == 2]
        if x["type"] != "other" and len(h2) < tcfg.get("min_h2", 3):
            add("seo", "mid", f"h2 が {len(h2)} 個だけ（目安 {tcfg.get('min_h2', 3)} 以上）")
        if d.imgs.count(""):
            add("seo", "low", f"alt のない画像が {d.imgs.count('')} 個")
        if ent and prio.get(ent):
            x["priority"] = prio[ent]

        # 4. ありきたり
        if x["sents"]:
            common = [s for s in x["sents"] if sent_count[s] >= max(3, n_docs * cfg.get("common_share", 0.3))]
            uniq_chars = sum(len(s) for s in x["sents"] if sent_count[s] == 1)
            ratio = len(common) / len(x["sents"])
            x["boilerplate"] = round(ratio, 2)
            x["unique_chars"] = uniq_chars
            if ratio >= cfg.get("boilerplate_warn", 0.5):
                add("originality", "mid", f"文の {ratio:.0%} が多くの記事と同じ定型文（この記事だけの文は約{uniq_chars}字）", "その地域・テーマだけの具体的な情報を足す")
            elif uniq_chars < tcfg.get("min_unique_chars", 0):
                add("originality", "mid", f"この記事だけの文が約{uniq_chars}字と少ない（目安 {tcfg.get('min_unique_chars')}字以上）")

        # 5. 困ったときに必要な情報
        for need in tcfg.get("needs", []):
            hay = body + "\n" + "\n".join(h for h, _ in d.links)
            if not any(re.search(p, hay) for p in need["any"]):
                add("needs", need.get("sev", "mid"), f"「{need['label']}」が見当たらない", need.get("hint", ""))

        # 6. 画像・図
        vis = len([a for a in d.imgs]) + d.figures
        x["visuals"] = vis
        x["tables"] = d.tables
        want = tcfg.get("visual_when", [])
        hits = [w for w in want if w in body]
        if vis == 0 and hits:
            add("visual", "low", f"画像・図が0（本文に「{'・'.join(hits[:3])}」など、図にすると伝わりやすい説明がある）", "手順・大きさの測り方・券の貼り方などを図にできないか")

        # 7. 最新か
        chk = None
        cre = cfg.get("checked_regex")
        if cre:
            m = re.search(cre, "".join(d.all_text))
            if m:
                chk = dt.date(int(m[1]), int(m[2]), int(m[3]))
        x["checked"] = chk.isoformat() if chk else None
        stale = cfg.get("stale_days", 180)
        if x["type"] != "other":
            if not chk and cre:
                add("freshness", "mid", "確認日が書かれていない")
            elif chk and (today - chk).days > stale:
                add("freshness", "mid", f"確認日 {chk} から {(today - chk).days} 日たっている（目安 {stale} 日）", "公式ページを見直して確認日を更新")
        soon = cfg.get("soon_days", 120)
        for dte, raw, c in find_dates(body):
            if re.search(r"(から|より|予定|改定|変わ|変更|開始|始ま|終了|まで)", c[c.find(raw):c.find(raw) + len(raw) + 15]):
                if today < dte <= today + dt.timedelta(days=soon):
                    add("freshness", "mid", f"もうすぐ変わる予定（{raw}）: …{c}…", "その日が来たら記事を直す。期限の一覧に入れる")
                elif today - dt.timedelta(days=400) <= dte <= today and re.search(r"(予定|検討|変わります|始まります|になります)", c):
                    add("freshness", "high", f"過ぎた日付を「これから」と書いている可能性（{raw}）: …{c}…", "いまの状態に書き直す")
            if dte.year <= today.year - cfg.get("old_source_years", 3) and re.search(r"(資料|現在|時点|出典|料金表)", c):
                add("freshness", "low", f"古い年の資料に頼っている可能性（{raw}）: …{c}…", "新しい資料がないか公式で探す")
    return docs


def is_official(host, cfg):
    return any(host.endswith(h) or h in host for h in cfg.get("official_hosts", []))


def internal_exists(root, cfg, path):
    base = os.path.join(root, cfg["source"].get("root", cfg["source"].get("dump_dir", ".")))
    f = urllib.parse.unquote(path).lstrip("/") or "index.html"
    if f.endswith("/"):
        f += "index.html"
    return os.path.exists(os.path.join(base, f)) or os.path.exists(os.path.join(base, f, "index.html"))


def check_url(u):
    try:
        req = urllib.request.Request(u, method="GET", headers={"User-Agent": "Mozilla/5.0 (article_review)"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return "" if r.status < 400 else str(r.status)
    except urllib.error.HTTPError as e:
        return str(e.code)
    except Exception as e:
        return f"接続できない {type(e).__name__}"


def load_priority(cfg, root):
    """キーワード表（markdown の | 名前 | 検索数 | の行）から、地域ごとの検索数を読む。"""
    p = cfg.get("priority_table")
    if not p or not os.path.exists(os.path.join(root, p)):
        return {}
    out = {}
    for line in open(os.path.join(root, p), encoding="utf-8"):
        m = re.match(r"\|\s*([^|]+?)※?\s*\|\s*([\d,]+)\s*\|", line)
        if m:
            out.setdefault(m[1].strip(), int(m[2].replace(",", "")))
    return out


# ---------- 出力 ----------

def write_report(cfg, docs, today, out):
    os.makedirs(out, exist_ok=True)
    stem = os.path.join(out, f"{cfg['name']}-{today.isoformat()}")
    rows = []
    for x in docs:
        rows.append({k: x.get(k) for k in ("file", "url", "type", "entity", "checked", "priority", "boilerplate", "unique_chars", "visuals", "issues")})
    json.dump({"site": cfg["name"], "date": today.isoformat(), "pages": rows}, open(stem + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    cnt = Counter((i["check"], i["sev"]) for x in docs for i in x["issues"])
    L = [f"# 記事チェック（機械の下調べ）: {cfg['name']} {today}", "",
         f"対象 {len(docs)} ページ。ここに出るのは機械でわかる問題だけ。事実の確認・ありきたりか・他より親切かは AGENT.md の手順でAIが判断する。", "",
         "| 観点 | 重い | 中 | 軽い |", "|---|---|---|---|"]
    for k, label in CHECKS.items():
        L.append(f"| {label} | {cnt[(k, 'high')]} | {cnt[(k, 'mid')]} | {cnt[(k, 'low')]} |")
    # 深く見る順（検索数 × 問題の重さ）
    def score(x):
        return (x.get("priority") or 0) * (1 + sum(3 - SEV[i["sev"]] for i in x["issues"]))
    top = sorted([x for x in docs if x["type"] != "other"], key=score, reverse=True)[:15]
    L += ["", "## AIが深く見る順（検索数 × 問題）", ""]
    for x in top:
        L.append(f"- {x.get('entity') or x['file']}（検索 {x.get('priority') or '-'}／問題 {len(x['issues'])}／定型文 {x.get('boilerplate')}）: {x['url']}")
    # 定型文が多い順
    L += ["", "## ありきたり度（定型文の割合が高い順・上位10）", ""]
    for x in sorted(docs, key=lambda x: -(x.get("boilerplate") or 0))[:10]:
        L.append(f"- {x.get('entity') or x['file']}: 定型文 {x.get('boilerplate')}・この記事だけの文 約{x.get('unique_chars')}字")
    L += ["", "## ページごとの問題（重い順）", ""]
    for x in sorted(docs, key=lambda x: min([SEV[i["sev"]] for i in x["issues"]] or [9])):
        if not x["issues"]:
            continue
        L.append(f"### {x.get('entity') or ''} {x['file']}")
        for i in sorted(x["issues"], key=lambda i: SEV[i["sev"]]):
            L.append(f"- [{ {'high': '重い', 'mid': '中', 'low': '軽い'}[i['sev']] }] {CHECKS[i['check']]}: {i['msg']}" + (f"（{i['hint']}）" if i["hint"] else ""))
        L.append("")
    open(stem + ".md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    return stem


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("-"):
        sys.exit(__doc__)
    cfg = json.load(open(args[0], encoding="utf-8"))
    opt = lambda k, d=None: args[args.index(k) + 1] if k in args else d
    root = opt("--root", cfg.get("repo_root", "."))
    today = dt.date.fromisoformat(opt("--today", dt.date.today().isoformat()))
    out = opt("--out", cfg.get("report_dir", "docs/article-review"))
    docs = review(cfg, root, today, "--external" in args)
    stem = write_report(cfg, docs, today, out)
    n = Counter(i["sev"] for x in docs for i in x["issues"])
    print(f"{len(docs)} ページ: 重い {n['high']} / 中 {n['mid']} / 軽い {n['low']} → {stem}.md")


if __name__ == "__main__":
    main()
