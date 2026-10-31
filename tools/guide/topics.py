# テーマ別のまとめページを、地域記事の元データ（city/*.html と data/areas.js）から作る
#   /guide/mochikomi/  粗大ごみの持ち込み（市区ごとの持込先）
#   /guide/shoriken/   粗大ごみ処理券（シール）の買い方・貼り方（市区ごとの料金と払い方）
#   /guide/item/<key>/ 品目別の捨て方（市区ごとの粗大ごみ料金の比較）
# キーワードは docs/keywords.md（キーワードプランナー 2026-10-31）。gencity.py → hub.py → areas.py のあとに実行する。
import json,os,re,sys
ROOT=sys.argv[1]; HERE=os.path.dirname(os.path.abspath(__file__)); CD=os.path.join(HERE,"city")
sys.path.insert(0,HERE); import figures  # 説明図（インラインSVG）
SITE="https://hinata.shiokonbu.com"; DATE="2026-10-31"; CHECK="2026年10月30〜31日"
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

def regtables(cell,head,pre):
    # 地方ごとに h3 と表を分け、表の上に地方へ飛ぶリンクを置く
    rs=[r for r in RORDER if any(REGION[k]==r for k in ORDER)]
    nav='<p>'+"・".join(f'<a href="#{pre}{i}">{r}</a>' for i,r in enumerate(rs))+'</p>\n'
    return nav+"".join(f'    <h3 id="{pre}{i}">{r}</h3>\n    <table class="cmp"><thead><tr><th scope="col">市区</th><th scope="col">{head}</th></tr></thead><tbody>'+"".join(cityrow(k,cell(k)) for k in ORDER if REGION[k]==r)+'</tbody></table>\n' for i,r in enumerate(rs))+'    <p>お住まいの市町村が表にないときは、<a href="/guide/how-to-check/">記事のない市町村の粗大ごみの調べ方</a>を見てください。</p>\n'
def cityrow(k,cell):
    n=C[k][0]
    return f'<tr><th scope="row"><a href="/guide/{k}/">{n}</a></th><td>{cell}</td></tr>'

# ---------- 持ち込み ----------
# areas.js のポイント欄に「持ち込み」がない市区は、記事本文の持ち込みの節から要点を書いた
MOCHI={
 "kawaguchi":"鳩ヶ谷衛生センターへ予約制（2週間前〜前日に電話）。10kgごとに150円。戸塚環境センターは2030年3月まで受け入れ停止",
 "fuchu":"市の公式ページに記載が見当たらない（府中市ごみ総合サポートセンター 042-370-1515 に問い合わせ）",
 "mitaka":"持ち込めない（クリーンプラザふじみは燃やせるごみだけ）",
 "funabashi":"北部清掃工場・西浦資源リサイクル施設へ。15kg未満150円、超える分は10kgごとに150円（＋10%）",
 "ichikawa":"市川市クリーンセンターへ予約制。10kgごとに220円（キャッシュレス可）",
 "matsudo":"松戸市リサイクルセンターへ予約制。1kgあたり17.6円・20kg未満は352円（現金のみ）",
 "hachioji":"戸吹・館クリーンセンターへ（要申込）。10kgごとに350円",
 "gifu":"市内3か所の自己搬入施設へ予約制。品目ごとの手数料を処理券・処理袋で先に払う",
 "hirakata":"穂谷川清掃工場へ予約制（当日も可）。粗ごみ5点ごとに300円、大型ごみは品目ごとに300円〜1,800円",
 "toyonaka":"豊中市伊丹市クリーンランドへ予約制。10kgごとに105円",
 "naha":"那覇・南風原クリーンセンターへ予約制。家庭ごみは10kgごとに60円",
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
rows=regtables(lambda k:pt(k).get("持ち込み") or MOCHI.get(k,FALLBACK),f"持ち込み（{CHECK}確認）","m")
mochi_body=f'''    <h2>粗大ごみの持ち込みとは</h2>
    <p>粗大ごみを自分の車で市区の施設へ運んで出す方法です。収集の予約が先まで埋まっているときや、引越しまで日がないときに使えます。予約がいらない市（札幌市・相模原市・北九州市・広島市など）や、収集より安い区（板橋区・葛飾区は半額、江戸川区は自転車が収集900円に対し持ち込み400円）もあります。</p>
    <p>一方で、持ち込みを受け付けていない区（江東区・目黒区・中央区など）や、公式ページに案内が見当たらない市区もあります。まず下の一覧で、お住まいの市区を確かめてください。</p>
    <p>持ち込む施設の名前は、清掃工場・クリーンセンター・リサイクルセンター・自己搬入ヤード・中継所など市区で違います。「ゴミ処理場に持ち込みたい」ときも、まずはお住まいの市区が案内している施設を確かめます。</p>

    <h2 id="kankatsu">持ち込み施設はだれが運営している？</h2>
    <p>清掃工場・クリーンセンター・リサイクルセンターは、基本的に<b>市区町村</b>の施設です。家庭のごみの処理は市区町村の仕事だからです。ただ、近くの市町村がいっしょに作った<b>組合（一部事務組合など）</b>が施設を持っていることもよくあります。</p>
    <ul>
      <li><b>東京23区</b>：収集は各区、清掃工場などの処理は23区が共同で作る東京二十三区清掃一部事務組合、埋め立ては東京都に頼んで行います（<a href="https://www.city.minato.tokyo.jp/jigyoukeikaku/kurashi/gomi/seso/jichitai/23ku.html" target="_blank" rel="noopener">港区の説明</a>）。持ち込みの受け付けは区ごとに決まっています。</li>
      <li><b>佐倉市</b>：持ち込み先の酒々井リサイクル文化センターは、佐倉市と酒々井町でつくる「佐倉市、酒々井町清掃組合」の施設です（<a href="https://www.env.go.jp/recycle/waste/3r_network/5_region/project_list/12_chiba/23_sakurashishisuimachi_r7.pdf" target="_blank" rel="noopener">環境省の資料</a>）。</li>
      <li><b>西東京市</b>は柳泉園組合、<b>東大阪市</b>は東大阪都市清掃施設組合の施設へ持ち込みます（各市の記事を参照）。</li>
    </ul>
    <p>組合の施設でも、持ち込めるのは決まった市町村に住む人の家のごみだけで、申し込み先や料金は市町村や組合の案内に従います。まずは自分の市区の案内を見るのが近道です。</p>
    <p>家電4品目の「指定引取場所」は別のしくみです。家電リサイクル法でメーカーが引き取る場所で、多くは物流会社の拠点などです（<a href="/guide/kaden/">家電リサイクル券の買い方</a>）。</p>

    <h2>持ち込む前に確かめること</h2>
    <ol>
      <li><b>予約がいるか</b>：要申込の市区が多く、日曜だけ・指定日だけの施設もあります。</li>
      <li><b>料金と払い方</b>：無料、品目ごと（処理券やシールを先に買う）、重さで現金払い（10kgごとに100円〜270円など）と市区で違います。</li>
      <li><b>本人確認書類</b>：その市区に住んでいて、自分の家のごみかを確かめる市区が多く、運転免許証などを求められます。</li>
      <li><b>回数と量の上限</b>：1回10個まで・年度内3回までなどの決まりがある区があります。</li>
      <li><b>荷下ろしは自分で</b>：施設の人は手伝ってくれないことが多いので、2人で行くと安心です。</li>
      <li><b>分け方</b>：燃やすごみ・燃やさないごみ・粗大ごみに分けて積んでおくよう求める施設があります（新潟市など）。</li>
    </ol>
    <p><b>持っていく物</b>：本人確認書類（運転免許証など）、予約番号（予約制のとき）、処理券（券で払う市区）か現金（重さで払う施設は現金だけのところが多い）、施設によっては申込書（新潟市の「廃棄物処理依頼書」など）。</p>

    <h2 id="nagare">当日の流れ</h2>
    <p>流れは、料金を<b>重さで払う施設</b>か、<b>処理券（シール）を先に買う市区</b>かで変わります。</p>
    <h3>重さで払う施設（新潟市・名古屋市・八王子市など）</h3>
    <ol>
      <li>受付で申込書（新潟市は「廃棄物処理依頼書」）を出します。予約番号や本人確認書類が要る施設もあります。</li>
      <li>ごみを積んだまま、車ごと重さを量ります（1回目）。</li>
      <li>案内された場所まで車で進み、自分で荷物を降ろします。</li>
      <li>空になった車をもう一度量り（2回目）、差の重さで手数料を払います。</li>
    </ol>
    <p class="src">流れは新潟市の案内（<a href="https://www.city.niigata.lg.jp/kurashi/gomi/gomishigen/zikohan/carry.files/gomizikohan.pdf" target="_blank" rel="noopener">ごみの自己搬入</a>、{CHECK}確認）による。施設ごとに細かい手順は違うので、お住まいの市区の案内で確かめてください。</p>
    <h3>処理券（シール）で払う市区（横浜市・浜松市など）</h3>
    <ol>
      <li>申し込みのときに言われた金額分の処理券を、先にお店で買って1品ずつ貼っておきます。</li>
      <li>受付で受付番号と本人確認書類を見せ、案内された場所で自分で降ろします。</li>
    </ol>
    <p>施設では処理券を売っていないことがあるので、当日の朝までに買っておきます（<a href="/guide/shoriken/">処理券の買い方・貼り方</a>）。</p>
    <p>家電4品目（エアコン・テレビ・冷蔵庫と冷凍庫・洗濯機と衣類乾燥機）は、市区の施設には持ち込めません。家電リサイクル券を買って指定引取場所へ運びます（<a href="/guide/kaden/">家電リサイクル券の買い方</a>）。</p>
    <p>持ち込めるのは、その市区に住む人の家のごみを本人が運ぶ場合だけです。家のごみを代わりに運べるのは市区の許可業者だけで、「無料で回収します」という巡回の業者に頼むのはやめましょう（<a href="/guide/scam/">ぼったくりの実例と見分け方</a>）。</p>

    <h2>市区ごとの持ち込み先</h2>
    <p>市区名を押すと、その市区の記事（申し込み・料金・家電・買取店）が開きます。施設の住所・受付時間・最新の料金は、記事の出典から市区の公式ページで確かめてください。</p>
    {rows}
    <h2>持ち込みのよくある質問</h2>
    <h3>ゴミ処理場（清掃工場）に持ち込むのに予約はいる？</h3>
    <p>予約がいる市区が多いです。札幌市・相模原市・北九州市・広島市などは予約なしで持ち込めます。日曜だけ・指定日だけの施設もあるので、上の一覧と市区の記事で確かめてください。</p>
    <h3>持ち込みの料金はいくら？</h3>
    <p>市区で大きく違います。無料（足立区・岡山市）、収集の半額（板橋区・葛飾区）、品目ごとに処理券を先に買う（横浜市・岐阜市など）、重さで現金払い（新潟市は10kgごとに100円、名古屋市は270円、八王子市は350円）などです。</p>
    <h3>リサイクルセンターやクリーンセンターは市の施設？</h3>
    <p>基本は市区町村の施設ですが、近くの市町村でつくる組合（一部事務組合など）の施設のこともあります。どちらの場合も、持ち込める人・予約・料金はお住まいの市区の案内で確かめます。</p>
    <h3>何を持っていけばいい？</h3>
    <p>運転免許証などの本人確認書類を求める市区が多いです。処理券で払う市区は、申し込んだ分の処理券を貼って持って行きます。現金だけの施設もあります。</p>
    <h3>冷蔵庫やテレビも持ち込める？</h3>
    <p>持ち込めません。家電4品目は家電リサイクル券を買って指定引取場所へ運びます（<a href="/guide/kaden/">家電リサイクル券の買い方と料金</a>）。</p>
    <h3>家族や知り合いの家のごみも持ち込める？</h3>
    <p>持ち込めるのは、その市区に住む人の家のごみを本人が運ぶ場合だけです。代わりに運べるのは市区の許可業者だけです。</p>
'''

# ---------- 処理券 ----------
PAY={
 "kyoto":"品目ごとに400円・800円・1,200円・2,000円など（払い方は記事で確認）",
 "shizuoka":"戸別収集の手数料は市の不燃・粗大ごみのページに記載がない（受付センターで確認）",
 "tokushima":"市の粗大ごみのページに手数料の記載が見当たらない（東部環境事業所 088-662-0985 で確認）",
}
def paycell(k):
    p=pt(k); xs=[x for x in (p.get("料金"),p.get("支払い")) if x]
    return "<br>".join(xs) if xs else PAY.get(k,FALLBACK)
rows=regtables(paycell,f"料金と払い方（{CHECK}確認）","r")
ken_body=f'''    <h2>粗大ごみ処理券（シール）とは</h2>
    <p>粗大ごみの手数料を前払いした印です。申し込みのときに言われた金額分を買い、出す物に貼っておきます。呼び方は市区で違い、東京23区の「有料粗大ごみ処理券」、横浜市の「粗大ごみ収集シール」、名古屋市や仙台市の「納付券」、神戸市の「大型ごみシール券」、浜松市の「納付済証」などがあります。</p>

    <h2>出し方の流れ</h2>
{figures.flow()}
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
{figures.ticket()}    <p>書き方や貼る場所の細かい決まりは市区で違います。お住まいの市区の記事から公式ページを確かめてください。持ち込みのときも、処理券を先に買っておく市区（横浜市・浜松市など）と、施設で重さに応じて現金で払う市区があります（<a href="/guide/mochikomi/">粗大ごみの持ち込み</a>）。</p>

    <h2 id="ryokin">市区ごとの料金と払い方</h2>
    {rows}
    <h2>処理券のよくある質問</h2>
    <h3>処理券（シール）はコンビニで買える？</h3>
    <p>多くの市区で、目印のステッカーがあるコンビニ・スーパー・ドラッグストアで買えます。どのお店が取扱所かは市区のページで確かめられます。</p>
    <h3>申し込む前に買っておいてもいい？</h3>
    <p>申し込んでから買うのが安全です。品目ごとの金額は申し込みのときにわかり、払い戻しや再発行ができない市区が多いためです。</p>
    <h3>前に住んでいた市区の処理券は使える？</h3>
    <p>使えません。処理券はその市区だけで使えます。引越し先では、新しい市区の券を買い直します。</p>
    <h3>粗大ごみの処理券は郵便局で買える？</h3>
    <p>市区によります。横浜市・鎌倉市・金沢市・長崎市などは郵便局でも売っています。一方で、川崎市（2026年3月31日で終了）・東大阪市（2023年4月から）・八尾市のように、郵便局での販売をやめた市もあります。取扱所はお住まいの市区の記事か公式ページで確かめてください。なお、冷蔵庫やテレビなど家電4品目は、郵便局で「家電リサイクル券」の料金を払い込みます（<a href="/guide/kaden/">家電リサイクル券の買い方</a>）。</p>
    <h3>処理券を買わずに払う方法はある？</h3>
    <p>横浜市・大阪市・名古屋市・練馬区・台東区などは、ネットで申し込むとクレジットカードやPayPayで払え、券がいらない場合があります。</p>
'''


# ---------- 家電リサイクル券（郵便局） ----------
# 出典：家電リサイクル券センター（郵便局振込方式の流れ・料金一覧）、新宿区・船橋市・匝瑳市・横浜市の案内（2026-10-31確認）
RKC_FLOW="https://www.rkc.aeha.or.jp/document/flow_post_office.pdf"
RKC_PRICE="https://www.rkc.aeha.or.jp/recycle_price_compact.html"
RKC_MAP="https://www.aeha-kadenrecycle.com/rkcmap"
kaden_body=f'''    <h2>家電リサイクル券とは</h2>
    <p>エアコン・テレビ・冷蔵庫と冷凍庫・洗濯機と衣類乾燥機の4品目は、<b>家電リサイクル法</b>の対象で、市区町村の粗大ごみでは回収しません。捨てるときは、メーカーが決めたリサイクル料金を払い、メーカーの<b>指定引取場所</b>に引き渡します。家電リサイクル券は、その料金を払ったことを示す券です。</p>
    <p>券をもらう方法は2つあります。お店に引き取りを頼むと、お店が券を用意します。自分で指定引取場所へ運ぶときは、<b>郵便局</b>に置いてある券で料金を払い込みます（郵便局振込方式）。</p>

    <h2>3つの出し方と、かかるお金</h2>
    <table class="cmp cmp3"><thead><tr><th scope="col">出し方</th><th scope="col">かかるお金</th><th scope="col">向いている人</th></tr></thead><tbody>
      <tr><th scope="row">買い替えるお店・買ったお店に引き取ってもらう</th><td>リサイクル料金＋お店の運ぶ料金</td><td>新しい家電を買う人。券はお店が用意</td></tr>
      <tr><th scope="row">市区が案内する受付先・業者に頼む</th><td>リサイクル料金＋運ぶ料金（業者ごとに違う）</td><td>買ったお店がわからない・遠い人。市区が集めるのではなく、案内された業者が運ぶ</td></tr>
      <tr><th scope="row">郵便局で払い込んで、自分で指定引取場所へ運ぶ</th><td>リサイクル料金＋郵便局の払込手数料</td><td>車があり、運ぶ料金を払いたくない人</td></tr>
    </tbody></table>
    <p>市区ごとの受付先（23区の家電リサイクル受付センターなど）や、市内の指定引取場所は、お住まいの市区の記事の「出せない物と家電4品目」にまとめています。</p>

    <h2>リサイクル料金の目安（主要メーカー・税込）</h2>
    <div class="tblw"><table>
      <thead><tr><th>品目</th><th>リサイクル料金</th></tr></thead>
      <tbody>
        <tr><td>エアコン</td><td class="num">550円〜990円</td></tr>
        <tr><td>テレビ（液晶・有機EL・プラズマ）</td><td class="num">小 1,870円／大 2,970円</td></tr>
        <tr><td>冷蔵庫・冷凍庫</td><td class="num">小 3,740円／大 4,730円</td></tr>
        <tr><td>洗濯機・衣類乾燥機</td><td class="num">2,530円</td></tr>
      </tbody>
    </table></div>
    <p class="src">パナソニック・シャープ・日立・三菱電機などの料金（{CHECK}、<a href="{RKC_PRICE}" target="_blank" rel="noopener">家電リサイクル券センターの料金一覧</a>で確認）。冷蔵庫・冷凍庫は内容積170L以下が小、171L以上が大です（<a href="https://www.city.shinjuku.lg.jp/seikatsu/file09_01_00019.html" target="_blank" rel="noopener">新宿区の案内</a>）。テレビは画面の大きさで小・大が分かれます。メーカーで料金が違うので、お持ちの物のメーカー名で確かめてください。</p>

    <h2 id="yubinkyoku">郵便局での買い方（郵便局振込方式）</h2>
    <ol>
      <li><b>メーカー名と大きさを調べる</b>：本体のラベルでメーカー名を、冷蔵庫は内容積（L）、テレビは画面の大きさを確かめます。メーカーがわからない・もうない場合は、払い込む前に家電リサイクル券センターに聞きます。</li>
      <li><b>郵便局で券をもらう</b>：郵便局に置いてある「家電リサイクル券」（郵便局用）を使います。郵便局にある冊子の料金表で、メーカーの<b>製造業者等名コード</b>（3桁）と<b>品目・料金区分コード</b>（2桁）を調べます。</li>
      <li><b>券に書く</b>：製造業者等名コード、品目・料金区分コード、リサイクル料金（税込）、自分の住所・名前・電話番号を書きます。</li>
      <li><b>払い込む</b>：券から払込書を切り離して、窓口かATMで払います。リサイクル料金とは別に<b>払込手数料</b>がかかります（例：匝瑳市の案内では1件 窓口203円・ATM152円。最新は郵便局で確認）。ATMで払えるのは、自分で指定引取場所へ運ぶ場合だけです。</li>
      <li><b>控えを受け取る</b>：窓口なら「振替払込請求書兼受領証」と「振替払込受付証明書」を受け取ります。ATMなら利用明細票を受け取り、窓口で受付証明書に日付の印を押してもらいます。</li>
      <li><b>受付証明書を券に貼る</b>：日付の印がある「振替払込受付証明書」を、券の1枚目（指定引取場所控）に貼ります。これが払い込んだ証明になります。</li>
    </ol>
    <p class="src">手順とコードの桁数は<a href="{RKC_FLOW}" target="_blank" rel="noopener">家電リサイクル券センター「郵便局振込方式での手続きの流れ」</a>、手数料は<a href="https://www.city.sosa.lg.jp/sp/page/page000239.html" target="_blank" rel="noopener">匝瑳市の案内</a>による（{CHECK}確認）。券の書き方は郵便局にある説明書にも載っています。</p>
    <p>コードの例（{CHECK}、料金一覧で確認）：パナソニックの製造業者等名コードは100、品目・料金区分コードはエアコン10、薄型テレビ小51・大52、冷蔵庫・冷凍庫小31・大32、洗濯機・衣類乾燥機40です。</p>

    <h2 id="hikitori">指定引取場所への持ち込み方</h2>
    <ol>
      <li><b>場所を探す</b>：<a href="{RKC_MAP}" target="_blank" rel="noopener">家電製品協会の指定引取場所の検索ページ</a>で、近くの場所を探します。市区の施設ではなく、物流会社の拠点などが指定されています（横浜市内なら日本通運やSBS即配サポートの拠点など）。</li>
      <li><b>受付日時を確かめる</b>：日曜・祝日が休みの場所が多く、横浜市の案内では受付は9時〜11時30分・13時〜16時30分です。場所ごとに違うので、家電リサイクル券センター（<a href="tel:0120319640">0120-319-640</a>）や検索ページで確かめます。新宿区は事前に連絡するよう案内しています。</li>
      <li><b>券を貼って運ぶ</b>：券の1枚目（指定引取場所控）を家電に貼ります。船橋市は、正面から見て右側の側面の上のほうに貼り、ガラス面には貼らないよう案内しています。</li>
      <li><b>控えを取っておく</b>：引き渡したら券の控えを受け取り、大切に取っておきます。券の番号で、引き取られたかを家電リサイクル券センターで確かめられます。</li>
    </ol>
    <p class="src">出典：<a href="https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/gomi-recycle/ongen/pamphlet/wakedashi.files/08P13-14.pdf" target="_blank" rel="noopener">横浜市の分け方・出し方</a>、<a href="https://www.city.shinjuku.lg.jp/seikatsu/file09_01_00019.html" target="_blank" rel="noopener">新宿区</a>、<a href="https://www.city.funabashi.lg.jp/kurashi/gomi/004/p001526.html" target="_blank" rel="noopener">船橋市</a>、<a href="https://www.kankyo.metro.tokyo.lg.jp/documents/d/kankyo/electronics-index-files-kadenrecycleqa0831" target="_blank" rel="noopener">東京都の家電リサイクルQ&amp;A</a>（{CHECK}確認）。</p>
    <p>指定引取場所の多くは物流会社の拠点などで、市区の清掃工場やリサイクルセンターとは別です。市区の持ち込み施設には家電4品目を持ち込めません（<a href="/guide/mochikomi/">粗大ごみの持ち込み</a>）。</p>

    <h2>気をつけたいこと</h2>
    <ul>
      <li><b>「無料回収」の業者には頼まない</b>：東京都は、無料回収をうたう業者は違法な不用品回収業者のおそれがあるとして、使わないよう呼びかけています（<a href="/guide/scam/">ぼったくりの実例と見分け方</a>）。</li>
      <li><b>まだ使えるなら買取も</b>：製造から年数の浅い物は、買取で値段がつくことがあります。リサイクル料金を払う前に見積もりを取るのも手です。</li>
      <li><b>対象かどうか</b>：家電リサイクル券センターに対象品と対象外品の一覧があります。迷ったら家電リサイクル券センター（<a href="tel:0120319640">0120-319-640</a>）に聞きます。</li>
    </ul>

    <h2>家電リサイクル券のよくある質問</h2>
    <h3>家電リサイクル券はコンビニで買える？</h3>
    <p>自分で運ぶときは、郵便局で料金を払い込んで券を使います（家電リサイクル券センターが案内しているのは郵便局での払い込みです）。お店に頼むときは、お店が券を用意します。</p>
    <h3>郵便局のATMで払える？</h3>
    <p>自分で指定引取場所へ運ぶ場合だけ、ATMで払えます。そのあと窓口で受付証明書に日付の印を押してもらいます。</p>
    <h3>払込手数料はいくら？</h3>
    <p>リサイクル料金とは別に、1件ごとにかかります。匝瑳市の案内では窓口203円・ATM152円です。変わることがあるので、郵便局で確かめてください。</p>
    <h3>冷蔵庫や洗濯機は粗大ごみに出せる？</h3>
    <p>出せません。家電4品目は市区町村では回収しないので、お店に頼むか、このページの方法で指定引取場所へ運びます。</p>
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
 ("bed","マットレス","マットレス・ベッド",["ベッド","マットレス"],r"ベビーベッド|ソファーベッド|マットレス別|マットレスを除く|マットは別|ベッドマットを除く|マットレス・毛布を除く",
  "マットレス・ベッドの捨て方",
  '''    <p>マットレスとベッドの枠（フレーム）は、別の品目として数える市区が多く、大きさ（シングル・ダブルなど）で料金が変わります。スプリング入りのマットレスは特に高い市区があります（さいたま市2,200円、仙台市3,000円など）。</p>
    <p>大きなベッドは、分解しないと部屋から出せないことがあります。収集の日までに分解して、家の前まで運べるか確かめておきます。まだ使えるマットレスやベッドは出張買取に見てもらうのも手です。</p>
    <h2>スプリング入りかどうかの見分け方</h2>
    <p>スプリング入りかどうかで料金が変わる市区が多く（下の表の「スプリング」の行）、伊勢崎市・長岡市・宇都宮市のように、スプリング入りのマットレスは市の粗大ごみで収集しない市もあります。申し込む前に確かめておきます。</p>
    <ul>
      <li><b>品質表示のタグを見る</b>：マットレスの側面や裏のタグに「スプリング」「コイル」「ポケットコイル」と書いてあればスプリング入りです。まずこれを見るのが確実です。</li>
      <li><b>押してみる</b>：手のひらで強く押すと、バネが押し返す感触や、きしむ音がすればスプリング入りの見込みが高いです。</li>
      <li><b>重さ</b>：同じ大きさなら、スプリング入りのほうがずっと重いのが目安です。</li>
    </ul>
'''+figures.spring()),
]
# 品目だけの方法（「〇つの方法」の数にも入る）
METHODS_EXTRA={"bed":['      <li><b>買い替えのときにお店に引き取ってもらう</b>：新しいマットレスやベッドを買う家具店・寝具店が、古い物を引き取ってくれることがあります。買うときだけ・有料・同じ数まで、などの条件がつくことが多いので、お店の公式ページで確かめてください。</li>\n']}
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
    desc=f"{name}の捨て方を、{n}市区の公式ページで調べた粗大ごみ料金の比較とあわせてまとめました。申し込みから収集までの流れ、持ち込み、まだ使えるときの買取、無料回収業者に頼まない理由も。"
    body=f'''    <h2>{name}は粗大ごみで出せる？</h2>
{intro}
    <h2>{name}を手放す{len(METHODS_EXTRA.get(key,[]))+4}つの方法</h2>
    <ol>
      <li><b>市区の粗大ごみ</b>：申し込んで、処理券（シール）を貼り、指定の日に出します（<a href="/guide/shoriken/">処理券の買い方・貼り方</a>）。</li>
      <li><b>自分で持ち込む</b>：車があれば、収集より早く・安く出せる市区もあります（<a href="/guide/mochikomi/">市区ごとの持ち込み先</a>）。</li>
      <li><b>買取・譲る</b>：まだ使える物は、出張査定とキャンセルが無料のチェーンに見てもらうか、市区が案内するリユース（ジモティーとの連携など）を使います。</li>
      <li><b>許可業者に頼む</b>：家のごみを運べるのは市区と市区の許可業者だけです。「無料で回収」の巡回業者には頼まないでください（<a href="/guide/scam/">ぼったくりの実例</a>）。</li>
{"".join(METHODS_EXTRA.get(key,[]))}    </ol>

    <h2>{name}の粗大ごみ料金（市区別）</h2>
    <p>各市区の記事にある料金表から、{name}が出てくる行をそのまま抜き出しました。大きさや材質で区分が変わるので、正確な金額は申し込みのときに確かめてください。表にない市区は、市区名の記事から公式の品目一覧を開いて調べられます。</p>
    <table class="cmp cmp3"><thead><tr><th scope="col">市区</th><th scope="col">料金</th><th scope="col">市区の表での書き方</th></tr></thead><tbody>{"".join(rows)}</tbody></table>
'''
    item_cards.append((f"/guide/item/{key}/",f"{name}の捨て方",f"{n}市区の粗大ごみ料金を比較。持ち込み・買取も。",title,desc,name,f"{h1base}（{n}市区の料金）",body))

# ---------- 大きさの基準（粗大ごみとは） ----------
def taisho(k):
    p=pt(k); return p.get("対象") or p.get("対象の目安")
SIZEFIX={"hamamatsu":"mixed","toyonaka":"mixed","funabashi":"mixed"}  # 物の種類・素材で基準が分かれる市
def sizegroup(t,k=None):
    if k in SIZEFIX: return SIZEFIX[k]
    if not t or not re.search(r"cm|メートル|袋|ポリタンク|\dm",t): return "other"
    if "ポリタンク" in t or ("袋" in t and "cm" not in t): return "bag"
    cm={int(x) for x in re.findall(r"(\d+)cm",t)}&{30,40,50}
    if len(cm)>1: return "mixed"
    if cm: return f"c{cm.pop()}"
    return "big"
SG=[("c30","一辺30cmが目安の市区"),("c40","一辺40cmが目安の市区"),("c50","一辺50cmが目安の市区"),("mixed","物の種類や素材で基準が違う市区"),("big","90cm・1mなど、もっと大きい物が対象の市区"),("bag","指定袋やポリタンクなど、入れ物の大きさで決める市区"),("other","基準の書き方が違う・公式で確認する市区")]
groups={g:[k for k in ORDER if sizegroup(taisho(k),k)==g] for g,_ in SG}
nsize=sum(1 for k in ORDER if sizegroup(taisho(k),k)!="other")
def sizetable(g):
    return '<table class="cmp"><thead><tr><th scope="col">市区</th><th scope="col">粗大ごみの対象（公式ページの要点）</th></tr></thead><tbody>'+"".join(cityrow(k,taisho(k) or FALLBACK) for k in groups[g])+'</tbody></table>'
size_body=f'''    <h2>粗大ごみとは</h2>
    <p>粗大ごみは、家具や寝具、自転車など、ふだんのごみ袋に入らない大きな家庭のごみのことです。どこからを粗大ごみとするかは市区が決めていて、「一辺30cmを超える物」とする区が多い一方、40cm・50cm・90cmを目安にする市や、大きさではなく「指定袋に入るかどうか」で決める市もあります。</p>
    <p>引越しで別の市区へ移ると、前の家では普通ごみに出せた物が粗大ごみになる（またはその逆の）ことがあります。下の表は、各市区の記事のもとになった公式ページの「粗大ごみの対象」を短くまとめたものです（{CHECK}確認）。</p>
    <p>大きさの測り方は、多くの市区が「一番長い辺」ですが、市原市・郡山市のように3辺（幅・奥行き・高さ）の合計で決める市や、水戸市のように上限だけを3辺の合計で決める市もあります。</p>
{figures.measure()}
    <h2>大きさのほかに気をつけること</h2>
    <ul>
      <li><b>分解しても粗大ごみ</b>：中央区・台東区・豊島区・練馬区・徳島市などは、分解したり切ったりしても粗大ごみとして扱います。</li>
      <li><b>小さくても粗大ごみになる物</b>：ストーブ・カセットコンロ・電子レンジなどは、大きさに関係なく粗大ごみとする市があります（越谷市・那覇市・調布市など）。</li>
      <li><b>重さや長さの上限</b>：重さ（5kg・10kg以上など）で決める市や、長すぎる物・重すぎる物は収集しない市もあります。</li>
      <li><b>家電4品目は別</b>：エアコン・テレビ・冷蔵庫と冷凍庫・洗濯機と衣類乾燥機は、大きさに関係なく粗大ごみには出せません（<a href="/guide/kaden/">家電リサイクル券の買い方と料金</a>）。</li>
    </ul>

    <h2>市区ごとの粗大ごみの大きさの基準</h2>
    <p>市区名を押すと、その市区の記事（申し込み・料金・持ち込み）が開きます。「おおむね」「超える」「以上」などの細かい書き方は市区で違うので、迷う物は申し込みのときに確かめてください。</p>
    <p>{"・".join(f'<a href="#{g}">{h}</a>' for g,h in SG if groups[g])}</p>
    <p>お住まいの市町村が表にないときは、<a href="/guide/how-to-check/">記事のない市町村の粗大ごみの調べ方</a>を見てください。</p>
'''+"".join(f'    <h3 id="{g}">{h}（{len(groups[g])}）</h3>\n    {sizetable(g)}\n' for g,h in SG if groups[g])+f'''
    <h2>大きさの基準のよくある質問</h2>
    <h3>粗大ごみは何cmから？</h3>
    <p>一辺30cm（を超える物、または以上の物）とする市区がいちばん多く、東京23区の多くがこの基準です。ただし横浜市は金属製品30cm・それ以外50cm、さいたま市は90cm以上など、市区で大きく違います。上の表でお住まいの市区を確かめてください。</p>
    <h3>小さく分解すれば、普通のごみに出せる？</h3>
    <p>市区によります。分解・切断しても粗大ごみとする区がある一方、袋に入れば普通のごみに出せる市もあります。お住まいの市区の記事から公式ページを確かめてください。</p>
    <h3>粗大ごみの料金は？</h3>
    <p>品目と大きさで決まり、処理券（シール）を買って貼るのが基本です（<a href="/guide/shoriken/#ryokin">市区ごとの料金と払い方</a>）。車があれば、施設へ持ち込める市区もあります（<a href="/guide/mochikomi/">粗大ごみの持ち込み</a>）。</p>
'''

RELATED=''.join(f'<a class="card" href="{u}"><b>{b}</b><span>{sp}</span></a>' for u,b,sp in [
 ("/guide/mochikomi/","粗大ごみの持ち込み","予約・料金・持ち物と、市区ごとの持込先。"),
 ("/guide/shoriken/","処理券（シール）の買い方・貼り方","買える場所と、市区ごとの料金と払い方。"),
 ("/guide/kaden/","家電リサイクル券の買い方（郵便局）","券の書き方・払込手数料と、指定引取場所への持ち込み方。"),
 ("/guide/fees/","粗大ごみの出し方と料金","市区の回収、持込施設、買取の手順と料金の目安。"),
 ("/guide/late/","引越しの不用品・家具処分","粗大ごみが間に合わないときの4つの方法。"),
 ("/guide/size/","粗大ごみとは（何cmから？）","市区ごとの大きさの基準を比較。"),
]+[(u,b,sp) for u,b,sp,*_ in item_cards])

page("/guide/mochikomi/","粗大ごみの持ち込み（ゴミ処理場）｜予約・料金・当日の流れと44市区".replace("44",str(len(ORDER))),
 f"粗大ごみを自分で市区の施設へ持ち込む方法をまとめました。予約の要否、料金（無料・処理券・重さで現金）、本人確認書類、回数の上限と、{len(ORDER)}市区それぞれの持込先を公式ページで確かめた一覧です。",
 "粗大ごみの持ち込み","粗大ごみの持ち込み（予約・料金・持ち物）",
 "収集の予約が取れないとき、車があれば市区の施設へ自分で持ち込めることがあります。予約・料金・持ち物の確かめ方と、市区ごとの持込先をまとめました。",mochi_body)
page("/guide/shoriken/",f"粗大ごみ処理券（シール）の買い方・貼り方｜コンビニ・料金・{len(ORDER)}市区",
 f"粗大ごみ処理券（シール・納付券）の買い方と貼り方をまとめました。コンビニなどの取扱所、申し込んでから買う理由、キャッシュレス払い、ほかの市区の券が使えないことと、{len(ORDER)}市区の料金と払い方の一覧です。",
 "粗大ごみ処理券（シール）","粗大ごみ処理券（シール）の買い方・貼り方",
 "粗大ごみの手数料は、処理券やシールを買って貼るのが基本です。どこで買うか、いつ買うか、どう貼るかと、市区ごとの料金と払い方をまとめました。",ken_body)
page("/guide/kaden/","家電リサイクル券の買い方と料金｜郵便局での書き方・指定引取場所",
 "家電リサイクル券を郵便局で買う手順を、券の書き方・払込手数料から、指定引取場所への持ち込みと控えの保管まで説明します。4品目のリサイクル料金の目安と、お店に頼む方法との違いも。",
 "家電リサイクル券の買い方","家電リサイクル券の買い方（郵便局）と指定引取場所への持ち込み",
 "冷蔵庫・洗濯機・テレビ・エアコンは粗大ごみに出せません。郵便局で家電リサイクル券の料金を払い込み、自分で指定引取場所へ運ぶ方法を、順番にまとめました。",kaden_body)
page("/guide/size/",f"粗大ごみとは｜何cmから？{nsize}市区の大きさの基準を比較",
 f"粗大ごみとは何か、何cmから粗大ごみになるかを{nsize}市区の公式ページで調べて比べました。30cm・40cm・50cm・指定袋など市区ごとの基準と、分解しても粗大ごみになる区、家電4品目の扱いもまとめています。",
 "粗大ごみとは（大きさの基準）","粗大ごみとは（何cmから？市区ごとの大きさの基準）",
 "粗大ごみになる大きさは、市区によって30cm・40cm・50cm・指定袋に入るかどうかなどと違います。市区ごとの基準を比べました。",size_body)
for u,b,sp,title,desc,name,h1,body in item_cards:
    page(u,title,desc,f"{name}の捨て方",h1,f"{name}を粗大ごみで出すときの料金を市区ごとに比べ、持ち込み・買取など、ほかの手放し方もまとめました。",body)

# 一覧ページのカードと ItemList、sitemap
TOPIC=[("/guide/mochikomi/","粗大ごみの持ち込み","予約・料金・持ち物と、市区ごとの持込先。","粗大ごみの持ち込み"),
       ("/guide/shoriken/","処理券（シール）の買い方・貼り方","コンビニなどの取扱所と、市区ごとの料金と払い方。","粗大ごみ処理券（シール）の買い方・貼り方"),
       ("/guide/size/","粗大ごみとは（何cmから？）","市区ごとの大きさの基準を比較。","粗大ごみとは（大きさの基準）"),
       ("/guide/kaden/","家電リサイクル券の買い方（郵便局）","券の書き方・払込手数料と、指定引取場所への持ち込み方。","家電リサイクル券の買い方と指定引取場所")]+[(u,b,sp,t.split("｜")[0]) for u,b,sp,t,*_ in item_cards]
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
# 出し方の記事とトップに、全地域記事への地方別リンクを入れる（<!-- arealinks:start --> 〜 end の間）
al="".join(f'<p><b>{r}</b>：'+"・".join(f'<a href="/guide/{k}/">{C[k][0]}</a>' for k in ORDER if REGION[k]==r)+"</p>" for r in RORDER if any(REGION[k]==r for k in ORDER))
for f in ["guide/fees/index.html","guide/late/index.html","index.html"]:
    p=os.path.join(ROOT,f); t=open(p,encoding="utf-8").read()
    t2=re.sub(r"(<!-- arealinks:start -->).*?(<!-- arealinks:end -->)",lambda m:m.group(1)+al+m.group(2),t,flags=re.S)
    if t2==t and "<!-- arealinks:start -->" not in t: print("arealinks marker missing:",f)
    open(p,"w",encoding="utf-8").write(t2)
print("topics ok")
