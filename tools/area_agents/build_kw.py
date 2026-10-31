#!/usr/bin/env python3
"""キーワードプランナーのCSV（UTF-16・タブ区切り）から、地域ごとの検索数をまとめる。

  python3 tools/area_agents/build_kw.py . <volumes.csv> [<ideas.csv> ...]

出力: tools/area_agents/kw_area.json
  {key: {"name": 横浜市, "volume": 地域名を含む粗大ごみ系の語の合計, "top": [[語, 月間], ...]}}
地域の一覧は guide/<key>/index.html の title（「〇〇市の…」）から取る。
CSV は Nori さんの Mac ~/Downloads/hinata-kw-*.csv（キーワードプランナー 2026-10-31取得）。
"""
import json, re, sys, glob, os

SKIP = {"fees", "late", "problem", "scam", "new-home", "how-to-check", "mochikomi",
        "shoriken", "size", "item", "kaden"}
SUF = "(粗大|大型|ごみ|ゴミ|持ち込|持込)"


def load_csv(path):
    lines = open(path, "rb").read().decode("utf-16").splitlines()
    hdr = next(i for i, l in enumerate(lines) if l.startswith("Keyword\t"))
    cols = lines[hdr].split("\t")
    i = cols.index("Avg. monthly searches")
    out = {}
    for l in lines[hdr + 1:]:
        c = l.split("\t")
        if not c[0] or len(c) <= i:
            continue
        try:
            out[c[0].replace(" ", "")] = float(c[i] or 0)
        except ValueError:
            pass
    return out


def areas(root):
    res = {}
    for p in sorted(glob.glob(os.path.join(root, "guide/*/index.html"))):
        k = p.split("/")[-2]
        if k in SKIP:
            continue
        t = re.search(r"<title>(.*?)</title>", open(p, encoding="utf-8").read(), re.S).group(1)
        m = re.match(r"(.+?[都道府県市区町村])の", t)
        if m:
            res[k] = m.group(1)
    return res


def main():
    root, csvs = sys.argv[1], sys.argv[2:]
    kw = {}
    for c in csvs:
        kw.update(load_csv(c))
    out = {}
    for k, name in areas(root).items():
        stem = re.sub(r"[市区町村]$", "", name)
        hits = [(q, int(v)) for q, v in kw.items()
                if q.startswith(name) or re.match(re.escape(stem) + SUF, q)]
        hits.sort(key=lambda x: -x[1])
        out[k] = {"name": name, "volume": sum(v for _, v in hits), "top": hits[:6]}
    dst = os.path.join(root, "tools/area_agents/kw_area.json")
    json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=0, sort_keys=True)
    print(f"{len(out)} 地域 → {dst}（検索数あり {sum(1 for v in out.values() if v['volume'])}）")


if __name__ == "__main__":
    main()
