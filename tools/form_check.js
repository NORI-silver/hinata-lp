// 診断フォームの自動チェック（粗大ごみフォーム点検エージェントが使う）
// 使い方: node tools/form_check.js .   （Playwright と Chromium が必要。NG があると終了コード1）
// 入力の組み合わせを実際にブラウザで入れて、判定と使いやすさを確かめる。
// 品目は「自由入力」で入れるので、チップの見た目を変えてもこのチェックは動く。
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const ROOT = path.resolve(process.argv[2] || ".");
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css", ".svg": "image/svg+xml", ".png": "image/png", ".webp": "image/webp", ".json": "application/json" };

function serve() {
  return new Promise(ok => {
    const s = http.createServer((q, r) => {
      let p = decodeURIComponent(q.url.split("?")[0]);
      if (p.endsWith("/")) p += "index.html";
      const f = path.join(ROOT, p);
      if (!f.startsWith(ROOT) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); }
      r.writeHead(200, { "content-type": TYPES[path.extname(f)] || "application/octet-stream" });
      fs.createReadStream(f).pipe(r);
    }).listen(0, () => ok(s));
  });
}

const results = [];
const check = (name, ok, detail = "") => { results.push({ name, ok: !!ok, detail }); };
const iso = n => { const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() + n); return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); };

// 入力のしかた（画面の操作と同じことをする）
async function fresh(page, base, q = "") { await page.goto(base + "/" + q); await page.waitForSelector("#qs .q"); }
async function city(page, v) { await page.click(`#qs button[data-k="city"][data-v="${v}"]`); }
async function addr(page, t) { await page.fill("#addr", t); await page.press("#addr", "Enter"); }
async function moveIn(page, n) { await page.fill("#move", iso(n)); await page.dispatchEvent("#move", "change"); }
async function item(page, t) { await page.fill("#free", t); await page.click("#addfree"); }
async function car(page, v) { await page.click(`#qs button[data-k="car"][data-v="${v}"]`); }
// 品目カードを読む：[{name, cat, rec, options:[{mark, name}]}]
const cards = page => page.$$eval("#out .icard", cs => cs.map(c => ({
  name: c.querySelector("h3").textContent.trim(),
  cat: (c.querySelector(".icat") || {}).textContent || "",
  rec: (c.querySelector(".irec") || {}).textContent || "",
  options: [...c.querySelectorAll(".io")].map(o => ({ mark: o.querySelector(".mk").textContent, name: o.querySelector(".ion b").textContent, text: o.textContent }))
})));
const cardOf = async (page, nm) => (await cards(page)).find(c => c.name === nm);
const cityOpt = c => c && c.options.find(o => /粗大ごみ回収$/.test(o.name));

async function run() {
  const srv = await serve(), base = `http://127.0.0.1:${srv.address().port}`;
  const br = await chromium.launch();
  const page = await br.newPage({ viewport: { width: 390, height: 844 } });
  const errs = []; page.on("pageerror", e => errs.push(e.message));
  await page.route(/^https?:\/\/(?!127\.0\.0\.1)/, r => r.abort()); // 外部には出ない

  // 1. 初期状態：勝手に選ばれていないこと
  await fresh(page, base);
  const pre = await page.evaluate(() => ({
    tags: document.querySelectorAll("#qs .tag").length,
    items: document.querySelectorAll('#qs [data-k="items"][aria-pressed="true"]').length,
    city: document.querySelectorAll('#qs [data-k="city"][aria-pressed="true"]').length,
    cards: document.querySelectorAll("#out .icard").length,
  }));
  check("初期状態で品目が選ばれていない（ソファなどの見本が入っていない）", pre.tags === 0 && pre.items === 0, JSON.stringify(pre));
  check("初期状態でお住まいが勝手に選ばれていない", pre.city === 0, `選択中 ${pre.city}`);
  check("入力前は品目カードを出さず、何を入れればよいかを案内する", pre.cards === 0, `カード ${pre.cards}`);

  // 2. 質問の数と選択肢の数（多すぎると迷う）
  const qs = await page.$$eval("#qs .q", qs => qs.map(q => ({ t: q.getAttribute("aria-label"), chips: q.querySelectorAll(".chips .chip").length })));
  check("質問は6つ以内", qs.length <= 6, qs.map(q => q.t).join("／"));
  const big = qs.filter(q => q.t !== "お住まい" && q.chips > 12);
  check("品目などのチップは1問12個以内（お住まいを除く）", !big.length, big.map(q => `${q.t}:${q.chips}`).join("、"));

  // 3. 家電4品目は市区で回収しない
  await fresh(page, base); await city(page, "yokohama"); await moveIn(page, 30);
  for (const t of ["冷蔵庫", "冷凍庫", "洗濯機", "衣類乾燥機", "テレビ", "エアコン"]) await item(page, t);
  for (const t of ["冷蔵庫", "冷凍庫", "洗濯機", "衣類乾燥機", "テレビ", "エアコン"]) {
    const c = await cardOf(page, t), o = cityOpt(c);
    check(`家電4品目「${t}」は市区の回収が×`, c && o && o.mark === "×", c ? `${c.cat} / ${o && o.mark}` : "カードなし");
  }

  // 4. 名前に家電の言葉が入っているだけの物を家電4品目にしない
  await fresh(page, base); await city(page, "yokohama"); await moveIn(page, 30);
  const look = ["テレビ台", "テレビボード", "食器乾燥機", "布団乾燥機", "洗濯機ラック", "冷蔵庫ラック", "エアコンカバー"];
  for (const t of look) await item(page, t);
  for (const t of look) {
    const c = await cardOf(page, t);
    check(`「${t}」を家電4品目として扱わない`, c && !/家電4品目/.test(c.cat), c ? c.cat : "カードなし");
  }

  // 5. 粗大ごみで出せないことが多い物を「市の回収◎」にしない
  await fresh(page, base); await city(page, "yokohama"); await moveIn(page, 30);
  for (const t of ["パソコン", "ノートパソコン", "ピアノ", "タイヤ", "消火器"]) await item(page, t);
  for (const t of ["パソコン", "ノートパソコン", "ピアノ", "タイヤ", "消火器"]) {
    const c = await cardOf(page, t), o = cityOpt(c);
    check(`「${t}」を市区の粗大ごみ回収のおすすめ（◎）にせず、ほかの出し方を示す`, c && !(o && o.mark === "◎") && c.options.filter(x => x.mark !== "×").length >= 1 && !c.options.some(x => /品目名を入れて/.test(x.name)), c ? `${c.cat} / ${o ? o.mark : "回収の行なし"} / ${c.options.map(x => x.mark + x.name).join("・")}` : "カードなし");
  }

  // 6. 一覧にない物を入れても、出し方の候補が出る（「名前を入れて」で止まらない）
  await fresh(page, base); await city(page, "yokohama"); await moveIn(page, 30);
  for (const t of ["衣装ケース", "ゴミ箱", "物干し竿", "ベビーカー"]) await item(page, t);
  for (const t of ["衣装ケース", "ゴミ箱", "物干し竿", "ベビーカー"]) {
    const c = await cardOf(page, t);
    check(`一覧にない「${t}」でも出し方の候補が出る`, c && c.options.length >= 2 && !c.options.some(o => /品目名を入れて/.test(o.name)), c ? `${c.options.length}件` : "カードなし");
  }

  // 7. 日数と車で判定が変わる
  await fresh(page, base); await city(page, "yokohama"); await moveIn(page, 30); await item(page, "ソファ");
  let c = await cardOf(page, "ソファ");
  check("横浜・30日後・ソファ → 市の回収がおすすめ", c && /粗大ごみ回収/.test(c.rec), c && c.rec);
  await moveIn(page, 3);
  c = await cardOf(page, "ソファ");
  check("横浜・3日後・車なし・ソファ → 市の回収はおすすめにしない", c && !/粗大ごみ回収$/.test(c.rec.replace("おすすめ:", "")), c && c.rec);
  await car(page, "yes");
  c = await cardOf(page, "ソファ");
  check("横浜・3日後・車あり・ソファ → 持込がおすすめ", c && /持込/.test(c.rec), c && c.rec);

  // 8. 住所入力・その他の地域
  await fresh(page, base); await addr(page, "佐倉市ユーカリが丘"); await moveIn(page, 30); await item(page, "ベッド");
  check("「佐倉市ユーカリが丘」→ 佐倉市で診断", /佐倉市/.test(await page.textContent("#addrmsg")), await page.textContent("#addrmsg"));
  await fresh(page, base); await addr(page, "大阪市北区"); await moveIn(page, 30); await item(page, "ベッド");
  const om = await page.textContent("#addrmsg");
  check("「大阪市北区」→ 大阪市で診断（東京の北区にしない）", /大阪市/.test(om), om);

  // 9. 料金は「目安」と出る
  await fresh(page, base); await city(page, "kawasaki"); await moveIn(page, 30); await item(page, "タンス"); await item(page, "冷蔵庫");
  const costs = await page.$$eval("#out .io:not(.ng) .ioc", es => es.map(e => e.textContent.trim()).filter(t => /¥|円/.test(t)));
  const bad = costs.filter(t => !/目安|受取/.test(t));
  check("金額にはすべて「目安」がつく", !bad.length, bad.join(" | "));

  // 10. スマホで横にはみ出さない・押しやすい
  const sw = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  check("スマホ幅（390px）で横スクロールが出ない", sw <= 1, `はみ出し ${sw}px`);
  const small = await page.$$eval("#qs .chip", es => es.filter(e => e.offsetParent && e.getBoundingClientRect().height < 36).map(e => e.textContent.trim()));
  check("チップの高さは36px以上（指で押しやすい）", !small.length, small.slice(0, 5).join("、"));

  // 11. 記事からの引き継ぎ（/?city=）
  await fresh(page, base, "?city=setagaya");
  const pc = await page.$$eval('#qs [data-k="city"][aria-pressed="true"]', es => es.map(e => e.dataset.v));
  check("/?city=setagaya で世田谷区が選ばれた状態になる", pc[0] === "setagaya", pc.join(","));

  check("ページのJavaScriptエラーがない", !errs.length, errs.join(" | "));

  await br.close(); srv.close();
  const ng = results.filter(r => !r.ok);
  for (const r of results) console.log(`${r.ok ? "OK" : "NG"}  ${r.name}${r.ok ? "" : `  … ${r.detail}`}`);
  console.log(`\n${results.length}件中 NG ${ng.length}件`);
  process.exit(ng.length ? 1 : 0);
}
run().catch(e => { console.error(e); process.exit(2); });
