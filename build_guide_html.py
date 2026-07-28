#!/usr/bin/env python3
"""Markdown マスターガイド -> 単一ファイル HTML への変換."""
import re
import unicodedata
from pathlib import Path

import markdown

SRC = Path("/home/user/-/NYANKO_DAISENSOU_MASTER_GUIDE.md")
DST = Path("/home/user/-/nyanko-master-guide.html")


def slugify(value, separator="-"):
    """GitHub 風のアンカー生成（Unicode を保持）."""
    value = unicodedata.normalize("NFKC", value).strip().lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    return re.sub(r"[\s]+", separator, value)


text = SRC.read_text(encoding="utf-8")

# 冒頭の「## 目次」ブロックは、サイドバー目次に置き換えるので削除する
text = re.sub(r"\n## 目次\n.*?\n---\n", "\n", text, count=1, flags=re.DOTALL)

# H1 はヒーロー見出しと重複するため本文からは外す
text = re.sub(r"^# .*?\n", "", text, count=1)

md = markdown.Markdown(
    extensions=["tables", "toc", "attr_list", "sane_lists", "fenced_code"],
    extension_configs={"toc": {"slugify": slugify, "toc_depth": "2-3"}},
)
body = md.convert(text)

# テーブルを横スクロール可能なラッパで囲む
body = body.replace("<table>", '<div class="table-wrap"><table>').replace(
    "</table>", "</table></div>"
)

nav = md.toc

HTML = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>にゃんこ大戦争 完全マスターガイド</title>
<style>
:root {{
  --bg: #fbfaf7;
  --surface: #ffffff;
  --surface-2: #f4f1ea;
  --text: #1f2328;
  --muted: #5b6570;
  --line: #e2ded4;
  --accent: #d9762b;
  --accent-soft: #fdf1e4;
  --link: #b1571a;
  --shadow: 0 1px 3px rgba(31,35,40,.08), 0 8px 24px rgba(31,35,40,.05);
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #14161a;
    --surface: #1b1e24;
    --surface-2: #22262e;
    --text: #e6e8eb;
    --muted: #9aa3ae;
    --line: #2e333c;
    --accent: #f0913f;
    --accent-soft: #2a211a;
    --link: #f3a85f;
    --shadow: 0 1px 3px rgba(0,0,0,.4), 0 8px 24px rgba(0,0,0,.3);
  }}
}}
:root[data-theme="light"] {{
  --bg: #fbfaf7; --surface: #ffffff; --surface-2: #f4f1ea;
  --text: #1f2328; --muted: #5b6570; --line: #e2ded4;
  --accent: #d9762b; --accent-soft: #fdf1e4; --link: #b1571a;
  --shadow: 0 1px 3px rgba(31,35,40,.08), 0 8px 24px rgba(31,35,40,.05);
}}
:root[data-theme="dark"] {{
  --bg: #14161a; --surface: #1b1e24; --surface-2: #22262e;
  --text: #e6e8eb; --muted: #9aa3ae; --line: #2e333c;
  --accent: #f0913f; --accent-soft: #2a211a; --link: #f3a85f;
  --shadow: 0 1px 3px rgba(0,0,0,.4), 0 8px 24px rgba(0,0,0,.3);
}}

* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Hiragino Kaku Gothic ProN",
               "Noto Sans JP", "Yu Gothic", Meiryo, sans-serif;
  font-size: 16px;
  line-height: 1.85;
  -webkit-text-size-adjust: 100%;
}}

/* ---------- レイアウト ---------- */
.shell {{
  display: grid;
  grid-template-columns: 288px minmax(0, 1fr);
  gap: 40px;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px 96px;
}}
@media (max-width: 900px) {{
  .shell {{ grid-template-columns: minmax(0, 1fr); gap: 0; padding: 0 16px 64px; }}
}}

/* ---------- ヘッダー ---------- */
header.hero {{
  background: linear-gradient(135deg, var(--accent) 0%, #b8541c 100%);
  color: #fff;
  padding: 56px 24px 48px;
  margin-bottom: 40px;
  text-align: center;
}}
header.hero h1 {{
  margin: 0 0 12px;
  font-size: clamp(1.6rem, 4.5vw, 2.6rem);
  line-height: 1.3;
  letter-spacing: .01em;
}}
header.hero p {{ margin: 0; opacity: .92; font-size: .95rem; }}
header.hero .meta {{ margin-top: 18px; font-size: .82rem; opacity: .85; }}

/* ---------- サイドバー目次 ---------- */
nav.toc {{
  position: sticky;
  top: 0;
  align-self: start;
  max-height: 100vh;
  overflow-y: auto;
  padding: 28px 0 40px;
  font-size: .875rem;
}}
nav.toc > .toctitle,
nav.toc h2 {{
  font-size: .72rem;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 0 0 12px;
  font-weight: 700;
}}
nav.toc ul {{ list-style: none; margin: 0; padding: 0; }}
nav.toc li {{ margin: 0; }}
nav.toc a {{
  display: block;
  padding: 5px 10px;
  color: var(--muted);
  text-decoration: none;
  border-left: 2px solid transparent;
  border-radius: 0 5px 5px 0;
  line-height: 1.5;
}}
nav.toc a:hover {{ color: var(--accent); background: var(--accent-soft); }}
nav.toc a.active {{ color: var(--accent); border-left-color: var(--accent); font-weight: 700; }}
nav.toc ul ul a {{ padding-left: 22px; font-size: .82rem; opacity: .85; }}
@media (max-width: 900px) {{
  nav.toc {{
    position: static; max-height: none; padding: 20px;
    background: var(--surface); border: 1px solid var(--line);
    border-radius: 12px; margin-bottom: 28px;
  }}
  nav.toc ul ul {{ display: none; }}
}}

/* ---------- 本文 ---------- */
main {{ min-width: 0; padding-top: 12px; }}
main h2 {{
  font-size: 1.45rem;
  margin: 64px 0 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--line);
  scroll-margin-top: 16px;
  line-height: 1.4;
}}
main h2:first-of-type {{ margin-top: 8px; }}
main h3 {{
  font-size: 1.1rem;
  margin: 40px 0 14px;
  color: var(--accent);
  scroll-margin-top: 16px;
  line-height: 1.5;
}}
main h4 {{ font-size: 1rem; margin: 28px 0 10px; }}
main p {{ margin: 0 0 16px; }}
main ul, main ol {{ margin: 0 0 18px; padding-left: 1.5em; }}
main li {{ margin-bottom: 7px; }}
main li > ul, main li > ol {{ margin: 7px 0 0; }}
a {{ color: var(--link); }}
a:hover {{ text-decoration: none; }}
strong {{ font-weight: 700; }}
hr {{ border: 0; border-top: 1px solid var(--line); margin: 48px 0; }}

blockquote {{
  margin: 22px 0;
  padding: 16px 20px;
  background: var(--accent-soft);
  border-left: 4px solid var(--accent);
  border-radius: 0 8px 8px 0;
}}
blockquote p {{ margin: 0 0 10px; }}
blockquote p:last-child {{ margin-bottom: 0; }}

code {{
  background: var(--surface-2);
  padding: .15em .4em;
  border-radius: 5px;
  font-size: .88em;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}}
pre {{
  background: var(--surface-2);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 18px;
  overflow-x: auto;
  line-height: 1.6;
}}
pre code {{ background: none; padding: 0; font-size: .85rem; }}

/* ---------- テーブル ---------- */
.table-wrap {{
  overflow-x: auto;
  margin: 22px 0;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: var(--surface);
  box-shadow: var(--shadow);
  -webkit-overflow-scrolling: touch;
}}
table {{ border-collapse: collapse; width: 100%; font-size: .9rem; }}
/* 狭い画面では潰さず、ラッパ内で横スクロールさせる */
.table-wrap table {{ min-width: 560px; }}
th, td {{
  padding: 11px 14px;
  text-align: left;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
  line-height: 1.65;
}}
th {{
  background: var(--surface-2);
  font-weight: 700;
  white-space: nowrap;
  position: sticky;
  top: 0;
}}
tbody tr:last-child td {{ border-bottom: none; }}
tbody tr:hover td {{ background: var(--accent-soft); }}

/* ---------- テーマ切替ボタン ---------- */
#theme-toggle {{
  position: fixed;
  right: 18px;
  bottom: 18px;
  z-index: 50;
  width: 46px;
  height: 46px;
  border-radius: 50%;
  border: 1px solid var(--line);
  background: var(--surface);
  color: var(--text);
  font-size: 1.15rem;
  cursor: pointer;
  box-shadow: var(--shadow);
  line-height: 1;
}}
#theme-toggle:hover {{ border-color: var(--accent); }}

/* ---------- 印刷 ---------- */
@media print {{
  nav.toc, #theme-toggle {{ display: none; }}
  .shell {{ display: block; max-width: none; padding: 0; }}
  header.hero {{ background: none; color: #000; padding: 0 0 24px; }}
  body {{ font-size: 11pt; }}
  main h2 {{ page-break-after: avoid; margin-top: 32px; }}
  .table-wrap {{ box-shadow: none; page-break-inside: avoid; }}
}}
</style>
</head>
<body>
<header class="hero">
  <h1>にゃんこ大戦争 完全マスターガイド</h1>
  <p>基礎システムから高難度攻略まで、一冊で完結する攻略リファレンス</p>
  <div class="meta">Ver.15.5.1 準拠 ／ 2026-07-28 作成 ／ 全28章</div>
</header>

<div class="shell">
  <nav class="toc" aria-label="目次">
    <h2>目次</h2>
    {nav}
  </nav>
  <main>
{body}
  </main>
</div>

<button id="theme-toggle" type="button" aria-label="配色を切り替える">◐</button>

<script>
(function () {{
  // --- テーマ切替 ---
  var root = document.documentElement;
  var saved = null;
  try {{ saved = localStorage.getItem('nyanko-theme'); }} catch (e) {{}}
  if (saved) root.setAttribute('data-theme', saved);

  document.getElementById('theme-toggle').addEventListener('click', function () {{
    var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    var current = root.getAttribute('data-theme') || (prefersDark ? 'dark' : 'light');
    var next = current === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try {{ localStorage.setItem('nyanko-theme', next); }} catch (e) {{}}
  }});

  // --- 目次の現在地ハイライト ---
  var links = Array.prototype.slice.call(document.querySelectorAll('nav.toc a'));
  var byId = {{}};
  var targets = [];
  links.forEach(function (a) {{
    var id = decodeURIComponent(a.getAttribute('href') || '').slice(1);
    var el = id && document.getElementById(id);
    if (el) {{ byId[id] = a; targets.push(el); }}
  }});
  if (!targets.length || !('IntersectionObserver' in window)) return;

  var visible = new Set();
  var observer = new IntersectionObserver(function (entries) {{
    entries.forEach(function (entry) {{
      if (entry.isIntersecting) visible.add(entry.target.id);
      else visible.delete(entry.target.id);
    }});
    var first = targets.filter(function (t) {{ return visible.has(t.id); }})[0];
    if (!first) return;
    links.forEach(function (a) {{ a.classList.remove('active'); }});
    if (byId[first.id]) byId[first.id].classList.add('active');
  }}, {{ rootMargin: '0px 0px -75% 0px', threshold: 0 }});

  targets.forEach(function (t) {{ observer.observe(t); }});
}})();
</script>
</body>
</html>
"""

DST.write_text(HTML, encoding="utf-8")
print(f"wrote {DST} ({DST.stat().st_size:,} bytes)")
