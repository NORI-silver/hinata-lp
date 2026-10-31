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
    C[_m["key"]]=(_m["name"],_m.get("title",""),_m["desc"]); REGION[_m["key"]]=_m["region"]
    if _m.get("mover"): MOVER[_m["key"]]=_m["mover"]

# 都道府県（「近くの地域」で同じ都道府県を先に出すため）。meta に pref があればそちらを使う
_P={"東京都":"setagaya suginami adachi arakawa bunkyo chiyoda chuo edogawa itabashi katsushika kita koto meguro minato nakano nerima ota shibuya shinagawa shinjuku sumida taito toshima fuchu mitaka musashino chofu machida nishitokyo hachioji tachikawa",
 "神奈川県":"yokohama kawasaki sagamihara yamato atsugi fujisawa","埼玉県":"saitama kawaguchi soka koshigaya","千葉県":"chiba sakura funabashi ichikawa matsudo kashiwa",
 "大阪府":"osaka sakai hirakata toyonaka higashiosaka","兵庫県":"kobe nishinomiya","京都府":"kyoto","和歌山県":"wakayama","愛知県":"nagoya","静岡県":"shizuoka hamamatsu","岐阜県":"gifu",
 "北海道":"sapporo","宮城県":"sendai","新潟県":"niigata","岡山県":"okayama","広島県":"hiroshima","徳島県":"tokushima","愛媛県":"matsuyama",
 "福岡県":"fukuoka kitakyushu","熊本県":"kumamoto","鹿児島県":"kagoshima","沖縄県":"naha"}
PREF={k:pf for pf,ks in _P.items() for k in ks.split()}
CHKD={}  # 地域ごとの確認日（meta の checked。無ければ DATE）
for _f in sorted(_g.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),"meta","*.json"))):
    _m=json.load(open(_f,encoding="utf-8"))
    if _m.get("pref"): PREF[_m["key"]]=_m["pref"]
    if _m.get("checked"): CHKD[_m["key"]]=_m["checked"]

# タイトルはキーワードプランナーの結果（2026-10-31）にそろえる：「市区名＋粗大ごみ」に、検索の多い「持ち込み」「受付センター」を入れる。
# 市の正式名が「大型ごみ」の市はそれを先に。持ち込みを受け付けていない区は「持ち込み」を入れない。
OOGATA={"sapporo","kobe","kyoto","hiroshima","kumamoto","ichikawa","fujisawa","higashiosaka","chigasaki","otsu","amagasaki","nara","tottori","iwaki","odawara","kawanishi","ogaki","tomakomai","hirosaki","obihiro","omuta"}
# 申し込み制の収集がない市（「収集の予約が」と書かない）
NOYOYAKU={"fujimino","fukaya","yaizu","fujieda","higashihiroshima","koga","joetsu","hirosaki","matsusaka","kakegawa","fujinomiya","isahaya","kirishima","nagahama","kashihara"}
NOMOCHI={"koto","meguro","chuo","mitaka","kodaira","kokubunji","koganei","zama","toda","kyotanabe","urasoe"}
NOFEE={"shizuoka"}
def _title(k):
    n=C[k][0]; body=open(os.path.join(CD,k+".html"),encoding="utf-8").read()
    has_c="受付センター" in body and k not in {"joetsu"}
    if k in OOGATA: return f"{n}の大型ごみ（粗大ごみ）の出し方｜料金・持ち込み・申込"
    if k in NOMOCHI: return f"{n}の粗大ごみの出し方｜料金・申込・受付センター・買取"
    if k in NOFEE: return f"{n}の粗大ごみの出し方｜持ち込み・申込・受付センター・家電"
    if has_c: return f"{n}の粗大ごみの出し方｜料金・持ち込み・申込・受付センター"
    return f"{n}の粗大ごみの出し方｜料金・持ち込み・申込・家電・買取"
for _k in list(C): C[_k]=(C[_k][0],_title(_k),C[_k][2])
# 地域ごとのタイトル・説明（記事を厚くした地域だけ。その地域ならではの事実を1つ入れる。料金の数字は入れない）
TITLE={
 "yokohama":"横浜市の粗大ごみの出し方｜料金表・持ち込み4か所・7日前締切",
 "osaka":"大阪市の粗大ごみの出し方｜料金表・工場への持ち込み・ネット申込",
 "kawasaki":"川崎市の粗大ごみの出し方｜料金・布団は5枚で1個・受付センター",
 "nagoya":"名古屋市の粗大ごみの出し方｜料金表・月1回収集・持ち込み",
 "nerima":"練馬区の粗大ごみの出し方｜料金表・持ち込みは土日も可・申込",
 "setagaya":"世田谷区の粗大ごみの出し方｜料金表・持ち込み・収集までの目安",
 "ota":"大田区の粗大ごみの出し方｜料金表・京浜島への持ち込み・申込",
 "edogawa":"江戸川区の粗大ごみの出し方｜料金表（収集・持ち込み）・申込",
 "suginami":"杉並区の粗大ごみの出し方｜料金表・予約・日曜の持ち込み・処理券",
 "shinagawa":"品川区の粗大ごみの出し方｜料金表・日曜の持ち込みは約半額",
 "kita":"北区の粗大ごみの出し方｜料金表・浮間清掃事業所への持ち込み・申込",
 "katsushika":"葛飾区の粗大ごみの出し方｜料金表・処理券の枚数・持ち込みは約半額",
 "shinjuku":"新宿区の粗大ごみの出し方｜料金表・申込・受付センター・処理券",
 "koto":"江東区の粗大ごみの出し方｜料金表・LINE申込・受付センター・処理券",
 "fukuoka":"福岡市の粗大ごみの出し方｜料金表・LINE申込・処理券の買い方",
 "chiba":"千葉市の粗大ごみの出し方｜料金表・スプリング入りは収集不可・持ち込み",
}
DESC={
 "yokohama":"横浜市の粗大ごみの料金を品目別の表で（ソファ・ベッド・マットレス・たんす・自転車など）。申し込みは収集日の7日前まで、収集まで2週間程度。4か所の自己搬入ヤードへの持ち込み、シールの買い方も公式ページをもとにまとめました。",
 "osaka":"大阪市の粗大ごみの料金を品目別の表で（200円〜1,000円の4区分）。申し込みから3日後以降に収集。急ぐときの舞洲工場などへの持ち込み（前日までに予約・10kgごとに90円）も公式ページをもとにまとめました。",
 "kawasaki":"川崎市の粗大ごみは品目ではなく、おもに一番長い辺の長さ（と材質）で300円・600円・1,200円。布団は5枚まで1個、ベッド枠とマットレスは組で1個になるなど、まとめて出せる物と申し込み方法を公式ページをもとにまとめました。",
 "nagoya":"名古屋市の粗大ごみの料金を品目別の表で（250円〜2,500円）。令和8年10月から45リットル袋に入らない物が対象、収集は地域ごとに月1回で締め切りは7日前。持ち込み（10kgごとに270円）も公式ページをもとにまとめました。",
 "nerima":"練馬区の粗大ごみの料金を、収集と資源循環センターへの持ち込みの2列の表で。ベッドはマットつきでも同じ料金。持ち込みは土日祝も可、ネット申込ならカード・PayPayで払えます。公式ページをもとにまとめました。",
 "setagaya":"世田谷区の粗大ごみの料金を品目別の表で（ソファは横幅、ベッドは大きさで決まる）。申し込みから収集までの目安、船橋粗大ごみ中継所への持ち込み、処理券の買い方を公式ページをもとにまとめました。",
 "ota":"大田区の粗大ごみの料金を、収集と京浜島への持ち込みの2列の表で。持ち込むと300円の品目は0円、ほかも約半分。申し込み（ネットは24時間、電話は日曜・祝日も受付）、処理券、臨時ごみの相談先も公式ページをもとにまとめました。",
 "edogawa":"江戸川区の粗大ごみの料金を、収集と持ち込みの2列の表で（令和8年10月申込分から）。たんす・棚は3辺の合計で5段階。申し込み方法、処理券、持込施設、引越しの多量ごみの相談先も公式ページをもとにまとめました。",
 "suginami":"杉並区の粗大ごみの料金を品目別の表で（ソファ・ベッド・マットレス・自転車など）。予約から収集まで2〜3週間程度が目安。日曜の持ち込み（1点400円・1回5点まで）、処理券の買い方も公式ページをもとにまとめました。",
 "shinagawa":"品川区の粗大ごみの料金を、収集と日曜の持ち込み（品川区資源化センター）の2列の表で。持ち込みは収集のおよそ半分。ネット・電話の申し込み、処理券とカード払いも公式ページをもとにまとめました。",
 "kita":"北区の粗大ごみの料金を、収集と浮間清掃事業所への持ち込みの2列の表で（持ち込みはおよそ半額）。ソファ・ベッド・ベッドマット・自転車・箱物家具の区分、申し込み方法と処理券も公式ページをもとにまとめました。",
 "katsushika":"葛飾区の粗大ごみの料金を、処理券A・Bの枚数つきの表で。持込ステーションへ運ぶと約半額、300円の品目は無料。土日・祝日も収集、ネットは24時間受付。申し込み方法も公式ページをもとにまとめました。",
 "shinjuku":"新宿区の粗大ごみの料金を品目別の表で（ソファは人数、机は袖の数、箱物家具は2辺の合計で決まる）。ネット・電話の申し込み、処理券の買い方、家電4品目も公式ページをもとにまとめました。",
 "koto":"江東区の粗大ごみの料金を品目別の表で（箱物家具は高さと幅の合計で5段階）。ネット・LINEで24時間申し込めます。区への持ち込みは受け付けていません。処理券の買い方も公式ページをもとにまとめました。",
 "fukuoka":"福岡市の粗大ごみの料金を品目別の表で（布団・自転車300円、スプリング入りマットレス1,000円など）。ネット・LINEの申し込み、処理券の買い方、市の工場への自己搬入（粗大ごみを持ち込めるかは予約のときに確認）もまとめました。",
 "chiba":"千葉市の粗大ごみの料金を、390円券で払う区分ごとの表で。コイルスプリング入りのマットレス・ソファは収集できず、ベッドは電話での申し込み。3つの環境事業所への自己搬入も公式ページをもとにまとめました。",
}
for _k in TITLE: C[_k]=(C[_k][0],TITLE[_k],DESC.get(_k,C[_k][2]))
# 「引越しで間に合わないとき」の文を、予約のしくみが違う市だけ差し替える
LATE1={
 "matsuyama":"次の申込期間（地区ごと・年6回）を市のページで確かめて、早めに申し込む",
 "higashiosaka":"受付に電話して、早い収集日がないか聞く（初めての人はインターネットで申し込めません）",
 "wakayama":"受付に電話して、早い収集日がないか聞く（初めての人はインターネットで申し込めません）",
 "sakura":"収集業者に電話して、早い収集日がないか聞く",
 "kumamoto":"受付に電話して、早い収集日がないか聞く",
 "gifu":"受付に電話して、早い収集日がないか聞く",
 "fukuyama":"次のステーション収集日（燃やせる粗大ごみは年4回）を市のページで確かめる",
 "kochi":"環境業務課（088-856-5374）に次の収集日を聞く",
 "himeji":"引越しで出るごみはステーションに出せないので、市に連絡してエコパークあぼしへ持ち込む",
 "suita":"大型複雑ごみは収集日に出せます。引越しでまとめて出る分は、市に電話して早い日がないか聞く",
 "aomori":"受付に電話して、次の申込期限日と収集日を聞く（収集は月2回）",
 "oita":"担当の清掃事業所に電話して、早い収集日がないか聞く",
 "hiratsuka":"受付に電話して、早い収集日がないか聞く",
 "kawagoe":"受付に電話して、早い収集日がないか聞く",
 "takasaki":"受付に電話して、早い収集日がないか聞く",
 "chigasaki":"引越しの前に申し込む（収集日にまだ住んでいれば予約できます。LINEは収集日の5日前・土日を除くまで）",
 "toyohashi":"受付に電話して、早い収集日がないか聞く（初めての人はインターネットで申し込めません）",
 "kurashiki":"受付に電話して、早い収集日がないか聞く（初めての人はインターネットで申し込めません）",
 "nara":"引越しのごみは市では収集しないので、持ち込みを予約する（前日まで、土日を除く）",
 "miyazaki":"受付に電話して、早い収集日がないか聞く（引越しなどの多量ごみは受け付けません）",
 "toyota":"引越し日より前の収集日で、締め切り（原則1週間前）までに申し込む（引っ越したあとは収集できません）",
 "fukushima":"専用ダイヤルに電話して、早い収集日がないか聞く",
 "koriyama":"金曜16時までに申し込めば、原則として翌週に収集されます",
 "kasukabe":"電話で「多量排出」（2トン車1台5,000円）を頼む",
 "kurume":"電話で「特別申込み収集」（2トンダンプ1台8,530円）を頼む",
 "takamatsu":"受付に電話して、早い収集日がないか聞く（市外へ引っ越す人は電話で申し込みます）",
 "fuji":"少しなら次の「不燃・粗大・危険ごみの日」（月1回）に。大きい・多いときは前日までに予約して新環境クリーンセンターへ",
 "toyama":"環境センターに電話して、戸別有料収集の早い日がないか聞く",
 "kure":"少しなら次の粗大ごみの日（月1回）に出す。引越しでまとめて出る分はクリーンセンターくれへ持ち込む",
 "hakodate":"受付に電話して、早い収集日がないか聞く",
 "hachinohe":"受付に電話して、早い収集日がないか聞く",
 "morioka":"受付に電話して、早い収集日がないか聞く",
 "ichihara":"受付に電話して、早い収集日がないか聞く",
 "yachiyo":"引越しでたくさん出るときは、前もって清掃センターに連絡して持ち込む",
 "yokkaichi":"受付に電話して、早い収集日がないか聞く",
 "neyagawa":"受付に電話して、早い収集日がないか聞く",
 "nagano":"大きい物は資源再生センターへ持ち込む。引越しでたくさん出るときは、有料の一時多量ごみ収集を電話で頼む",
 "kofu":"少しなら処理券を貼って次の燃えないごみの日に。引越しでたくさん出るときは甲府・峡東クリーンセンターへ",
 "takarazuka":"受付に電話して、早い収集日がないか聞く（初めての人はインターネットで申し込めません）",
 "tsu":"施設の案内で持ち込める日時を確かめて、分けて持ち込む",
 "isesaki":"少しなら次の収集日に出す。一度にたくさん出る分は集積所に出せないので、清掃リサイクルセンター21へ（前もって申請）",
 "otagunma":"少しなら処理シールを貼って次のごみステーションの収集日に。多いときや大きい物はリサイクルプラザへ持ち込む",
 "takatsuki":"少しなら月1回の収集日に。引越しでまとめて出る分は、臨時ごみを電話で頼む（4〜5日前まで）",
 "ibaraki":"少しなら月1回の収集日に（1家庭3点まで）。引越しでまとめて出る分は、臨時ごみを電話で予約する",
 "kasugai":"受付に電話して、早い収集日がないか聞く",
 "matsue":"受付に電話して、早い収集日がないか聞く",
 "fukui":"受付に電話して、早い収集日がないか聞く",
 "ageo":"受付に電話して、早い収集日がないか聞く",
 "kanazawa":"受付に電話して、早い収集日がないか聞く",
 "matsumoto":"受付に電話して、早い収集日がないか聞く",
 "iwaki":"受付に電話して、早い収集日がないか聞く",
 "saga":"委託業者の臨時収集（1週間前まで）を頼むか、清掃工場へ持ち込む",
 "kodaira":"引越しでたくさん出るごみは市に持ち込めないので、早めに申し込んで何回かに分けて出す",
 "kokubunji":"数週間に分けて申し込む。間に合わない分は、引越し業者か廃棄物の収集運搬業者に頼む（持ち込みは休止中）",
 "kamakura":"大量なら市の許可業者に頼む。急な引越しで困ったら環境センターに相談する",
 "koganei":"早めに申し込んで、何回かに分けて出す（市には持ち込める施設がありません）",
 "zama":"何回かに分けて出す（1日5点まで。市には持ち込めません）",
 "urayasu":"引越しの多量ごみは市では収集できないので、本人が同乗してクリーンセンターへ持ち込む",
 "narashino":"引越しの当日以降は収集しないので、収集日が前日までになるよう早めに申し込む。多い分はクリーンセンターへ持ち込む",
 "numazu":"多いときは、クリーンセンターへ自分で持ち込む",
 "moriguchi":"「多量排出ごみ」（収集車1台8,000円）を電話で予約する",
 "minoh":"臨時収集を1週間前までに予約するか、環境クリーンセンターへの持ち込みを予約する",
 "odawara":"引越しのごみは集積場所に出せないので、環境事業センターへ持ち込む",
 "hadano":"多いときは、環境資源センターへ持ち込む（予約不要）",
 "kumagaya":"運べない家具は有料リクエスト収集を申し込む。多い分は処理施設へ持ち込む",
 "niiza":"量が多いときは、環境センターへの持ち込みを受付センターに電話で予約する",
 "sayama":"多い分は、環境センターへ持ち込む",
 "iruma":"総合クリーンセンターへ直接運ぶ",
 "anjo":"多い分は、施設へ持ち込む",
 "toyokawa":"粗大ごみ受付センターへ自分で運ぶ（無料・予約不要）",
 "uji":"まち美化推進課に電話して、臨時の有料収集を頼む",
 "kishiwada":"受付に電話して、早い収集日がないか聞く",
 "misato":"受付に電話して、早い収集日がないか聞く",
 "suzuka":"受付に電話して、早い収集日がないか聞く",
 "nishio":"受付に電話して、早い収集日がないか聞く",
 "hino":"一度に多いときは、市内の許可業者に有料で頼む（市の案内）",
 "ebina":"受付に電話して、早い収集日がないか聞く",
 "kusatsu":"受付に電話して、早い収集日がないか聞く",
 "fukaya":"清掃センターへ直接持ち込む",
 "kazo":"クリーンセンターへ自分で持ち込む",
 "noda":"受付に電話して、早い収集日がないか聞く",
 "abiko":"クリーンセンターへ自分で持ち込む（予約不要）",
 "kamagaya":"クリーンセンターしらさぎへ自分で持ち込む",
 "inzai":"一度に多いときは、市の許可業者に有料で頼む（粗大ごみは持ち込めません）",
 "narita":"受付に電話して、早い収集日がないか聞く",
 "kisarazu":"2営業日前までにLINEかウェブで予約して、自分で持ち込む",
 "tsuchiura":"清掃センターへ自分で持ち込む",
 "toride":"市役所の窓口で許可をとってから、常総環境センターへ持ち込む（平日のみ）",
 "hitachinaka":"クリーンセンター・資源リサイクルセンターへ自分で持ち込む",
 "kariya":"クリーンセンターへ自分で持ち込む（家庭のごみは無料）",
 "komaki":"小牧岩倉エコルセンターへ自分で持ち込む（平日・予約不要）",
 "seto":"晴丘センターへ自分で持ち込む（平日・予約不要）",
 "fujimino":"ふじみ野市・三芳町環境センターへ自分で持ち込む",
 "konosu":"受付に電話して、早い収集日がないか聞く",
 "ikeda":"クリーンセンターへ電話で予約して持ち込む（多いときは業務センターの有料臨時収集）",
 "sanda":"クリーンセンターへ前日までに予約して持ち込む",
 "kyotanabe":"受付に電話して、早い収集日がないか聞く",
 "kameoka":"エコトピア亀岡へ前日までに予約して持ち込む",
 "fujieda":"クリーンセンター志太へ予約して自分で持ち込む",
 "yaizu":"クリーンセンター志太へ予約して自分で持ち込む",
 "higashihiroshima":"市の処理施設へ自分で持ち込む（多いときは先に市へ申請）",
 "koga":"クリーンセンターへ自分で持ち込む",
 "daito":"7点以上は環境室に電話して、有料の臨時（引越）ごみを頼む",
 "kadoma":"6点以上は受付センターに電話して、有料の臨時ごみを頼む",
 "matsubara":"8点を超える分は市が集めないので、許可業者に頼めるか市に確かめる",
 "kuki":"受付に電話して、早い収集日がないか聞く",
 "okinawashi":"市役所で搬入許可証をもらい、倉浜衛生施設組合へ自分で持ち込む",
 "uruma":"市役所で許可証をもらい、処分場へ自分で持ち込む",
 "kasuga":"地区の担当業者に、有料の臨時収集を頼めるか聞く",
 "joetsu":"燃やせる物はクリーンセンターへ自分で持ち込む（運べないときは市の許可業者に頼む）",
 "tomakomai":"受付に電話して、早い収集日がないか聞く",
 "hirosaki":"弘前地区環境整備センターへ自分で持ち込む",
 "omuta":"受付センターに、有料の臨時収集を頼む",
 "beppu":"清掃事務所に、有料の一時多量ごみ収集を頼む",
 "matsusaka":"松阪市クリーンセンターへ自分で持ち込む",
 "iwata":"クリーンセンター・中遠広域粗大ごみ処理施設へ自分で持ち込む",
 "kakegawa":"環境資源ギャラリーへ自分で持ち込む",
 "mishima":"清掃センターへ自分で持ち込む（予約不要）",
 "fujinomiya":"清掃センターに連絡してから、自分で運ぶ",
 "hitachi":"清掃センターへ自分で持ち込む（土日・祝日も受付）",
 "ashikaga":"南部クリーンセンターへ自分で持ち込む",
 "tochigi":"とちぎクリーンプラザへ自分で持ち込む",
 "kiryu":"清掃センターへ自分で持ち込む",
 "ube":"環境保全センターへ自分で持ち込む",
 "izumo":"受付に電話して、早い収集日がないか聞く",
 "imabari":"バリクリーンへ自分で持ち込む",
 "isahaya":"自分の地域の次の粗大ごみの日を待つか、市の許可業者に頼む",
 "kirishima":"クリーンセンターへ自分で持ち込む",
 "miyakonojo":"クリーンセンター・リサイクルプラザへ持ち込む（先に電話で確かめる）",
 "ashiya":"収集事業課に、有料の一時多量ごみ収集を頼む",
 "hikone":"清掃センターへ自分で持ち込む",
 "nagahama":"住む地域のクリーンプラント・クリーンプラザへ自分で持ち込む",
  "urasoe":"受付センターに電話して、早い収集日がないか聞く",
 "kashihara":"資源循環課に、有料の一時多量ごみ収集を電話で頼む",
}
LATE3={
 "kishiwada":"可燃ごみ・金属ごみが多いときは岸和田貝塚クリーンセンターへ（粗大ごみを持ち込めるかは組合に確認）",
 "hino":"持ち込むなら、粗大ごみを受け付けるか先に市に確かめる",
 "urayasu":"",
 "numazu":"",
 "iruma":"",
 "toyokawa":"",
 "narashino":"",
 "ome":"受付に電話して、早い収集日がないか聞く",
 "toda":"受付に電話して、早い収集日がないか聞く（1回10点まで）",
 "kamakura":"",
 "soka":"少しなら環境業務センターへ持ち込む（引越しで一度にたくさん出る分は持ち込めません）",
 "hiratsuka":"自家用車があれば、上の持ち込み先へ（引越しの多量ごみを持ち込めるかは施設に確認）",
 "fukaya":"",
 "kazo":"",
 "abiko":"",
 "kamagaya":"",
 "inzai":"",
 "kisarazu":"",
 "tsuchiura":"",
 "toride":"",
 "hitachinaka":"",
 "kariya":"",
 "komaki":"",
 "seto":"",
 "fujimino":"",
 "ikeda":"",
 "sanda":"",
 "kameoka":"",
 "fujieda":"",
 "yaizu":"",
 "higashihiroshima":"",
 "koga":"",
 "matsubara":"",
 "okinawashi":"",
 "uruma":"",
 "joetsu":"",
 "hirosaki":"",
 "matsusaka":"",
 "iwata":"",
 "kakegawa":"",
 "mishima":"",
 "fujinomiya":"",
 "hitachi":"",
 "ashikaga":"",
 "tochigi":"",
 "kiryu":"",
 "ube":"",
 "imabari":"",
 "kirishima":"",
 "miyakonojo":"",
 "hikone":"",
 "nagahama":"",
 "kasuga":"燃える物はクリーン・エネ・パーク南部（予約制）、燃えない物は春日大野城リサイクルプラザへ持ち込む",
 "isahaya":"持ち込むなら、粗大ごみを受け付けるか先に施設に確かめる",
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
    D=CHKD.get(k,DATE); y,mo,da=D.split("-"); CK=f"{int(y)}年{int(mo)}月{int(da)}日"
    art={"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,"inLanguage":"ja","datePublished":D,"dateModified":D,"mainEntityOfPage":url,"image":SITE+"/og.png","author":{"@type":"Organization","name":"粗大ごみ手配ナビ","url":SITE+"/"},"publisher":{"@type":"Organization","name":"粗大ごみ手配ナビ","url":SITE+"/"},"about":{"@type":"City","name":name}}
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
    <p class="meta">{CK}に{name}の公式ページで確認・料金や日数は目安です</p>
  </header>
  <article>
'''
    body=open(os.path.join(CD,k+".html"),encoding="utf-8").read()
    if MOVER.get(k): mv_intro=f"<p>{name}の公式ページでは、引越しや転入について次のように案内しています（{CK}確認）。最後の3つは、どの市区でも気をつけたいことです。</p>"
    else: mv_intro=f"<p>前の家から持ってきた家具などを{name}で粗大ごみに出すときの決まりは、{name}の公式ページには特に書かれていませんでした（{CK}確認）。{name}の家庭のごみとして申し込むので、申し込むときに「引越しで持ってきた物」と伝えて確かめると安心です。</p>"
    late1=LATE1.get(k,"予約ページをこまめに見る（キャンセルで早い日が空くことがあります）")
    lateh="市の収集では引越しに間に合わないときは" if k in NOYOYAKU else "収集の予約が引越しに間に合わないときは"
    _l3=LATE3.get(k,"自家用車があれば、上の持ち込み先へ")  # "" は持ち込みできない市
    late3="" if k in NOMOCHI or not _l3 else "<li>"+_l3+"</li>"
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
    <p>{lateh}、次の順番で考えます。</p>
    <ol>
      <li>{late1}</li>
      <li>まだ使える物は買取に出す（下の買取店へ）</li>
      {late3}
      <li>それでも無理なら新居へ運ぶ（<a href="/guide/new-home/">損しやすい理由</a>も読んでください）</li>
    </ol>
    <p>品目ごとの出し方と、ほかの市区との料金の比べ方：<a href="/guide/item/futon/">布団</a>・<a href="/guide/item/sofa/">ソファ</a>・<a href="/guide/item/bed/">マットレス・ベッド</a>・<a href="/guide/item/bicycle/">自転車</a></p>
    <p>「無料で回収します」という巡回・チラシの業者に頼むのはやめましょう。お金を払ってごみの回収を頼めるのは、市区か、市区の許可業者だけです（家電4品目は買ったお店・買い替えるお店でも引き取れます）（<a href="/guide/scam/">ぼったくりの実例と見分け方</a>）。</p>

    <h2>{name}の近くのリサイクルショップ（買取）</h2>
    <p>まだ使える家具や家電は、処分代がかからず値段がつくこともあるので、出張査定・キャンセル無料をはっきり書いているチェーンの買取店に見てもらい、値段がつかなければ断って{name}の粗大ごみに切り替えます（どのお店とも提携していません）。</p>
    <div class="shops" data-city="{k}" data-name="{name}"><p>セカンドストリート、ハードオフ・オフハウス、トレジャーファクトリーなどの買取チェーンが出張買取をしています。</p></div>
'''
    # 診断ツールの CITIES にある市区だけ、その市区を選んだ状態で開く（/?city=key）
    if k in DIAG: cta_href,cta_go=f"/?city={k}",f"{name}で出し方を診断する"
    else: cta_href,cta_go="/","無料で診断する"
    # 同じ地方から最大6件。区は区どうし・市は市どうしを優先し、記事ごとに並びをずらして偏らないようにする
    same=[x for x in C if REGION[x]==REGION[k]]
    kind=lambda x:C[x][0][-1]
    pref=[x for x in same if kind(x)==kind(k)]
    i=pref.index(k); pref=pref[i+1:]+pref[:i]
    order=pref+[x for x in same if kind(x)!=kind(k)]
    # 同じ都道府県を先に（23区は区どうし、市は市どうしの順はそのまま）
    pk=PREF.get(k)
    if pk: order=[x for x in order if PREF.get(x)==pk]+[x for x in order if PREF.get(x)!=pk]
    others=order[:6]
    tail=f'''  </article>
  <a class="cta" href="{cta_href}">
    <b>あなたの粗大ごみ、どう出すのがいい？</b>
    <span>引越し日と出したい物を入れると、品目ごとに使える出し方と料金の目安がわかります。無料で、入力内容はどこにも送りません。</span>
    <span class="go">{cta_go}</span>
  </a>
  <section class="related" aria-label="ほかの地域">
    <h2>同じ県・地方の粗大ごみ</h2>
    <div class="cards">{cards(others)}</div>
    <p style="margin-top:12px;font-size:14px"><a href="/guide/#area">ほかの地域の記事を見る</a>・<a href="/guide/how-to-check/">記事のない市町村の調べ方</a></p>
  </section>
  <section class="related" aria-label="ほかの記事">
    <h2>あわせて読みたい</h2>
    <div class="cards"><a class="card" href="/guide/late/"><b>間に合わないときの出し方</b><span>4つの方法と基本の流れ。</span></a><a class="card" href="/guide/fees/"><b>出し方と料金（役所・郵便局・持込）</b><span>市区の回収、家電リサイクル券、持込施設、買取の手順と料金の目安。</span></a><a class="card" href="/guide/mochikomi/"><b>粗大ごみの持ち込み</b><span>予約・料金・持ち物と、市区ごとの持込先。</span></a><a class="card" href="/guide/shoriken/"><b>処理券（シール）の買い方・貼り方</b><span>コンビニなどの取扱所と、市区ごとの料金と払い方。</span></a></div>
  </section>
'''
    foot=FOOT.replace("</body>",'<script src="/reviews.js" defer></script>\n</body>').replace("2026年10月30日に確認",f"{CK}に確認")
    p=os.path.join(ROOT,"guide",k,"index.html"); os.makedirs(os.path.dirname(p),exist_ok=True)
    open(p,"w",encoding="utf-8").write(h+body+tail+foot)
    print(k,len(title),len(desc))
