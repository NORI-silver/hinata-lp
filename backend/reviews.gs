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
var AREAS = {yokohama:'横浜市', kawasaki:'川崎市', setagaya:'世田谷区', suginami:'杉並区', saitama:'さいたま市', chiba:'千葉市', sakura:'佐倉市'};
var CHAINS = ['セカンドストリート', 'ハードオフ', 'トレジャーファクトリー'];

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
  var query = CHAINS[chain] + ' ' + AREAS[city], idKey = 'PLACE_ID_' + city + '_' + chain;
  var placeId = props.getProperty(idKey);
  if (!placeId) {
    // IDだけの検索は無料
    var found = JSON.parse(UrlFetchApp.fetch('https://places.googleapis.com/v1/places:searchText', {
      method:'post', contentType:'application/json', muteHttpExceptions:true,
      headers:{'X-Goog-Api-Key':apiKey, 'X-Goog-FieldMask':'places.id'},
      payload:JSON.stringify({textQuery:query, languageCode:'ja', regionCode:'JP'})
    }).getContentText());
    placeId = found.places && found.places[0] && found.places[0].id;
    if (!placeId) return null;
    props.setProperty(idKey, placeId);
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
