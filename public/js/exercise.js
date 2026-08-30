(() => {
  const root = document.getElementById("passage");
  const pageRoot = document.querySelector(".docs-main") || document.body;

  const body = document.body;
  const togHighlight = document.getElementById("togHighlight");
  const togIpa = document.getElementById("togIpa");
  const togVi = document.getElementById("togVi");
  const voiceSelect = document.getElementById("voiceSelect");
  const rateRange = document.getElementById("rateRange");
  const rateVal = document.getElementById("rateVal");
  const btnPlay = document.getElementById("btnPlay");
  const btnStop = document.getElementById("btnStop");

  const applyToggles = () => {
    body.classList.toggle("ex-hide-hl", togHighlight && !togHighlight.checked);
    body.classList.toggle("ex-hide-ipa", togIpa && !togIpa.checked);
    body.classList.toggle("ex-show-vi", togVi && togVi.checked);
  };
  if (root) {
    [togHighlight, togIpa, togVi].forEach((el) => el && el.addEventListener("change", applyToggles));
    applyToggles();
  }

  /** Plain English from a sentence node — IPA is display-only, never spoken/copied. */
  const plainFromEn = (el) => {
    const clone = el.cloneNode(true);
    clone.querySelectorAll(".ipa").forEach((n) => n.remove());
    return clone.textContent.replace(/\s+/g, " ").trim();
  };

  const sentenceTexts = () =>
    root ? [...root.querySelectorAll(".ex-en")].map(plainFromEn).filter(Boolean) : [];

  const passageText = () => sentenceTexts().join(" ");

  /** One continuous paragraph for NaturalReader / external TTS paste. */
  const ensureContinuousBlock = () => {
    if (!root) return;
    let section = document.getElementById("exContinuous");
    if (!section) {
      section = document.createElement("section");
      section.className = "ex-continuous";
      section.id = "exContinuous";
      section.innerHTML = `
        <div class="ex-continuous-head">
          <h2>Continuous paragraph</h2>
          <button type="button" class="ex-btn primary" id="btnCopyPara">Copy</button>
        </div>
        <p class="ex-continuous-hint">Plain English only (no IPA) — copy and paste into <a href="https://www.naturalreaders.com/online/" target="_blank" rel="noopener noreferrer">NaturalReader</a> or any TTS.</p>
        <textarea id="exParaText" class="ex-para" readonly rows="8" aria-label="Continuous paragraph for external TTS"></textarea>
      `;
      root.insertAdjacentElement("afterend", section);
    }
    const ta = document.getElementById("exParaText");
    if (ta) ta.value = passageText();

    const btn = document.getElementById("btnCopyPara");
    if (btn && !btn.dataset.bound) {
      btn.dataset.bound = "1";
      btn.addEventListener("click", async () => {
        const text = (ta && ta.value) || passageText();
        if (!text) return;
        try {
          await navigator.clipboard.writeText(text);
          const prev = btn.textContent;
          btn.textContent = "Copied";
          setTimeout(() => {
            btn.textContent = prev;
          }, 1400);
        } catch {
          if (ta) {
            ta.focus();
            ta.select();
          }
        }
      });
    }
  };
  if (root) ensureContinuousBlock();

  const shuffle = (arr) => {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  };

  const loadVocab = () => {
    const raw = document.getElementById("exVocabData");
    if (raw && raw.textContent.trim()) {
      try {
        const data = JSON.parse(raw.textContent);
        return data.filter((w) => w.form && (w.vi || w.word || w.ipa));
      } catch {
        /* fall through */
      }
    }
    return [...document.querySelectorAll(".ex-vocab-list li")]
      .map((li, i) => {
        const form = (li.querySelector("mark.vocab") || {}).textContent || "";
        const ipaEl = li.querySelector(".ipa");
        const ipa = ipaEl ? ipaEl.textContent.replace(/\//g, "").trim() : "";
        const parts = li.textContent.split("—");
        const vi = parts.length > 1 ? parts.slice(1).join("—").trim() : "";
        return { id: i, form: form.trim(), word: form.trim(), ipa, vi, pos: "" };
      })
      .filter((w) => w.form);
  };

  const escapeHtml = (s) =>
    String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");

  /* ── Scroll read (VOA-style teleprompter + cloze vocab) ───────────── */
  const initScrollRead = () => {
    if (!root) return;
    const vocab = loadVocab();
    const byKey = new Map();
    vocab.forEach((w) => {
      byKey.set(String(w.word || "").toLowerCase(), w);
      byKey.set(String(w.form || "").toLowerCase(), w);
    });

    let section = document.getElementById("exScroll");
    if (!section) {
      section = document.createElement("section");
      section.className = "ex-scroll";
      section.id = "exScroll";
      section.setAttribute("aria-label", "Scroll reading teleprompter");
      section.innerHTML = `
        <div class="ex-scroll-head">
          <div>
            <h2>Scroll read · speaking</h2>
            <p class="ex-scroll-hint">Đọc theo chữ cuộn kiểu teleprompter (VOA-style). Từ mới bị ẩn — hiện nghĩa VI hoặc IPA để bạn tự nhớ và nói ra tiếng Anh.</p>
          </div>
        </div>
        <div class="ex-scroll-toolbar">
          <button type="button" class="ex-btn primary" id="btnScrollPlay">▶ Play</button>
          <button type="button" class="ex-btn" id="btnScrollPause">Pause</button>
          <button type="button" class="ex-btn" id="btnScrollRestart">⟲ Restart</button>
          <label class="ex-voice">Speed
            <input id="scrollSpeed" type="range" min="12" max="90" step="1" value="32">
            <span id="scrollSpeedVal">32</span> px/s
          </label>
          <label class="ex-voice">Hint
            <select id="scrollHintMode" aria-label="Hint mode for hidden words">
              <option value="vi" selected>Nghĩa VI</option>
              <option value="ipa">IPA</option>
              <option value="both">VI + IPA</option>
            </select>
          </label>
          <label class="ex-toggle"><input type="checkbox" id="scrollReveal"> Hiện từ EN</label>
        </div>
        <div class="ex-scroll-stage">
          <div class="ex-scroll-focus" aria-hidden="true"></div>
          <div class="ex-scroll-viewport" id="scrollViewport">
            <div class="ex-scroll-track" id="scrollTrack"></div>
          </div>
        </div>
      `;
      const continuous = document.getElementById("exContinuous");
      const match = document.getElementById("exMatch");
      if (continuous) continuous.insertAdjacentElement("afterend", section);
      else if (match) match.insertAdjacentElement("beforebegin", section);
      else root.insertAdjacentElement("afterend", section);
    }

    const track = document.getElementById("scrollTrack");
    const viewport = document.getElementById("scrollViewport");
    const speedRange = document.getElementById("scrollSpeed");
    const speedVal = document.getElementById("scrollSpeedVal");
    const hintMode = document.getElementById("scrollHintMode");
    const revealTog = document.getElementById("scrollReveal");
    const btnPlay = document.getElementById("btnScrollPlay");
    const btnPause = document.getElementById("btnScrollPause");
    const btnRestart = document.getElementById("btnScrollRestart");
    if (!track || !viewport) return;

    let playing = false;
    let offset = 0;
    let raf = 0;
    let lastTs = 0;
    let pxPerSec = speedRange ? Number(speedRange.value) : 32;

    const hintFor = (meta, mode) => {
      const vi = (meta && meta.vi) || "";
      const ipa = (meta && meta.ipa) || "";
      if (mode === "ipa") return ipa ? `/${ipa}/` : "????";
      if (mode === "both") {
        if (vi && ipa) return `${vi} · /${ipa}/`;
        return vi || (ipa ? `/${ipa}/` : "????");
      }
      return vi || (ipa ? `/${ipa}/` : "????");
    };

    const buildTrack = () => {
      const mode = hintMode ? hintMode.value : "vi";
      const reveal = !!(revealTog && revealTog.checked);
      const blocks = [];
      root.querySelectorAll(".ex-en").forEach((el) => {
        const clone = el.cloneNode(true);
        clone.querySelectorAll("mark.vocab").forEach((mark) => {
          const form = mark.textContent.trim();
          const wordKey = (mark.getAttribute("data-word") || form).toLowerCase();
          let ipa = "";
          const next = mark.nextElementSibling;
          if (next && next.classList && next.classList.contains("ipa")) {
            ipa = next.textContent.replace(/\//g, "").trim();
            next.remove();
          }
          const meta =
            byKey.get(wordKey) ||
            byKey.get(form.toLowerCase()) ||
            { form, vi: "", ipa };
          if (!meta.ipa && ipa) meta.ipa = ipa;

          const blank = document.createElement("span");
          blank.className = "scroll-blank";
          blank.dataset.answer = form;
          blank.title = "Click to peek answer";
          if (reveal) {
            blank.classList.add("is-revealed");
            blank.innerHTML = `<span class="scroll-blank-answer">${escapeHtml(form)}</span>`;
          } else {
            blank.innerHTML = `<span class="scroll-blank-gap">______</span><span class="scroll-blank-hint">${escapeHtml(
              hintFor(meta, mode)
            )}</span>`;
          }
          blank.addEventListener("click", (e) => {
            e.preventDefault();
            if (blank.classList.contains("is-revealed")) {
              blank.classList.remove("is-revealed");
              blank.innerHTML = `<span class="scroll-blank-gap">______</span><span class="scroll-blank-hint">${escapeHtml(
                hintFor(meta, mode)
              )}</span>`;
            } else {
              blank.classList.add("is-revealed");
              blank.innerHTML = `<span class="scroll-blank-answer">${escapeHtml(form)}</span>`;
            }
          });
          mark.replaceWith(blank);
        });
        clone.querySelectorAll(".ipa").forEach((n) => n.remove());
        const html = clone.innerHTML.replace(/\s+/g, " ").trim();
        if (html) blocks.push(`<p class="scroll-line">${html}</p>`);
      });
      track.innerHTML =
        `<div class="scroll-pad scroll-pad--top"></div>${blocks.join("")}<div class="scroll-pad scroll-pad--bottom"></div>`;
      // Lead-in must be in px — % height on track children is unreliable.
      // Top pad ~75% viewport so text starts below the focus line and you have time to prepare.
      const viewH = viewport.clientHeight || 420;
      const topPad = track.querySelector(".scroll-pad--top");
      const bottomPad = track.querySelector(".scroll-pad--bottom");
      if (topPad) topPad.style.height = `${Math.round(viewH * 0.78)}px`;
      if (bottomPad) bottomPad.style.height = `${Math.round(viewH * 0.55)}px`;
    };

    const applyTransform = () => {
      track.style.transform = `translate3d(0, ${-offset}px, 0)`;
    };

    const maxOffset = () => {
      const trackH = track.scrollHeight;
      const viewH = viewport.clientHeight;
      return Math.max(0, trackH - viewH);
    };

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
      const wasPlaying = playing;
      pause();
      buildTrack();
      offset = Math.min(offset, maxOffset());
      applyTransform();
      if (wasPlaying) play();
    };

    buildTrack();
    applyTransform();

    btnPlay && btnPlay.addEventListener("click", play);
    btnPause && btnPause.addEventListener("click", pause);
    btnRestart && btnRestart.addEventListener("click", restart);
    if (speedRange && speedVal) {
      speedRange.addEventListener("input", () => {
        pxPerSec = Number(speedRange.value);
        speedVal.textContent = String(pxPerSec);
      });
    }
    hintMode && hintMode.addEventListener("change", rebuild);
    revealTog && revealTog.addEventListener("change", rebuild);
  };
  initScrollRead();

  /* ── Match quiz (word ↔ nghĩa) ─────────────────────────────────────── */
  const PAIR_COUNT = 6;

  const initMatchGame = () => {
    const vocab = loadVocab();
    let section = document.getElementById("exMatch");
    if (!vocab.length) {
      if (section) section.hidden = true;
      return;
    }

    if (!section) {
      section = document.createElement("section");
      section.className = "ex-match";
      section.id = "exMatch";
      section.setAttribute("aria-label", "Vocabulary match quiz");
      section.innerHTML = `
        <div class="ex-match-head">
          <div>
            <h2>Match quiz</h2>
            <p class="ex-match-hint">Ghép từ (EN + IPA) với nghĩa tiếng Việt — mỗi ván 6 cặp. Tính điểm, có thể Reset / New round.</p>
          </div>
          <div class="ex-match-controls">
            <div class="ex-match-stats" aria-live="polite">
              <span>Score <strong id="matchScore">0</strong></span>
              <span>Matched <strong id="matchDone">0</strong>/<strong id="matchTotal">0</strong></span>
              <span>Misses <strong id="matchMiss">0</strong></span>
            </div>
            <button type="button" class="ex-btn" id="btnMatchReset">Reset</button>
            <button type="button" class="ex-btn primary" id="btnMatchNew">New round</button>
          </div>
        </div>
        <div class="ex-match-grid" id="matchGrid"></div>
        <p class="ex-match-msg" id="matchMsg" hidden></p>
      `;
      const scroll = document.getElementById("exScroll");
      const continuous = document.getElementById("exContinuous");
      const vocabSec = document.querySelector(".ex-vocab");
      if (scroll) scroll.insertAdjacentElement("afterend", section);
      else if (continuous) continuous.insertAdjacentElement("afterend", section);
      else if (vocabSec) vocabSec.insertAdjacentElement("beforebegin", section);
      else pageRoot.insertAdjacentElement("afterend", section);
    }

    const grid = document.getElementById("matchGrid");
    const elScore = document.getElementById("matchScore");
    const elDone = document.getElementById("matchDone");
    const elTotal = document.getElementById("matchTotal");
    const elMiss = document.getElementById("matchMiss");
    const elMsg = document.getElementById("matchMsg");
    const btnReset = document.getElementById("btnMatchReset");
    const btnNew = document.getElementById("btnMatchNew");
    if (!grid) return;

    let score = 0;
    let misses = 0;
    let matched = 0;
    let total = 0;
    let selected = null;
    let locked = false;
    let roundPairs = [];
    let usedIds = new Set();

    const renderStats = () => {
      if (elScore) elScore.textContent = String(score);
      if (elDone) elDone.textContent = String(matched);
      if (elTotal) elTotal.textContent = String(total);
      if (elMiss) elMiss.textContent = String(misses);
    };

    const showMsg = (text, ok) => {
      if (!elMsg) return;
      elMsg.hidden = !text;
      elMsg.textContent = text || "";
      elMsg.classList.toggle("ok", !!ok);
    };

    const pickRound = (freshPool) => {
      const pool = freshPool
        ? shuffle(vocab)
        : shuffle(vocab.filter((w) => !usedIds.has(w.id)));
      if (!pool.length || (pool.length < Math.min(PAIR_COUNT, vocab.length) && !freshPool)) {
        usedIds = new Set();
        return pickRound(true);
      }
      const n = Math.min(PAIR_COUNT, pool.length);
      roundPairs = pool.slice(0, n);
      roundPairs.forEach((w) => usedIds.add(w.id));
      return roundPairs;
    };

    const buildBoard = (pairs) => {
      matched = 0;
      total = pairs.length;
      selected = null;
      locked = false;
      showMsg("");
      renderStats();

      const cards = [];
      pairs.forEach((w) => {
        cards.push({
          key: String(w.id),
          kind: "word",
          label: w.form,
          ipa: w.ipa ? `/${w.ipa}/` : "",
        });
        cards.push({
          key: String(w.id),
          kind: "def",
          label: w.vi || w.form,
          meta: [w.pos, w.form].filter(Boolean).join(" · "),
        });
      });

      grid.innerHTML = "";
      shuffle(cards).forEach((c) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = `ex-match-card ex-match-card--${c.kind}`;
        btn.dataset.key = c.key;
        btn.dataset.kind = c.kind;
        if (c.kind === "word") {
          btn.innerHTML = `<span class="ex-match-term">${escapeHtml(c.label)}</span>${
            c.ipa ? `<span class="ex-match-ipa">${escapeHtml(c.ipa)}</span>` : ""
          }`;
        } else {
          btn.innerHTML = `<span class="ex-match-vi"><em>Nghĩa</em> ${escapeHtml(c.label)}</span>${
            c.meta ? `<span class="ex-match-meta">${escapeHtml(c.meta)}</span>` : ""
          }`;
        }
        btn.addEventListener("click", () => onCard(btn));
        grid.appendChild(btn);
      });
    };

    const clearSelection = () => {
      grid.querySelectorAll(".ex-match-card.is-selected").forEach((el) => {
        el.classList.remove("is-selected");
      });
      selected = null;
    };

    const onCard = (btn) => {
      if (locked || btn.classList.contains("is-matched") || btn.classList.contains("is-selected")) {
        return;
      }
      if (!selected) {
        selected = btn;
        btn.classList.add("is-selected");
        return;
      }
      if (selected.dataset.kind === btn.dataset.kind) {
        clearSelection();
        selected = btn;
        btn.classList.add("is-selected");
        return;
      }

      locked = true;
      btn.classList.add("is-selected");
      const a = selected;
      const b = btn;
      const ok = a.dataset.key === b.dataset.key;

      if (ok) {
        score += 10;
        matched += 1;
        a.classList.remove("is-selected");
        b.classList.remove("is-selected");
        a.classList.add("is-matched");
        b.classList.add("is-matched");
        a.disabled = true;
        b.disabled = true;
        selected = null;
        locked = false;
        renderStats();
        if (matched >= total) {
          const bonus = Math.max(0, 20 - misses * 2);
          score += bonus;
          renderStats();
          showMsg(
            `Round clear! +${bonus} bonus (misses: ${misses}). Score: ${score}. Bấm New round để chơi tiếp.`,
            true
          );
        }
      } else {
        misses += 1;
        score = Math.max(0, score - 2);
        a.classList.add("is-wrong");
        b.classList.add("is-wrong");
        renderStats();
        setTimeout(() => {
          a.classList.remove("is-selected", "is-wrong");
          b.classList.remove("is-selected", "is-wrong");
          selected = null;
          locked = false;
        }, 520);
      }
    };

    const startRound = (resetScore) => {
      if (resetScore) {
        score = 0;
        misses = 0;
        usedIds = new Set();
      }
      const pairs = pickRound(resetScore);
      buildBoard(pairs);
    };

    btnReset &&
      btnReset.addEventListener("click", () => {
        startRound(true);
      });
    btnNew &&
      btnNew.addEventListener("click", () => {
        misses = 0;
        startRound(false);
      });

    startRound(true);
  };
  initMatchGame();

  /* ── Flashcards (LanGeek-style front / back + self-grade) ───────────── */
  const POS_VI = {
    noun: "Danh từ",
    verb: "Động từ",
    adjective: "Tính từ",
    adverb: "Trạng từ",
    preposition: "Giới từ",
    conjunction: "Liên từ",
    pronoun: "Đại từ",
    interjection: "Thán từ",
    determiner: "Hạn định từ",
    phrase: "Cụm từ",
    numeral: "Số từ",
  };

  const posLabel = (pos) => {
    const key = String(pos || "")
      .toLowerCase()
      .trim();
    if (!key) return "";
    return POS_VI[key] || pos;
  };

  const escapeRegExp = (s) => String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

  const aAn = (word) => (/^[aeiou]/i.test(String(word || "").trim()) ? "an" : "a");

  const highlightWordHtml = (sentence, form) => {
    const s = String(sentence || "");
    const f = String(form || "").trim();
    if (!s) return "";
    if (!f) return escapeHtml(s);
    const re = new RegExp(`\\b(${escapeRegExp(f)})\\b`, "gi");
    let out = "";
    let last = 0;
    let m;
    let hit = false;
    while ((m = re.exec(s))) {
      hit = true;
      out += escapeHtml(s.slice(last, m.index));
      out += `<mark class="ex-flash-hl">${escapeHtml(m[1])}</mark>`;
      last = m.index + m[0].length;
    }
    out += escapeHtml(s.slice(last));
    if (!hit) {
      const idx = s.toLowerCase().indexOf(f.toLowerCase());
      if (idx >= 0) {
        return (
          escapeHtml(s.slice(0, idx)) +
          `<mark class="ex-flash-hl">${escapeHtml(s.slice(idx, idx + f.length))}</mark>` +
          escapeHtml(s.slice(idx + f.length))
        );
      }
    }
    return out;
  };

  /** Hand-tuned spoken contexts — used when meaning is easy to get wrong. */
  const FLASH_OVERRIDES = {
    chubby: [
      {
        title: "1. Trêu đùa vui vẻ giữa bạn bè (Về ngoại hình)",
        situation: "Bạn nhận xét về cơ thể của chính mình hoặc bạn thân sau kỳ nghỉ lễ.",
        en: "Look at me, I'm getting a bit chubby after all those Tet holidays!",
        vi: "Nhìn tôi xem, mập lên một chút sau mấy ngày Tết rồi đây này!",
      },
      {
        title: "2. Khen ngợi đáng yêu (Khen trẻ con hoặc thú cưng)",
        situation: "Nhìn thấy một em bé hoặc chú cún cưng có thân hình mũm mĩm, tròn trịa.",
        en: "Aww, look at those chubby little hands! So cute!",
        vi: "Ôi, nhìn đôi bàn tay mũm mĩm kìa! Dễ thương quá!",
      },
      {
        title: "3. Nói về các bộ phận trên cơ thể (Má, tay, chân)",
        situation: "Nhận xét về đặc điểm cơ thể một cách gần gũi, không chê bai.",
        en: "She has such a cute chubby face, it makes her look younger.",
        vi: "Cậu ấy có khuôn mặt mũm mĩm trông rất đáng yêu, khiến cậu ấy trông trẻ hơn.",
      },
    ],
    spot: [
      {
        title: "1. So gương / chăm sóc da",
        situation: "Bạn vừa thức khuya và nhìn thấy mụn trên mặt.",
        en: "Ugh, I got a huge spot on my chin after staying up all night.",
        vi: "Ước, mình lên một cái mụn to trên cằm sau khi thức trắng đêm.",
      },
      {
        title: "2. Than thở với bạn thân",
        situation: "Nhắn tin / nói chuyện về da trước buổi gặp mặt.",
        en: "Please don't take close-up photos today — I've got a spot right on my nose.",
        vi: "Hôm nay đừng chụp cận mặt mình nhé — đang có mụn ngay trên mũi.",
      },
      {
        title: "3. Hỏi nhẹ về skincare",
        situation: "Hỏi bạn từng bị mụn cách xử lý thế nào.",
        en: "What do you use when you get a spot before an important meeting?",
        vi: "Bạn dùng gì khi bị mụn trước một buổi họp quan trọng vậy?",
      },
    ],
    childish: [
      {
        title: "1. Phàn nàn nhẹ với bạn thân",
        situation: "Kể về người yêu / bạn bè phản ứng thiếu chín chắn.",
        en: "He ignored my texts all day then got angry — that was so childish.",
        vi: "Anh ấy cả ngày không trả lời tin nhắn rồi lại giận — trẻ con quá.",
      },
      {
        title: "2. Nói về đồng nghiệp / nhóm làm việc",
        situation: "Nhận xét hành vi thiếu chuyên nghiệp trong công việc.",
        en: "Arguing about who gets the last snack in a meeting feels childish.",
        vi: "Cãi nhau trong họp chỉ vì miếng snack cuối cùng trông rất trẻ con.",
      },
      {
        title: "3. Tự nhận / đùa về bản thân",
        situation: "Bạn tự nhận mình hơi nông nổi rồi cười trừ.",
        en: "Okay, maybe I was being childish — I should just apologize.",
        vi: "Thôi được, có lẽ mình hơi trẻ con — chắc nên xin lỗi thôi.",
      },
    ],
  };

  const shortenAroundWord = (text, form, maxLen = 130) => {
    const s = String(text || "").replace(/\s+/g, " ").trim();
    if (s.length <= maxLen) return s;
    const f = String(form || "").toLowerCase();
    const idx = s.toLowerCase().indexOf(f);
    if (idx < 0) return `${s.slice(0, maxLen - 1)}…`;
    const start = Math.max(0, idx - 40);
    const end = Math.min(s.length, idx + f.length + 70);
    let chunk = s.slice(start, end).trim();
    if (start > 0) chunk = `…${chunk}`;
    if (end < s.length) chunk = `${chunk}…`;
    return chunk;
  };

  const passageContextsForWord = (w) => {
    if (!root) return [];
    const form = String(w.form || "").trim();
    const keys = [w.word, w.form]
      .map((s) => String(s || "").toLowerCase().trim())
      .filter(Boolean);
    if (!keys.length) return [];
    const out = [];
    const titles = [
      "1. Trong đoạn luyện đọc",
      "2. Ngữ cảnh khác trong bài",
      "3. Luyện nói lại câu trong bài",
    ];
    for (const sent of root.querySelectorAll(".ex-sent")) {
      const enEl = sent.querySelector(".ex-en");
      const viEl = sent.querySelector(".ex-vi");
      if (!enEl) continue;
      const marks = [...enEl.querySelectorAll("mark.vocab")];
      const hit = marks.some((m) => {
        const dw = String(m.dataset.word || m.textContent || "")
          .toLowerCase()
          .trim();
        return keys.some((k) => dw === k || dw.includes(k) || k.includes(dw));
      });
      if (!hit && !keys.some((k) => plainFromEn(enEl).toLowerCase().includes(k))) {
        continue;
      }
      const en = shortenAroundWord(plainFromEn(enEl), form);
      const viRaw = viEl ? viEl.textContent.replace(/\s+/g, " ").trim() : "";
      const vi = shortenAroundWord(viRaw, w.vi || form, 140);
      if (!en) continue;
      out.push({
        title: titles[out.length] || `${out.length + 1}. Trong bài đọc`,
        situation: "Câu lấy từ đoạn exercise — nói lại cho tự nhiên, đúng nghĩa từ.",
        en,
        vi,
      });
      if (out.length >= 3) break;
    }
    return out;
  };

  const classifySense = (w) => {
    const form = String(w.form || "").toLowerCase();
    const vi = String(w.vi || "").toLowerCase();
    const pos = String(w.pos || "").toLowerCase();
    const word = String(w.word || "").toLowerCase();
    const blob = `${form} ${vi} ${word}`;

    if (
      /mụn|nốt mụn|trứng cá|\bpimple\b|\bacne\b|\bblemi\w*\b|\bblackhead\b|\bzit\b/.test(blob) ||
      (form === "spot" && /mụn/.test(vi))
    ) {
      return "skin_blemish";
    }
    if (
      form === "spot" &&
      /chỗ|nơi|vị trí|địa điểm|place|location|area|seat/.test(vi)
    ) {
      return "place";
    }
    if (
      /mũm|béo|gầy|mảnh|tròn trịa|thừa cân|gầy guộc|plump|chubby|skinny|slim|overweight|\bfat\b|\bthin\b|\blean\b/.test(
        blob
      )
    ) {
      return "body_size";
    }
    if (
      pos === "adjective" &&
      /trẻ con|ích kỷ|thô lỗ|kiêu|hách|bướng|ghen|cáu|đỏng đảnh|childish|selfish|rude|arrogant|mean|nasty|moody|stubborn|jealous|immature|petty/.test(
        blob
      )
    ) {
      return "adj_negative";
    }
    if (
      pos === "adjective" &&
      /đẹp|xinh|lộng lẫy|hấp dẫn|dễ thương|stunning|gorgeous|pretty|handsome|attractive|lovely|cute|charming|elegant/.test(
        blob
      )
    ) {
      return "adj_positive";
    }
    if (
      pos === "adjective" &&
      /vui|buồn|tức|lo|hạnh phúc|tức giận|happy|sad|angry|worried|excited|nervous|calm|stressed|afraid|scared/.test(
        blob
      )
    ) {
      return "adj_emotion";
    }
    if (
      pos === "noun" &&
      /tay|chân|mặt|tóc|mắt|mũi|miệng|vai|lưng|cằm|má|da|hand|face|hair|eye|leg|arm|skin|chin|cheek|nose|mouth|shoulder/.test(
        blob
      )
    ) {
      return "body_part";
    }
    if (pos === "noun" && /chỗ|nơi|vị trí|địa điểm|place|location|area|spot|seat|venue/.test(blob)) {
      return "place";
    }
    if (pos === "verb") return "verb_action";
    if (pos === "adverb") return "adverb";
    if (pos === "adjective") return "adj_general";
    if (pos === "interjection") return "interjection";
    if (pos === "phrase" || form.includes(" ")) return "phrase";
    if (pos === "noun") return "noun_thing";
    return "generic";
  };

  const senseContexts = (w, sense) => {
    const form = String(w.form || "").trim();
    const vi = String(w.vi || form).trim();
    const art = aAn(form);

    const banks = {
      skin_blemish: [
        {
          title: "1. So gương buổi sáng",
          situation: "Bạn vừa ngủ dậy và thấy da có vấn đề.",
          en: `Oh no — I've got ${art} ${form} right on my forehead.`,
          vi: `Trời — mình lên ${vi} ngay trên trán rồi.`,
        },
        {
          title: "2. Than với bạn trước buổi gặp mặt",
          situation: "Muốn trông gọn gàng nhưng da đang xấu.",
          en: `Can you even see this ${form}? Makeup isn't covering it at all.`,
          vi: `Bạn có thấy ${vi} này không? Makeup chẳng che được gì.`,
        },
        {
          title: "3. Xin lời khuyên skincare",
          situation: "Hỏi bạn / anh chị cách xử lý nhẹ nhàng.",
          en: `Whenever I get ${art} ${form}, I just use a simple cream — what about you?`,
          vi: `Hễ bị ${vi} là mình chỉ bôi kem đơn giản — còn bạn thì sao?`,
        },
      ],
      body_size: [
        {
          title: "1. Trêu đùa vui về bản thân",
          situation: "Nói vui sau kỳ nghỉ hoặc ăn uống nhiều.",
          en: `I've been feeling a bit ${form} after the holidays.`,
          vi: `Sau kỳ nghỉ mình thấy hơi ${vi} rồi.`,
        },
        {
          title: "2. Khen đáng yêu (trẻ nhỏ / thú cưng)",
          situation: "Nhìn thấy hình dáng tròn trịa dễ thương.",
          en: `Look at those ${form} cheeks — so adorable!`,
          vi: `Nhìn má ${vi} kìa — đáng yêu quá!`,
        },
        {
          title: "3. Mô tả trung lập, không công kích",
          situation: "Nhắc đặc điểm ngoại hình một cách nhẹ nhàng.",
          en: `He's always been a little ${form}, and it suits him.`,
          vi: `Anh ấy vốn hơi ${vi}, mà trông cũng hợp.`,
        },
      ],
      adj_negative: [
        {
          title: "1. Phàn nàn nhẹ với bạn thân",
          situation: "Kể về hành vi làm bạn khó chịu.",
          en: `Leaving me on read and then blaming me is pretty ${form}.`,
          vi: `Bỏ đọc tin nhắn rồi đổ lỗi cho mình thì khá là ${vi}.`,
        },
        {
          title: "2. Nhận xét trong học tập / công việc",
          situation: "Nói về thái độ thiếu chín chắn của ai đó.",
          en: `Throwing a tantrum over feedback feels ${form} in a team.`,
          vi: `Nổi cáu vì góp ý trong team trông rất ${vi}.`,
        },
        {
          title: "3. Tự nhận và sửa sai",
          situation: "Bạn thừa nhận mình hơi quá đà.",
          en: `I was being ${form} earlier — sorry about that.`,
          vi: `Lúc nãy mình hơi ${vi} — xin lỗi nhé.`,
        },
      ],
      adj_positive: [
        {
          title: "1. Khen bạn / người thân",
          situation: "Khen ngoại hình hoặc khí chất một cách chân thành.",
          en: `You look really ${form} tonight — did you change your hair?`,
          vi: `Tối nay bạn trông ${vi} quá — đổi kiểu tóc à?`,
        },
        {
          title: "2. Nhận xét khi xem ảnh",
          situation: "Comment vui trên ảnh bạn đăng.",
          en: `This photo is so ${form} — you should post it!`,
          vi: `Ảnh này ${vi} quá — đăng lên đi!`,
        },
        {
          title: "3. Giới thiệu ai đó với bạn khác",
          situation: "Miêu tả người mới một cách tích cực.",
          en: `You'll like her — she's smart and genuinely ${form}.`,
          vi: `Bạn sẽ thích cô ấy — vừa thông minh vừa ${vi} thật.`,
        },
      ],
      adj_emotion: [
        {
          title: "1. Chia sẻ cảm xúc hôm nay",
          situation: "Trả lời câu 'How are you?' một cách thật.",
          en: `To be honest, I've been feeling ${form} all morning.`,
          vi: `Thành thật thì sáng nay mình thấy khá ${vi}.`,
        },
        {
          title: "2. Hỏi thăm bạn",
          situation: "Thấy bạn khác thường và hỏi nhẹ.",
          en: `You seem a bit ${form} — want to talk about it?`,
          vi: `Trông bạn hơi ${vi} — muốn nói chuyện không?`,
        },
        {
          title: "3. Kể lại phản ứng",
          situation: "Kể chuyện vừa xảy ra và cảm xúc lúc đó.",
          en: `When I heard the news, I felt suddenly ${form}.`,
          vi: `Khi nghe tin, mình bỗng thấy ${vi}.`,
        },
      ],
      adj_general: [
        {
          title: "1. Miêu tả tình huống thực tế",
          situation: "Dùng tính từ để nói rõ hơn về việc đang bàn.",
          en: `The whole situation feels ${form} if you ask me.`,
          vi: `Theo mình thì cả chuyện này khá ${vi}.`,
        },
        {
          title: "2. Hỏi ý kiến bạn",
          situation: "Muốn xác nhận cảm nhận của mình.",
          en: `Does this sound ${form} to you, or am I overthinking?`,
          vi: `Bạn thấy chuyện này có ${vi} không, hay mình đang nghĩ nhiều?`,
        },
        {
          title: "3. So sánh nhẹ trong hội thoại",
          situation: "Đối chiếu hai lựa chọn / hai người.",
          en: `This option is more ${form} than the last one.`,
          vi: `Lựa chọn này ${vi} hơn cái trước.`,
        },
      ],
      body_part: [
        {
          title: "1. Nói về khó chịu / đau nhẹ",
          situation: "Than với bạn về cơ thể.",
          en: `My ${form} still hurts from yesterday's workout.`,
          vi: `${vi.charAt(0).toUpperCase()}${vi.slice(1)} mình vẫn đau vì tập hôm qua.`,
        },
        {
          title: "2. Nhờ nhìn / kiểm tra giúp",
          situation: "Hỏi bạn có thấy gì bất thường không.",
          en: `Can you check my ${form}? It looks a bit red.`,
          vi: `Nhìn giúp ${vi} mình với — đang hơi đỏ.`,
        },
        {
          title: "3. Mô tả ngoại hình trung lập",
          situation: "Nhắc đặc điểm cơ thể khi kể chuyện.",
          en: `She covered her ${form} with a scarf because of the wind.`,
          vi: `Cô ấy che ${vi} bằng khăn vì gió.`,
        },
      ],
      place: [
        {
          title: "1. Rủ bạn gặp mặt",
          situation: "Hẹn chỗ gặp trong thành phố.",
          en: `Let's meet at our usual ${form} after work.`,
          vi: `Tan làm gặp nhau ở ${vi} quen thuộc nhé.`,
        },
        {
          title: "2. Hỏi đường / chỗ ngồi",
          situation: "Đang tìm chỗ trong quán / sự kiện.",
          en: `Is there a quiet ${form} near the window?`,
          vi: `Gần cửa sổ còn ${vi} yên tĩnh không?`,
        },
        {
          title: "3. Kể về chuyến đi",
          situation: "Chia sẻ trải nghiệm vừa đi về.",
          en: `That ${form} was crowded, but the view was worth it.`,
          vi: `${vi.charAt(0).toUpperCase()}${vi.slice(1)} đông thật, nhưng view đáng lắm.`,
        },
      ],
      noun_thing: [
        {
          title: "1. Giải thích nghĩa khi tán gẫu",
          situation: "Bạn hỏi từ này nghĩa gì trong ngữ cảnh đang nói.",
          en: `In this context, "${form}" basically means "${vi}".`,
          vi: `Trong ngữ cảnh này, "${form}" đại khái nghĩa là "${vi}".`,
        },
        {
          title: "2. Nhắc lại từ vừa học",
          situation: "Tự luyện nói: dùng từ mới trong câu tự nhiên.",
          en: `I just learned "${form}" — people use it when they talk about ${vi}.`,
          vi: `Mình vừa học "${form}" — người ta dùng khi nói về ${vi}.`,
        },
        {
          title: "3. Xác nhận cách dùng",
          situation: "Hỏi bạn bản xứ / bạn giỏi tiếng Anh.",
          en: `Would you say "${form}" here, or is there a more natural word?`,
          vi: `Ở đây nói "${form}" có ổn không, hay có từ tự nhiên hơn?`,
        },
      ],
      verb_action: [
        {
          title: "1. Kể thói quen",
          situation: "Nói về việc mình thường làm.",
          en: `I try to ${form} every morning if I have time.`,
          vi: `Có thời gian là mình cố ${vi} mỗi sáng.`,
        },
        {
          title: "2. Đưa lời khuyên ngắn",
          situation: "Gợi ý bạn trong tình huống thực tế.",
          en: `If that happens again, just ${form} and stay calm.`,
          vi: `Nếu lại thế thì cứ ${vi} và giữ bình tĩnh.`,
        },
        {
          title: "3. Kể chuyện vừa xảy ra",
          situation: "Thuật lại một khoảnh khắc gần đây.",
          en: `I had to ${form} quickly before anyone noticed.`,
          vi: `Mình phải ${vi} thật nhanh trước khi ai để ý.`,
        },
      ],
      adverb: [
        {
          title: "1. Mô tả cách làm việc",
          situation: "Kể bạn mình hoàn thành việc ra sao.",
          en: `I finished the report ${form}, so I went home early.`,
          vi: `Mình làm xong report khá ${vi} nên về sớm.`,
        },
        {
          title: "2. Làm mềm ý kiến",
          situation: "Không đồng ý hoàn toàn nhưng lịch sự.",
          en: `I ${form} disagree, but I get what you mean.`,
          vi: `Mình ${vi} không đồng ý lắm, nhưng hiểu ý bạn.`,
        },
        {
          title: "3. Thêm chi tiết khi kể",
          situation: "Nhấn mạnh cách sự việc diễn ra.",
          en: `She answered ${form}, and the room went quiet.`,
          vi: `Cô ấy trả lời ${vi}, rồi cả phòng im bặt.`,
        },
      ],
      phrase: [
        {
          title: "1. Dùng cụm trong tán gẫu",
          situation: "Nói chuyện đời thường với bạn.",
          en: `I need to ${form} before the weekend gets busy.`,
          vi: `Mình cần ${vi} trước khi cuối tuần bận rộn.`,
        },
        {
          title: "2. Hỏi xác nhận",
          situation: "Không chắc mình nghe đúng.",
          en: `Sorry — did you say we should ${form}?`,
          vi: `Khoan — bạn bảo mình nên ${vi} à?`,
        },
        {
          title: "3. Chia sẻ trải nghiệm",
          situation: "Kể việc vừa thử làm.",
          en: `I tried to ${form} yesterday, and it actually helped.`,
          vi: `Hôm qua mình thử ${vi}, hóa ra cũng hữu ích.`,
        },
      ],
      interjection: [
        {
          title: "1. Chào / bắt chuyện",
          situation: "Gặp bạn sau một thời gian.",
          en: `${form}! I didn't expect to see you here.`,
          vi: `${vi}! Không ngờ gặp bạn ở đây.`,
        },
        {
          title: "2. Phản ứng nhanh",
          situation: "Đáp lại tin vui hoặc bất ngờ.",
          en: `${form}! That's great news.`,
          vi: `${vi}! Tin vui quá.`,
        },
        {
          title: "3. Kết thúc hội thoại",
          situation: "Tạm biệt một cách tự nhiên.",
          en: `Alright, ${form}! Message me later.`,
          vi: `Thôi, ${vi}! Nhắn mình sau nhé.`,
        },
      ],
      generic: [
        {
          title: "1. Học nghĩa trong hội thoại",
          situation: "Bạn hỏi và bạn giải thích ngắn.",
          en: `"${form}" means "${vi}" in the sentence we just read.`,
          vi: `"${form}" trong câu vừa rồi nghĩa là "${vi}".`,
        },
        {
          title: "2. Tự luyện nói",
          situation: "Đặt câu tối giản để nhớ từ.",
          en: `Today's word is ${form} — I should use it in a real chat.`,
          vi: `Từ hôm nay là ${form} — mình nên dùng trong chat thật.`,
        },
        {
          title: "3. Kiểm tra cách dùng",
          situation: "Nhờ bạn chỉnh nếu nghe không tự nhiên.",
          en: `Is it natural to use "${form}" when talking about ${vi}?`,
          vi: `Dùng "${form}" khi nói về ${vi} có tự nhiên không?`,
        },
      ],
    };

    return banks[sense] || banks.generic;
  };

  const buildSpokenContexts = (w) => {
    const key = String(w.form || "")
      .toLowerCase()
      .trim();
    if (FLASH_OVERRIDES[key]) return FLASH_OVERRIDES[key];

    const fromPassage = passageContextsForWord(w);
    if (fromPassage.length >= 3) return fromPassage;

    const sense = classifySense(w);
    const fromSense = senseContexts(w, sense);
    if (!fromPassage.length) return fromSense;

    const merged = fromPassage.slice();
    for (const item of fromSense) {
      if (merged.length >= 3) break;
      const dup = merged.some(
        (m) => m.en.toLowerCase() === item.en.toLowerCase()
      );
      if (!dup) {
        merged.push({
          ...item,
          title: `${merged.length + 1}. ${item.title.replace(/^\d+\.\s*/, "")}`,
        });
      }
    }
    return merged.slice(0, 3);
  };

  const speakText = (text) => {
    if (!text || !window.speechSynthesis) return;
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = "en-US";
    u.rate = rateRange ? Number(rateRange.value) : 0.95;
    const pick = () => {
      const list = speechSynthesis.getVoices().filter((v) => /^en/i.test(v.lang));
      if (voiceSelect && list.length) {
        const idx = Number(voiceSelect.value || 0);
        if (list[idx]) return list[idx];
      }
      return list[0] || null;
    };
    const v = pick();
    if (v) {
      u.voice = v;
      u.lang = v.lang || "en-US";
    }
    speechSynthesis.speak(u);
  };

  const initFlashcards = () => {
    const vocab = loadVocab();
    let section = document.getElementById("exFlash");
    if (!vocab.length) {
      if (section) section.hidden = true;
      return;
    }

    if (!section) {
      section = document.createElement("section");
      section.className = "ex-flash";
      section.id = "exFlash";
      section.setAttribute("aria-label", "Vocabulary flashcards");
      section.innerHTML = `
        <div class="ex-flash-head">
          <div>
            <h2>Flashcards</h2>
            <p class="ex-flash-hint">Lật thẻ — nghĩa VI, <strong>định nghĩa tiếng Anh</strong> và <strong>ví dụ</strong> từ LanGeek (có ảnh minh họa khi có). Đánh giá <strong>Chính xác</strong> / <strong>Không chính xác</strong>.</p>
          </div>
          <div class="ex-flash-controls">
            <div class="ex-flash-stats" aria-live="polite">
              <span>Card <strong id="flashIndex">0</strong>/<strong id="flashTotal">0</strong></span>
              <span>Known <strong id="flashKnown">0</strong></span>
              <span>Learning <strong id="flashMiss">0</strong></span>
            </div>
            <button type="button" class="ex-btn" id="btnFlashShuffle">Shuffle</button>
            <button type="button" class="ex-btn primary" id="btnFlashRestart">Restart</button>
          </div>
        </div>
        <div class="ex-flash-stage" id="flashStage"></div>
        <p class="ex-flash-msg" id="flashMsg" hidden></p>
      `;
      const match = document.getElementById("exMatch");
      const vocabSec = document.querySelector(".ex-vocab");
      if (match) match.insertAdjacentElement("afterend", section);
      else if (vocabSec) vocabSec.insertAdjacentElement("beforebegin", section);
      else pageRoot.insertAdjacentElement("afterend", section);
    } else {
      const hint = section.querySelector(".ex-flash-hint");
      if (hint) {
        hint.innerHTML =
          'Lật thẻ — nghĩa VI, <strong>định nghĩa tiếng Anh</strong> và <strong>ví dụ</strong> từ LanGeek (có ảnh minh họa khi có). Đánh giá <strong>Chính xác</strong> / <strong>Không chính xác</strong>.';
      }
    }

    const stage = document.getElementById("flashStage");
    const elIndex = document.getElementById("flashIndex");
    const elTotal = document.getElementById("flashTotal");
    const elKnown = document.getElementById("flashKnown");
    const elMiss = document.getElementById("flashMiss");
    const elMsg = document.getElementById("flashMsg");
    const btnShuffle = document.getElementById("btnFlashShuffle");
    const btnRestart = document.getElementById("btnFlashRestart");
    if (!stage) return;

    let deck = [];
    let idx = 0;
    let known = 0;
    let learning = 0;
    let flipped = false;

    const showMsg = (text, ok) => {
      if (!elMsg) return;
      elMsg.hidden = !text;
      elMsg.textContent = text || "";
      elMsg.classList.toggle("ok", !!ok);
    };

    const renderStats = () => {
      if (elIndex) elIndex.textContent = String(deck.length ? idx + 1 : 0);
      if (elTotal) elTotal.textContent = String(deck.length);
      if (elKnown) elKnown.textContent = String(known);
      if (elMiss) elMiss.textContent = String(learning);
    };

    const current = () => deck[idx] || null;

    const peekWord = () => {
      if (idx + 1 >= deck.length) return null;
      return deck[idx + 1];
    };

    const stripMd = (s) => String(s || "").replace(/\*\*([^*]+)\*\*/g, "$1");

    const renderLanGeekBack = (w) => {
      const defEn = (w.def_en || "").trim();
      const exEn = (w.ex_en || "").trim();
      const exVi = stripMd(w.ex_vi || "");
      const photo = (w.photo || "").trim();
      let html = "";

      if (defEn) {
        html += `<p class="ex-flash-def-en">${escapeHtml(defEn)}</p>`;
      }
      if (photo) {
        html += `<figure class="ex-flash-photo"><img src="${escapeHtml(photo)}" alt="" loading="lazy" decoding="async" width="280" height="200"></figure>`;
      }
      if (exEn) {
        const enHtml = highlightWordHtml(exEn, w.form);
        html += `<div class="ex-flash-example">
          <div class="ex-flash-example-label">Ví dụ</div>
          <p class="ex-flash-example-en">
            ${enHtml}
            <button type="button" class="ex-flash-example-speak" data-speak-en="${escapeHtml(exEn)}" aria-label="Nghe ví dụ">▶</button>
          </p>
          ${exVi ? `<p class="ex-flash-example-vi">${escapeHtml(exVi)}</p>` : ""}
        </div>`;
      } else if (!defEn) {
        html += `<p class="ex-flash-def-en ex-flash-def-en--muted">${escapeHtml(w.vi || w.form)}</p>`;
      }
      return html;
    };

    const renderCard = () => {
      const w = current();
      flipped = false;
      showMsg("");
      renderStats();
      if (!w) {
        stage.innerHTML = `<div class="ex-flash-done">
          <p>Hoàn thành bộ thẻ.</p>
          <p class="ex-flash-done-meta">Known ${known} · Learning ${learning}</p>
          <button type="button" class="ex-btn primary" id="btnFlashAgain">Luyện lại</button>
        </div>`;
        const again = document.getElementById("btnFlashAgain");
        again && again.addEventListener("click", () => restart(true));
        return;
      }

      const pos = posLabel(w.pos);
      const ipa = w.ipa ? `/${w.ipa}/` : "";
      const next = peekWord();

      stage.innerHTML = `
        <div class="ex-flash-deck">
          <div class="ex-flash-card${flipped ? " is-flipped" : ""}" id="flashCard" tabindex="0" role="button" aria-label="Flashcard ${escapeHtml(w.form)}">
            <div class="ex-flash-face ex-flash-face--front">
              <button type="button" class="ex-flash-speak" id="flashSpeak" aria-label="Phát âm ${escapeHtml(w.form)}">
                <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>
              </button>
              <div class="ex-flash-front-body">
                <div class="ex-flash-term">${escapeHtml(w.form)}</div>
                ${pos ? `<div class="ex-flash-pos">[${escapeHtml(pos)}]</div>` : ""}
                ${
                  ipa
                    ? `<div class="ex-flash-ipa"><span class="ex-flash-flag" title="US">🇺🇸</span> ${escapeHtml(ipa)}</div>`
                    : ""
                }
              </div>
              <button type="button" class="ex-flash-flipbar" id="flashFlip">
                <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z"/></svg>
                Xem Định nghĩa
              </button>
            </div>
            <div class="ex-flash-face ex-flash-face--back">
              <button type="button" class="ex-flash-backnav" id="flashUnflip" aria-label="Quay lại mặt trước">
                <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
              </button>
              <div class="ex-flash-back-body">
                <div class="ex-flash-meaning">
                  <span class="ex-flash-star" aria-hidden="true">★</span>
                  <strong>${escapeHtml(w.vi || w.form)}</strong>
                </div>
                ${renderLanGeekBack(w)}
              </div>
              <div class="ex-flash-grade">
                <button type="button" class="ex-flash-grade-btn ex-flash-grade-btn--miss" id="flashMissBtn">
                  ✕ Không chính xác
                </button>
                <button type="button" class="ex-flash-grade-btn ex-flash-grade-btn--ok" id="flashOkBtn">
                  ✓ Chính xác
                </button>
              </div>
            </div>
          </div>
          ${
            next
              ? `<div class="ex-flash-peek" aria-hidden="true">
                  <div class="ex-flash-peek-term">${escapeHtml(next.form)}</div>
                  ${posLabel(next.pos) ? `<div class="ex-flash-peek-pos">[${escapeHtml(posLabel(next.pos))}]</div>` : ""}
                </div>`
              : ""
          }
        </div>
      `;

      const card = document.getElementById("flashCard");
      const setFlip = (on) => {
        if (flipped === on) return;
        flipped = on;
        card && card.classList.toggle("is-flipped", on);
        speakText(w.form);
      };

      const speakBtn = document.getElementById("flashSpeak");
      speakBtn &&
        speakBtn.addEventListener("click", (e) => {
          e.stopPropagation();
          speakText(w.form);
        });

      const flipBtn = document.getElementById("flashFlip");
      flipBtn &&
        flipBtn.addEventListener("click", (e) => {
          e.stopPropagation();
          setFlip(true);
        });

      const unflipBtn = document.getElementById("flashUnflip");
      unflipBtn &&
        unflipBtn.addEventListener("click", (e) => {
          e.stopPropagation();
          setFlip(false);
        });

      card &&
        card.addEventListener("keydown", (e) => {
          if (e.key === " " || e.key === "Enter") {
            e.preventDefault();
            setFlip(!flipped);
          }
        });

      stage.querySelectorAll("[data-speak-en]").forEach((btn) => {
        btn.addEventListener("click", (e) => {
          e.stopPropagation();
          speakText(btn.getAttribute("data-speak-en") || "");
        });
      });

      const advance = (ok) => {
        if (ok) known += 1;
        else learning += 1;
        idx += 1;
        renderCard();
      };

      const missBtn = document.getElementById("flashMissBtn");
      const okBtn = document.getElementById("flashOkBtn");
      missBtn && missBtn.addEventListener("click", () => advance(false));
      okBtn && okBtn.addEventListener("click", () => advance(true));
    };

    const restart = (doShuffle) => {
      deck = doShuffle ? shuffle(vocab) : vocab.slice();
      idx = 0;
      known = 0;
      learning = 0;
      renderCard();
    };

    btnShuffle &&
      btnShuffle.addEventListener("click", () => {
        restart(true);
      });
    btnRestart &&
      btnRestart.addEventListener("click", () => {
        restart(true);
      });

    restart(true);
  };
  initFlashcards();

  /* ── Browser TTS (skip IPA) ────────────────────────────────────────── */
  if (!window.speechSynthesis) return;

  let voices = [];
  const preferred = [
    /google us english/i,
    /google uk english/i,
    /microsoft aria/i,
    /microsoft jenny/i,
    /microsoft guy/i,
    /samantha/i,
    /karen/i,
    /daniel/i,
    /en-us/i,
    /en-gb/i,
  ];

  const scoreVoice = (v) => {
    const label = `${v.name} ${v.lang}`;
    if (!/^en/i.test(v.lang)) return 1000;
    for (let i = 0; i < preferred.length; i++) {
      if (preferred[i].test(label)) return i;
    }
    return 50;
  };

  const fillVoices = () => {
    voices = speechSynthesis.getVoices().filter((v) => /^en/i.test(v.lang));
    voices.sort((a, b) => scoreVoice(a) - scoreVoice(b));
    if (!voiceSelect) return;
    voiceSelect.innerHTML = "";
    voices.forEach((v, i) => {
      const opt = document.createElement("option");
      opt.value = String(i);
      opt.textContent = `${v.name} (${v.lang})`;
      voiceSelect.appendChild(opt);
    });
  };
  fillVoices();
  speechSynthesis.onvoiceschanged = fillVoices;

  if (rateRange && rateVal) {
    rateRange.addEventListener("input", () => {
      rateVal.textContent = Number(rateRange.value).toFixed(2);
    });
  }

  const stop = () => speechSynthesis.cancel();
  btnStop && btnStop.addEventListener("click", stop);

  btnPlay &&
    btnPlay.addEventListener("click", () => {
      stop();
      const text = passageText();
      if (!text) return;
      const u = new SpeechSynthesisUtterance(text);
      const idx = voiceSelect ? Number(voiceSelect.value || 0) : 0;
      if (voices[idx]) u.voice = voices[idx];
      u.rate = rateRange ? Number(rateRange.value) : 0.95;
      u.lang = (voices[idx] && voices[idx].lang) || "en-US";
      speechSynthesis.speak(u);
    });
})();
