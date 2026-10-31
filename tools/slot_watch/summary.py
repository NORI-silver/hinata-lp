"""空き枠見張りの記録（CSV）から「最短収集日が前より早くなった＝キャンセル等で空きが出た」回を数える。
使い方: python3 tools/slot_watch/summary.py /mnt/project-files/slot-watch/chiba.csv
"""
import csv, re, sys
from collections import defaultdict

def day(s):
    m = re.match(r'(\d{4})年(\d{2})月(\d{2})日', s)
    return '-'.join(m.groups()) if m else None

rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8')))
last, opens, checks, errors = {}, defaultdict(list), defaultdict(int), 0
for r in rows:
    k = (r['city'], r['ward'])
    d = day(r['earliest'])
    if not d:
        errors += 1
        continue
    checks[k] += 1
    if k in last and d < last[k]:
        opens[k].append(f"{r['checked_at_jst']} {last[k]}→{d}")
    last[k] = d
print(f"記録 {len(rows)} 行 / 読めなかった回 {errors}")
for k in sorted(checks):
    print(f"{k[0]} {k[1]}: 確認 {checks[k]} 回, 早まった回 {len(opens[k])}, いまの最短 {last[k]}")
    for o in opens[k]:
        print('   ', o)
