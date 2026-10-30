import json, os, re, sys
ROOT=sys.argv[1]; CD=os.path.join(os.path.dirname(os.path.abspath(__file__)),"city")
SITE="https://hinata.shiokonbu.com"; DATE="2026-10-30"; CHECK="2026年10月30日"
C={ # key: (name, title, desc, blurb)
 "yokohama":("横浜市","横浜市の粗大ごみの出し方と料金｜申込・持込・家電・買取まとめ",
  "横浜市の粗大ごみの申し込み方法（ネット・電話）、収集シールの払い方、収集まで2週間程度の目安、自己搬入ヤードへの持ち込み、家電4品目の指定引取場所、近くの買取店をまとめました。"),
 "kawasaki":("川崎市","川崎市の粗大ごみの出し方と料金｜300円・600円・1,200円",
  "川崎市の粗大ごみは300円・600円・1,200円の3区分。申し込み方法、粗大ごみ処理券の買い方と出し方、出せない物、家電4品目の出し方、引越しで急ぐときの方法と近くの買取店をまとめました。"),
 "setagaya":("世田谷区","世田谷区の粗大ごみの出し方と料金｜申込・持込・家電・買取",
  "世田谷区の粗大ごみの申し込み方法、処理券（A券200円・B券300円）の使い方、収集の半額程度で出せる船橋粗大ごみ中継所への持ち込み、家電4品目の出し方、近くの買取店をまとめました。"),
 "suginami":("杉並区","杉並区の粗大ごみの出し方と料金｜申込・日曜持込・家電・買取",
  "杉並区の粗大ごみは申し込みから2〜3週間が目安。ネット・電話での申し込み方、処理券A・Bの払い方、日曜だけの持ち込み（1点400円）、家電4品目の出し方、近くの買取店をまとめました。"),
 "saitama":("さいたま市","さいたま市の粗大ごみの出し方と料金｜1品550円・持込・家電",
  "さいたま市の粗大ごみは1品550円。混雑時は収集まで1か月ほどかかることも。申し込み方法、納付券の買い方、市の3施設への持ち込み（予約制）、家電4品目の指定引取場所、近くの買取店をまとめました。"),
 "chiba":("千葉市","千葉市の粗大ごみの出し方と料金｜390円〜1,560円・持込・家電",
  "千葉市の粗大ごみは390円〜1,560円の4段階で、収集まで1〜2週間。ネット・LINE・電話の申し込み方、納付券の買い方、環境事業所への自己搬入、家電4品目の出し方、近くの買取店をまとめました。"),
 "sakura":("佐倉市","佐倉市の粗大ごみの出し方と料金｜電話予約・持込・家電・買取",
  "佐倉市の粗大ごみは地区ごとの収集業者へ電話で予約します。料金の目安、酒々井リサイクル文化センターへの持ち込み、家電4品目の出し方、引越しで急ぐときの方法、近くの買取店をまとめました。"),
 "osaka":("大阪市","大阪市の粗大ごみの出し方と料金｜申込・手数料券・家電・買取",
  "大阪市の粗大ごみは申し込みから3日後以降に収集。ネット・電話での申し込み方、粗大ごみ処理手数料券（200円〜1,000円）の買い方と出し方、家電4品目、引越してきた人の注意、近くの買取店をまとめました。"),
 "nagoya":("名古屋市","名古屋市の粗大ごみの出し方と料金｜250円〜・月1回収集・持込",
  "名古屋市の粗大ごみは令和8年10月から45L袋に入らない物が対象。250円〜2,500円の6段階、月1回の収集、7日前の締め切り、持ち込み（10kg270円）、引越しの一時多量ごみ、近くの買取店をまとめました。"),
 "sapporo":("札幌市","札幌市の大型ごみの出し方と料金｜申込締切・予約なし持込",
  "札幌市の大型ごみ（粗大ごみ）の申し込み方法と区ごとの締め切り、手数料シールの買い方、予約なしで持ち込める破砕工場（10kg210円）、家電4品目、引越してきた人の注意、近くの買取店をまとめました。"),
 "fukuoka":("福岡市","福岡市の粗大ごみの出し方と料金｜LINE申込・処理券・持込",
  "福岡市の粗大ごみは最短1週間ほどで収集。ネット・LINE・電話での申し込み方、粗大ごみ処理券（300円・500円・1,000円）の使い方、市の工場への持ち込み（予約制）、家電4品目、近くの買取店をまとめました。"),
 "kobe":("神戸市","神戸市の大型ごみの出し方と料金｜申込・シール券・出す時間",
  "神戸市の大型ごみ（粗大ごみ）は45L袋に入らない物や5kg超の物が対象。申し込み方法、大型ごみシール券とPayPay払い、朝5時〜8時の出し方、1回5点まで、家電4品目、近くの買取店をまとめました。"),
 "kyoto":("京都市","京都市の大型ごみの出し方と料金｜400円〜・申込・持込予約",
  "京都市の大型ごみ（粗大ごみ）の手数料（400円・800円・1,200円・2,000円など）、大型ごみ受付センターでの申し込み方、2営業日前の締め切り、前日予約の持ち込み、家電4品目、近くの買取店をまとめました。"),
}
REGION={"yokohama":"首都圏","kawasaki":"首都圏","setagaya":"首都圏","suginami":"首都圏","saitama":"首都圏","chiba":"首都圏","sakura":"首都圏","osaka":"関西","kobe":"関西","kyoto":"関西","nagoya":"東海","sapporo":"北海道・東北","fukuoka":"九州"}
RORDER=["首都圏","関西","東海","北海道・東北","甲信越・北陸","中国・四国","九州"]
MOVER={
 "yokohama":["引越しなどで一度にたくさん出るごみは、ごみの集積場所に出せません。市の処理施設に持ち込むか、一般廃棄物収集運搬の許可業者に頼みます。粗大ごみの自己搬入ヤードは、空きがあれば当日の持ち込みもできます（<a href=\"https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/gomi-recycle/gomi/shushufuka/itijitaryou.html\" target=\"_blank\" rel=\"noopener\">横浜市 一時多量ごみ</a>）。","横浜市は「市外からの持込み」は受け付けないとしています。"],
 "setagaya":["ほかの区や市の処理券は使えないと、区がはっきり書いています。"],
 "suginami":["区の持ち込みは区民だけで、区内の住所がわかる本人確認書類が必要です。免許証の住所を変える前なら、受付で確かめてください。"],
 "saitama":["持ち込みでは、住所がわかる運転免許証などで市内のごみかを確かめます。免許証の住所を変える前なら、予約のときに確かめてください。"],
 "chiba":["引越しなどで一度にたくさん出るごみは、ごみステーションに出せません（<a href=\"https://www.city.chiba.jp/kankyo/junkan/shushugyomu/hikkoshigomi.html\" target=\"_blank\" rel=\"noopener\">千葉市 引越し等で出るごみ</a>）。持ち込みも、市内の家庭から出たごみだけです。"],
 "nagoya":["引越しなどで一度にたくさん出るごみ（一時多量ごみ）は、通常の収集に少しずつ出すか、自分で処理施設に持ち込むか（10kgごとに270円）、市の許可業者に頼みます。"],
 "sapporo":["持ち込めるのは札幌市内の家庭ごみで、本人のごみだけです。"],
 "fukuoka":["持ち込みには運転免許証が必要です。レンタカーで持ち込むときは貸渡証明書も要ります。"],
}

import glob as _g
for _f in sorted(_g.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),"meta","*.json"))):
    _m=json.load(open(_f,encoding="utf-8"))
    if not os.path.exists(os.path.join(CD,_m["key"]+".html")): continue
    C[_m["key"]]=(_m["name"],_m["title"],_m["desc"]); REGION[_m["key"]]=_m["region"]
    if _m.get("mover"): MOVER[_m["key"]]=_m["mover"]

# タイトルはキーワードプランナーの結果（2026-10-31）にそろえる：「市区名＋粗大ごみ」に、検索の多い「持ち込み」「受付センター」を入れる。
# 市の正式名が「大型ごみ」の市はそれを先に。持ち込みを受け付けていない区は「持ち込み」を入れない。
OOGATA={"sapporo","kobe","kyoto","hiroshima","kumamoto","ichikawa","fujisawa","higashiosaka"}
NOMOCHI={"koto","meguro","chuo","mitaka"}
NOFEE={"shizuoka"}
def _title(k):
    n=C[k][0]; body=open(os.path.join(CD,k+".html"),encoding="utf-8").read()
    has_c="受付センター" in body
    if k in OOGATA: return f"{n}の大型ごみ（粗大ごみ）の出し方｜料金・持ち込み・申込"
    if k in NOMOCHI: return f"{n}の粗大ごみの出し方｜料金・申込・受付センター・買取"
    if k in NOFEE: return f"{n}の粗大ごみの出し方｜持ち込み・申込・受付センター・家電"
    if has_c: return f"{n}の粗大ごみの出し方｜料金・持ち込み・申込・受付センター"
    return f"{n}の粗大ごみの出し方｜料金・持ち込み・申込・家電・買取"
for _k in list(C): C[_k]=(C[_k][0],_title(_k),C[_k][2])
# 「引越しで間に合わないとき」の文を、予約のしくみが違う市だけ差し替える
LATE1={
 "matsuyama":"次の申込期間（地区ごと・年6回）を市のページで確かめて、早めに申し込む",
 "higashiosaka":"受付に電話して、早い収集日がないか聞く（初めての人はインターネットで申し込めません）",
 "wakayama":"受付に電話して、早い収集日がないか聞く（初めての人はインターネットで申し込めません）",
 "sakura":"収集業者に電話して、早い収集日がないか聞く",
 "kumamoto":"受付に電話して、早い収集日がないか聞く",
 "gifu":"受付に電話して、早い収集日がないか聞く",
}
LATE3={
 "soka":"少しなら環境業務センターへ持ち込む（引越しで一度にたくさん出る分は持ち込めません）",
}
_top=open(os.path.join(ROOT,"index.html"),encoding="utf-8").read()
DIAG=set(re.findall(r"^  (\w+):\[",_top.split("const CITIES={",1)[1].split("\n};",1)[0],re.M))
fees=open(os.path.join(ROOT,"guide/fees/index.html"),encoding="utf-8").read()
HEAD_TPL=fees.split("<title>")[0]  # doctype..viewport/robots
FOOT=fees[fees.index("  <footer class=\"foot\">"):]
FONTS=re.search(r'<link rel="icon".*?guide\.css">\n',fees,re.S).group(0)
def cards(keys,base="/guide/"):
    return "".join(f'<a class="card" href="/guide/{k}/"><b>{C[k][0]}の粗大ごみ</b><span>申し込み・料金・持ち込み・家電の出し方</span></a>' for k in keys)
for k,(name,title,desc) in C.items():
    url=f"{SITE}/guide/{k}/"
    art={"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,"inLanguage":"ja","datePublished":DATE,"dateModified":DATE,"mainEntityOfPage":url,"image":SITE+"/og.png","author":{"@type":"Organization","name":"粗大ごみ手配ナビ","url":SITE+"/"},"publisher":{"@type":"Organization","name":"粗大ごみ手配ナビ","url":SITE+"/"},"about":{"@type":"City","name":name}}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"トップ","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"粗大ごみの基礎知識","item":SITE+"/guide/"},{"@type":"ListItem","position":3,"name":f"{name}の粗大ごみ","item":url}]}
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
  <nav aria-label="パンくず"><ol class="crumb"><li><a href="/">トップ</a></li><li><a href="/guide/">粗大ごみの基礎知識</a></li><li aria-current="page">{name}の粗大ごみ</li></ol></nav>
  <header class="hero">
    <h1>{name}の粗大ごみの出し方と料金</h1>
    <p>申し込み方法、料金と払い方、出し方、持ち込み先、家電4品目、引越しで急ぐときの方法を、{name}の公式ページをもとにまとめました。</p>
    <p class="meta">{CHECK}に{name}の公式ページで確認・料金や日数は目安です</p>
  </header>
  <article>
'''
    body=open(os.path.join(CD,k+".html"),encoding="utf-8").read()
    if MOVER.get(k): mv_intro=f"<p>{name}の公式ページでは、引越しや転入について次のように案内しています（{CHECK}確認）。最後の3つは、どの市区でも気をつけたいことです。</p>"
    else: mv_intro=f"<p>前の家から持ってきた家具などを{name}で粗大ごみに出すときの決まりは、{name}の公式ページには特に書かれていませんでした（{CHECK}確認）。{name}の家庭のごみとして申し込むので、申し込むときに「引越しで持ってきた物」と伝えて確かめると安心です。</p>"
    late1=LATE1.get(k,"予約ページをこまめに見る（キャンセルで早い日が空くことがあります）")
    late3="" if k in NOMOCHI else "<li>"+LATE3.get(k,"自家用車があれば、上の持ち込み先へ")+"</li>"
    extra="".join(f"<li>{x}</li>" for x in MOVER.get(k,[]))
    body+=f'''
    <h2>{name}に引っ越してきた人へ</h2>
    {mv_intro}
    <ul>
      {extra}
      <li>申し込みは、住み始めてから新しい住所で。住む前に申し込めるかは受付で確かめてください。</li>
      <li>処理券やシールは自治体ごとに別の物です。前の自治体で買った券は使えません。</li>
      <li>段ボールや梱包材は粗大ごみではありません。{name}の分け方に従って出します。</li>
    </ul>

    <h2>引越しで間に合わないとき</h2>
    <p>収集の予約が引越しに間に合わないときは、次の順番で考えます。</p>
    <ol>
      <li>{late1}</li>
      <li>まだ使える物は買取に出す（下の買取店へ）</li>
      {late3}
      <li>それでも無理なら新居へ運ぶ（<a href="/guide/new-home/">損しやすい理由</a>も読んでください）</li>
    </ol>
    <p>品目ごとの出し方と、ほかの市区との料金の比べ方：<a href="/guide/item/futon/">布団</a>・<a href="/guide/item/sofa/">ソファ</a>・<a href="/guide/item/bed/">マットレス・ベッド</a>・<a href="/guide/item/bicycle/">自転車</a></p>
    <p>「無料で回収します」という巡回・チラシの業者に頼むのはやめましょう。家庭のごみを運べるのは市区と市区の許可業者だけです（<a href="/guide/scam/">ぼったくりの実例と見分け方</a>）。</p>

    <h2>{name}の近くのリサイクルショップ（買取）</h2>
    <p>まだ使える家具や家電は、出張査定・キャンセル無料をはっきり書いているチェーンの買取店に見てもらうと、処分代がかからず、値段がつくこともあります。値段がつかなければ断って、{name}の粗大ごみに切り替えます。セカンドストリート、ハードオフ・オフハウス、トレジャーファクトリーなどのチェーンが出張買取をしています（どのお店とも提携していません）。</p>
    <div class="shops" data-city="{k}" data-name="{name}"></div>
'''
    # 診断ツールの CITIES にある市区だけ、その市区を選んだ状態で開く（/?city=key）
    if k in DIAG: cta_href,cta_go=f"/?city={k}",f"{name}で出し方を診断する"
    else: cta_href,cta_go="/","無料で診断する"
    # 同じ地方から最大6件。区は区どうし・市は市どうしを優先し、記事ごとに並びをずらして偏らないようにする
    same=[x for x in C if REGION[x]==REGION[k]]
    kind=lambda x:C[x][0][-1]
    pref=[x for x in same if kind(x)==kind(k)]
    i=pref.index(k); pref=pref[i+1:]+pref[:i]
    others=(pref+[x for x in same if kind(x)!=kind(k)])[:6]
    tail=f'''  </article>
  <a class="cta" href="{cta_href}">
    <b>あなたの粗大ごみ、どう出すのがいい？</b>
    <span>引越し日と出したい物を入れると、品目ごとに使える出し方と料金の目安がわかります。無料で、入力内容はどこにも送りません。</span>
    <span class="go">{cta_go}</span>
  </a>
  <section class="related" aria-label="ほかの地域">
    <h2>近くの地域の粗大ごみ</h2>
    <div class="cards">{cards(others)}</div>
    <p style="margin-top:12px;font-size:14px"><a href="/guide/#area">ほかの地域の記事を見る</a></p>
  </section>
  <section class="related" aria-label="ほかの記事">
    <h2>あわせて読みたい</h2>
    <div class="cards"><a class="card" href="/guide/late/"><b>間に合わないときの出し方</b><span>4つの方法と基本の流れ。</span></a><a class="card" href="/guide/fees/"><b>出し方と料金（役所・郵便局・持込）</b><span>市区の回収、家電リサイクル券、持込施設、買取の手順と料金の目安。</span></a><a class="card" href="/guide/mochikomi/"><b>粗大ごみの持ち込み</b><span>予約・料金・持ち物と、市区ごとの持込先。</span></a><a class="card" href="/guide/shoriken/"><b>処理券（シール）の買い方・貼り方</b><span>コンビニなどの取扱所と、市区ごとの料金と払い方。</span></a></div>
  </section>
'''
    foot=FOOT.replace("</body>",'<script src="/reviews.js" defer></script>\n</body>')
    p=os.path.join(ROOT,"guide",k,"index.html"); os.makedirs(os.path.dirname(p),exist_ok=True)
    open(p,"w",encoding="utf-8").write(h+body+tail+foot)
    print(k,len(title),len(desc))
