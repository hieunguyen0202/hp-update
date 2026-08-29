(() => {
  const root = document.getElementById("passage");
  if (!root) return;

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
  [togHighlight, togIpa, togVi].forEach((el) => el && el.addEventListener("change", applyToggles));
  applyToggles();

  /** Plain English from a sentence node — IPA is display-only, never spoken/copied. */
  const plainFromEn = (el) => {
    const clone = el.cloneNode(true);
    clone.querySelectorAll(".ipa").forEach((n) => n.remove());
    return clone.textContent.replace(/\s+/g, " ").trim();
  };

  const sentenceTexts = () =>
    [...root.querySelectorAll(".ex-en")].map(plainFromEn).filter(Boolean);

  const passageText = () => sentenceTexts().join(" ");

  /** One continuous paragraph for NaturalReader / external TTS paste. */
  const ensureContinuousBlock = () => {
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
  ensureContinuousBlock();

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
      else root.insertAdjacentElement("afterend", section);
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

  /** Hand-tuned spoken contexts for words where templates feel wrong. */
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
  };

  const buildSpokenContexts = (w) => {
    const form = String(w.form || "").trim();
    const vi = String(w.vi || form).trim();
    const pos = String(w.pos || "")
      .toLowerCase()
      .trim();
    const key = form.toLowerCase();
    if (FLASH_OVERRIDES[key]) return FLASH_OVERRIDES[key];

    const art = aAn(form);

    if (pos === "adjective") {
      return [
        {
          title: "1. Trêu đùa vui vẻ giữa bạn bè",
          situation: "Bạn nhận xét vui về bản thân hoặc bạn thân trong hội thoại thường ngày.",
          en: `Look at me — I'm getting a bit ${form} these days!`,
          vi: `Nhìn tôi xem — dạo này hơi ${vi} rồi đây này!`,
        },
        {
          title: "2. Khen ngợi nhẹ nhàng / đáng yêu",
          situation: "Khen một người, em bé hoặc thú cưng một cách gần gũi, tích cực.",
          en: `Aww, you look so ${form} today — I love that!`,
          vi: `Ôi, hôm nay trông ${vi} quá — mình thích kiểu đó!`,
        },
        {
          title: "3. Mô tả trung lập trong nói chuyện",
          situation: "Miêu tả đặc điểm một cách tự nhiên, không công kích.",
          en: `She has such a ${form} vibe; it makes her easy to talk to.`,
          vi: `Cậu ấy mang vibe khá ${vi}, nên nói chuyện rất dễ chịu.`,
        },
      ];
    }

    if (pos === "verb") {
      return [
        {
          title: "1. Kể về thói quen hàng ngày",
          situation: "Bạn nói với bạn bè về việc mình thường làm.",
          en: `I usually ${form} for a few minutes before I start work.`,
          vi: `Mình thường ${vi} vài phút trước khi bắt đầu làm việc.`,
        },
        {
          title: "2. Khuyên / gợi ý bạn bè",
          situation: "Đưa lời khuyên ngắn trong hội thoại đời thường.",
          en: `If you're tired, just ${form} a little — it really helps.`,
          vi: `Nếu mệt thì cứ ${vi} một chút đi — giúp lắm đó.`,
        },
        {
          title: "3. Kể lại một khoảnh khắc",
          situation: "Kể chuyện ngắn với bạn: chuyện vừa xảy ra.",
          en: `Yesterday I had to ${form} in front of everyone. So awkward!`,
          vi: `Hôm qua mình phải ${vi} trước mọi người. Ngại hết sức!`,
        },
      ];
    }

    if (pos === "adverb") {
      return [
        {
          title: "1. Kể cách mình làm việc gì đó",
          situation: "Mô tả cách hành động trong nói chuyện hàng ngày.",
          en: `I finished it ${form}, so don't worry.`,
          vi: `Mình làm xong khá ${vi}, nên khỏi lo nhé.`,
        },
        {
          title: "2. Làm mềm ý kiến với bạn",
          situation: "Đưa ý kiến nhẹ nhàng, không cứng.",
          en: `I ${form} disagree, but I see your point.`,
          vi: `Mình ${vi} không đồng ý lắm, nhưng hiểu ý bạn.`,
        },
        {
          title: "3. Thêm chi tiết khi kể chuyện",
          situation: "Kể lại sự việc và nhấn cách thức diễn ra.",
          en: `She answered ${form}, and everyone went quiet.`,
          vi: `Cô ấy trả lời ${vi}, rồi cả phòng im hết.`,
        },
      ];
    }

    if (pos === "phrase" || form.includes(" ")) {
      return [
        {
          title: "1. Nói chuyện đời thường với bạn",
          situation: "Dùng cụm từ tự nhiên khi tán gẫu.",
          en: `To be honest, I ${form} more than I planned.`,
          vi: `Thật ra thì mình ${vi} nhiều hơn dự định.`,
        },
        {
          title: "2. Hỏi / xác nhận nhanh",
          situation: "Hỏi bạn trong tình huống thực tế.",
          en: `Wait — did you just ${form}?`,
          vi: `Khoan đã — bạn vừa ${vi} á?`,
        },
        {
          title: "3. Kể trải nghiệm ngắn",
          situation: "Chia sẻ trải nghiệm gần đây.",
          en: `Last weekend I tried to ${form}, and it felt weird at first.`,
          vi: `Cuối tuần trước mình thử ${vi}, lúc đầu thấy hơi lạ.`,
        },
      ];
    }

    if (pos === "interjection") {
      return [
        {
          title: "1. Chào hỏi / bắt chuyện",
          situation: "Mở lời với bạn hoặc đồng nghiệp.",
          en: `${form}! Long time no see.`,
          vi: `${vi}! Lâu rồi không gặp.`,
        },
        {
          title: "2. Phản ứng nhanh trong hội thoại",
          situation: "Đáp lại một tin vui hoặc bất ngờ.",
          en: `${form}! That's awesome news.`,
          vi: `${vi}! Tin vui quá đi.`,
        },
        {
          title: "3. Kết thúc cuộc gọi / tạm biệt",
          situation: "Kết thúc cuộc trò chuyện một cách tự nhiên.",
          en: `Alright, ${form}! Talk later.`,
          vi: `Thôi được, ${vi}! Nói chuyện sau nhé.`,
        },
      ];
    }

    // noun (default) + other POS
    return [
      {
        title: "1. Nói về đời sống hàng ngày",
        situation: "Bạn kể với bạn bè về thứ đang dùng / gặp trong ngày.",
        en: `I always keep ${art} ${form} in my bag, just in case.`,
        vi: `Mình luôn để ${vi} trong túi, phòng khi cần.`,
      },
      {
        title: "2. Hỏi hoặc nhờ giúp thực tế",
        situation: "Hỏi người khác trong tình huống gần gũi.",
        en: `Hey, can I borrow your ${form} for a second?`,
        vi: `Ê, cho mình mượn ${vi} một chút được không?`,
      },
      {
        title: "3. Miêu tả cho bạn nghe",
        situation: "Giải thích ngắn gọn khi kể chuyện.",
        en: `The ${form} was smaller than I expected, but it worked fine.`,
        vi: `${vi.charAt(0).toUpperCase()}${vi.slice(1)} nhỏ hơn mình nghĩ, nhưng dùng ổn.`,
      },
    ];
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
            <p class="ex-flash-hint">Mỗi từ có <strong>3 ngữ cảnh nói hàng ngày</strong> (có highlight từ mới) — học nghĩa và cách dùng khi nói chuyện. Đánh giá <strong>Chính xác</strong> / <strong>Không chính xác</strong>.</p>
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
      else root.insertAdjacentElement("afterend", section);
    } else {
      const hint = section.querySelector(".ex-flash-hint");
      if (hint) {
        hint.innerHTML =
          'Mỗi từ có <strong>3 ngữ cảnh nói hàng ngày</strong> (có highlight từ mới) — học nghĩa và cách dùng khi nói chuyện. Đánh giá <strong>Chính xác</strong> / <strong>Không chính xác</strong>.';
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

    const renderContextsHtml = (w, contexts) => {
      const items = contexts
        .map((c, i) => {
          const enHtml = highlightWordHtml(c.en, w.form);
          return `<article class="ex-flash-ctx">
            <h3 class="ex-flash-ctx-title">${escapeHtml(c.title)}</h3>
            <p class="ex-flash-ctx-sit"><span>Tình huống:</span> ${escapeHtml(c.situation)}</p>
            <p class="ex-flash-example-en">
              <span class="ex-flash-ctx-label">Câu:</span> ${enHtml}
              <button type="button" class="ex-flash-example-speak" data-speak-en="${escapeHtml(c.en)}" aria-label="Nghe ví dụ ${i + 1}">▶</button>
            </p>
            <p class="ex-flash-example-vi"><span class="ex-flash-ctx-label">Dịch:</span> ${escapeHtml(c.vi)}</p>
          </article>`;
        })
        .join("");
      return `<div class="ex-flash-example">
        <div class="ex-flash-example-label">Ví dụ · 3 ngữ cảnh nói</div>
        <div class="ex-flash-contexts">${items}</div>
      </div>`;
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
      const contexts = buildSpokenContexts(w);
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
                <p class="ex-flash-gloss"><em>${escapeHtml(w.form)}</em>${
                  pos ? ` · ${escapeHtml(pos)}` : ""
                }${ipa ? ` · ${escapeHtml(ipa)}` : ""}</p>
                ${renderContextsHtml(w, contexts)}
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
        flipped = on;
        card && card.classList.toggle("is-flipped", on);
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
