# 口コミ部品（reviews.js と backend/reviews.gs）の AREAS を、地域記事の市区（data/areas.js）から作り直す
#   値は地図サービスで検索するときの市区名。東京23区と府中市は同じ名前がほかの県にもあるので「東京都」を付ける。
#   backend/reviews.gs を変えたら、Apps Script「hinata 口コミ」に貼り直して、同じデプロイの新しいバージョンを出す（URLは変えない）。
import json,os,re,sys
ROOT=sys.argv[1]
s=open(os.path.join(ROOT,"data/areas.js"),encoding="utf-8").read()
A=json.loads(s[s.index("{"):s.rindex("}")+1])
TOKYO={"fuchu"}
def q(k):
    n=A[k]["n"]
    return "東京都"+n if n.endswith("区") or k in TOKYO else n
first=["yokohama","kawasaki","setagaya","suginami","saitama","chiba","sakura"]
keys=first+sorted(k for k in A if k not in first)
for f,quote in [("reviews.js",'"'),("backend/reviews.gs","'")]:
    p=os.path.join(ROOT,f); t=open(p,encoding="utf-8").read()
    body=", ".join(f"{k}:{quote}{q(k)}{quote}" for k in keys)
    t2=re.sub(r"var AREAS = \{[^}]*\};",lambda m:"var AREAS = {"+body+"};",t,count=1)
    assert t2!=t or body in t, f
    open(p,"w",encoding="utf-8").write(t2)
print("reviews areas",len(keys))
