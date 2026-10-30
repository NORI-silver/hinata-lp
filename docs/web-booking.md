# ウェブ予約できる自治体（2026-10-30 確認）

`python3 tools/guide/areas.py .` が地域記事と `tools/guide/booking.json` から作る一覧。手で直さない。
予約サイトの「形」は URL から分けたもので、同じ形なら空き枠の見張りを同じしくみで作れる見込み（運営会社は確かめていない）。
メール登録＝申し込みの前にメールアドレスの登録が要ると公式・予約サイトで確かめたもの（空欄は未確認）。

| 地域 | ウェブ予約 | 予約サイト | 形 | メール登録 | メモ |
|---|---|---|---|---|---|
| [足立区](/guide/adachi/) | ◯ だれでも | https://ecolife.e-tumo.jp/sodai-adachi-u/ | e-tumo.jp |  |  |
| [荒川区](/guide/arakawa/) | ◯ だれでも | https://www2.sodai-web.jp/arakawa/index.html | sodai-web.jp |  |  |
| [文京区](/guide/bunkyo/) | ◯ だれでも | https://ecolife.e-tumo.jp/sodai-bunkyo-tokyo-u/ | e-tumo.jp |  |  |
| [千葉市](/guide/chiba/) | ◯ だれでも | https://www.sodai-web.jp/chiba/index.html | sodai-web.jp |  |  |
| [千代田区](/guide/chiyoda/) | ◯ だれでも | https://ecolife.e-tumo.jp/sodai.city.chiyoda-u/offer/offerList_initDisplay | e-tumo.jp |  |  |
| [調布市](/guide/chofu/) | ◯ だれでも | https://sodai.city.chofu.tokyo.jp/ | 独自 |  |  |
| [中央区](/guide/chuo/) | ◯ だれでも | https://ecolife.e-tumo.jp/kankyo-chuo-tokyo-u/ | e-tumo.jp |  |  |
| [江戸川区](/guide/edogawa/) | ◯ だれでも | https://ecolife.e-tumo.jp/edogawa.tokyo-u/offer/offerList_initDisplay | e-tumo.jp | 要 |  |
| [府中市](/guide/fuchu/) | ◯ だれでも | https://www.eg-resource.jp/sodai_fuchu/web/ | eg-resource.jp |  |  |
| [福岡市](/guide/fukuoka/) | ◯ だれでも | https://sodaigomi-kankyo.city.fukuoka.lg.jp/<br>https://www.city.fukuoka.lg.jp/kankyo/kateigomi/hp/LINE-sodaigomi.html | 独自 |  |  |
| [船橋市](/guide/funabashi/) | ◯ だれでも | https://www.sodai-funabashi.jp/ | 独自 |  |  |
| [岐阜市](/guide/gifu/) | × 電話など | https://logoform.jp/form/BcLm/62949 | logoform.jp（フォーム） |  | 収集の予約は電話だけ。インターネット（オンライン受付）は持ち込み（直接搬入）の予約に使えます |
| [八王子市](/guide/hachioji/) | ◯ だれでも | https://sodai.city.hachioji.tokyo.jp/eco/view/hachioji/top.html | /eco/view/ 形式 |  |  |
| [浜松市](/guide/hamamatsu/) | ◯ だれでも | https://www.city.hamamatsu.shizuoka.jp/ippai/gomi/dashikata/dashikata/renrakugomi_line.html<br>https://www.city.hamamatsu.shizuoka.jp/ippai/gomi/dashikata/dashikata/renrakugomi_in_nagare.html | 独自 |  |  |
| [枚方市](/guide/hirakata/) | △ 条件つき | https://www.city.hirakata.osaka.jp/0000010721.html | 独自 |  | インターネット予約は、今までに電話で申し込んだことがある人だけ。初めての人・住所が変わった人は電話で |
| [広島市](/guide/hiroshima/) | ◯ だれでも | https://ogatagomi.city.hiroshima.lg.jp/ | 独自 |  |  |
| [市川市](/guide/ichikawa/) | × 一時停止中 | — | — |  | インターネット・LINE受付は一時停止中（再開は市の公式ページで確認）。いまは電話で |
| [板橋区](/guide/itabashi/) | ◯ だれでも | https://ecolife.e-tumo.jp/itabashi_sodai-u/ | e-tumo.jp |  |  |
| [葛飾区](/guide/katsushika/) | ◯ だれでも | https://www2.sodai-web.jp/katsushika/index.html | sodai-web.jp |  |  |
| [川口市](/guide/kawaguchi/) | ◯ だれでも | https://www.sodai-kawaguchi.jp/eco/view/kawaguchi/top.html | /eco/view/ 形式 |  |  |
| [川崎市](/guide/kawasaki/) | ◯ だれでも | https://www.sodai.city.kawasaki.jp/ | 独自 |  |  |
| [北区](/guide/kita/) | ◯ だれでも | https://ecolife.e-tumo.jp/sodai-kita-tokyo-u/ | e-tumo.jp | 要 |  |
| [北九州市](/guide/kitakyushu/) | ◯ だれでも | https://www.sodai-kitakyushu.net/eco/view/kitakyushu/top.html | /eco/view/ 形式 |  |  |
| [神戸市](/guide/kobe/) | ◯ だれでも | https://www.ogatagomi.city.kobe.lg.jp/eco/view/kobe/top.html | /eco/view/ 形式 |  |  |
| [江東区](/guide/koto/) | ◯ だれでも | https://www2.sodai-web.jp/koto/index.html | sodai-web.jp | 要 |  |
| [熊本市](/guide/kumamoto/) | × 電話など | — | — |  | 申し込みは電話（ごみゼロコール）かファクス |
| [京都市](/guide/kyoto/) | ◯ だれでも | — | — |  | インターネット受付（年中無休）は、市の公式ページの案内から申し込みます |
| [町田市](/guide/machida/) | ◯ だれでも | https://www.m-ecokosha.or.jp/ | 独自 |  |  |
| [松戸市](/guide/matsudo/) | ◯ だれでも | https://lgpos.task-asp.net/cu/122076/ea/residents/procedures/apply/13b97bdc-1bd6-483c-b05d-7bded6ed47d3/start | task-asp.net（フォーム） |  |  |
| [目黒区](/guide/meguro/) | ◯ だれでも | https://www2.sodai-web.jp/meguro/index.html | sodai-web.jp |  |  |
| [港区](/guide/minato/) | ◯ だれでも | https://ecolife.e-tumo.jp/sodai-minato-tokyo-u/offer/offerList_initDisplay | e-tumo.jp |  |  |
| [三鷹市](/guide/mitaka/) | ◯ だれでも | https://www2.sodai-web.jp/mitaka/index.html | sodai-web.jp |  |  |
| [武蔵野市](/guide/musashino/) | ◯ だれでも | https://www2.sodai-web.jp/musashino/index.html | sodai-web.jp |  |  |
| [名古屋市](/guide/nagoya/) | ◯ だれでも | https://www.nagoya-sodaigomi.jp/eco/view/nagoya/top.html | /eco/view/ 形式 |  |  |
| [那覇市](/guide/naha/) | × 一時停止中 | — | — |  | インターネット受付は2026年10月時点で一時停止中（再開は市の公式ページで確認）。いまは電話で |
| [中野区](/guide/nakano/) | ◯ だれでも | https://www2.sodai-web.jp/nakano/index.html | sodai-web.jp |  |  |
| [練馬区](/guide/nerima/) | ◯ だれでも | https://www.sodai-nerima.jp/ | 独自 |  |  |
| [新潟市](/guide/niigata/) | ◯ だれでも | https://www.sodai.city.niigata.jp/<br>https://www.city.niigata.lg.jp/kurashi/gomi/gomishigen/gomidasi/niigata/discard.html | 独自 | 要 |  |
| [西東京市](/guide/nishitokyo/) | ◯ だれでも | https://logoform.jp/form/AAZE/199944 | logoform.jp（フォーム） |  |  |
| [岡山市](/guide/okayama/) | △ 条件つき | https://sodai.city.okayama.jp/ | 独自 |  | インターネット受付（戸別収集）は、前に電話で申し込んだことがある人が使えます。初めての人は電話で |
| [大阪市](/guide/osaka/) | ◯ だれでも | https://ecolife.e-tumo.jp/kankyo-osaka-u/ | e-tumo.jp |  |  |
| [大田区](/guide/ota/) | ◯ だれでも | https://www.ota-sodai.com | 独自 |  |  |
| [相模原市](/guide/sagamihara/) | ◯ だれでも | https://www.sagamiharasodai-web.jp/sagamihara/index.html | sodai-web.jp |  |  |
| [さいたま市](/guide/saitama/) | ◯ だれでも | https://www.sodai.city.saitama.jp/ | 独自 |  |  |
| [堺市](/guide/sakai/) | ◯ だれでも | https://www.eg-resource.jp/sakai/ | eg-resource.jp |  |  |
| [佐倉市](/guide/sakura/) | × 電話など | — | — |  | 申し込みは地区ごとの収集業者へ電話 |
| [札幌市](/guide/sapporo/) | ◯ だれでも | https://sapporo-oogatagomi.jp/receipts/home | 独自 | 要 |  |
| [仙台市](/guide/sendai/) | ◯ だれでも | https://www.sendai-sodai.jp/eco/view/sendai/top.html | /eco/view/ 形式 |  |  |
| [世田谷区](/guide/setagaya/) | ◯ だれでも | https://www.sodai-setagaya.jp/ | /eco/view/ 形式 |  |  |
| [渋谷区](/guide/shibuya/) | ◯ だれでも | https://p1.govtech-express.com/webui/1496310592?survey=a0OIj000000M4WMMA0 | govtech-express.com（フォーム） |  |  |
| [品川区](/guide/shinagawa/) | ◯ だれでも | https://shinagawa-sodai.com/items | 独自 |  |  |
| [新宿区](/guide/shinjuku/) | ◯ だれでも | https://www.shinjuku-sodai.com | 独自 | 要 |  |
| [静岡市](/guide/shizuoka/) | △ 条件つき | http://gomi.city.shizuoka.jp/gomi/ | 独自 |  | インターネット受付は2回目から。初めての人・住所が変わった人は電話で |
| [杉並区](/guide/suginami/) | ◯ だれでも | https://ecolife.e-tumo.jp/kankyo-suginami-tokyo-u/ | e-tumo.jp |  |  |
| [墨田区](/guide/sumida/) | ◯ だれでも | https://www2.sodai-web.jp/sumida/index.html | sodai-web.jp |  |  |
| [台東区](/guide/taito/) | ◯ だれでも | https://ecolife.e-tumo.jp/taitosodai-u/<br>https://www.city.taito.lg.jp/kurashi/gomi/wakekata/gomiinfo/sodaigomi/tyattotukaikata.html | e-tumo.jp |  |  |
| [徳島市](/guide/tokushima/) | ◯ だれでも | https://sodai.city.tokushima.lg.jp/eco/view/tokushima/top.html | /eco/view/ 形式 |  |  |
| [豊島区](/guide/toshima/) | ◯ だれでも | https://ecolife.e-tumo.jp/toshima-sodai-u/ | e-tumo.jp |  |  |
| [豊中市](/guide/toyonaka/) | ◯ だれでも | https://www.eg-resource.jp/toyonaka | eg-resource.jp |  |  |
| [横浜市](/guide/yokohama/) | ◯ だれでも | https://www.sodai.city.yokohama.lg.jp/eco/view/yokohama/top.html | /eco/view/ 形式 |  |  |

合計: ◯ だれでも 52、× 電話など 3、△ 条件つき 3、× 一時停止中 2

## 予約サイトの形ごと（ウェブ予約できる地域）

- 独自（17）：調布市・福岡市・船橋市・浜松市・枚方市・広島市・川崎市・町田市・練馬区・新潟市・岡山市・大田区・さいたま市・札幌市・品川区・新宿区・静岡市
- e-tumo.jp（12）：足立区・文京区・千代田区・中央区・江戸川区・板橋区・北区・港区・大阪市・杉並区・台東区・豊島区
- sodai-web.jp（10）：荒川区・千葉市・葛飾区・江東区・目黒区・三鷹市・武蔵野市・中野区・相模原市・墨田区
- /eco/view/ 形式（9）：八王子市・川口市・北九州市・神戸市・名古屋市・仙台市・世田谷区・徳島市・横浜市
- eg-resource.jp（3）：府中市・堺市・豊中市
- task-asp.net（フォーム）（1）：松戸市
- logoform.jp（フォーム）（1）：西東京市
- govtech-express.com（フォーム）（1）：渋谷区
