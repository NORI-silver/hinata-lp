/* 買取チェーンの近くのお店と口コミ（Google マップ）を、このサイトの中で見せる部品。
 * 置き方：<div class="shops" data-city="yokohama"></div> を置いて、このファイルを defer で読み込む。
 * 中身を後から差し替えたときは window.hinataShops.scan() を呼ぶ。
 * 点数・口コミは backend/reviews.gs が毎回取り寄せる（規約で保存しない）。出どころの「Google Maps」は訳さずそのまま出す。 */
(function(){
// backend/reviews.gs をウェブアプリとして公開した URL。空のあいだは、お店の名前と地図へのリンクだけを出す
var GAS_URL = "";
var AREAS = {yokohama:"横浜市", kawasaki:"川崎市", setagaya:"世田谷区", suginami:"杉並区", saitama:"さいたま市", chiba:"千葉市", sakura:"佐倉市"};
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

function fallback(box, city){
  box.replaceChildren();
  CHAINS.forEach(function(c){
    var s = el("div", "shop"); s.appendChild(el("h4", "", c + "（" + AREAS[city] + "周辺）"));
    var a = el("a", "ext", "地図でお店を見る（Google マップ）"); a.href = mapUrl(c + " " + AREAS[city]); a.target = "_blank"; a.rel = "noopener";
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
  if (!AREAS[city]) { box.replaceChildren(); return; }
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
function scan(){ document.querySelectorAll(".shops[data-city]").forEach(function(b){ if (io && GAS_URL && !memo[JSON.stringify({kind:"shops", city:b.getAttribute("data-city")})]) io.observe(b); else render(b); }); }
window.hinataShops = {scan:scan, render:render};
if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", scan); else scan();
})();
