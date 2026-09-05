#!/usr/bin/env python3
"""Write HSK lesson HTML shells (content comes from hsk-lesson-N-data.js)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def page(
    *,
    lesson: int,
    title: str,
    badge: str,
    words: int,
    hanzi: int,
    prev: tuple[int, str] | None,
    nxt: tuple[int, str] | None,
) -> str:
    prev_html = f'<a href="../lesson-{prev[0]}/">← {prev[0]} · {prev[1]}</a>' if prev else '<a href="../">← HSK Corner</a>'
    next_html = f'<a href="../lesson-{nxt[0]}/">{nxt[0]} · {nxt[1]} →</a>' if nxt else '<a href="../../../#blogs">Blogs →</a>'
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HSK {lesson} · {title} — HSK Corner — Hieu Nguyen</title>
  <meta name="description" content="HSK Lesson {lesson} — flashcards, vlog script (~{hanzi} 字), English + Pinyin toggle, and Scroll read speaking with cloze new words.">
  <link rel="icon" href="../../../favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Noto+Sans+SC:wght@400;500;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../../css/docs.css?v=hsk2">
</head>
<body class="docs hsk-page">
  <div class="cursor" id="cursor"></div>
  <div class="cursor-ring" id="cursorRing"></div>
  <canvas id="matrix-canvas"></canvas>
  <div class="grid-bg"></div>
  <header class="docs-topbar">
    <button class="docs-menu-btn" id="docsMenuBtn" type="button">menu</button>
    <a class="docs-brand" href="../../../"><span>✦</span> The Quiet Corner <span>✦</span></a>
    <nav class="docs-series">
      <a href="../../web-security/">DevSecOps</a>
      <a href="../../kubestronaut/">Kubestronaut</a>
      <a href="../../career-roadmap/">Career</a>
      <a href="../../english/">English</a>
      <a class="active" href="../">HSK</a>
      <a href="../../tech-hub/">Tech Hub</a>
    </nav>
    <span class="docs-topbar-spacer"></span>
    <a class="docs-top-link" href="../../../#blogs">blogs</a>
  </header>
  <div class="docs-shell">
    <aside class="docs-sidebar" id="docsSidebar" data-nav="hsk" data-docs-root="../" data-active="lesson-{lesson}">
      <div class="docs-nav-label">HSK Corner</div>
      <ul class="docs-nav" id="docsNav"></ul>
    </aside>
    <article class="docs-main">
      <div class="docs-breadcrumb">
        <a href="../../../">Home</a>
        <span>›</span>
        <a href="../../../#blogs">Blogs</a>
        <span>›</span>
        <a href="../">HSK Corner</a>
        <span>›</span>
        <span>Lesson {lesson}</span>
      </div>

      <div class="vocab-topic-hero">
        <div class="vocab-topic-card__img" style="display:grid;place-items:center;width:112px;height:112px;border-radius:18px;border:1px solid rgba(34,211,238,.35);font-family:'Noto Sans SC',sans-serif;font-size:1.8rem;color:#22d3ee;">{badge}</div>
        <div>
          <h1>Lesson {lesson} · {title}</h1>
          <p class="lede">
            Ôn {words} từ mới bằng <strong>flashcards</strong>, rồi đọc vlog mức
            <strong>HSK 1 → bài {lesson}</strong>. Bật English + Pinyin trên script.
            Scroll read ẩn từ mới — bạn điền lại khi luyện nói.
          </p>
          <div class="docs-meta">
            <span><strong>New words:</strong> {words}</span>
            <span><strong>Script:</strong> ~{hanzi} 字</span>
            <span><strong>Level:</strong> HSK 1 → {lesson}</span>
          </div>
        </div>
      </div>

      <nav class="hsk-jump" aria-label="On this page">
        <a href="#exFlash">Flashcards</a>
        <a href="#hskScript">Vlog script</a>
        <a href="#hskScroll">Scroll read</a>
        <a href="#hskVocab">Word list</a>
      </nav>

      <section class="ex-flash" id="exFlash" aria-label="HSK flashcards">
        <div class="ex-flash-head">
          <div>
            <h2>Flashcards · {words} từ mới</h2>
            <p class="ex-flash-hint">
              Mặt trước: 汉字 + pinyin. Lật thẻ: nghĩa VI / EN + ví dụ từ bài.
              Phân loại <strong>Đã biết</strong> · <strong>Phải học</strong> · <strong>Bỏ qua</strong>.
            </p>
          </div>
          <div class="ex-flash-controls">
            <div class="ex-flash-stats" aria-live="polite">
              <span>Card <strong id="flashIndex">0</strong>/<strong id="flashTotal">0</strong></span>
              <span>Phải học <strong id="flashGold">0</strong></span>
              <span>Đã biết <strong id="flashKnown">0</strong></span>
              <span>Bỏ qua <strong id="flashTrash">0</strong></span>
            </div>
            <button type="button" class="ex-btn" id="btnFlashDownload">Tải .txt</button>
            <button type="button" class="ex-btn" id="btnFlashShuffle">Shuffle</button>
            <button type="button" class="ex-btn primary" id="btnFlashRestart">Restart</button>
          </div>
        </div>
        <div class="ex-flash-stage" id="flashStage"></div>
        <p class="ex-flash-msg" id="flashMsg" hidden></p>
      </section>

      <section class="hsk-script" id="hskScript" aria-label="Vlog script">
        <div class="ex-flash-head">
          <div>
            <h2>Vlog script · {title}</h2>
            <p class="ex-flash-hint">
              Đoạn văn kiểu vlog, mức HSK 1 đến bài {lesson}. Từ mới được
              <mark class="hsk-new">highlight</mark>. Bật Pinyin và English khi cần.
            </p>
          </div>
          <div class="hsk-script-actions">
            <button type="button" class="ex-btn primary" id="btnCopyZh">Copy 汉字</button>
          </div>
        </div>
        <div class="hsk-script-toolbar">
          <label class="ex-toggle"><input type="checkbox" id="togPinyin"> Hiện Pinyin</label>
          <label class="ex-toggle"><input type="checkbox" id="togEnglish"> Hiện English</label>
        </div>
        <div id="hskScriptBody"></div>
      </section>

      <section class="ex-scroll" id="hskScroll" aria-label="Scroll read speaking">
        <div class="ex-scroll-head">
          <div>
            <h2>Scroll read · speaking</h2>
            <p class="ex-scroll-hint">
              Teleprompter luyện đọc. Từ mới bị ẩn — hint VI / Pinyin / English.
              Bật <strong>Hiện chữ Hán</strong> để thấy đáp án. Bật <strong>Hiện pinyin đoạn</strong>
              để cả dòng có phiên âm. Click ô trống để peek.
            </p>
          </div>
          <div class="ex-scroll-nr-actions">
            <a class="ex-btn ex-scroll-nr-link" href="https://www.naturalreaders.com/online/" target="_blank" rel="noopener noreferrer">NaturalReaders ↗</a>
            <button type="button" class="ex-btn primary" id="hskScrollCopy">Copy for NaturalReader</button>
          </div>
        </div>
        <div class="ex-scroll-toolbar">
          <button type="button" class="ex-btn primary" id="hskScrollPlay">▶ Play</button>
          <button type="button" class="ex-btn" id="hskScrollPause">Pause</button>
          <button type="button" class="ex-btn" id="hskScrollRestart">⟲ Restart</button>
          <label class="ex-voice">Speed
            <input id="hskScrollSpeed" type="range" min="12" max="90" step="1" value="32">
            <span id="hskScrollSpeedVal">32</span> px/s
          </label>
          <label class="ex-voice">Hint
            <select id="hskScrollHint" aria-label="Hint mode">
              <option value="vi" selected>Nghĩa VI</option>
              <option value="py">Pinyin</option>
              <option value="en">English</option>
              <option value="both">VI + Pinyin</option>
            </select>
          </label>
          <label class="ex-toggle"><input type="checkbox" id="hskScrollReveal"> Hiện chữ Hán</label>
          <label class="ex-toggle"><input type="checkbox" id="hskScrollShowPy"> Hiện pinyin đoạn</label>
        </div>
        <div class="ex-scroll-stage">
          <div class="ex-scroll-focus" aria-hidden="true"></div>
          <div class="ex-scroll-viewport" id="hskScrollViewport">
            <div class="ex-scroll-track" id="hskScrollTrack"></div>
          </div>
        </div>
      </section>

      <section class="ex-vocab" id="hskVocab">
        <h2>Word checklist · {words}</h2>
        <ul class="ex-vocab-list" id="hskVocabList"></ul>
      </section>

      <div class="docs-pager">
        {prev_html}
        {next_html}
      </div>
    </article>
  </div>
  <script src="../../../js/docs.js"></script>
  <script src="../../../js/hsk-lesson-{lesson}-data.js"></script>
  <script src="../../../js/hsk.js?v=hsk2"></script>
</body>
</html>
"""


def write_lesson(**kwargs) -> None:
    lesson = kwargs["lesson"]
    dest = ROOT / "public" / "blog" / "hsk" / f"lesson-{lesson}" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page(**kwargs), encoding="utf-8")
    print(f"wrote {dest}")


if __name__ == "__main__":
    write_lesson(lesson=14, title="开学这一天", badge="开学", words=31, hanzi=1111, prev=None, nxt=(15, "朋友的婚礼"))
    write_lesson(lesson=15, title="朋友的婚礼", badge="婚礼", words=25, hanzi=975, prev=(14, "开学这一天"), nxt=(16, "我的一天"))
    write_lesson(lesson=16, title="我的一天", badge="一天", words=43, hanzi=1032, prev=(15, "朋友的婚礼"), nxt=None)
