# 一覧ページの地域セクション・トップのリンク・sitemap を gencity の C/REGION から作り直す
import re,json,sys,os,importlib.util
ROOT=sys.argv[1]
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"gencity.py"),encoding="utf-8").read()
ns={"__file__":os.path.join(os.path.dirname(os.path.abspath(__file__)),"gencity.py"),"sys":sys,"os":os}; exec("import json,os,re,sys\n"+src.split("fees=open")[0].split("\n",1)[1].replace("ROOT=sys.argv[1];","ROOT=\"\";"),ns)
C,REGION,RORDER=ns["C"],ns["REGION"],ns["RORDER"]
SITE="https://hinata.shiokonbu.com"
p=os.path.join(ROOT,"guide/index.html"); s=open(p,encoding="utf-8").read()
blocks=[]
for r in RORDER:
    ks=[k for k in C if REGION[k]==r]
    if not ks: continue
    cards="".join(f'<a class="card" href="/guide/{k}/"><b>{C[k][0]}の粗大ごみ</b><span>申し込み・料金・持ち込み・家電の出し方と近くの買取店。</span></a>' for k in ks)
    blocks.append(f'    <h3 style="font-size:16px;margin:24px 0 10px">{r}</h3>\n    <div class="cards">{cards}</div>\n')
sec='    <!-- area:start -->\n    <h2 id="area" style="font-size:20px;margin:40px 0 12px">地域ごとの粗大ごみの出し方</h2>\n    <p>お住まいの市町村の記事がないときは、<a href="/guide/how-to-check/">自分の市町村の調べ方</a>を見てください。</p>\n'+"".join(blocks)+'    <!-- area:end -->\n'
if "<!-- area:start -->" in s:
    s=re.sub(r"    <!-- area:start -->.*?<!-- area:end -->\n",sec,s,flags=re.S)
else:
    s=re.sub(r'    <h2 style="font-size:20px;margin:40px 0 12px">地域ごとの粗大ごみの出し方</h2>\n    <div class="cards">.*?</div>\n',sec,s,flags=re.S)
m=re.search(r'(<script type="application/ld\+json">\n)(\{"@context": "https://schema.org", "@type": "ItemList".*?)(\n</script>)',s,re.S)
d=json.loads(m.group(2))
items=[x for x in d["itemListElement"] if not any(x["url"].endswith(f"/guide/{k}/") for k in C)]
for k in C: items.append({"@type":"ListItem","url":f"{SITE}/guide/{k}/","name":C[k][1].split("｜")[0]})
for i,x in enumerate(items): x["position"]=i+1
d["itemListElement"]=items
s=s[:m.start(2)]+json.dumps(d,ensure_ascii=False)+s[m.end(2):]
open(p,"w",encoding="utf-8").write(s)
# sitemap
p=os.path.join(ROOT,"sitemap.xml"); s=open(p,encoding="utf-8").read()
for k in C:
    u=f"{SITE}/guide/{k}/"
    if u not in s: s=s.replace("</urlset>",f"  <url><loc>{u}</loc><lastmod>2026-10-30</lastmod></url>\n</urlset>")
open(p,"w",encoding="utf-8").write(s)
print("hub ok",len(C))
