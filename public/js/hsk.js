(() => {
  const data =
    window.HSK_LESSON ||
    window.HSK_LESSON_16 ||
    window.HSK_LESSON_15 ||
    window.HSK_LESSON_14;
  if (!data) return;
  const lessonNo = data.lesson || 14;
  const slug = `hsk-lesson-${lessonNo}`;

  const vocab = Array.isArray(data.vocab) ? data.vocab : [];
  const byId = new Map(vocab.map((w) => [w.id, w]));
  const body = document.body;
  body.classList.add("hsk-page");

  const escapeHtml = (s) =>
    String(s ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");

  const shuffle = (arr) => {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  };

  const pickZhVoice = () => {
    if (!window.speechSynthesis) return null;
    const voices = speechSynthesis.getVoices();
    const scored = voices
      .map((v, i) => {
        const label = `${v.name} ${v.lang}`;
        let score = 80;
        if (/zh-CN|cmn-Hans|Chinese \(China\)/i.test(label)) score = 0;
        else if (/zh-TW|cmn-Hant/i.test(label)) score = 10;
        else if (/zh|Chinese|Tingting|Meijia|Lisheng/i.test(label)) score = 20;
        else score = 1000;
        return { v, i, score };
      })
      .filter((x) => x.score < 1000)
      .sort((a, b) => a.score - b.score);
    return scored[0]?.v || null;
  };

  const speakZh = (text) => {
    if (!window.speechSynthesis || !text) return;
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    const voice = pickZhVoice();
    if (voice) u.voice = voice;
    u.lang = voice?.lang || "zh-CN";
    u.rate = 0.9;
    speechSynthesis.speak(u);
  };
  if (window.speechSynthesis) speechSynthesis.onvoiceschanged = () => {};

  /* ── Flashcards ───────────────────────────────────────────────────── */
  const initFlashcards = () => {
    const stage = document.getElementById("flashStage");
    if (!stage || !vocab.length) return;

    const elIndex = document.getElementById("flashIndex");
    const elTotal = document.getElementById("flashTotal");
    const elGold = document.getElementById("flashGold");
    const elKnown = document.getElementById("flashKnown");
    const elTrash = document.getElementById("flashTrash");
    const elMsg = document.getElementById("flashMsg");
    const btnShuffle = document.getElementById("btnFlashShuffle");
    const btnRestart = document.getElementById("btnFlashRestart");
    const btnDownload = document.getElementById("btnFlashDownload");

    let deck = [];
    let idx = 0;
    const classified = { known: [], gold: [], trash: [] };
    let flipped = false;

    const formatWordLine = (w) =>
      [w.hanzi, w.pinyin, w.vi, w.en].filter(Boolean).join(" | ");

    const showMsg = (text, ok) => {
      if (!elMsg) return;
      elMsg.hidden = !text;
      elMsg.textContent = text || "";
      elMsg.classList.toggle("ok", !!ok);
    };

    const renderStats = () => {
      if (elIndex) elIndex.textContent = String(deck.length ? idx + 1 : 0);
      if (elTotal) elTotal.textContent = String(deck.length);
      if (elGold) elGold.textContent = String(classified.gold.length);
      if (elKnown) elKnown.textContent = String(classified.known.length);
      if (elTrash) elTrash.textContent = String(classified.trash.length);
    };

    const current = () => deck[idx] || null;
    const peekWord = () => (idx + 1 < deck.length ? deck[idx + 1] : null);

    const downloadClassified = () => {
      const title = data.title || `HSK Lesson ${lessonNo}`;
      const pending = deck.slice(idx);
      const lines = [
        `# HSK Lesson ${lessonNo} · ${title}`,
        `# Exported: ${new Date().toISOString().slice(0, 10)}`,
        "",
        `## Phải học — ${classified.gold.length}`,
        ...classified.gold.map(formatWordLine),
        "",
        `## Đã biết — ${classified.known.length}`,
        ...classified.known.map(formatWordLine),
        "",
        `## Không thông dụng — ${classified.trash.length}`,
        ...classified.trash.map(formatWordLine),
      ];
      if (pending.length) {
        lines.push("", `## Chưa phân loại — ${pending.length}`, ...pending.map(formatWordLine));
      }
      const blob = new Blob([lines.join("\n")], { type: "text/plain;charset=utf-8" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `${slug}-pareto.txt`;
      a.click();
      URL.revokeObjectURL(a.href);
      showMsg(`Đã tải ${slug}-pareto.txt`, true);
    };

    const renderCard = () => {
      if (window.speechSynthesis) speechSynthesis.cancel();
      const w = current();
      flipped = false;
      showMsg("");
      renderStats();
      if (!w) {
        stage.innerHTML = `<div class="ex-flash-done">
          <p>Đã ôn xong ${vocab.length} từ bài 14.</p>
          <p class="ex-flash-done-meta">Phải học <strong>${classified.gold.length}</strong> · Đã biết ${classified.known.length} · Bỏ qua ${classified.trash.length}</p>
          <div class="ex-flash-done-actions">
            <button type="button" class="ex-btn primary" id="btnFlashDownloadDone">Tải .txt</button>
            <button type="button" class="ex-btn" id="btnFlashAgain">Luyện lại</button>
          </div>
        </div>`;
        document.getElementById("btnFlashAgain")?.addEventListener("click", () => restart(true));
        document.getElementById("btnFlashDownloadDone")?.addEventListener("click", downloadClassified);
        return;
      }

      const ex = (w.examples && w.examples[0]) || null;
      const next = peekWord();
      stage.innerHTML = `
        <div class="ex-flash-deck">
          <div class="ex-flash-card" id="flashCard" tabindex="0" role="button" aria-label="Flashcard ${escapeHtml(w.hanzi)}">
            <div class="ex-flash-face ex-flash-face--front">
              <button type="button" class="ex-flash-speak" id="flashSpeak" aria-label="Phát âm">
                <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>
              </button>
              <div class="ex-flash-front-body">
                <div class="ex-flash-term hsk-flash-hanzi">${escapeHtml(w.hanzi)}</div>
                <div class="ex-flash-ipa hsk-flash-py">${escapeHtml(w.pinyin || "")}</div>
                ${w.pos ? `<div class="ex-flash-pos">[${escapeHtml(w.pos)}]</div>` : ""}
              </div>
              <button type="button" class="ex-flash-flipbar" id="flashFlip">Xem nghĩa · ví dụ</button>
            </div>
            <div class="ex-flash-face ex-flash-face--back">
              <button type="button" class="ex-flash-backnav" id="flashUnflip" aria-label="Quay lại">←</button>
              <div class="ex-flash-back-body">
                <div class="ex-flash-meaning">
                  <span class="ex-flash-star" aria-hidden="true">★</span>
                  <strong>${escapeHtml(w.vi || w.hanzi)}</strong>
                </div>
                <p class="ex-flash-def-en">${escapeHtml(w.en || "")}</p>
                <p class="hsk-flash-py-back">${escapeHtml(w.pinyin || "")}</p>
                ${
                  ex
                    ? `<div class="ex-flash-example">
                        <div class="ex-flash-example-label">Ví dụ</div>
                        <p class="ex-flash-example-en hsk-flash-ex-zh">${escapeHtml(ex.zh)}
                          <button type="button" class="ex-flash-example-speak" id="flashSpeakEx" aria-label="Nghe ví dụ">▶</button>
                        </p>
                        <p class="hsk-flash-ex-py">${escapeHtml(ex.py || "")}</p>
                        <p class="ex-flash-example-vi">${escapeHtml(ex.vi || "")}</p>
                        <p class="hsk-flash-ex-en">${escapeHtml(ex.en || "")}</p>
                      </div>`
                    : ""
                }
              </div>
              <div class="ex-flash-grade ex-flash-grade--pareto">
                <button type="button" class="ex-flash-grade-btn ex-flash-grade-btn--known" id="flashKnownBtn">Đã biết</button>
                <button type="button" class="ex-flash-grade-btn ex-flash-grade-btn--gold" id="flashGoldBtn">★ Phải học</button>
                <button type="button" class="ex-flash-grade-btn ex-flash-grade-btn--trash" id="flashTrashBtn">Bỏ qua</button>
              </div>
            </div>
          </div>
          ${
            next
              ? `<div class="ex-flash-peek" aria-hidden="true">
                  <div class="ex-flash-peek-term hsk-flash-hanzi">${escapeHtml(next.hanzi)}</div>
                </div>`
              : ""
          }
        </div>
      `;

      const card = document.getElementById("flashCard");
      const setFlip = (on) => {
        if (flipped === on) return;
        flipped = on;
        card?.classList.toggle("is-flipped", on);
        if (on) speakZh(w.hanzi);
      };
      document.getElementById("flashSpeak")?.addEventListener("click", (e) => {
        e.stopPropagation();
        speakZh(w.hanzi);
      });
      document.getElementById("flashSpeakEx")?.addEventListener("click", (e) => {
        e.stopPropagation();
        speakZh(ex?.zh || "");
      });
      document.getElementById("flashFlip")?.addEventListener("click", (e) => {
        e.stopPropagation();
        setFlip(true);
      });
      document.getElementById("flashUnflip")?.addEventListener("click", (e) => {
        e.stopPropagation();
        setFlip(false);
      });
      card?.addEventListener("keydown", (e) => {
        if (e.key === " " || e.key === "Enter") {
          e.preventDefault();
          setFlip(!flipped);
        }
      });
      const advance = (bucket) => {
        const cur = current();
        if (!cur || !classified[bucket]) return;
        classified[bucket].push(cur);
        idx += 1;
        renderCard();
      };
      document.getElementById("flashKnownBtn")?.addEventListener("click", () => advance("known"));
      document.getElementById("flashGoldBtn")?.addEventListener("click", () => advance("gold"));
      document.getElementById("flashTrashBtn")?.addEventListener("click", () => advance("trash"));
    };

    const restart = (doShuffle) => {
      deck = doShuffle ? shuffle(vocab) : vocab.slice();
      idx = 0;
      classified.known = [];
      classified.gold = [];
      classified.trash = [];
      renderCard();
    };

    btnDownload?.addEventListener("click", downloadClassified);
    btnShuffle?.addEventListener("click", () => restart(true));
    btnRestart?.addEventListener("click", () => restart(true));
    restart(true);
  };

  /* ── Vlog script ──────────────────────────────────────────────────── */
  const renderScript = () => {
    const root = document.getElementById("hskScriptBody");
    if (!root) return;
    const paras = data.script || [];
    root.innerHTML = paras
      .map((p, i) => {
        const zh = (p.tokens || [])
          .map((tok) => {
            if (tok.new) {
              const meta = byId.get(tok.new) || {};
              return `<mark class="hsk-new" data-word="${escapeHtml(tok.new)}" title="${escapeHtml(
                [meta.pinyin, meta.en, meta.vi].filter(Boolean).join(" · ")
              )}">${escapeHtml(tok.t)}</mark>`;
            }
            return escapeHtml(tok.t);
          })
          .join("");
        return `<div class="hsk-para" data-idx="${i}">
          <p class="hsk-zh">${zh}</p>
          <p class="hsk-py">${escapeHtml(p.py || "")}</p>
          <p class="hsk-en">${escapeHtml(p.en || "")}</p>
        </div>`;
      })
      .join("");

    const togPy = document.getElementById("togPinyin");
    const togEn = document.getElementById("togEnglish");
    const apply = () => {
      body.classList.toggle("hsk-show-py", !!(togPy && togPy.checked));
      body.classList.toggle("hsk-show-en", !!(togEn && togEn.checked));
    };
    togPy?.addEventListener("change", apply);
    togEn?.addEventListener("change", apply);
    apply();

    document.getElementById("btnCopyZh")?.addEventListener("click", async (e) => {
      const btn = e.currentTarget;
      const text = paras.map((p) => p.zh).join("\n\n");
      try {
        await navigator.clipboard.writeText(text);
        const prev = btn.textContent;
        btn.textContent = "Copied";
        setTimeout(() => {
          btn.textContent = prev;
        }, 1400);
      } catch {
        /* ignore */
      }
    });
  };

  /* ── Scroll read · speaking ───────────────────────────────────────── */
  const initScrollRead = () => {
    const track = document.getElementById("hskScrollTrack");
    const viewport = document.getElementById("hskScrollViewport");
    if (!track || !viewport) return;

    const speedRange = document.getElementById("hskScrollSpeed");
    const speedVal = document.getElementById("hskScrollSpeedVal");
    const hintMode = document.getElementById("hskScrollHint");
    const revealTog = document.getElementById("hskScrollReveal");
    const showPyTog = document.getElementById("hskScrollShowPy");
    const btnPlay = document.getElementById("hskScrollPlay");
    const btnPause = document.getElementById("hskScrollPause");
    const btnRestart = document.getElementById("hskScrollRestart");
    const btnCopy = document.getElementById("hskScrollCopy");

    let playing = false;
    let offset = 0;
    let raf = 0;
    let lastTs = 0;
    let pxPerSec = speedRange ? Number(speedRange.value) : 32;

    const hintFor = (meta, mode) => {
      const vi = meta?.vi || "";
      const py = meta?.pinyin || "";
      const en = meta?.en || "";
      if (mode === "py") return py || "????";
      if (mode === "en") return en || "????";
      if (mode === "both") {
        if (vi && py) return `${vi} · ${py}`;
        return vi || py || "????";
      }
      return vi || py || "????";
    };

    const makeBlank = (tok, mode, reveal) => {
      const meta = byId.get(tok.new) || { hanzi: tok.t };
      const form = tok.t;
      const blank = document.createElement("span");
      blank.className = "scroll-blank";
      blank.dataset.answer = form;
      blank.title = "Click để xem đáp án";
      const paint = (shown) => {
        if (shown) {
          blank.classList.add("is-revealed");
          blank.innerHTML = `<span class="scroll-blank-answer">${escapeHtml(form)}</span>`;
        } else {
          blank.classList.remove("is-revealed");
          blank.innerHTML = `<span class="scroll-blank-gap">______</span><span class="scroll-blank-hint">${escapeHtml(
            hintFor(meta, mode)
          )}</span>`;
        }
      };
      paint(reveal);
      blank.addEventListener("click", (e) => {
        e.preventDefault();
        paint(!blank.classList.contains("is-revealed"));
      });
      return blank;
    };

    const buildTrack = () => {
      const mode = hintMode ? hintMode.value : "vi";
      const reveal = !!(revealTog && revealTog.checked);
      const showPy = !!(showPyTog && showPyTog.checked);
      const frag = document.createDocumentFragment();
      const top = document.createElement("div");
      top.className = "scroll-pad scroll-pad--top";
      frag.appendChild(top);

      (data.script || []).forEach((p) => {
        const line = document.createElement("p");
        line.className = "scroll-line hsk-scroll-zh";
        (p.tokens || []).forEach((tok) => {
          if (tok.new) line.appendChild(makeBlank(tok, mode, reveal));
          else line.appendChild(document.createTextNode(tok.t));
        });
        frag.appendChild(line);
        if (showPy && p.py) {
          const py = document.createElement("p");
          py.className = "scroll-line hsk-scroll-py";
          py.textContent = p.py;
          frag.appendChild(py);
        }
      });

      const bottom = document.createElement("div");
      bottom.className = "scroll-pad scroll-pad--bottom";
      frag.appendChild(bottom);
      track.innerHTML = "";
      track.appendChild(frag);
      const viewH = viewport.clientHeight || 420;
      const topPad = track.querySelector(".scroll-pad--top");
      const bottomPad = track.querySelector(".scroll-pad--bottom");
      if (topPad) topPad.style.height = `${Math.round(viewH * 0.78)}px`;
      if (bottomPad) bottomPad.style.height = `${Math.round(viewH * 0.55)}px`;
    };

    const applyTransform = () => {
      track.style.transform = `translate3d(0, ${-offset}px, 0)`;
    };
    const maxOffset = () => Math.max(0, track.scrollHeight - viewport.clientHeight);

    const tick = (ts) => {
      if (!playing) return;
      if (!lastTs) lastTs = ts;
      const dt = (ts - lastTs) / 1000;
      lastTs = ts;
      offset += pxPerSec * dt;
      const max = maxOffset();
      if (offset >= max) {
        offset = max;
        playing = false;
        lastTs = 0;
        if (btnPlay) btnPlay.textContent = "▶ Play";
        applyTransform();
        return;
      }
      applyTransform();
      raf = requestAnimationFrame(tick);
    };

    const play = () => {
      if (playing) return;
      if (offset >= maxOffset() - 1) offset = 0;
      playing = true;
      lastTs = 0;
      if (btnPlay) btnPlay.textContent = "▶ Playing…";
      raf = requestAnimationFrame(tick);
    };
    const pause = () => {
      playing = false;
      lastTs = 0;
      if (raf) cancelAnimationFrame(raf);
      if (btnPlay) btnPlay.textContent = "▶ Play";
    };
    const restart = () => {
      pause();
      offset = 0;
      applyTransform();
    };
    const rebuild = () => {
      const was = playing;
      pause();
      buildTrack();
      offset = Math.min(offset, maxOffset());
      applyTransform();
      if (was) play();
    };

    buildTrack();
    applyTransform();
    btnPlay?.addEventListener("click", play);
    btnPause?.addEventListener("click", pause);
    btnRestart?.addEventListener("click", restart);
    if (speedRange && speedVal) {
      speedRange.addEventListener("input", () => {
        pxPerSec = Number(speedRange.value);
        speedVal.textContent = String(pxPerSec);
      });
    }
    hintMode?.addEventListener("change", rebuild);
    revealTog?.addEventListener("change", rebuild);
    showPyTog?.addEventListener("change", rebuild);
    btnCopy?.addEventListener("click", async () => {
      const text = (data.script || []).map((p) => p.zh).join("\n\n");
      try {
        await navigator.clipboard.writeText(text);
        const prev = btnCopy.textContent;
        btnCopy.textContent = "Copied";
        setTimeout(() => {
          btnCopy.textContent = prev;
        }, 1400);
      } catch {
        /* ignore */
      }
    });
  };

  /* ── Word checklist ───────────────────────────────────────────────── */
  const renderChecklist = () => {
    const list = document.getElementById("hskVocabList");
    if (!list) return;
    list.innerHTML = vocab
      .map(
        (w) =>
          `<li><mark class="vocab hsk-new">${escapeHtml(w.hanzi)}</mark> <span class="ipa">${escapeHtml(
            w.pinyin
          )}</span> — ${escapeHtml(w.vi)} <span class="hsk-check-en">· ${escapeHtml(w.en)}</span></li>`
      )
      .join("");
  };

  initFlashcards();
  renderScript();
  initScrollRead();
  renderChecklist();
})();
