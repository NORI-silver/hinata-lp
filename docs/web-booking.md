# ウェブ予約できる自治体（2026-10-30〜31 確認）

`python3 tools/guide/areas.py .` が地域記事と `tools/guide/booking.json` から作る一覧。手で直さない。
予約サイトの「形」は URL から分けたもので、同じ形なら空き枠の見張りを同じしくみで作れる見込み（運営会社は確かめていない）。
メール登録＝申し込みの前にメールアドレスの登録が要ると公式・予約サイトで確かめたもの（空欄は未確認）。

| 地域 | ウェブ予約 | 予約サイト | 形 | メール登録 | メモ |
|---|---|---|---|---|---|
| [足立区](/guide/adachi/) | ◯ だれでも | https://ecolife.e-tumo.jp/sodai-adachi-u/ | e-tumo.jp |  |  |
| [上尾市](/guide/ageo/) | ◯ だれでも | https://apply.e-tumo.jp/city-ageo-saitama-u/profile/userLogin_initDisplay?nextURL=CqTLFdO4voZHuPTdfqR%2B5N7dRrdLP0zYtUINsUzZVMu6FfqtX6L0xoUsjq5vuNFNDi5fGIqMAk9s%0D%0AKTyW032Ql8RiKGMscmvTIe1dD2WrZycU4pzKp4jJNA%3D%3D4LmoBSC2iOM%3D%0D%0A | e-tumo.jp |  | 1世帯月1回・3点まで |
| [明石市](/guide/akashi/) | ◯ だれでも | https://sodai.city.akashi.lg.jp/ | 独自 |  |  |
| [秋田市](/guide/akita/) | △ 条件つき | https://sodai-sys.jp/akita/users/ | 独自 |  | 締め切りは収集希望日の5日前。一覧にない品目は電話 |
| [尼崎市](/guide/amagasaki/) | ◯ だれでも | https://www.ogatagomi-amagasaki.jp/eco/view/amagasaki/top.html | /eco/view/ 形式 |  |  |
| [安城市](/guide/anjo/) | ◯ だれでも | https://anjosodaigomi.com/ | 独自 |  |  |
| [青森市](/guide/aomori/) | × 電話など | — | — |  | 申し込みは電話だけ（ネット・ファクス・メールは不可） |
| [荒川区](/guide/arakawa/) | ◯ だれでも | https://www2.sodai-web.jp/arakawa/index.html | sodai-web.jp |  |  |
| [旭川市](/guide/asahikawa/) | ◯ だれでも | https://www.city.asahikawa.hokkaido.jp/kurashi/271/272/osirasegomi/d079727.html | 独自 |  | 締め切りは収集日の3日前（土日祝を除く）。1回10点まで |
| [朝霞市](/guide/asaka/) | ◯ だれでも | https://apply.e-tumo.jp/city-asaka-saitama-u/offer/offerList_detail?tempSeq=2113 | e-tumo.jp |  | 1回5点まで |
| [厚木市](/guide/atsugi/) | ◯ だれでも | https://www.sodai-atsugi.jp/eco/view/atsugi/top.html | /eco/view/ 形式 |  |  |
| [文京区](/guide/bunkyo/) | ◯ だれでも | https://ecolife.e-tumo.jp/sodai-bunkyo-tokyo-u/ | e-tumo.jp |  |  |
| [千葉市](/guide/chiba/) | ◯ だれでも | https://www.sodai-web.jp/chiba/index.html | sodai-web.jp |  |  |
| [茅ヶ崎市](/guide/chigasaki/) | △ 条件つき | https://www.city.chigasaki.kanagawa.jp/kankyo/gomi/1067062.html | 独自 |  | 市公式LINEで申し込めるのは市民だけ・写真が必要・締め切りは収集日の5日前（土日を除く）。引越しで出た大型ごみは原則として持ち込み |
| [千代田区](/guide/chiyoda/) | ◯ だれでも | https://ecolife.e-tumo.jp/sodai.city.chiyoda-u/offer/offerList_initDisplay | e-tumo.jp |  |  |
| [調布市](/guide/chofu/) | ◯ だれでも | https://sodai.city.chofu.tokyo.jp/ | 独自 |  |  |
| [中央区](/guide/chuo/) | ◯ だれでも | https://ecolife.e-tumo.jp/kankyo-chuo-tokyo-u/ | e-tumo.jp |  |  |
| [海老名市](/guide/ebina/) | ◯ だれでも | https://nav.cx/bHjpcBr | 独自 |  | 市のLINEから |
| [江戸川区](/guide/edogawa/) | ◯ だれでも | https://ecolife.e-tumo.jp/edogawa.tokyo-u/offer/offerList_initDisplay | e-tumo.jp | 要 |  |
| [府中市](/guide/fuchu/) | ◯ だれでも | https://www.eg-resource.jp/sodai_fuchu/web/ | eg-resource.jp |  |  |
| [富士市](/guide/fuji/) | × 電話など | — | — |  | 申し込みの制度はありません。月1回の「不燃・粗大・危険ごみの日」に資源物集積所へ出します |
| [藤沢市](/guide/fujisawa/) | ◯ だれでも | https://sodai-sys.jp/fujisawa/users/ | 独自 |  |  |
| [福井市](/guide/fukui/) | ◯ だれでも | https://shinsei.e-fukui.lg.jp/SksJuminWeb/EntryForm?id=b9Lkahm3 | 独自 | 要 | メールアドレスを入れると申請のしかたがメールで届きます（1人1件まで） |
| [福岡市](/guide/fukuoka/) | ◯ だれでも | https://sodaigomi-kankyo.city.fukuoka.lg.jp/<br>https://www.city.fukuoka.lg.jp/kankyo/kateigomi/hp/LINE-sodaigomi.html | 独自 |  |  |
| [福島市](/guide/fukushima/) | △ 条件つき | https://logoform.jp/form/PBtX/801001 | logoform.jp（フォーム） |  | フォームは仮受付。担当者からの電話で正式な申し込みになります |
| [福山市](/guide/fukuyama/) | × 電話など | — | — |  | 申し込みの制度は見当たりません。ステーション収集に出します |
| [船橋市](/guide/funabashi/) | ◯ だれでも | https://www.sodai-funabashi.jp/ | 独自 |  |  |
| [岐阜市](/guide/gifu/) | × 電話など | https://logoform.jp/form/BcLm/62949 | logoform.jp（フォーム） |  | 収集の予約は電話だけ。インターネット（オンライン受付）は持ち込み（直接搬入）の予約に使えます |
| [八戸市](/guide/hachinohe/) | × 電話など | — | — |  | 2026年10月31日時点では電話だけ。ごみ収集アプリでの受付が2026年11月から始まる予定（市のページで確認） |
| [八王子市](/guide/hachioji/) | ◯ だれでも | https://sodai.city.hachioji.tokyo.jp/eco/view/hachioji/top.html | /eco/view/ 形式 |  |  |
| [秦野市](/guide/hadano/) | ◯ だれでも | https://dshinsei.e-kanagawa.lg.jp/142115-u/offer/offerList_initDisplay | 独自 |  | 先にID登録が必要。収集日の1週間前まで、1回5点まで |
| [函館市](/guide/hakodate/) | × 電話など | — | — |  | 申し込みは電話だけ（1回3点まで）。持ち込み先の予約はネットでもできます |
| [浜松市](/guide/hamamatsu/) | ◯ だれでも | https://www.city.hamamatsu.shizuoka.jp/ippai/gomi/dashikata/dashikata/renrakugomi_line.html<br>https://www.city.hamamatsu.shizuoka.jp/ippai/gomi/dashikata/dashikata/renrakugomi_in_nagare.html | 独自 |  |  |
| [東村山市](/guide/higashimurayama/) | ◯ だれでも | https://sodai-sys.jp/higashimurayama/users/ | 独自 |  | 1か月に同じ世帯で3回まで、1回8点まで |
| [東大阪市](/guide/higashiosaka/) | △ 条件つき | https://www.ogomi-higashiosaka.jp/eco/view/higashiosaka/top.html | /eco/view/ 形式 |  | インターネット受付は、前に電話で申し込んだことがあり住所・氏名が変わっていない人だけ。初めての人は電話で |
| [姫路市](/guide/himeji/) | × 電話など | — | — |  | 申し込みの制度はありません。決まった日に粗大ごみステーションへ出します（旧姫路市域）。引越しで出るごみはステーションに出せません |
| [日野市](/guide/hino/) | △ 条件つき | https://logoform.jp/form/Z9UK/858763 | logoform.jp（フォーム） |  | 申請したあと受付から電話があり、収集日と金額を確かめます |
| [枚方市](/guide/hirakata/) | △ 条件つき | https://www.city.hirakata.osaka.jp/0000010721.html | 独自 |  | インターネット予約は、今までに電話で申し込んだことがある人だけ。初めての人・住所が変わった人は電話で |
| [平塚市](/guide/hiratsuka/) | × 電話など | — | — |  | 申し込みは電話。電話が難しい人は窓口・ファクス・市のフォームでも |
| [広島市](/guide/hiroshima/) | ◯ だれでも | https://ogatagomi.city.hiroshima.lg.jp/ | 独自 |  |  |
| [茨木市](/guide/ibaraki/) | × 電話など | — | — |  | 申し込みの制度はありません。月1回の収集日に1家庭3点まで。臨時ごみは電話で予約 |
| [市原市](/guide/ichihara/) | × 電話など | — | — |  | 申し込みは電話だけ |
| [市川市](/guide/ichikawa/) | × 一時停止中 | — | — |  | インターネット・LINE受付は一時停止中（再開は市の公式ページで確認）。いまは電話で |
| [一宮市](/guide/ichinomiya/) | △ 条件つき | https://logoform.jp/form/Z3LR/325058 | logoform.jp（フォーム） |  | インターネットで申し込めるのは一部の品目だけ。一覧にない物は電話 |
| [入間市](/guide/iruma/) | ◯ だれでも | https://lin.ee/CLMytWg | 独自 |  | 市の公式LINEから |
| [伊勢崎市](/guide/isesaki/) | × 電話など | — | — |  | 申し込みの制度はありません。収集カレンダーの日に、名前を書いた紙を貼って集積所へ出します |
| [板橋区](/guide/itabashi/) | ◯ だれでも | https://ecolife.e-tumo.jp/itabashi_sodai-u/ | e-tumo.jp |  |  |
| [伊丹市](/guide/itami/) | ◯ だれでも | https://itami-sodai.jp | 独自 |  | ネットは先にキャッシュレスで払い、立ち会い不要。初めての人は先に受付センターに確かめるよう案内されています |
| [いわき市](/guide/iwaki/) | △ 条件つき | https://www.city.iwaki.lg.jp/www/contents/1722312210664/index.html | 独自 |  | 市公式LINEで1回3個まで。一覧にない品目と、枠がいっぱいのときは電話 |
| [和泉市](/guide/izumi/) | ◯ だれでも | — | — |  | 1回6点まで |
| [鹿児島市](/guide/kagoshima/) | ◯ だれでも | https://sodaigomi-city-kagoshima.jp/kagoshima/Web/login | 独自 |  | 初めての人・住所を変えた人は仮受付になり、市から確認の連絡が来ることがあります |
| [加古川市](/guide/kakogawa/) | ◯ だれでも | https://s-kantan.com/sodai-kakogawa-u/ | 独自 | 要 |  |
| [鎌倉市](/guide/kamakura/) | ◯ だれでも | http://sodai-sys.jp/kamakura/users/ | 独自 |  | 仮予約のあと、環境センターから本予約のメールが届きます |
| [金沢市](/guide/kanazawa/) | ◯ だれでも | https://www4.city.kanazawa.lg.jp/soshikikarasagasu/gomigenryosuishinka/gyomuannai/1/3/gomidasi_benri/line_sodaigomi.html | 独自 |  | 金沢市LINE公式アカウントの「ごみ出しサポート」から。申し込み内容の変更は電話 |
| [柏市](/guide/kashiwa/) | △ 条件つき | https://kashiwa.sodai.jp/ | 独自 |  | インターネット予約は柏地域だけ。沼南地域はクリーンセンターしらさぎへ電話で |
| [春日井市](/guide/kasugai/) | ◯ だれでも | https://ttzk.graffer.jp/city-kasugai/smart-apply/apply-procedure-alias/sadai | 独自 |  | 送ったあと市の担当者から電話があり、そこで収集日と料金が決まります（3営業日以内に折り返さないと取り下げになることがあります） |
| [春日部市](/guide/kasukabe/) | ◯ だれでも | — | — |  | 返事は次の開庁日以降。引越しなどの多量排出は電話だけ |
| [葛飾区](/guide/katsushika/) | ◯ だれでも | https://www2.sodai-web.jp/katsushika/index.html | sodai-web.jp |  |  |
| [川越市](/guide/kawagoe/) | × 電話など | — | — |  | 申し込みは電話 |
| [川口市](/guide/kawaguchi/) | ◯ だれでも | https://www.sodai-kawaguchi.jp/eco/view/kawaguchi/top.html | /eco/view/ 形式 |  |  |
| [川西市](/guide/kawanishi/) | ◯ だれでも | https://ecolife.e-tumo.jp/oogata-kawanishi-u/offer/offerList_initDisplay.action | e-tumo.jp |  |  |
| [川崎市](/guide/kawasaki/) | ◯ だれでも | https://www.sodai.city.kawasaki.jp/ | 独自 |  |  |
| [岸和田市](/guide/kishiwada/) | × 電話など | — | — |  | 申し込みは電話だけ |
| [北区](/guide/kita/) | ◯ だれでも | https://ecolife.e-tumo.jp/sodai-kita-tokyo-u/ | e-tumo.jp | 要 |  |
| [北九州市](/guide/kitakyushu/) | ◯ だれでも | https://www.sodai-kitakyushu.net/eco/view/kitakyushu/top.html | /eco/view/ 形式 |  |  |
| [神戸市](/guide/kobe/) | ◯ だれでも | https://www.ogatagomi.city.kobe.lg.jp/eco/view/kobe/top.html | /eco/view/ 形式 |  |  |
| [高知市](/guide/kochi/) | × 電話など | — | — |  | 申し込みの制度は見当たりません。月1回のステーション収集に出します |
| [小平市](/guide/kodaira/) | ◯ だれでも | https://www.city.kodaira.tokyo.jp/kurashi/000/000313.html | 独自 |  |  |
| [甲府市](/guide/kofu/) | × 電話など | — | — |  | 申し込みの制度はありません。処理券を貼って燃えないごみの日に集積所へ出します |
| [小金井市](/guide/koganei/) | △ 条件つき | https://logoform.jp/form/pCd3/1344660 | logoform.jp（フォーム） |  | オンラインフォームは試行中で、申し込みの多い約30品目だけ。ほかは電話か窓口 |
| [国分寺市](/guide/kokubunji/) | ◯ だれでも | https://www.city.kokubunji.tokyo.jp/kurashi/gomi/1012527/1016051.html | 独自 |  |  |
| [郡山市](/guide/koriyama/) | △ 条件つき | https://lgpos.task-asp.net/cu/072036/ea/residents/procedures/apply/56d9cc8a-de9f-4db2-94b6-3399651ab386/start | task-asp.net（フォーム） |  | インターネットで申し込めるのは決められた品目だけ。ほかは電話 |
| [越谷市](/guide/koshigaya/) | ◯ だれでも | https://www.city.koshigaya.saitama.jp/net/shigenjunkansuishinka/tetsuzukiapp050.html | 独自 |  |  |
| [江東区](/guide/koto/) | ◯ だれでも | https://www2.sodai-web.jp/koto/index.html | sodai-web.jp | 要 |  |
| [熊谷市](/guide/kumagaya/) | ◯ だれでも | https://s-kantan.jp/city-kumagaya-saitama-u/profile/userLogin_initDisplay.action?nextURL=CqTLFdO4voajwj31OrTw9DQ9f2VYJzSnVtXuWY28Gc8lkB36Cxx49L47m3NOeU81Di5fGIqMAk9s%0D%0AKTyW032Ql3UrNvJWF1JySYbmbX7brNI7%2FgSfkWZW6FzjJGpIAwOtdGGuJuVBVRj49pBRaLna5Q%3D%3D%0D%0Au%2F2pnQTLAb0%3D%0D%0A | 独自 |  | 運べない家具などの有料リクエスト収集の申し込み。小さい粗大ごみは申し込みなしで集積所へ |
| [熊本市](/guide/kumamoto/) | × 電話など | — | — |  | 申し込みは電話（ごみゼロコール）かファクス |
| [倉敷市](/guide/kurashiki/) | △ 条件つき | https://kurashiki.eco-ryobi.net/eco/view/kurashiki/top.html | /eco/view/ 形式 |  | インターネットは前に戸別収集を使った人だけ。初めての人は電話 |
| [呉市](/guide/kure/) | × 電話など | — | — |  | 申し込みの制度はありません。シールを貼って月1回の粗大ごみの日に出します（一部の地区は予約） |
| [久留米市](/guide/kurume/) | △ 条件つき | https://kurume-sodaigomi.com/receipts/home/<br>https://page.line.me/905lgpyt?openQrModal=true | 独自 |  | Web・LINEで申し込めるのは受付品目だけ。ほかは電話。締め切りは収集日の前日から数えて1週間前の17時 |
| [草津市](/guide/kusatsu/) | ◯ だれでも | https://lin.ee/5gQPgRP | 独自 |  | ウェブの予約サイトはなく、市のLINEから。締め切りは収集日の7日前 |
| [京都市](/guide/kyoto/) | ◯ だれでも | — | — |  | インターネット受付（年中無休）は、市の公式ページの案内から申し込みます |
| [町田市](/guide/machida/) | ◯ だれでも | https://www.m-ecokosha.or.jp/ | 独自 |  |  |
| [前橋市](/guide/maebashi/) | ◯ だれでも | https://ecolife.e-tumo.jp/kankyo-maebashi-u/ | e-tumo.jp |  | 1回3点まで |
| [松戸市](/guide/matsudo/) | ◯ だれでも | https://lgpos.task-asp.net/cu/122076/ea/residents/procedures/apply/13b97bdc-1bd6-483c-b05d-7bded6ed47d3/start | task-asp.net（フォーム） |  |  |
| [松江市](/guide/matsue/) | ◯ だれでも | https://f0e9e3ec.form.kintoneapp.com/public/sodaigomi-kaisyu-uketsuke | 独自 |  | 送ったあと粗大ごみ受付センターから電話で確認があります |
| [松本市](/guide/matsumoto/) | ◯ だれでも | https://logoform.jp/form/N7tm/697053 | logoform.jp（フォーム） |  | 軒先収集の対象は市が決めた11品目だけ |
| [松山市](/guide/matsuyama/) | △ 条件つき | https://www.city.matsuyama.ehime.jp/kurashi/gomi/dashikata/sodaigomi.html | 独自 |  | えひめ電子申請システムへの利用者登録が必要。地区ごとの申込期間（年6回）だけ受け付け。電話では申し込めない |
| [目黒区](/guide/meguro/) | ◯ だれでも | https://www2.sodai-web.jp/meguro/index.html | sodai-web.jp |  |  |
| [港区](/guide/minato/) | ◯ だれでも | https://ecolife.e-tumo.jp/sodai-minato-tokyo-u/offer/offerList_initDisplay | e-tumo.jp |  |  |
| [箕面市](/guide/minoh/) | × 電話など | https://www.city.minoh.lg.jp/seibi/02_howto/09how_to_rinji.html | 独自 |  | 申し込みの制度はありません。月2回の大型ごみの日に1回1個まで。臨時収集は電話かフォームで1週間前まで |
| [三郷市](/guide/misato/) | × 電話など | — | — |  | 申し込みは電話だけ |
| [三鷹市](/guide/mitaka/) | ◯ だれでも | https://www2.sodai-web.jp/mitaka/index.html | sodai-web.jp |  |  |
| [水戸市](/guide/mito/) | ◯ だれでも | https://94fef734.form.kintoneapp.com/public/bulky-garbage | 独自 |  | 送信したあとコールセンターから連絡があり、そこで収集日が決まります |
| [宮崎市](/guide/miyazaki/) | △ 条件つき | https://logoform.jp/form/HxnK/10590 | logoform.jp（フォーム） |  | 受付フォームを送ったあと市から電話があり、そこで受付完了（数日かかることがあります） |
| [守口市](/guide/moriguchi/) | △ 条件つき | https://www.eg-resource.jp/moriguchi/web | eg-resource.jp |  | 先に一度コールセンターに電話で申し込み、出す場所を登録した人だけ |
| [盛岡市](/guide/morioka/) | × 電話など | — | — |  | 申し込みは電話だけ（1回3点まで） |
| [武蔵野市](/guide/musashino/) | ◯ だれでも | https://www2.sodai-web.jp/musashino/index.html | sodai-web.jp |  |  |
| [長野市](/guide/nagano/) | × 電話など | — | — |  | 申し込みの制度はありません。小さい物はシールを貼って集積所へ、大きい物は資源再生センターへ持ち込み |
| [長岡市](/guide/nagaoka/) | ◯ だれでも | https://ecolife.e-tumo.jp/sodai-nagaoka-u/ | e-tumo.jp |  | 1回5点まで |
| [流山市](/guide/nagareyama/) | ◯ だれでも | https://sodai-sys.jp/nagareyama/users/ | 独自 |  | 収集は、いちばん早くて申し込みの10日後 |
| [長崎市](/guide/nagasaki/) | △ 条件つき | https://sodai.city.nagasaki.lg.jp/eco/view/nagasaki/top.html | /eco/view/ 形式 |  | インターネットで申し込めるのは品目一覧にある物だけ。ほかは電話 |
| [名古屋市](/guide/nagoya/) | ◯ だれでも | https://www.nagoya-sodaigomi.jp/eco/view/nagoya/top.html | /eco/view/ 形式 |  |  |
| [那覇市](/guide/naha/) | × 一時停止中 | — | — |  | インターネット受付は2026年10月時点で一時停止中（再開は市の公式ページで確認）。いまは電話で |
| [中野区](/guide/nakano/) | ◯ だれでも | https://www2.sodai-web.jp/nakano/index.html | sodai-web.jp |  |  |
| [奈良市](/guide/nara/) | △ 条件つき | https://www.city.nara.lg.jp/site/gomi-syusyu/121812.html | 独自 |  | インターネット受付は、2年以内に電話で申し込んだことがあり、氏名・町名・電話番号が一致する人だけ。キャンセルは電話だけ |
| [習志野市](/guide/narashino/) | ◯ だれでも | https://s-kantan.jp/city-narashino-chiba-u/offer/offerList_detail.action?tempSeq=1335 | 独自 |  | 受付が済んだあとの変更・取り消しは電話 |
| [練馬区](/guide/nerima/) | ◯ だれでも | https://www.sodai-nerima.jp/ | 独自 |  |  |
| [寝屋川市](/guide/neyagawa/) | × 電話など | — | — |  | 申し込みは電話だけ（臨時ごみ） |
| [新潟市](/guide/niigata/) | ◯ だれでも | https://www.sodai.city.niigata.jp/<br>https://www.city.niigata.lg.jp/kurashi/gomi/gomishigen/gomidasi/niigata/discard.html | 独自 | 要 |  |
| [新座市](/guide/niiza/) | ◯ だれでも | https://ecolife.e-tumo.jp/niizasodaiuketuke-u/offer/offerList_initDisplay.action | e-tumo.jp |  | 1回5点まで。回収が終わるまで次は申し込めません。収集まで1か月ほど |
| [西宮市](/guide/nishinomiya/) | ◯ だれでも | https://www.nishi.or.jp/kurashi/gomi/gominoshushu/seikatsugomi/moshikomi.html | 独自 |  | ウェブのフォームはなく、市の公式LINEで申し込みます（初回は仮受付） |
| [西尾市](/guide/nishio/) | × 電話など | — | — |  | 申し込みは電話か窓口 |
| [西東京市](/guide/nishitokyo/) | ◯ だれでも | https://logoform.jp/form/AAZE/199944 | logoform.jp（フォーム） |  |  |
| [沼津市](/guide/numazu/) | × 電話など | — | — |  | 申し込みの制度はありません。月1回の埋め立てごみの日に出すか、自分で持ち込みます |
| [小田原市](/guide/odawara/) | △ 条件つき | https://dshinsei.e-kanagawa.lg.jp/142069-u/offer/offerList_detail.action?tempSeq=34156 | 独自 |  | e-kanagawa の仮受付（先に利用者登録）。リサイクルセンターからの電話で予約が決まります |
| [大分市](/guide/oita/) | × 電話など | — | — |  | 申し込みは校区ごとの清掃事業所へ電話 |
| [岡山市](/guide/okayama/) | △ 条件つき | https://sodai.city.okayama.jp/ | 独自 |  | インターネット受付（戸別収集）は、前に電話で申し込んだことがある人が使えます。初めての人は電話で |
| [岡崎市](/guide/okazaki/) | ◯ だれでも | https://vein.bridgesany.com/okazaki/index.html | 独自 |  | 予約サイトの利用にLINEアカウントが必要 |
| [青梅市](/guide/ome/) | ◯ だれでも | https://www.city.ome.tokyo.jp/soshiki/23/100846.html | 独自 |  | 青梅市LINE公式アカウントから。市が確かめてから予約が決まります |
| [大阪市](/guide/osaka/) | ◯ だれでも | https://ecolife.e-tumo.jp/kankyo-osaka-u/ | e-tumo.jp |  |  |
| [大田区](/guide/ota/) | ◯ だれでも | https://www.ota-sodai.com | 独自 |  |  |
| [太田市](/guide/otagunma/) | × 電話など | — | — |  | 戸別収集は電話で予約。処理シールを貼ってごみステーションに出す方法は申し込み不要 |
| [大津市](/guide/otsu/) | ◯ だれでも | https://www.eg-resource.jp/otsu/web | eg-resource.jp |  | 初めての人は仮受付のあと本受付。5点を超える立会収集・一覧にない品目は電話 |
| [佐賀市](/guide/saga/) | △ 条件つき | https://www.gomiyoyaku.city.saga.lg.jp/eco/view/saga/top.html | /eco/view/ 形式 |  | 一覧にない品目・前に買ったステッカーを使うとき・2件目の申し込みは電話 |
| [相模原市](/guide/sagamihara/) | ◯ だれでも | https://www.sagamiharasodai-web.jp/sagamihara/index.html | sodai-web.jp |  |  |
| [さいたま市](/guide/saitama/) | ◯ だれでも | https://www.sodai.city.saitama.jp/ | 独自 |  |  |
| [堺市](/guide/sakai/) | ◯ だれでも | https://www.eg-resource.jp/sakai/ | eg-resource.jp |  |  |
| [佐倉市](/guide/sakura/) | × 電話など | — | — |  | 申し込みは地区ごとの収集業者へ電話 |
| [札幌市](/guide/sapporo/) | ◯ だれでも | https://sapporo-oogatagomi.jp/receipts/home | 独自 | 要 |  |
| [佐世保市](/guide/sasebo/) | ◯ だれでも | https://sodai-sys.jp/sasebo/users/ | 独自 |  | 締め切りは収集日の10日前。追加・変更・取り消しは電話 |
| [狭山市](/guide/sayama/) | ◯ だれでも | https://logoform.jp/form/6LWm/403949 | logoform.jp（フォーム） |  | 利用者登録が必要。1回5点まで |
| [仙台市](/guide/sendai/) | ◯ だれでも | https://www.sendai-sodai.jp/eco/view/sendai/top.html | /eco/view/ 形式 |  |  |
| [世田谷区](/guide/setagaya/) | ◯ だれでも | https://www.sodai-setagaya.jp/ | /eco/view/ 形式 |  |  |
| [渋谷区](/guide/shibuya/) | ◯ だれでも | https://p1.govtech-express.com/webui/1496310592?survey=a0OIj000000M4WMMA0 | govtech-express.com（フォーム） |  |  |
| [下関市](/guide/shimonoseki/) | ◯ だれでも | https://www.eco.city.shimonoseki.yamaguchi.jp/www2/pc/index.html | 独自 |  |  |
| [品川区](/guide/shinagawa/) | ◯ だれでも | https://shinagawa-sodai.com/items | 独自 |  |  |
| [新宿区](/guide/shinjuku/) | ◯ だれでも | https://www.shinjuku-sodai.com | 独自 | 要 |  |
| [静岡市](/guide/shizuoka/) | △ 条件つき | http://gomi.city.shizuoka.jp/gomi/ | 独自 |  | インターネット受付は2回目から。初めての人・住所が変わった人は電話で |
| [草加市](/guide/soka/) | ◯ だれでも | https://www.sodai-soka.jp/ | 独自 |  |  |
| [杉並区](/guide/suginami/) | ◯ だれでも | https://ecolife.e-tumo.jp/kankyo-suginami-tokyo-u/ | e-tumo.jp |  |  |
| [吹田市](/guide/suita/) | × 電話など | — | — |  | 大型複雑ごみは申し込み不要（収集日に出す）。引越しごみは電話 |
| [墨田区](/guide/sumida/) | ◯ だれでも | https://www2.sodai-web.jp/sumida/index.html | sodai-web.jp |  |  |
| [鈴鹿市](/guide/suzuka/) | × 電話など | — | — |  | 申し込みは電話だけ |
| [立川市](/guide/tachikawa/) | ◯ だれでも | https://sodaigomi.city.tachikawa.lg.jp/Public | 独自 |  |  |
| [台東区](/guide/taito/) | ◯ だれでも | https://ecolife.e-tumo.jp/taitosodai-u/<br>https://www.city.taito.lg.jp/kurashi/gomi/wakekata/gomiinfo/sodaigomi/tyattotukaikata.html | e-tumo.jp |  |  |
| [高松市](/guide/takamatsu/) | △ 条件つき | https://logoform.jp/form/dV7M/107290 | logoform.jp（フォーム） |  | 1回3点まで。品目リストにない物と、市外へ引っ越す人は電話 |
| [宝塚市](/guide/takarazuka/) | △ 条件つき | https://www.sodai-takarazuka.jp/eco/view/takarazuka/top.html | /eco/view/ 形式 |  | 初めての人と、2014年4月から使っていない人は、先に電話で申し込みます。名前・住所が変わったときも電話 |
| [高崎市](/guide/takasaki/) | × 電話など | — | — |  | 申し込みは電話（市が案内する地域ごとの受付先） |
| [高槻市](/guide/takatsuki/) | × 電話など | — | — |  | 申し込みの制度はありません。月1回の収集日に出します。引越しの臨時ごみは電話 |
| [多摩市](/guide/tama/) | ◯ だれでも | https://logoform.jp/form/4N4o/tamasodai | logoform.jp（フォーム） |  | 申請から収集まで中3日ほど。1回3点まで（引越しする人は最後の週に6点まで） |
| [戸田市](/guide/toda/) | ◯ だれでも | https://www.city.toda.saitama.jp/soshiki/154/joho-line-cashless.html | 独自 |  | ウェブの予約サイトはなく、市のLINEから（1回10点まで） |
| [所沢市](/guide/tokorozawa/) | ◯ だれでも | https://apply.e-tumo.jp/city-tokorozawa-saitama-u/offer/offerList_detail?tempSeq=83938<br>https://apply.e-tumo.jp/city-tokorozawa-saitama-u/inquiry/inquiry_initDisplay | e-tumo.jp |  | 申し込んだあと照会ページで収集日と手数料を確かめて完了する二段階式（反映まで数日かかることがあります） |
| [徳島市](/guide/tokushima/) | ◯ だれでも | https://sodai.city.tokushima.lg.jp/eco/view/tokushima/top.html | /eco/view/ 形式 |  |  |
| [豊島区](/guide/toshima/) | ◯ だれでも | https://ecolife.e-tumo.jp/toshima-sodai-u/ | e-tumo.jp |  |  |
| [鳥取市](/guide/tottori/) | ◯ だれでも | https://www.tottori-oogatagomi.com | 独自 |  |  |
| [富山市](/guide/toyama/) | × 電話など | — | — |  | 申し込みは電話だけ。品目ごとの申し込みはなく、多いときは予約制の戸別有料収集 |
| [豊橋市](/guide/toyohashi/) | △ 条件つき | https://gomi-yoyaku-toyohashi.jp/eco/view/toyohashi/top.html | /eco/view/ 形式 |  | インターネットは2回目から。初めての人は電話 |
| [豊川市](/guide/toyokawa/) | × 電話など | — | — |  | 申し込みは電話かファクス。粗大ごみ受付センターへ自分で運べば無料 |
| [豊中市](/guide/toyonaka/) | ◯ だれでも | https://www.eg-resource.jp/toyonaka | eg-resource.jp |  |  |
| [豊田市](/guide/toyota/) | ◯ だれでも | https://liff.line.me/1645278921-kWRPP32q/?accountId=toyotacity | LINE |  | ウェブのフォームはなく、豊田市LINE公式アカウントから（1回5個まで、6個以上は電話） |
| [津市](/guide/tsu/) | × 電話など | — | — |  | 申し込みの制度はありません。1m未満にして一時集積所に出すか、施設へ持ち込みます |
| [つくば市](/guide/tsukuba/) | ◯ だれでも | https://eco.city.tsukuba.ibaraki.jp/eco/view/tsukuba/top.html | /eco/view/ 形式 |  | 送信した時点では仮の受付。確認メールで決まります。締め切りは収集日の5日前 |
| [宇治市](/guide/uji/) | × 電話など | — | — |  | 申し込みの制度はありません。大きい物は電話で臨時の有料収集 |
| [浦安市](/guide/urayasu/) | △ 条件つき | https://s-kantan.jp/city-urayasu-chiba-u/offer/offerList_detail.action?tempSeq=957 | 独自 |  | 先に電子申請の利用者登録が必要。収集日は選べません。料金表にない品目は電話 |
| [宇都宮市](/guide/utsunomiya/) | ◯ だれでも | https://lgpos.task-asp.net/cu/092011/ea/residents/portal/home | task-asp.net（フォーム） |  | 送った時点では仮の予約。受付センターからの完了メールで決まります |
| [和歌山市](/guide/wakayama/) | △ 条件つき | https://www.sodai-wakayama-city.jp/ | 独自 |  | インターネット受付は2回目から。初めての人・市内で引っ越した人は電話で |
| [八千代市](/guide/yachiyo/) | × 電話など | — | — |  | 申し込みは電話だけ |
| [山形市](/guide/yamagata/) | △ 条件つき | https://www.yamagata-sodai.com/ | 独自 | 要 | 1回3点まで。一覧にない品目は電話。メールアドレスの登録が必要 |
| [大和市](/guide/yamato/) | △ 条件つき | https://dshinsei.e-kanagawa.lg.jp/142131-u/offer/offerList_detail?tempSeq=101381<br>https://dshinsei.e-kanagawa.lg.jp/142131-u/offer/offerList_detail?tempSeq=133707 | 独自 |  | インターネット（神奈川県の電子申請）は、市の「電子申請対象品一覧」に載っている品目だけ。ほかは電話で |
| [八尾市](/guide/yao/) | △ 条件つき | https://yao.sodai-web.jp/yao/index.html | sodai-web.jp | 要 | メールアドレスが必要。大きい物・重い物・一覧にない品目は電話 |
| [四日市市](/guide/yokkaichi/) | × 電話など | — | — |  | 申し込みは電話だけ |
| [横浜市](/guide/yokohama/) | ◯ だれでも | https://www.sodai.city.yokohama.lg.jp/eco/view/yokohama/top.html | /eco/view/ 形式 |  |  |
| [横須賀市](/guide/yokosuka/) | ◯ だれでも | https://www.yokosuka-sodai.com/receipts/home | 独自 |  |  |
| [座間市](/guide/zama/) | ◯ だれでも | https://page.line.me/810zmawg?openQrModal=true<br>https://www.city.zama.kanagawa.jp/shisei/koho/hashin/1005094.html | 独自 |  | 市のLINE公式アカウントから |

合計: ◯ だれでも 105、△ 条件つき 30、× 電話など 37、× 一時停止中 2

## 予約サイトの形ごと（ウェブ予約できる地域）

- 独自（64）：明石市・秋田市・安城市・旭川市・茅ヶ崎市・調布市・海老名市・藤沢市・福井市・福岡市・船橋市・秦野市・浜松市・東村山市・枚方市・広島市・入間市・伊丹市・いわき市・鹿児島市・加古川市・鎌倉市・金沢市・柏市・春日井市・川崎市・小平市・国分寺市・越谷市・熊谷市・久留米市・草津市・町田市・松江市・松山市・水戸市・流山市・奈良市・習志野市・練馬区・新潟市・西宮市・小田原市・岡山市・岡崎市・青梅市・大田区・さいたま市・札幌市・佐世保市・下関市・品川区・新宿区・静岡市・草加市・立川市・戸田市・鳥取市・浦安市・和歌山市・山形市・大和市・横須賀市・座間市
- e-tumo.jp（19）：足立区・上尾市・朝霞市・文京区・千代田区・中央区・江戸川区・板橋区・川西市・北区・前橋市・港区・長岡市・新座市・大阪市・杉並区・台東区・所沢市・豊島区
- /eco/view/ 形式（18）：尼崎市・厚木市・八王子市・東大阪市・川口市・北九州市・神戸市・倉敷市・長崎市・名古屋市・佐賀市・仙台市・世田谷区・宝塚市・徳島市・豊橋市・つくば市・横浜市
- sodai-web.jp（11）：荒川区・千葉市・葛飾区・江東区・目黒区・三鷹市・武蔵野市・中野区・相模原市・墨田区・八尾市
- logoform.jp（フォーム）（10）：福島市・日野市・一宮市・小金井市・松本市・宮崎市・西東京市・狭山市・高松市・多摩市
- eg-resource.jp（5）：府中市・守口市・大津市・堺市・豊中市
- task-asp.net（フォーム）（3）：郡山市・松戸市・宇都宮市
- govtech-express.com（フォーム）（1）：渋谷区
