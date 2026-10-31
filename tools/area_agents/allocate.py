#!/usr/bin/env python3
"""エリア担当Agentの割り振りと、次に動かす担当・地域を決める。

  python3 tools/area_agents/allocate.py .          # 割り振り表を作り直す
  python3 tools/area_agents/allocate.py . --next   # 次に動かす担当と、今回見る地域を出す
  python3 tools/area_agents/allocate.py . --agent kansai   # その担当で今回見る地域

点数（月の検索の見込み）= max(キーワードプランナーの検索数, Search Console の表示回数/28日)。
GSC の数字は docs/area-agents/gsc.csv（列: page,clicks,impressions,position）があれば使う。
出力: tools/area_agents/assignments.json と docs/area-agents/assignments.md
台帳: docs/area-agents/ledger.json（runs = 動いた記録、areas = 地域ごとに最後に見た日）
"""
import csv, glob, json, math, os, re, sys
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_kw import areas as list_areas  # noqa: E402

PREF_RE = re.compile(r"\.(hokkaido|aomori|iwate|miyagi|akita|yamagata|fukushima|ibaraki|tochigi|gunma|saitama|chiba|tokyo|kanagawa|niigata|toyama|ishikawa|fukui|yamanashi|nagano|gifu|shizuoka|aichi|mie|shiga|kyoto|osaka|hyogo|nara|wakayama|tottori|shimane|okayama|hiroshima|yamaguchi|tokushima|kagawa|ehime|kochi|fukuoka|saga|nagasaki|kumamoto|oita|miyazaki|kagoshima|okinawa)\.(?:lg\.)?jp")


def load(root):
    g = json.load(open(os.path.join(HERE, "groups.json"), encoding="utf-8"))
    kw = json.load(open(os.path.join(HERE, "kw_area.json"), encoding="utf-8"))
    gsc = {}
    p = os.path.join(root, "docs/area-agents/gsc.csv")
    if os.path.exists(p):
        for r in csv.DictReader(open(p, encoding="utf-8")):
            m = re.search(r"/guide/([a-z]+)/", r.get("page", ""))
            if m:
                k = m.group(1)
                gsc[k] = gsc.get(k, 0) + int(float(r.get("impressions") or 0))
    ledger_p = os.path.join(root, "docs/area-agents/ledger.json")
    ledger = json.load(open(ledger_p, encoding="utf-8")) if os.path.exists(ledger_p) else {"runs": [], "areas": {}}
    return g, kw, gsc, ledger


def pref_of(root, key):
    p = os.path.join(root, "tools/guide/city", key + ".html")
    if not os.path.exists(p):
        return None
    hits = PREF_RE.findall(open(p, encoding="utf-8").read())
    return max(set(hits), key=hits.count) if hits else None


def region_of(root, key):
    p = os.path.join(root, "tools/guide/meta", key + ".json")
    return json.load(open(p, encoding="utf-8")).get("region") if os.path.exists(p) else None


def build(root):
    g, kw, gsc, ledger = load(root)
    by_key = {k: a["id"] for a in g["agents"] for k in a["keys"]}
    by_pref = {p: a["id"] for a in g["agents"] for p in a.get("prefs", [])}
    rows = []
    for key, name in list_areas(root).items():
        k = kw.get(key, {})
        vol = k.get("volume", 0)
        est = vol or g["no_data_volume"]
        score = max(est, gsc.get(key, 0))
        agent = by_key.get(key)
        if not agent:
            pref = pref_of(root, key)
            agent = by_pref.get(pref) or g["fallback_region"].get(region_of(root, key) or "", g["fallback_region"]["*"])
        tier = "A" if score >= g["tiers"]["A"] else "B" if score >= g["tiers"]["B"] else "C"
        rows.append({"key": key, "name": name, "agent": agent, "kw_volume": vol, "gsc_impressions": gsc.get(key),
                     "score": score, "tier": tier, "top": k.get("top", [])[:4]})
    rows.sort(key=lambda r: -r["score"])
    total = sum(r["score"] for r in rows)
    agents = []
    for a in g["agents"]:
        mine = [r for r in rows if r["agent"] == a["id"]]
        s = sum(r["score"] for r in mine)
        agents.append({"id": a["id"], "label": a["label"], "score": s, "share": round(s / total, 4),
                       "areas": len(mine), "tiers": {t: [r["key"] for r in mine if r["tier"] == t] for t in "ABC"}})
    return g, ledger, rows, agents, total


def write(root, g, rows, agents, total, gsc_used):
    out = {"generated": date.today().isoformat(), "total": total, "gsc": gsc_used, "agents": agents, "areas": rows}
    json.dump(out, open(os.path.join(HERE, "assignments.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    L = ["# エリア担当Agentの割り振り（自動生成・手で直さない）", "",
         f"- 作った日: {out['generated']}　/ 地域記事 {len(rows)}　/ 検索の見込み合計 月{total:,}",
         f"- 点数の元: キーワードプランナー（2026-10-31取得）{'＋ Search Console' if gsc_used else '（Search Console はまだ未使用）'}。データの無い市は月{g['no_data_volume']}と仮置き。",
         f"- 重さ: A＝月{g['tiers']['A']:,}以上（{g['revisit_days']['A']}日ごとに深く）、B＝{g['tiers']['B']:,}以上（{g['revisit_days']['B']}日ごと）、C＝それ未満（{g['revisit_days']['C']}日ごとに機械チェックだけ）",
         "- 作り直し: `python3 tools/area_agents/allocate.py .`（手順は tools/area_agents/AGENT.md）", "",
         "| 担当 | 受け持ち | 地域数 | 見込み/月 | 割合 | A | B | C |", "|---|---|---|---|---|---|---|---|"]
    name = {r["key"]: r["name"] for r in rows}
    for a in sorted(agents, key=lambda a: -a["score"]):
        t = a["tiers"]
        L.append(f"| `{a['id']}` | {a['label']} | {a['areas']} | {a['score']:,} | {a['share']:.0%} | "
                 f"{'・'.join(name[k] for k in t['A']) or '—'} | {'・'.join(name[k] for k in t['B']) or '—'} | {len(t['C'])}地域 |")
    L += ["", "## 地域ごと（見込みの多い順）", "", "| 地域 | 担当 | 重さ | 検索数 | GSC表示 | 主な語 |", "|---|---|---|---|---|---|"]
    for r in rows:
        top = "、".join(f"{q}({v:,})" for q, v in r["top"][:3])
        L.append(f"| {r['name']} | {r['agent']} | {r['tier']} | {r['kw_volume']:,} | {r['gsc_impressions'] if r['gsc_impressions'] is not None else '—'} | {top or '（未取得）'} |")
    open(os.path.join(root, "docs/area-agents/assignments.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    write_agents(root, g, rows, agents)


def write_agents(root, g, rows, agents):
    """担当ごとの .claude/agents/area-<id>.md（中身は受け持ちだけ。手順は AGENT.md）。"""
    d = os.path.join(root, ".claude/agents")
    for f in glob.glob(os.path.join(d, "area-*.md")):
        os.remove(f)
    name = {r["key"]: r["name"] for r in rows}
    for a in agents:
        t = a["tiers"]
        body = [
            "---",
            f"name: area-{a['id']}",
            f"description: hinata の地域記事のエリア担当「{a['label']}」。担当地域の記事を、検索の見込みが大きい順に公式と照合し、検索で取りこぼしている語に答える形で直す。この地域の記事の手直しを頼まれたとき・定期の巡回で使う。",
            "tools: Read, Grep, Glob, Bash, Edit, Write, WebFetch, WebSearch, Agent",
            "---", "",
            f"あなたは hinata.shiokonbu.com の地域記事のエリア担当 `{a['id']}`（{a['label']}）です。",
            "手順の正本は `tools/area_agents/AGENT.md`。最初に読み、そのとおりに1回ぶん進めてください。文言のルールは `AGENTS.md`、照合の仕方は `tools/article_review/AGENT.md`。", "",
            f"- 今回見る地域: `python3 tools/area_agents/allocate.py . --agent {a['id']}` が出したものだけ。",
            f"- 受け持ち: {a['areas']}地域・検索の見込み 月{a['score']:,}（全体の{a['share']:.0%}）。",
            f"- A（深く・{g['revisit_days']['A']}日ごと）: {'・'.join(name[k] for k in t['A']) or 'なし'}",
            f"- B（{g['revisit_days']['B']}日ごと）: {'・'.join(name[k] for k in t['B']) or 'なし'}",
            f"- C（機械チェックだけ・{g['revisit_days']['C']}日ごと）: {'・'.join(name[k] for k in t['C']) or 'なし'}",
            "- 受け持ち以外の記事・共通ページ・新しい市の記事は触らない（AGENT.md「受け持ちの線引き」）。",
            "- 批判役は `article-critic` に頼む。",
            "",
            "（このファイルは allocate.py が作る。受け持ちを変えるときは tools/area_agents/groups.json を直して作り直す）",
        ]
        open(os.path.join(d, f"area-{a['id']}.md"), "w", encoding="utf-8").write("\n".join(body) + "\n")


def due(g, ledger, rows, agent_id, today):
    """その担当で今回見る地域（見込みの多い順、予算まで）。"""
    picked, spent = [], 0.0
    seen = ledger.get("areas", {})
    for r in rows:
        if r["agent"] != agent_id:
            continue
        last = seen.get(r["key"], {}).get("checked")
        days = g["revisit_days"][r["tier"]]
        if last and date.fromisoformat(last) > today - timedelta(days=days):
            continue
        c = g["cost"][r["tier"]]
        if spent + c > g["budget_per_run"] + 1e-9:
            continue
        picked.append(r)
        spent += c
    return picked


def next_agent(g, ledger, rows, agents, today):
    """割合どおりに回るよう、直近60日で「割合に比べて動いていない」担当を選ぶ。やることの無い担当は飛ばす。"""
    since = today - timedelta(days=60)
    runs = [x for x in ledger.get("runs", []) if date.fromisoformat(x["date"]) >= since]
    n = len(runs) + 1
    cand = []
    for a in agents:
        done = sum(1 for x in runs if x["agent"] == a["id"])
        work = due(g, ledger, rows, a["id"], today)
        if work:
            # 遅れ（割合どおりなら動いているはずの回数との差）を整数で比べ、同じなら今回見る地域の見込みが大きい担当
            cand.append((math.floor(a["share"] * n - done), sum(r["score"] for r in work), a, work))
    if not cand:
        return None, []
    cand.sort(key=lambda c: (-c[0], -c[1]))
    return cand[0][2], cand[0][3]


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    g, ledger, rows, agents, total = build(root)
    gsc_used = os.path.exists(os.path.join(root, "docs/area-agents/gsc.csv"))
    today = date.today()
    if "--next" in sys.argv or "--agent" in sys.argv:
        if "--agent" in sys.argv:
            aid = sys.argv[sys.argv.index("--agent") + 1]
            a = next(x for x in agents if x["id"] == aid)
            work = due(g, ledger, rows, aid, today)
        else:
            a, work = next_agent(g, ledger, rows, agents, today)
            if not a:
                print("今日見る地域はありません（どの担当も見直しの間隔内）")
                return
        print(f"担当: {a['id']}（{a['label']}）")
        for r in work:
            top = "、".join(f"{q}({v:,})" for q, v in r["top"])
            print(f"- [{r['tier']}] {r['key']} {r['name']} 見込み{r['score']:,}/月  {top}")
        return
    write(root, g, rows, agents, total, gsc_used)
    for a in sorted(agents, key=lambda a: -a["score"]):
        print(f"{a['id']:14} {a['areas']:3}地域 {a['score']:>8,} {a['share']:.0%}  A{len(a['tiers']['A'])} B{len(a['tiers']['B'])} C{len(a['tiers']['C'])}")


if __name__ == "__main__":
    main()
