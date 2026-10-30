# テーマ別のまとめページを、地域記事の元データ（city/*.html と data/areas.js）から作る
#   /guide/mochikomi/  粗大ごみの持ち込み（市区ごとの持込先）
#   /guide/shoriken/   粗大ごみ処理券（シール）の買い方・貼り方（市区ごとの料金と払い方）
#   /guide/item/<key>/ 品目別の捨て方（市区ごとの粗大ごみ料金の比較）
# キーワードは docs/keywords.md（キーワードプランナー 2026-10-31）。gencity.py → hub.py → areas.py のあとに実行する。
import json,os,re,sys
ROOT=sys.argv[1]; HERE=os.path.dirname(os.path.abspath(__file__)); CD=os.path.join(HERE,"city")
SITE="https://hinata.shiokonbu.com"; DATE="2026-10-31"; CHECK="2026年10月30日"
src=open(os.path.join(HERE,"gencity.py"),encoding="utf-8").read()
_cwd=os.getcwd(); os.chdir(ROOT)
ns={"__file__":os.path.join(HERE,"gencity.py"),"sys":sys,"os":os}; exec("import json,os,re,sys\n"+src.split("fees=open")[0].split("\n",1)[1].replace("ROOT=sys.argv[1];","ROOT=\"\";"),ns)
os.chdir(_cwd)
C,REGION,RORDER=ns["C"],ns["REGION"],ns["RORDER"]
s=open(os.path.join(ROOT,"data/areas.js"),encoding="utf-8").read()
A=json.loads(s[s.index("{"):s.rindex("}")+1])
fees=open(os.path.join(ROOT,"guide/fees/index.html"),encoding="utf-8").read()
HEAD_TPL=fees.split("<title>")[0]
FOOT=fees[fees.index("  <footer class=\"foot\">"):]
FONTS=re.search(r'<link rel="icon".*?guide\.css">\n',fees,re.S).group(0)
ORDER=[k for r in RORDER for k in C if REGION[k]==r]
def pt(k): return {x[0]:x[1] for x in A[k]["pt"]}

def page(path,title,desc,crumb,h1,lead,body):
    url=f"{SITE}{path}"
    art={"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,"inLanguage":"ja","datePublished":DATE,"dateModified":DATE,"mainEntityOfPage":url,"image":SITE+"/og.png","author":{"@type":"Organization","name":"粗大ごみ手配ナビ","url":SITE+"/"},"publisher":{"@type":"Organization","name":"粗大ごみ手配ナビ","url":SITE+"/"}}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"トップ","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"粗大ごみの基礎知識","item":SITE+"/guide/"},{"@type":"ListItem","position":3,"name":crumb,"item":url}]}
    h=HEAD_TPL+f'''<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="粗大ごみ手配ナビ">
<meta property="og:locale" content="ja_JP">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0A74B8">
{FONTS}<script type="application/ld+json">
{json.dumps(art,ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(bc,ensure_ascii=False)}
</script>
</head>
<body>
<div class="wrap">
  <div class="top">
    <a class="brand" href="/"><svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="9" fill="#0A74B8"/><g fill="none" stroke="#fff" stroke-width="2.4" stroke-linejoin="round"><path d="M7 13h18v12H7z"/><path d="M5 9h22v4H5z"/><path d="M13 9V7h6v2"/></g></svg>粗大ごみ手配ナビ</a>
    <small>無料・登録なし</small>
  </div>
  <nav aria-label="パンくず"><ol class="crumb"><li><a href="/">トップ</a></li><li><a href="/guide/">粗大ごみの基礎知識</a></li><li aria-current="page">{crumb}</li></ol></nav>
  <header class="hero">
    <h1>{h1}</h1>
    <p>{lead}</p>
    <p class="meta">{CHECK}に各市区の公式ページで確認・料金や日数は目安です</p>
  </header>
  <article>
{body}
  </article>
  <a class="cta" href="/">
    <b>あなたの粗大ごみ、どう出すのがいい？</b>
    <span>引越し日と出したい物を入れると、品目ごとに使える出し方と料金の目安がわかります。無料で、入力内容はどこにも送りません。</span>
    <span class="go">無料で診断する</span>
  </a>
  <section class="related" aria-label="ほかの記事">
    <h2>あわせて読みたい</h2>
    <div class="cards">{RELATED.replace(f'<a class="card" href="{path}">','<a class="card" hidden href="#">')}</div>
  </section>
'''
    p=os.path.join(ROOT,path.strip("/"),"index.html"); os.makedirs(os.path.dirname(p),exist_ok=True)
    out=h+FOOT
    out=re.sub(r'<a class="card" hidden href="#">.*?</a>','',out)
    open(p,"w",encoding="utf-8").write(out)
    print(path,len(title),len(desc))

def cityrow(k,cell):
    n=C[k][0]
    return f'<tr><th scope="row"><a href="/guide/{k}/">{n}</a></th><td>{cell}</td></tr>'

# ---------- 持ち込み ----------
# areas.js のポイント欄に「持ち込み」がない市区は、記事本文の持ち込みの節から要点を書いた
MOCHI={
 "bunkyo":"区の公式ページに記載が見当たらない（文京清掃事務所 03-3813-6661 に問い合わせ）",
 "hamamatsu":"前日か当日に連絡ごみ受付センターへ電話し、納付済証を貼って市の施設へ（軽トラック1台分まで）",
 "hiroshima":"安佐南工場 大型ごみ破砕処理施設へ、予約不要・平日9:00〜16:00。手数料は原則なし（木製家具やふとんなどは有料）",
 "kawasaki":"市の粗大ごみのページに持ち込みの案内がない（粗大ごみ受付センターに相談）",
 "kitakyushu":"市の3つの工場へ予約不要・10kgごとに150円（2027年9月から230円の予定）。写真つきの本人確認書類が必要",
 "kobe":"市の自己搬入の案内に従う（施設・料金は市の公式ページで確認）",
 "kumamoto":"東部環境工場（燃えるもの）・扇田環境センター（燃えないもの）へ。日曜以外、10kgごとに150円",
 "nagoya":"区の環境事業所で手続きしてから処理施設へ。10kgごとに270円",
 "nakano":"区の公式ページに記載が見当たらない（中野区清掃事務所 03-3387-5353 に問い合わせ）",
 "niigata":"住んでいる区で決まった清掃センターなどへ。10kgごとに100円（現金のみ）",
 "osaka":"市の案内に記載が見当たらない（区の環境事業センターに問い合わせ）",
 "sagamihara":"北部・南部の粗大ごみ受入施設と津久井クリーンセンターへ、予約不要。10kgごとに240円",
 "sakai":"クリーンセンター臨海工場・東工場へ（要予約）。粗大ごみは1回100kgまで1,700円",
 "sendai":"今泉・葛岡・松森工場へ平日に。1回100kgまで1,500円（現金のみ）",
 "shizuoka":"西ケ谷・沼上清掃工場へ（料金は市のページか各工場で確認）",
 "sumida":"区の公式ページに記載が見当たらない（すみだ清掃事務所 03-3613-2228 に相談）",
 "toshima":"区の公式ページに記載が見当たらない（ごみ減量推進課 03-3981-1320 に問い合わせ）",
 "yokohama":"市内4か所の自己搬入ヤードへ（要申込・ネットは当日15時まで）。手数料は収集と同じで、先にシールを買っておく",
}
# 要点も辞書もない市は、記事の出典で確かめてもらう（新しい市を足したときに止まらないように）
FALLBACK="記事と市区の公式ページで確認"
rows="".join(cityrow(k,pt(k).get("持ち込み") or MOCHI.get(k,FALLBACK)) for k in ORDER)
mochi_body=f'''    <h2>粗大ごみの持ち込みとは</h2>
    <p>粗大ごみを自分の車で市区の施設へ運んで出す方法です。収集の予約が先まで埋まっているときや、引越しまで日がないときに使えます。予約がいらない市（札幌市・相模原市・北九州市・広島市など）や、収集より安い区（板橋区・葛飾区は半額、江戸川区は自転車が収集900円に対し持ち込み400円）もあります。</p>
    <p>一方で、持ち込みを受け付けていない区（江東区・目黒区・中央区など）や、公式ページに案内が見当たらない市区もあります。まず下の一覧で、お住まいの市区を確かめてください。</p>

    <h2>持ち込む前に確かめること</h2>
    <ol>
      <li><b>予約がいるか</b>：要申込の市区が多く、日曜だけ・指定日だけの施設もあります。</li>
      <li><b>料金と払い方</b>：無料、品目ごと（処理券やシールを先に買う）、重さで現金払い（10kgごとに100円〜270円など）と市区で違います。</li>
      <li><b>本人確認書類</b>：その市区に住んでいて、自分の家のごみかを確かめる市区が多く、運転免許証などを求められます。</li>
      <li><b>回数と量の上限</b>：1回10個まで・年度内3回までなどの決まりがある区があります。</li>
      <li><b>荷下ろしは自分で</b>：施設の人は手伝ってくれないことが多いので、2人で行くと安心です。</li>
    </ol>
    <p>家電4品目（エアコン・テレビ・冷蔵庫と冷凍庫・洗濯機と衣類乾燥機）は、市区の施設には持ち込めません。家電リサイクル券を買って指定引取場所へ運びます（<a href="/guide/fees/">出し方と料金</a>）。</p>
    <p>持ち込めるのは、その市区に住む人の家のごみを本人が運ぶ場合だけです。家のごみを代わりに運べるのは市区の許可業者だけで、「無料で回収します」という巡回の業者に頼むのはやめましょう（<a href="/guide/scam/">ぼったくりの実例と見分け方</a>）。</p>

    <h2>市区ごとの持ち込み先</h2>
    <p>市区名を押すと、その市区の記事（申し込み・料金・家電・買取店）が開きます。施設の住所・受付時間・最新の料金は、記事の出典から市区の公式ページで確かめてください。</p>
    <table class="cmp"><thead><tr><th scope="col">市区</th><th scope="col">持ち込み（{CHECK}確認）</th></tr></thead><tbody>{rows}</tbody></table>
'''

# ---------- 処理券 ----------
PAY={
 "kyoto":"品目ごとに400円・800円・1,200円・2,000円など（払い方は記事で確認）",
 "shizuoka":"戸別収集の手数料は市の不燃・粗大ごみのページに記載がない（受付センターで確認）",
}
def paycell(k):
    p=pt(k); xs=[x for x in (p.get("料金"),p.get("支払い")) if x]
    return "<br>".join(xs) if xs else PAY.get(k,FALLBACK)
rows="".join(cityrow(k,paycell(k)) for k in ORDER)
ken_body=f'''    <h2>粗大ごみ処理券（シール）とは</h2>
    <p>粗大ごみの手数料を前払いした印です。申し込みのときに言われた金額分を買い、出す物に貼っておきます。呼び方は市区で違い、東京23区の「有料粗大ごみ処理券」、横浜市の「粗大ごみ収集シール」、名古屋市や仙台市の「納付券」、神戸市の「大型ごみシール券」、浜松市の「納付済証」などがあります。</p>

    <h2>買い方</h2>
    <ol>
      <li><b>先に申し込む</b>：品目ごとの金額は申し込みのときにわかります。払い戻しや再発行ができない市区が多いので、申し込んでから買います。</li>
      <li><b>取扱所で買う</b>：多くの市区で、コンビニやスーパー、ドラッグストアなどの取扱所（目印のステッカーがあるお店）で買えます。区役所や出張所で買える市区もあります。</li>
      <li><b>ネット申込ならキャッシュレスも</b>：横浜市・大阪市・名古屋市・練馬区・台東区などは、ネットで申し込むとクレジットカードやPayPayで払え、券がいらない場合があります。</li>
    </ol>
    <p>処理券はその市区だけで使えます。前に住んでいた市区の券は使えないと、世田谷区や荒川区ははっきり書いています。</p>

    <h2>貼り方</h2>
    <ul>
      <li>受付番号や名前など、市区に言われたことを券に書いてから貼ります。</li>
      <li>収集の人から見やすい所に、1品ずつ貼ります。はがれやすい物はテープで留めると安心です。</li>
      <li>台紙や領収証は、収集が終わるまで取っておきます（仙台市・広島市などが案内）。</li>
    </ul>
    <p>書き方や貼る場所の細かい決まりは市区で違います。お住まいの市区の記事から公式ページを確かめてください。持ち込みのときも、処理券を先に買っておく市区（横浜市・浜松市など）と、施設で重さに応じて現金で払う市区があります（<a href="/guide/mochikomi/">粗大ごみの持ち込み</a>）。</p>

    <h2>市区ごとの料金と払い方</h2>
    <table class="cmp"><thead><tr><th scope="col">市区</th><th scope="col">料金と払い方（{CHECK}確認）</th></tr></thead><tbody>{rows}</tbody></table>
'''

# ---------- 品目別 ----------
def tablerows(k):
    t=open(os.path.join(CD,k+".html"),encoding="utf-8").read()
    for tb in re.findall(r"<table.*?</table>",t,re.S):
        for tr in re.findall(r"<tr>(.*?)</tr>",tb,re.S):
            cells=[re.sub(r"<[^>]+>","",c).strip() for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>",tr,re.S)]
            price=[c for c in cells if re.fullmatch(r"[\d,]+円.*",c)]
            if len(cells)<2 or not price: continue
            yield [c for c in cells if c not in price],price[0]
ITEMS=[
 ("futon","布団","布団",["布団","ふとん"],"",
  "布団（ふとん）の捨て方・処分方法",
  '''    <p>布団は、多くの市区で粗大ごみとして出せる品目です。料金は1枚あたり数百円の市区が多く、下の表のように市区で違います。市区によっては、小さく切ったりひもで縛ったりして燃やすごみに出せる場合もあるので、お住まいの市区の分け方で確かめてください。</p>
    <p>まだ使える布団でも、リサイクルショップの買取はあまり期待できません。引越しで急ぐなら、市区の粗大ごみか持ち込みが確実です。</p>
'''),
 ("sofa","ソファ","ソファ",["ソファ"],r"（ソファ[^）]*(以外|除く)）|ソファーベッド",
  "ソファの捨て方・処分方法",
  '''    <p>ソファは大きさ（1人掛け・2人掛け以上）やスプリングの有無で料金が変わる市区が多く、粗大ごみの中では高めの品目です。玄関や階段から出せるか、収集の日に家の前まで運べるかも先に考えておきます。</p>
    <p>まだきれいなソファは、出張買取（キャンセル無料をはっきり書いているチェーン）に見てもらうと、処分代がかからないことがあります。値段がつかなければ断って、市区の粗大ごみに切り替えます。</p>
'''),
 ("bicycle","自転車","自転車",["自転車"],"",
  "自転車の捨て方・処分方法",
  '''    <p>自転車は、多くの市区で粗大ごみとして出せます。タイヤの大きさ（インチ）や電動アシストかどうかで料金が変わる市区があります。持ち込みなら安くなる区もあります（江戸川区は収集900円、持ち込み400円）。</p>
    <p>まだ乗れる自転車は、買取や譲渡も考えられます。人に譲るときなどは防犯登録の手続きが必要になることがあるので、お住まいの都道府県の防犯登録の案内で確かめてください。</p>
'''),
 ("bed","ベッド","ベッド・マットレス",["ベッド","マットレス"],r"ベビーベッド|ソファーベッド|マットレス別|マットレスを除く|マットは別|ベッドマットを除く",
  "ベッド・マットレスの捨て方",
  '''    <p>ベッドは、枠（フレーム）とマットレスを別の品目として数える市区が多く、大きさ（シングル・ダブルなど）で料金が変わります。スプリング入りのマットレスは特に高い市区があります（さいたま市2,200円、仙台市3,000円など）。</p>
    <p>大きなベッドは、分解しないと部屋から出せないことがあります。収集の日までに分解して、家の前まで運べるか確かめておきます。まだ使えるベッドは出張買取に見てもらうのも手です。</p>
'''),
]
item_cards=[]
for key,short,name,words,excl,h1base,intro in ITEMS:
    rows=[]; cities=set()
    for k in ORDER:
        for cells,price in tablerows(k):
            # 品目名の入ったセルだけを見せる（持ち込み料金や券の組み合わせの列は出さない）
            hit=[c for c in cells if any(w in re.sub(excl,"",c) for w in words)] if excl else [c for c in cells if any(w in c for w in words)]
            txt="、".join(hit)
            if hit:
                rows.append(f'<tr><th scope="row"><a href="/guide/{k}/">{C[k][0]}</a></th><td>{price}</td><td>{txt}</td></tr>'); cities.add(k)
    n=len(cities)
    title=f"{h1base}｜粗大ごみの料金を{n}市区で比較"
    if len(title)<28: title=f"{name}の捨て方・処分方法｜粗大ごみの料金を{n}市区で比較"
    desc=f"{name}を粗大ごみで出すときの料金を{n}市区の公式ページで調べて比べました。申し込みから収集までの流れ、持ち込み、まだ使えるときの買取、無料回収業者に頼まない理由もまとめています。"
    body=f'''    <h2>{name}は粗大ごみで出せる？</h2>
{intro}
    <h2>{name}を手放す4つの方法</h2>
    <ol>
      <li><b>市区の粗大ごみ</b>：申し込んで、処理券（シール）を貼り、指定の日に出します（<a href="/guide/shoriken/">処理券の買い方・貼り方</a>）。</li>
      <li><b>自分で持ち込む</b>：車があれば、収集より早く・安く出せる市区もあります（<a href="/guide/mochikomi/">市区ごとの持ち込み先</a>）。</li>
      <li><b>買取・譲る</b>：まだ使える物は、出張査定とキャンセルが無料のチェーンに見てもらうか、市区が案内するリユース（ジモティーとの連携など）を使います。</li>
      <li><b>許可業者に頼む</b>：家のごみを運べるのは市区と市区の許可業者だけです。「無料で回収」の巡回業者には頼まないでください（<a href="/guide/scam/">ぼったくりの実例</a>）。</li>
    </ol>

    <h2>市区ごとの{name}の粗大ごみ料金</h2>
    <p>各市区の記事にある料金表から、{name}が出てくる行をそのまま抜き出しました。大きさや材質で区分が変わるので、正確な金額は申し込みのときに確かめてください。表にない市区は、市区名の記事から公式の品目一覧を開いて調べられます。</p>
    <table class="cmp cmp3"><thead><tr><th scope="col">市区</th><th scope="col">料金</th><th scope="col">市区の表での書き方</th></tr></thead><tbody>{"".join(rows)}</tbody></table>
'''
    item_cards.append((f"/guide/item/{key}/",f"{name}の捨て方",f"{n}市区の粗大ごみ料金を比較。持ち込み・買取も。",title,desc,name,f"{h1base}（{n}市区の料金）",body))

RELATED=''.join(f'<a class="card" href="{u}"><b>{b}</b><span>{sp}</span></a>' for u,b,sp in [
 ("/guide/mochikomi/","粗大ごみの持ち込み","予約・料金・持ち物と、市区ごとの持込先。"),
 ("/guide/shoriken/","処理券（シール）の買い方・貼り方","買える場所と、市区ごとの料金と払い方。"),
 ("/guide/fees/","出し方と料金（役所・郵便局・持込）","市区の回収、家電リサイクル券、持込施設、買取の手順。"),
 ("/guide/late/","引越しの不用品・家具処分","粗大ごみが間に合わないときの4つの方法。"),
]+[(u,b,sp) for u,b,sp,*_ in item_cards])

page("/guide/mochikomi/","粗大ごみの持ち込み｜予約・料金・持ち物と44市区の持込先".replace("44",str(len(ORDER))),
 f"粗大ごみを自分で市区の施設へ持ち込む方法をまとめました。予約の要否、料金（無料・処理券・重さで現金）、本人確認書類、回数の上限と、{len(ORDER)}市区それぞれの持込先を公式ページで確かめた一覧です。",
 "粗大ごみの持ち込み","粗大ごみの持ち込み（予約・料金・持ち物）",
 "収集の予約が取れないとき、車があれば市区の施設へ自分で持ち込めることがあります。予約・料金・持ち物の確かめ方と、市区ごとの持込先をまとめました。",mochi_body)
page("/guide/shoriken/",f"粗大ごみ処理券（シール）の買い方・貼り方｜コンビニ・料金・{len(ORDER)}市区",
 f"粗大ごみ処理券（シール・納付券）の買い方と貼り方をまとめました。コンビニなどの取扱所、申し込んでから買う理由、キャッシュレス払い、ほかの市区の券が使えないことと、{len(ORDER)}市区の料金と払い方の一覧です。",
 "粗大ごみ処理券（シール）","粗大ごみ処理券（シール）の買い方・貼り方",
 "粗大ごみの手数料は、処理券やシールを買って貼るのが基本です。どこで買うか、いつ買うか、どう貼るかと、市区ごとの料金と払い方をまとめました。",ken_body)
for u,b,sp,title,desc,name,h1,body in item_cards:
    page(u,title,desc,f"{name}の捨て方",h1,f"{name}を粗大ごみで出すときの料金を市区ごとに比べ、持ち込み・買取など、ほかの手放し方もまとめました。",body)

# 一覧ページのカードと ItemList、sitemap
TOPIC=[("/guide/mochikomi/","粗大ごみの持ち込み","予約・料金・持ち物と、市区ごとの持込先。","粗大ごみの持ち込み"),
       ("/guide/shoriken/","処理券（シール）の買い方・貼り方","コンビニなどの取扱所と、市区ごとの料金と払い方。","粗大ごみ処理券（シール）の買い方・貼り方")]+[(u,b,sp,t.split("｜")[0]) for u,b,sp,t,*_ in item_cards]
p=os.path.join(ROOT,"guide/index.html"); g=open(p,encoding="utf-8").read()
sec='    <!-- topic:start -->\n    <h2 id="topic" style="font-size:20px;margin:40px 0 12px">テーマ別・品目別の出し方</h2>\n    <div class="cards">'+"".join(f'<a class="card" href="{u}"><b>{b}</b><span>{sp}</span></a>' for u,b,sp,_ in TOPIC)+'</div>\n    <!-- topic:end -->\n'
if "<!-- topic:start -->" in g: g=re.sub(r"    <!-- topic:start -->.*?<!-- topic:end -->\n",sec,g,flags=re.S)
else: g=g.replace("    <!-- area:start -->",sec+"    <!-- area:start -->",1)
m=re.search(r'(<script type="application/ld\+json">\n)(\{"@context": "https://schema.org", "@type": "ItemList".*?)(\n</script>)',g,re.S)
d=json.loads(m.group(2)); urls=[SITE+u for u,*_ in TOPIC]
items=[x for x in d["itemListElement"] if x["url"] not in urls]
items+= [{"@type":"ListItem","url":SITE+u,"name":n} for u,_,_,n in TOPIC]
for i,x in enumerate(items): x["position"]=i+1
d["itemListElement"]=items
g=g[:m.start(2)]+json.dumps(d,ensure_ascii=False)+g[m.end(2):]
open(p,"w",encoding="utf-8").write(g)
p=os.path.join(ROOT,"sitemap.xml"); sm=open(p,encoding="utf-8").read()
for u in urls:
    if u not in sm: sm=sm.replace("</urlset>",f"  <url><loc>{u}</loc><lastmod>{DATE}</lastmod></url>\n</urlset>")
open(p,"w",encoding="utf-8").write(sm)
print("topics ok")
