# 地域記事の生成

`/guide/<key>/index.html` の地域記事は、ここにある元データから作ります。

- `city/<key>.html`：記事の本文（区市ごとの申し込み・料金・持ち込み・家電など）
- `meta/<key>.json`：title・description・地方・「引っ越してきた人へ」の文（最初の13地域は `gencity.py` の中）
- `gencity.py`：本文に、ヘッダー・共通の欄（引っ越してきた人へ／間に合わないとき／買取店）・近くの地域・フッターを付けて書き出す
- `hub.py`：`/guide/` の地域一覧・ItemList・`sitemap.xml` を作り直す

```
python3 tools/guide/gencity.py .
python3 tools/guide/hub.py .
python3 tools/guide/areas.py .   # 診断ページ用の data/areas.js
python3 tools/seo_check.py .
```

数字・電話番号・URL は区市の公式ページで確かめたものだけを書き、確認日を残します。
