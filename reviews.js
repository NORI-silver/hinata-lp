/* 買取チェーンの近くのお店と口コミ（Google マップ）を、このサイトの中で見せる部品。
 * 置き方：<div class="shops" data-city="yokohama"></div> を置いて、このファイルを defer で読み込む。
 * 口コミに対応していない市区は data-name="大阪市" のように市の名前を添えると、地図へのリンクだけを出す。
 * 中身を後から差し替えたときは window.hinataShops.scan() を呼ぶ。
 * 点数・口コミは backend/reviews.gs が毎回取り寄せる（規約で保存しない）。出どころの「Google Maps」は訳さずそのまま出す。 */
(function(){
// backend/reviews.gs をウェブアプリとして公開した URL。空のあいだは、お店の名前と地図へのリンクだけを出す
var GAS_URL = "https://script.google.com/macros/s/AKfycbw36d8YjMsAUqsVjVIU8u7ORWclYjX0kyid2XcGlljrHyJIjPJGmp3jEADxTr56UskjvA/exec";
var AREAS = {yokohama:"横浜市", kawasaki:"川崎市", setagaya:"東京都世田谷区", suginami:"東京都杉並区", saitama:"さいたま市", chiba:"千葉市", sakura:"佐倉市", adachi:"東京都足立区", ageo:"上尾市", akashi:"明石市", akita:"秋田市", amagasaki:"尼崎市", anjo:"安城市", aomori:"青森市", arakawa:"東京都荒川区", asahikawa:"旭川市", asaka:"朝霞市", atsugi:"厚木市", bunkyo:"東京都文京区", chigasaki:"茅ヶ崎市", chiyoda:"東京都千代田区", chofu:"調布市", chuo:"東京都中央区", ebina:"海老名市", edogawa:"東京都江戸川区", fuchu:"東京都府中市", fuji:"富士市", fujisawa:"藤沢市", fukui:"福井市", fukuoka:"福岡市", fukushima:"福島市", fukuyama:"福山市", funabashi:"船橋市", gifu:"岐阜市", hachinohe:"八戸市", hachioji:"八王子市", hadano:"秦野市", hakodate:"函館市", hamamatsu:"浜松市", higashimurayama:"東村山市", higashiosaka:"東大阪市", himeji:"姫路市", hino:"日野市", hirakata:"枚方市", hiratsuka:"平塚市", hiroshima:"広島市", ibaraki:"茨木市", ichihara:"市原市", ichikawa:"市川市", ichinomiya:"一宮市", iruma:"入間市", isesaki:"伊勢崎市", itabashi:"東京都板橋区", itami:"伊丹市", iwaki:"いわき市", izumi:"和泉市", kagoshima:"鹿児島市", kakogawa:"加古川市", kamakura:"鎌倉市", kanazawa:"金沢市", kashiwa:"柏市", kasugai:"春日井市", kasukabe:"春日部市", katsushika:"東京都葛飾区", kawagoe:"川越市", kawaguchi:"川口市", kawanishi:"川西市", kishiwada:"岸和田市", kita:"東京都北区", kitakyushu:"北九州市", kobe:"神戸市", kochi:"高知市", kodaira:"小平市", kofu:"甲府市", koganei:"小金井市", kokubunji:"国分寺市", koriyama:"郡山市", koshigaya:"越谷市", koto:"東京都江東区", kumagaya:"熊谷市", kumamoto:"熊本市", kurashiki:"倉敷市", kure:"呉市", kurume:"久留米市", kusatsu:"草津市", kyoto:"京都市", machida:"町田市", maebashi:"前橋市", matsudo:"松戸市", matsue:"松江市", matsumoto:"松本市", matsuyama:"松山市", meguro:"東京都目黒区", minato:"東京都港区", minoh:"箕面市", misato:"三郷市", mitaka:"三鷹市", mito:"水戸市", miyazaki:"宮崎市", moriguchi:"守口市", morioka:"盛岡市", musashino:"武蔵野市", nagano:"長野市", nagaoka:"長岡市", nagareyama:"流山市", nagasaki:"長崎市", nagoya:"名古屋市", naha:"那覇市", nakano:"東京都中野区", nara:"奈良市", narashino:"習志野市", nerima:"東京都練馬区", neyagawa:"寝屋川市", niigata:"新潟市", niiza:"新座市", nishinomiya:"西宮市", nishio:"西尾市", nishitokyo:"西東京市", numazu:"沼津市", odawara:"小田原市", oita:"大分市", okayama:"岡山市", okazaki:"岡崎市", ome:"青梅市", osaka:"大阪市", ota:"東京都大田区", otagunma:"太田市", otsu:"大津市", saga:"佐賀市", sagamihara:"相模原市", sakai:"堺市", sapporo:"札幌市", sasebo:"佐世保市", sayama:"狭山市", sendai:"仙台市", shibuya:"東京都渋谷区", shimonoseki:"下関市", shinagawa:"東京都品川区", shinjuku:"東京都新宿区", shizuoka:"静岡市", soka:"草加市", suita:"吹田市", sumida:"東京都墨田区", suzuka:"鈴鹿市", tachikawa:"立川市", taito:"東京都台東区", takamatsu:"高松市", takarazuka:"宝塚市", takasaki:"高崎市", takatsuki:"高槻市", tama:"多摩市", toda:"戸田市", tokorozawa:"所沢市", tokushima:"徳島市", toshima:"東京都豊島区", tottori:"鳥取市", toyama:"富山市", toyohashi:"豊橋市", toyokawa:"豊川市", toyonaka:"豊中市", toyota:"豊田市", tsu:"津市", tsukuba:"つくば市", uji:"宇治市", urayasu:"浦安市", utsunomiya:"宇都宮市", wakayama:"和歌山市", yachiyo:"八千代市", yamagata:"山形市", yamato:"大和市", yao:"八尾市", yokkaichi:"四日市市", yokosuka:"横須賀市", zama:"座間市"};
var CHAINS = ["セカンドストリート", "ハードオフ", "トレジャーファクトリー"];
var memo = {}; // 同じページを開いているあいだだけ覚える（保存はしない）

var css = ".shops{display:flex;flex-direction:column;gap:8px;margin:6px 0}"
 + ".shop{border:1px solid var(--line,#DCE6EE);border-radius:12px;padding:10px 12px;background:var(--bg,#fff);display:flex;flex-direction:column;gap:4px;text-align:left}"
 + ".shop h4{margin:0;font-size:14px;line-height:1.4;color:var(--ink,#14324A)}"
 + ".shop .addr{font-size:11px;color:var(--muted,#587184)}"
 + ".shop .score{display:flex;align-items:center;gap:6px;flex-wrap:wrap;font-size:13px;margin:0}"
 + ".shop .stars{position:relative;display:inline-block;font-size:14px;letter-spacing:1px;color:#D6DDE3;line-height:1}"
 + ".shop .stars::before{content:'★★★★★'}.shop .stars i{position:absolute;inset:0 auto 0 0;overflow:hidden;color:#F5A623;font-style:normal;white-space:nowrap;width:var(--fill)}.shop .stars i::before{content:'★★★★★'}"
 + ".shop .cnt{font-size:12px;color:var(--muted,#587184)}"
 + ".shop .open{border:0;background:none;padding:0;font:inherit;font-size:12px;font-weight:700;color:var(--accent,#0A74B8);text-decoration:underline;text-underline-offset:3px;cursor:pointer;align-self:flex-start}"
 + ".shop .src{font-family:Roboto,Arial,sans-serif;font-size:11px;color:#5f6368}"
 + ".shop .panel{background:var(--tint,#F2F8FC);border-radius:10px;padding:8px 10px;font-size:12px}.shop .panel[hidden]{display:none}"
 + ".shop .rv{border-top:1px solid var(--line,#DCE6EE);padding:8px 0}.shop .rv:first-of-type{border-top:0}"
 + ".shop .who{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.shop .who img{border-radius:50%}.shop .who a,.shop .who span{font-weight:700;color:var(--ink,#14324A)}.shop .who small{color:var(--muted,#587184)}"
 + ".shop .rv p{margin:4px 0;white-space:pre-wrap;line-height:1.6}.shop .rv a.orig{font-size:11px;color:var(--muted,#587184)}"
 + ".shop .head{margin:0 0 4px;font-size:11px;color:var(--muted,#587184)}.shop .panel .src{display:block;text-align:right;margin-top:4px}"
 + ".shop .ext{font-size:12px;color:var(--accent,#0A74B8)}.shops .note{font-size:11px;color:var(--muted,#587184);margin:0}";
var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

function el(tag, cls, text){ var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
function mapUrl(q){ return "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(q); }
function get(params){
  var key = JSON.stringify(params);
  if (!memo[key]) memo[key] = fetch(GAS_URL + "?" + new URLSearchParams(params)).then(function(r){ return r.json(); }).catch(function(){ delete memo[key]; return null; });
  return memo[key];
}
function track(name){ try { if (window.gtag) window.gtag("event", name); } catch (e) {} }

function fallback(box, city, area){
  area = area || AREAS[city];
  box.replaceChildren();
  CHAINS.forEach(function(c){
    var s = el("div", "shop"); s.appendChild(el("h4", "", c + "（" + area + "周辺）"));
    var a = el("a", "ext", "地図でお店を見る（Google マップ）"); a.href = mapUrl(c + " " + area); a.target = "_blank"; a.rel = "noopener";
    s.appendChild(a); box.appendChild(s);
  });
  box.appendChild(el("p", "note", "買取チェーンの例です。提携しているお店ではありません。出張査定・キャンセル無料かどうかを確認してから頼みます。"));
}

function openReviews(city, chain, panel, btn){
  if (!panel.hidden) { panel.hidden = true; btn.setAttribute("aria-expanded", "false"); return; }
  panel.hidden = false; btn.setAttribute("aria-expanded", "true"); track("open_reviews");
  if (panel.dataset.done) return;
  panel.textContent = "口コミを読み込んでいます…";
  get({kind:"reviews", city:city, chain:chain}).then(function(j){
    if (!j || !j.ok || !Array.isArray(j.reviews)) throw 0;
    panel.dataset.done = "1"; panel.replaceChildren();
    panel.appendChild(el("p", "head", "関連度の高い順に、最大5件を表示しています（全" + j.count + "件）。"));
    j.reviews.forEach(function(v){
      var item = el("div", "rv"), who = el("div", "who");
      if (v.photo) { var img = el("img"); img.src = v.photo; img.alt = ""; img.width = 24; img.height = 24; img.loading = "lazy"; img.referrerPolicy = "no-referrer"; who.appendChild(img); }
      var name = el(v.authorUrl ? "a" : "span", "", v.author || "投稿者");
      if (v.authorUrl) { name.href = v.authorUrl; name.target = "_blank"; name.rel = "noopener"; }
      who.append(name, el("small", "", "★" + v.rating + (v.when ? "・" + v.when : "")));
      item.appendChild(who);
      if (v.text) item.appendChild(el("p", "", v.text));
      if (v.url) { var a = el("a", "orig", "元の口コミを見る"); a.href = v.url; a.target = "_blank"; a.rel = "noopener"; item.appendChild(a); }
      panel.appendChild(item);
    });
    panel.appendChild(el("span", "src", "Google Maps"));
  }).catch(function(){ panel.textContent = "口コミを読み込めませんでした。時間をおいてもう一度お試しください。"; });
}

function render(box){
  var city = box.getAttribute("data-city");
  // 口コミを取り寄せていない市区（全国の記事など）は、data-name の市の名前で地図へのリンクだけを出す
  if (!AREAS[city]) { var nm = (box.getAttribute("data-name") || "").trim(); if (nm) fallback(box, city, nm); else box.replaceChildren(); return; }
  if (box.dataset.shown === city && box.childNodes.length) return;
  box.dataset.shown = city;
  if (!GAS_URL) { fallback(box, city); return; }
  box.textContent = "近くのお店を読み込んでいます…";
  get({kind:"shops", city:city}).then(function(j){
    if (!j || !j.ok || !j.shops || !j.shops.length) throw 0;
    box.replaceChildren();
    j.shops.forEach(function(v){
      var s = el("div", "shop");
      s.appendChild(el("h4", "", v.name));
      if (v.address) s.appendChild(el("span", "addr", v.address.replace(/^日本、(〒\d{3}-\d{4} )?/, "")));
      if (v.rating > 0) {
        var score = el("p", "score"), stars = el("span", "stars"); stars.setAttribute("aria-hidden", "true");
        var fill = el("i"); fill.style.setProperty("--fill", Math.max(0, Math.min(5, v.rating)) / 5 * 100 + "%"); stars.appendChild(fill);
        score.setAttribute("aria-label", "口コミの評価 5点中" + Number(v.rating).toFixed(1) + "点、" + v.count + "件");
        score.append(stars, el("b", "", Number(v.rating).toFixed(1)), el("span", "cnt", "（口コミ " + v.count + "件）"), el("span", "src", "Google Maps"));
        s.appendChild(score);
        var btn = el("button", "open", "Google マップの口コミ"); btn.type = "button"; btn.setAttribute("aria-expanded", "false");
        var panel = el("div", "panel"); panel.hidden = true;
        btn.addEventListener("click", function(){ openReviews(city, v.chain, panel, btn); });
        s.append(btn, panel);
      }
      box.appendChild(s);
    });
    box.appendChild(el("p", "note", "買取チェーンの近くのお店です。提携しているお店ではありません。出張査定・キャンセル無料かどうかを確認してから頼みます。"));
  }).catch(function(){ fallback(box, city); });
}

// 画面に入ったときだけ読み込む（地図サービスへの問い合わせ回数を抑える）
var io = "IntersectionObserver" in window ? new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting) { io.unobserve(e.target); render(e.target); } }); }, {rootMargin:"200px"}) : null;
function scan(){ document.querySelectorAll(".shops[data-city]").forEach(function(b){ if (io && GAS_URL && AREAS[b.getAttribute("data-city")] && !memo[JSON.stringify({kind:"shops", city:b.getAttribute("data-city")})]) io.observe(b); else render(b); }); }
window.hinataShops = {scan:scan, render:render};
if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", scan); else scan();
})();
