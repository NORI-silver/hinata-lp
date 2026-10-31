/**
 * 粗大ごみ手配ナビ（hinata.shiokonbu.com）の「買取チェーンの口コミ」を取り寄せる Google Apps Script。
 * サイトは静的ページなので、地図サービスのキーはここ（スクリプトのプロパティ PLACES_API_KEY）にだけ置く。
 * 公開リポジトリなのでキーをこのファイルに書かないこと。
 *
 * 置き方：script.google.com で新しいプロジェクトを作り、このファイルの中身を貼る →
 *   プロジェクトの設定 → スクリプト プロパティ に PLACES_API_KEY を追加 →
 *   デプロイ → 新しいデプロイ → 種類「ウェブアプリ」・実行ユーザー「自分」・アクセス「全員」→ URL を reviews.js の GAS_URL に入れる。
 *
 * 規約（Google Maps Platform）に合わせて：点数・口コミは毎回取り寄せて保存しない（場所のIDだけは保存してよい）。
 * 出どころの表示「Google Maps」、書いた人（名前・アイコン・プロフィールへのリンク）、元の口コミへのリンクはサイト側で出す。
 */
var MONTHLY_LIMIT = 300; // 1か月に地図サービスへ問い合わせる回数の上限（pet と同じキーなら、合わせて無料の範囲に収める）
var TZ = 'Asia/Tokyo';
// 問い合わせてよい市区と買取チェーン（これ以外は受け付けない。reviews.js と同じ並び）
var AREAS = {yokohama:'横浜市', kawasaki:'川崎市', setagaya:'東京都世田谷区', suginami:'東京都杉並区', saitama:'さいたま市', chiba:'千葉市', sakura:'佐倉市', abiko:'我孫子市', adachi:'東京都足立区', ageo:'上尾市', akashi:'明石市', akishima:'昭島市', akita:'秋田市', amagasaki:'尼崎市', anjo:'安城市', aomori:'青森市', arakawa:'東京都荒川区', asahikawa:'旭川市', asaka:'朝霞市', atsugi:'厚木市', bunkyo:'東京都文京区', chigasaki:'茅ヶ崎市', chiyoda:'東京都千代田区', chofu:'調布市', chuo:'東京都中央区', daito:'大東市', ebina:'海老名市', edogawa:'東京都江戸川区', fuchu:'東京都府中市', fuji:'富士市', fujieda:'藤枝市', fujimi:'富士見市', fujimino:'ふじみ野市', fujisawa:'藤沢市', fukaya:'深谷市', fukui:'福井市', fukuoka:'福岡市', fukushima:'福島市', fukuyama:'福山市', funabashi:'船橋市', gifu:'岐阜市', hachinohe:'八戸市', hachioji:'八王子市', hadano:'秦野市', hakodate:'函館市', hamamatsu:'浜松市', higashihiroshima:'東広島市', higashikurume:'東久留米市', higashimurayama:'東村山市', higashiosaka:'東大阪市', himeji:'姫路市', hino:'日野市', hirakata:'枚方市', hiratsuka:'平塚市', hiroshima:'広島市', hitachinaka:'ひたちなか市', ibaraki:'茨木市', ichihara:'市原市', ichikawa:'市川市', ichinomiya:'一宮市', ikeda:'池田市', inagi:'稲城市', inzai:'印西市', iruma:'入間市', isesaki:'伊勢崎市', itabashi:'東京都板橋区', itami:'伊丹市', iwaki:'いわき市', izumi:'和泉市', kadoma:'門真市', kagoshima:'鹿児島市', kakogawa:'加古川市', kamagaya:'鎌ケ谷市', kamakura:'鎌倉市', kameoka:'亀岡市', kanazawa:'金沢市', kariya:'刈谷市', kashiwa:'柏市', kasugai:'春日井市', kasukabe:'春日部市', katsushika:'東京都葛飾区', kawagoe:'川越市', kawaguchi:'川口市', kawanishi:'川西市', kazo:'加須市', kisarazu:'木更津市', kishiwada:'岸和田市', kita:'東京都北区', kitakyushu:'北九州市', kobe:'神戸市', kochi:'高知市', kodaira:'小平市', kofu:'甲府市', koga:'古河市', koganei:'小金井市', kokubunji:'国分寺市', komaki:'小牧市', konosu:'鴻巣市', koriyama:'郡山市', koshigaya:'越谷市', koto:'東京都江東区', kuki:'久喜市', kumagaya:'熊谷市', kumamoto:'熊本市', kurashiki:'倉敷市', kure:'呉市', kurume:'久留米市', kusatsu:'草津市', kyotanabe:'京田辺市', kyoto:'京都市', machida:'町田市', maebashi:'前橋市', matsubara:'松原市', matsudo:'松戸市', matsue:'松江市', matsumoto:'松本市', matsuyama:'松山市', meguro:'東京都目黒区', minato:'東京都港区', minoh:'箕面市', misato:'三郷市', mitaka:'三鷹市', mito:'水戸市', miyazaki:'宮崎市', moriguchi:'守口市', morioka:'盛岡市', musashino:'武蔵野市', nagano:'長野市', nagaoka:'長岡市', nagareyama:'流山市', nagasaki:'長崎市', nagoya:'名古屋市', naha:'那覇市', nakano:'東京都中野区', nara:'奈良市', narashino:'習志野市', narita:'成田市', nerima:'東京都練馬区', neyagawa:'寝屋川市', niigata:'新潟市', niiza:'新座市', nishinomiya:'西宮市', nishio:'西尾市', nishitokyo:'西東京市', noda:'野田市', numazu:'沼津市', odawara:'小田原市', ogaki:'大垣市', oita:'大分市', okayama:'岡山市', okazaki:'岡崎市', ome:'青梅市', osaka:'大阪市', ota:'東京都大田区', otagunma:'太田市', otsu:'大津市', oyama:'小山市', saga:'佐賀市', sagamihara:'相模原市', sakado:'坂戸市', sakai:'堺市', sanda:'三田市', sapporo:'札幌市', sasebo:'佐世保市', sayama:'狭山市', sendai:'仙台市', seto:'瀬戸市', shibuya:'東京都渋谷区', shimonoseki:'下関市', shinagawa:'東京都品川区', shinjuku:'東京都新宿区', shizuoka:'静岡市', soka:'草加市', suita:'吹田市', sumida:'東京都墨田区', suzuka:'鈴鹿市', tachikawa:'立川市', taito:'東京都台東区', takamatsu:'高松市', takarazuka:'宝塚市', takasaki:'高崎市', takatsuki:'高槻市', tama:'多摩市', toda:'戸田市', tokorozawa:'所沢市', tokushima:'徳島市', toride:'取手市', toshima:'東京都豊島区', tottori:'鳥取市', toyama:'富山市', toyohashi:'豊橋市', toyokawa:'豊川市', toyonaka:'豊中市', toyota:'豊田市', tsu:'津市', tsuchiura:'土浦市', tsukuba:'つくば市', uji:'宇治市', urayasu:'浦安市', utsunomiya:'宇都宮市', wakayama:'和歌山市', yachiyo:'八千代市', yaizu:'焼津市', yamagata:'山形市', yamato:'大和市', yao:'八尾市', yokkaichi:'四日市市', yokosuka:'横須賀市', zama:'座間市'};
var CHAINS = ['セカンドストリート', 'ハードオフ', 'トレジャーファクトリー'];
// 検索で出た店がそのチェーンかを店名で確かめる（別の店・個人店を出さないため。AGENTS.md）
var CHAIN_RE = [/セカンドストリート|2nd ?STREET|セカスト/i, /ハードオフ|HARD ?OFF/i, /トレジャー ?ファクトリー|トレファク|TREASURE ?FACTORY/i];

function doGet(e) {
  var p = (e && e.parameter) || {};
  try {
    if (p.kind === 'shops') return json_(shops_(String(p.city || '')));
    if (p.kind === 'reviews') return json_(reviews_(String(p.city || ''), Number(p.chain)));
  } catch (err) {
    console.error(err);
  }
  return json_({ok:false, error:'unavailable'});
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

// 市区の買取チェーン（最寄りの1店ずつ）の名前・住所・点数・件数
function shops_(city) {
  if (!AREAS[city]) return {ok:false, error:'unknown'};
  var list = CHAINS.map(function(_, i) {
    var v = place_(city, i, 'displayName,formattedAddress,rating,userRatingCount');
    if (!v) return null;
    return {chain:i, name:(v.displayName || {}).text || CHAINS[i], address:v.formattedAddress || '', rating:v.rating || 0, count:Number(v.userRatingCount) || 0};
  }).filter(function(x) { return x; });
  return {ok:true, shops:list};
}

// 口コミ本文（地図サービスが関連度の高い順に返す最大5件）
function reviews_(city, chain) {
  if (!AREAS[city] || !(chain >= 0 && chain < CHAINS.length)) return {ok:false, error:'unknown'};
  var v = place_(city, chain, 'rating,userRatingCount,reviews,googleMapsUri');
  if (!v) return {ok:false, error:'unavailable'};
  return {ok:true, rating:v.rating || 0, count:Number(v.userRatingCount) || 0, mapsUrl:v.googleMapsUri || '', reviews:(v.reviews || []).slice(0, 5).map(function(x) {
    var a = x.authorAttribution || {};
    return {rating:x.rating || 0, when:x.relativePublishTimeDescription || '', text:((x.text || x.originalText || {}).text || '').slice(0, 2000),
      author:a.displayName || '', authorUrl:a.uri || '', photo:a.photoUri || '', url:x.googleMapsUri || ''};
  })};
}

function place_(city, chain, fields) {
  var props = PropertiesService.getScriptProperties(), apiKey = props.getProperty('PLACES_API_KEY');
  if (!apiKey) return null;
  var query = CHAINS[chain] + ' ' + AREAS[city], idKey = 'PID2_' + city + '_' + chain;
  var placeId = props.getProperty(idKey);
  if (placeId === 'none') return null;
  if (!placeId) {
    // 店名も取り寄せて、チェーン名に合う最初の店だけを使う（市区とチェーンごとに1回だけ）
    var found = JSON.parse(UrlFetchApp.fetch('https://places.googleapis.com/v1/places:searchText', {
      method:'post', contentType:'application/json', muteHttpExceptions:true,
      headers:{'X-Goog-Api-Key':apiKey, 'X-Goog-FieldMask':'places.id,places.displayName'},
      payload:JSON.stringify({textQuery:query, languageCode:'ja', regionCode:'JP', pageSize:5})
    }).getContentText());
    if (found.error) return null; // 検索の失敗は記録しない（次にもう一度試す）
    var hit = (found.places || []).filter(function(x) { return CHAIN_RE[chain].test((x.displayName || {}).text || ''); })[0];
    placeId = hit ? hit.id : 'none';
    props.setProperty(idKey, placeId);
    if (placeId === 'none') return null;
  }
  var month = 'COUNT_' + Utilities.formatDate(new Date(), TZ, 'yyyyMM'), used = Number(props.getProperty(month)) || 0;
  if (used >= MONTHLY_LIMIT) return null;
  props.setProperty(month, String(used + 1));
  var res = UrlFetchApp.fetch('https://places.googleapis.com/v1/places/' + encodeURIComponent(placeId) + '?languageCode=ja', {
    muteHttpExceptions:true, headers:{'X-Goog-Api-Key':apiKey, 'X-Goog-FieldMask':fields}
  });
  if (res.getResponseCode() !== 200) return null;
  return JSON.parse(res.getContentText());
}
