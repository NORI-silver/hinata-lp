# 記事チェックエージェント（tools/article_review/）

記事を7つの観点（正確さ・リンク・SEO・ありきたり・困ったときの情報・画像・最新か）でチェックする仕組みです。どのサイトでも使えるように、サイトの違いは `sites/<site>.json` に分けています。

| ファイル | 中身 |
|---|---|
| `AGENT.md` | AIが読む手順の正本（7つの観点・事実の確かめ方・上位ページとの比べ方・批判役） |
| `review.py` | 機械でわかる問題を拾う下調べ（Python 3 の標準ライブラリだけ） |
| `sites/hinata.json` | hinata.shiokonbu.com（このリポジトリ）。一番くわしい例 |
| `sites/shiokonbu.json` | shiokonbu.com（WordPress。SHIOKONBU_SEO のツールで記事を取り出して使う） |
| `sites/pet.json` | pet.shiokonbu.com（sitemap から読む。pet-lp で使うときは local に） |
| `../../.claude/agents/article-reviewer.md` `article-critic.md` | Claude Code のサブエージェント（チェック役・批判役） |
| `../../.github/workflows/article-review.yml` | 週1回（月曜）外部リンクも含めて下調べを走らせ、結果を Actions の Summary に出す |

```
python3 tools/article_review/review.py tools/article_review/sites/hinata.json            # 下調べ → docs/article-review/
python3 tools/article_review/review.py tools/article_review/sites/hinata.json --external # 外部リンクも（ネットにつながる所で）
```

AIに頼むとき：「tools/article_review/AGENT.md の手順で、hinata の記事をチェックして直して」。
ほかのリポジトリで使うときは、このフォルダと `.claude/agents/article-*.md` を写し、`sites/` に設定を足します。
