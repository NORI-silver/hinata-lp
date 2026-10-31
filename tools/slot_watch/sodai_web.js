// 粗大ごみ 空き枠見張り PoC（2026-10-31〜11-14、無料・記録のみ）
// sodai-web.jp の公開ページ「収集日の確認（最短収集日）」を区ごとに読み、CSV に1行ずつ足す。
// ログインや申し込みはしない。1回の実行で数リクエストだけ、間を5秒あける。
// 使い方: node tools/slot_watch/sodai_web.js <追記するCSVのパス>
const { chromium } = require('playwright');
const fs = require('fs');

// 見張る市（公開の最短収集日ページがある sodai-web.jp の市だけ）
const TARGETS = [
  { city: 'chiba', name: '千葉市', url: 'https://www.sodai-web.jp/sodai/shortest_calendar.na?id=09' },
];
const UA = 'hinata-slot-poc/1.0 (+https://hinata.shiokonbu.com/about/)';
const WAIT_MS = 5000;

(async () => {
  const out = process.argv[2] || 'slot-watch.csv';
  if (!fs.existsSync(out)) fs.writeFileSync(out, 'checked_at_jst,city,ward_code,ward,earliest\n');
  const now = new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 16).replace('T', ' ');
  const browser = await chromium.launch();
  const page = await browser.newPage({ userAgent: UA, locale: 'ja-JP' });
  // 翻訳スクリプトなど見張りに不要な外部読み込みは止めて、相手の負担を減らす
  await page.route(u => !/sodai-web\.jp|ajax\.googleapis\.com/.test(u.hostname), r => r.abort());
  await page.route(/\.(png|jpe?g|gif|svg|woff2?)(\?|$)/, r => r.abort());
  const rows = [];
  for (const t of TARGETS) {
    await page.goto(t.url, { waitUntil: 'load' });
    const wards = await page.$$eval('#chome option', os =>
      os.filter(o => o.value !== 'UN_SELECT').map(o => ({ code: o.value, name: o.textContent.trim() })));
    for (const w of wards) {
      let earliest = '';
      try {
        await page.selectOption('#chome', w.code);
        await page.evaluate(() => { const d = document.querySelector('#shortest_collection_date'); if (d) d.textContent = ''; });
        await page.click('#confirm_collection_date');
        await page.waitForFunction(() => document.querySelector('#shortest_collection_date')?.textContent.trim(), null, { timeout: 15000 });
        earliest = (await page.textContent('#shortest_collection_date')).trim();
      } catch (e) {
        earliest = 'ERROR:' + e.message.split('\n')[0].slice(0, 80);
      }
      rows.push([now, t.city, w.code, w.name, earliest].map(v => `"${String(v).replace(/"/g, '""')}"`).join(','));
      await page.waitForTimeout(WAIT_MS);
    }
  }
  await browser.close();
  fs.appendFileSync(out, rows.join('\n') + '\n');
  console.log(rows.join('\n'));
})();
