# エリア担当Agent（hinata.shiokonbu.com の地域記事）

地域記事（`/guide/<key>/`）を、地域ごとの担当がトラフィックの大きい順に育てるための手順です。
2026-10-31 Nori さんの依頼「各エリア担当のAgentを作って。トークンが無駄に使われないよう、Trafficが最大になるようにAgentの数とカバーエリアを配置」で作りました。
文言・表示のルールは `AGENTS.md`、事実の確かめ方は `tools/article_review/AGENT.md` が正本です。ここに書くのは「どの担当が・いつ・どこまでやるか」だけです。

## 割り振りの決め方

- **点数＝月の検索の見込み**。`max(キーワードプランナーの「市区名＋粗大ごみ」系の検索数の合計, Search Console の表示回数)`。
  - 検索数は `kw_area.json`（`build_kw.py` がキーワードプランナーのCSVから作る。2026-10-31取得）。
  - Search Console は `docs/area-agents/gsc.csv`（列 `page,clicks,impressions,position`、直近28日）があれば使う。2026-10-31 時点では SEOツールが hinata に未対応で、データもまだ少ないので使っていない。
  - キーワードプランナーで取っていない市（人口10〜20万人の55市）は、同じくらいの人口の市の実数（月480〜1,900）から **月500と仮置き**。
- **担当の数＝7**。1担当の見込みが月85,000〜117,000（全体の12〜16%）にそろうように、近い地域（ルール・家電リサイクル窓口・競合が共通）をまとめた。23区は1担当では回りきらないので3つに分けた。地方は1市ずつの見込みが小さいので1担当にまとめた。
- **重さ（A/B/C）でトークンを配る**。見込み月8,000以上＝A（14日ごとに深く）、2,000以上＝B（30日ごと）、それ未満＝C（90日ごとに機械チェックだけ）。Aの30地域とBの28地域で見込みの約9割。
- **回す順**：毎回 `allocate.py --next` が、直近60日で「割合に比べて動いていない担当」を選び、その担当の中で見直しの時期が来た地域を見込みの多い順に、1回の予算（A=1・B=0.5・C=0.1、合計3まで）だけ出す。
- 割り振りの表：`docs/area-agents/assignments.md`（自動生成）。設定：`groups.json`。

作り直すとき（キーワードプランナーを取り直した・GSCの数字を入れた・新しい地域記事ができた）：

```
python3 tools/area_agents/build_kw.py . ~/Downloads/hinata-kw-volumes.csv ~/Downloads/hinata-kw-ideas.csv   # 検索数を取り直したときだけ
python3 tools/area_agents/allocate.py .      # 表と .claude/agents/area-*.md を作り直す
```

新しい地域記事は `allocate.py` が自動で担当に入れる（公式URLの都道府県 → 地方の順で判定）。

## 受け持ちの線引き（重ならないように）

| 作業 | だれ |
|---|---|
| 地域記事の中身（`tools/guide/city/<key>.html`・`tools/guide/meta/<key>.json`・`booking.json` のその地域の行） | **エリア担当**（このファイル） |
| 新しい市の記事を作る | 地域記事を広げる作業（エリア担当は作らない。できたら自動で担当に入る） |
| トップ・診断・`/guide/` の共通ページ・品目ページ・持ち込み/処理券まとめ・全地域共通の型（`gencity.py` の共通欄や title の型） | SEO の定期作業（`docs/seo-playbook.md`） |
| 公式との照合の手順・機械チェック | `tools/article_review/`（エリア担当はこれを道具として使う） |
| まとめての記事チェック（記事チェック◯回目） | 続けるときは `docs/area-agents/ledger.json` の `fact` を書く。エリア担当は `fact` が30日以内の地域の全面照合を飛ばす |

## 1回の流れ

1. **重ならないか確かめる**：`git pull` で最新の main。開いている PR を見て、今回の地域の `city/<key>.html`・`meta/<key>.json` を触っている PR があればその地域は飛ばす。エリア担当の PR がまだ2本以上開いていたら、何もせず終わる。
2. **担当と地域を決める**：`python3 tools/area_agents/allocate.py . --next`（担当を指定されたら `--agent <id>`）。出てきた地域だけを見る。ほかの記事は読まない。
3. **機械の下調べ（1回だけ）**：`python3 tools/article_review/review.py tools/article_review/sites/hinata.json --out /tmp/area-review` を走らせ、今回の地域の指摘だけ拾う（`docs/article-review/` には書かない）。
4. **地域ごとに、重さに合わせて**：

   | | A（深く） | B | C（軽く） |
   |---|---|---|---|
   | 公式との照合 | `fact` が30日より前なら全部の数字・電話・URL。30日以内なら直す所だけ | Aと同じ | 機械チェックの「重い」だけ |
   | 検索の取りこぼし | `kw_area.json` の語（持ち込み・料金・予約・受付センター）で、月200以上あるのに見出し・本文で答えていない語を探す。GSCがあれば4〜20位の語 | 本体の語だけ | しない |
   | 上位ページとの比べ | 「〇〇 粗大ごみ」と、一番大きい副語（例「〇〇 粗大ごみ 持ち込み」）で上位3件を読む（`tools/article_review/AGENT.md` の表） | 本体の語で上位3件 | しない |
   | 直す案 | 3つまで | 1つまで | 事実の誤りだけ |

   - 案は「その地域にしかない、公式で確かめた情報」で答えるものだけ。文字数を増やすための案、どの地域にも書ける一般論は出さない。
   - title は `gencity.py` の `_title` で全地域共通の型。その地域だけ変えられるのは、事実として型が違う（大型ごみと呼ぶ・持ち込みが無い・無料）ときに型の一覧（`OOGATA` など）へキーを足すことだけ。型そのものを変えたいときは SEO の定期作業へ（`docs/seo-log.md` に「提案」と書いておく）。
5. **批判役**（AGENTS.md の決まり）：A・B の案は `article-critic` に案と読むべきファイルだけ渡し、残った案だけ直す。直した差分ももう一度見せ、`must_fix` を直す。C の事実の修正だけなら不要。
6. **作り直しとチェック**：`tools/guide/README.md` の順にスクリプトを実行（gencity → hub → areas → reviews_areas → topics）。`python3 tools/seo_check.py .` を NG 0 に。`data/areas.js` が変わったら `node tools/form_check.js .` も NG 0。
7. **記録**：`docs/area-agents/ledger.json` の `areas.<key>` に `checked`（今日）・照合したら `fact`・検索向けに直したら `seo`・`by`（担当id）・`note`（1行）。`runs` に `{date, agent, areas, pr}` を足す。`docs/seo-log.md` の先頭に1〜2行。
8. **PR**：ブランチを切って PR。説明に「担当・見た地域・直したこと（公式URLと確認日）・棄却した案と理由」。SEO check が緑ならマージしてよい（AGENTS.md）。

## トークンを無駄にしない決まり

- 見るのは `--next` が出した地域だけ。174記事を全部読まない。
- review.py は1回だけ。WebFetch は照合する公式ページと上位3件まで。
- C の地域では検索・上位ページの読み比べをしない。
- 前回 `fact` から30日以内の地域は、全部を照合し直さない。
- 直すことが見つからなくても、台帳（`checked`）だけの PR は出してマージする（出さないと次の回が同じ地域をもう一度見てしまう）。

## 定期実行

Claude の定期実行「hinata エリア担当の巡回」（毎日1回）が、上の流れを1担当ぶん行う。1日1担当×30日で、Aの地域が約14日ごと・Bが約30日ごとに回る量にしてある。担当を増やすより、`groups.json` の `tiers`・`revisit_days`・`budget_per_run` で配分を変える。
