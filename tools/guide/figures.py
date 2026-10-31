# 記事の説明図（インラインSVG）。topics.py から読み込む。文字はすべて「例」か、どの市区でも同じ流れだけを書く。
# 色は guide/guide.css と同じ値（--accent #0A74B8 / --accent-soft #E4F1FA / --ink #14324A / --muted #587184 / --line #DCE6EE）
A, AS, INK, MU, LN, WS = "#0A74B8", "#E4F1FA", "#14324A", "#587184", "#DCE6EE", "#FFF3DC"
T = 'font-family="Noto Sans JP, Hiragino Sans, sans-serif"'


def _fig(svg, cap, label):
    return f'''    <figure class="fig">
      <svg viewBox="{svg[0]}" role="img" aria-label="{label}" {T}>{svg[1]}</svg>
      <figcaption>{cap}</figcaption>
    </figure>
'''


def _box(x, y, w, h, n, head, lines, fill=AS):
    t = "".join(f'<text x="{x + 20}" y="{y + 82 + i * 28}" font-size="19" fill="{MU}">{s}</text>' for i, s in enumerate(lines))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}"/>'
            f'<circle cx="{x + 34}" cy="{y + 36}" r="18" fill="{A}"/><text x="{x + 34}" y="{y + 43}" font-size="20" font-weight="700" fill="#fff" text-anchor="middle">{n}</text>'
            f'<text x="{x + 64}" y="{y + 44}" font-size="23" font-weight="700" fill="{INK}">{head}</text>{t}')


def flow():
    """申し込み → 払う（券／キャッシュレス）→ 書いて貼る → 朝出す。2列2段（スマホでも字が読める大きさ）"""
    arrow = lambda x1, y1, x2, y2: f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{A}" stroke-width="4" marker-end="url(#ar)"/>'
    s = (f'<defs><marker id="ar" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="{A}"/></marker></defs>'
         + _box(0, 0, 300, 190, 1, "申し込む", ["ネット（24時間の市区も）", "か電話で。品目と数を伝え、", "収集日と金額・受付番号を聞く"])
         + arrow(304, 95, 336, 95)
         + _box(340, 0, 300, 190, 2, "払う", ["コンビニなどで処理券を買う", "ネット申込ならカード・PayPay", "で払えて券がいらない市区も"])
         + f'<path d="M490 194V214H150V232" fill="none" stroke="{A}" stroke-width="4" marker-end="url(#ar)"/>'
         + _box(0, 240, 300, 190, 3, "書いて貼る", ["券に受付番号や名前を書き、", "1品ずつ見やすい所に貼る", "（券なしの人は番号を書いた紙）"])
         + arrow(304, 335, 336, 335)
         + _box(340, 240, 300, 190, 4, "朝、出す", ["収集日の朝（8時までなど", "市区の決まり）に、申し込みで", "決めた場所へ。立ち会い不要も"]))
    return _fig(("0 0 640 430", s), "粗大ごみの出し方の流れ（どの市区でもほぼ同じ。締め切り・時間・払い方は市区の記事で確かめてください）",
                "粗大ごみの出し方の4ステップ：1 申し込む、2 処理券を買うかネットで払う、3 券に書いて貼る、4 収集日の朝に出す")


def ticket():
    """処理券の記入見本（例）。"""
    row = lambda y, k, v: (f'<text x="196" y="{y}" font-size="20" fill="{MU}">{k}</text>'
                           f'<rect x="300" y="{y - 26}" width="240" height="38" rx="6" fill="#fff" stroke="{LN}" stroke-width="2"/>'
                           f'<text x="314" y="{y}" font-size="21" fill="{INK}" font-family="Zen Maru Gothic, sans-serif">{v}</text>')
    s = (f'<rect x="20" y="10" width="600" height="250" rx="18" fill="{WS}" stroke="#E2C27A" stroke-width="2" stroke-dasharray="8 6"/>'
         f'<rect x="44" y="34" width="130" height="200" rx="12" fill="{A}"/>'
         f'<text x="109" y="100" font-size="22" font-weight="700" fill="#fff" text-anchor="middle">粗大ごみ</text>'
         f'<text x="109" y="130" font-size="22" font-weight="700" fill="#fff" text-anchor="middle">処理券</text>'
         f'<text x="109" y="182" font-size="34" font-weight="700" fill="#fff" text-anchor="middle">例</text>'
         f'<text x="196" y="58" font-size="19" font-weight="700" fill="{INK}">ここに書く（書く項目は市区で違う）</text>'
         + row(112, "受付番号", "123456") + row(166, "収集日", "11月14日") + row(220, "氏名", "ひなた"))
    return _fig(("0 0 640 270", s), "処理券の記入見本（例）。受付番号だけ・名前だけ・収集日も、など、書く項目は市区で違います",
                "処理券の記入見本の例：受付番号123456、収集日11月14日、氏名ひなた、を券の記入欄に書く")


def measure():
    """「一番長い辺」と「3辺の合計」の2つの測り方（例は背の高い棚）。"""
    box = (f'<path d="M100 70L190 70L235 40L145 40Z" fill="{AS}" stroke="{A}" stroke-width="3"/>'
           f'<path d="M100 70L100 240L190 240L190 70Z" fill="#fff" stroke="{A}" stroke-width="3"/>'
           f'<path d="M190 70L235 40L235 210L190 240Z" fill="{AS}" stroke="{A}" stroke-width="3"/>'
           f'<path d="M108 125H182M108 182H182" stroke="{A}" stroke-width="2"/>')
    R = "#C2410C"
    s = (f'<g>{box}'
         + f'<path d="M78 70V240" stroke="{R}" stroke-width="5"/><text x="68" y="164" font-size="24" font-weight="700" fill="{R}" text-anchor="end">高さ</text>'
         + f'<text x="160" y="284" font-size="25" font-weight="700" fill="{INK}" text-anchor="middle" dy="8">一番長い辺で測る</text>'
         + f'<text x="160" y="312" font-size="22" fill="{MU}" text-anchor="middle" dy="8">この棚なら高さ</text></g>'
         + f'<g transform="translate(340 0)">{box}'
         + f'<path d="M78 70V240" stroke="{R}" stroke-width="5"/><text x="68" y="164" font-size="24" font-weight="700" fill="{R}" text-anchor="end">高さ</text>'
         + f'<path d="M100 256H190" stroke="{R}" stroke-width="5"/><text x="80" y="264" font-size="24" font-weight="700" fill="{R}" text-anchor="end">横</text>'
         + f'<path d="M200 250L245 220" stroke="{R}" stroke-width="5"/><text x="252" y="246" font-size="24" font-weight="700" fill="{R}">奥行</text>'
         + f'<text x="160" y="284" font-size="25" font-weight="700" fill="{INK}" text-anchor="middle" dy="8">3辺の合計で測る</text>'
         + f'<text x="160" y="312" font-size="22" fill="{MU}" text-anchor="middle" dy="8">横＋奥行＋高さ</text></g>')
    return _fig(("0 0 680 330", s), "大きさの測り方は2通り。どちらで測るか、何cmからかは市区で違います（下の表で確かめてください）",
                "測り方の図：左は一番長い辺（背の高い棚なら高さ）で測る方法、右は横・奥行・高さの3辺を足す方法")


def spring():
    """ウレタンだけのマットレスと、スプリング入りのマットレスの断面を並べる。"""
    U, UL = "#F6E7B8", "#C9A24A"
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="{UL}" opacity=".45"/>' for x in range(60, 290, 22) for y in (92, 118, 144))
    coils = "".join(f'<path d="M{x} 152 q12 -7 0 -14 q-12 -7 0 -14 q12 -7 0 -14 q-12 -7 0 -14" fill="none" stroke="{A}" stroke-width="3"/>' for x in range(372, 600, 26))
    s = (f'<text x="165" y="34" font-size="22" font-weight="700" fill="{INK}" text-anchor="middle">ウレタン（スプリングなし）</text>'
         f'<rect x="40" y="70" width="250" height="100" rx="12" fill="{U}" stroke="{UL}" stroke-width="2"/>{dots}'
         f'<text x="165" y="210" font-size="22" fill="{MU}" text-anchor="middle">中までスポンジ。軽い</text>'
         f'<text x="165" y="240" font-size="22" fill="{MU}" text-anchor="middle">押すと全体が沈む</text>'
         f'<text x="485" y="34" font-size="22" font-weight="700" fill="{INK}" text-anchor="middle">スプリング入り</text>'
         f'<rect x="360" y="70" width="250" height="100" rx="12" fill="#fff" stroke="{UL}" stroke-width="2"/>'
         f'<rect x="360" y="70" width="250" height="18" rx="9" fill="{U}"/><rect x="360" y="152" width="250" height="18" rx="9" fill="{U}"/>{coils}'
         f'<text x="485" y="210" font-size="22" fill="{MU}" text-anchor="middle">中に金属のバネ。重い</text>'
         f'<text x="485" y="240" font-size="22" fill="{MU}" text-anchor="middle">料金が高くなる市区も</text>')
    return _fig(("0 0 650 256", s), "マットレスの中の違い（断面のイメージ）。品質表示のタグに「スプリング」「コイル」と書いてあればスプリング入りです",
                "マットレスの断面の図：ウレタンだけのマットレスは中までスポンジ、スプリング入りは中に金属のバネが並んでいる")
