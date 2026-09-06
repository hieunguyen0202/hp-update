(() => {
  const body = document.body;
  const togVi = document.getElementById("togVi");
  if (togVi) {
    togVi.addEventListener("change", () => {
      body.classList.toggle("ex-show-vi", togVi.checked);
    });
  }

  /** Replace only the first `{slot}` so repeated slots map 1:1 to dropdown order */
  const replaceFirstPlaceholder = (text, slot, value) => {
    const token = `{${slot}}`;
    const i = text.indexOf(token);
    if (i < 0) return text;
    return text.slice(0, i) + value + text.slice(i + token.length);
  };

  /** Fill {slot} placeholders in a chain example from dropdowns in the same chain */
  const fillChainTemplate = (template, chain) => {
    if (!template) return "";
    let out = template;
    chain.querySelectorAll(".lr-word-pick").forEach((sel) => {
      const slot = sel.dataset.slot;
      if (!slot) return;
      const word = sel.value.trim();
      const mark =
        word && word !== "—"
          ? `<mark class="vocab">${word}</mark>`
          : "";
      out = replaceFirstPlaceholder(out, slot, mark);
    });
    return out.replace(/\s{2,}/g, " ").replace(/\s+([.,!?])/g, "$1").trim();
  };

  const updateChainExample = (chain) => {
    const enTpl = chain.dataset.exEn || "";
    const viTpl = chain.dataset.exVi || "";
    const enEl = chain.querySelector(".lr-chain-ex-text");
    const viEl = chain.querySelector(".lr-chain-ex-vi");
    if (enEl) enEl.innerHTML = fillChainTemplate(enTpl, chain);
    if (viEl) viEl.innerHTML = fillChainTemplate(viTpl, chain);
  };

  const initChainExamples = () => {
    document.querySelectorAll(".lr-chain[data-ex-en]").forEach(updateChainExample);
  };

  /** Sync visible answer text when user changes vocab dropdown */
  const picks = document.querySelectorAll(".lr-word-pick");
  picks.forEach((sel) => {
    sel.addEventListener("change", () => {
      sel.classList.add("lr-word-pick--changed");
      const chain = sel.closest(".lr-chain");
      if (chain) updateChainExample(chain);
      const answer = sel.closest(".lr-answer-text");
      if (answer) updateFoodAnswerTip(answer);
    });
  });

  const optionVi = (sel) => {
    const opt = sel.selectedOptions && sel.selectedOptions[0];
    if (!opt) return "";
    return (opt.getAttribute("data-vi") || opt.getAttribute("title") || "").trim();
  };

  const escapeRegExp = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

  /** Plain text from answer block — reads live dropdown values at copy time */
  const plainTextFromEl = (root) => {
    if (!root) return "";
    const liveSelects = [...root.querySelectorAll(".lr-word-pick")];
    const clone = root.cloneNode(true);
    clone.querySelectorAll(".lr-tense-tag").forEach((n) => n.remove());
    [...clone.querySelectorAll(".lr-word-pick")].forEach((sel, i) => {
      const span = document.createElement("span");
      span.textContent = liveSelects[i]?.value ?? sel.value;
      sel.replaceWith(span);
    });
    clone.querySelectorAll("strong, em").forEach((n) => {
      n.replaceWith(document.createTextNode(n.textContent));
    });
    return clone.textContent.replace(/\s+/g, " ").trim();
  };

  /** Rebuild whole-line VI tooltip from template or by swapping option meanings */
  const updateFoodAnswerTip = (answer) => {
    if (!answer) return;
    const selects = [...answer.querySelectorAll(".lr-word-pick")];
    const tpl = (answer.dataset.viTpl || "").trim();
    let tip = "";
    if (tpl) {
      tip = tpl;
      selects.forEach((sel) => {
        const slot = sel.dataset.slot;
        if (!slot) return;
        const vi = optionVi(sel) || sel.value.trim();
        tip = replaceFirstPlaceholder(tip, slot, vi);
      });
      tip = tip.replace(/\s{2,}/g, " ").replace(/\s+([.,!?])/g, "$1").trim();
    } else {
      tip = answer.getAttribute("data-tip") || answer.getAttribute("title") || "";
      selects.forEach((sel) => {
        const prev = (sel.dataset.activeVi || "").trim();
        const next = optionVi(sel);
        if (prev && next && prev !== next && tip) {
          const re = new RegExp(escapeRegExp(prev), "i");
          if (re.test(tip)) tip = tip.replace(re, next);
        }
        if (next) sel.dataset.activeVi = next;
      });
    }
    if (tip) {
      answer.setAttribute("data-tip", tip);
      answer.setAttribute("title", tip);
    }
    // Keep plain EN in sync with live dropdowns (scroll / copy helpers)
    const livePlain = plainTextFromEl(answer);
    if (livePlain) answer.dataset.plain = livePlain;
    selects.forEach((sel) => {
      const vi = optionVi(sel);
      if (vi) sel.dataset.activeVi = vi;
    });
  };

  const initFoodAnswerTips = () => {
    document.querySelectorAll(".lr-answer-text").forEach((answer) => {
      answer.querySelectorAll(".lr-word-pick").forEach((sel) => {
        const vi = optionVi(sel);
        if (vi) sel.dataset.activeVi = vi;
      });
      if (answer.dataset.viTpl) updateFoodAnswerTip(answer);
    });
  };

  initChainExamples();
  initFoodAnswerTips();

  const plainQuestion = (qa) => {
    const q = qa.querySelector(".ex-q");
    if (!q) return "";
    const clone = q.cloneNode(true);
    clone.querySelector(".ex-role")?.remove();
    return clone.textContent.replace(/\s+/g, " ").trim();
  };

  const allAnswersText = () => {
    const mock = document.getElementById("mockPassage");
    if (!mock) return "";

    const blocks = [];
    let lastPartTitle = "";

    mock.querySelectorAll(".ex-ielts-part").forEach((part) => {
      const partTitle =
        part.querySelector(".ex-ielts-part-title")?.textContent.trim() || "";

      if (part.dataset.part === "2") {
        const cue = part.querySelector(".ex-cue-title")?.textContent.trim();
        const ans = part.querySelector(".lr-answer-text");
        if (!cue || !ans) return;
        if (partTitle && partTitle !== lastPartTitle) {
          blocks.push(partTitle);
          lastPartTitle = partTitle;
        }
        blocks.push(cue);
        blocks.push(plainTextFromEl(ans));
        return;
      }

      part.querySelectorAll(".ex-qa").forEach((qa) => {
        const ans = qa.querySelector(".lr-answer-text");
        if (!ans) return;
        if (partTitle && partTitle !== lastPartTitle) {
          blocks.push(partTitle);
          lastPartTitle = partTitle;
        }
        const question = plainQuestion(qa);
        if (question) blocks.push(question);
        blocks.push(plainTextFromEl(ans));
      });
    });

    return blocks.filter(Boolean).join("\n\n");
  };

  const btnCopy = document.getElementById("btnCopyAnswer");
  if (btnCopy) {
    btnCopy.addEventListener("click", async () => {
      const text = allAnswersText();
      if (!text) return;
      try {
        await navigator.clipboard.writeText(text);
        btnCopy.textContent = "Copied!";
        setTimeout(() => {
          btnCopy.textContent = "Copy current answers";
        }, 2000);
      } catch {
        window.prompt("Copy your answers:", text);
      }
    });
  }

  /** Smooth scroll for in-page TOC */
  document.querySelectorAll('.lr-toc a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href").slice(1);
      const el = document.getElementById(id);
      if (el) {
        e.preventDefault();
        el.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  /** Scroll read teleprompter — built from mock Q&A + dropdown cloze */
  const escapeHtml = (s) =>
    String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");

  const initMockScrollRead = () => {
    const mock = document.getElementById("mockPassage");
    const track = document.getElementById("scrollTrack");
    const viewport = document.getElementById("scrollViewport");
    if (!mock || !track || !viewport) return;

    let slots = {};
    try {
      slots = JSON.parse(document.getElementById("lrWordSlots").textContent);
    } catch {
      /* no slots */
    }

    const speedRange = document.getElementById("scrollSpeed");
    const speedVal = document.getElementById("scrollSpeedVal");
    const hintMode = document.getElementById("scrollHintMode");
    const revealTog = document.getElementById("scrollReveal");
    const btnPlay = document.getElementById("btnScrollPlay");
    const btnPause = document.getElementById("btnScrollPause");
    const btnRestart = document.getElementById("btnScrollRestart");

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

    const metaForPick = (slotId, form) => {
      const opts = slots[slotId] || [];
      return opts.find((o) => o.form === form) || { form, vi: "" };
    };

    const attachBlank = (form, meta, mode, reveal) => {
      const blank = document.createElement("span");
      blank.className = "scroll-blank";
      blank.dataset.answer = form;
      blank.title = "Click to peek answer";

      const setContent = (revealed) => {
        if (revealed) {
          blank.classList.add("is-revealed");
          blank.innerHTML = `<span class="scroll-blank-answer">${escapeHtml(form)}</span>`;
        } else {
          blank.classList.remove("is-revealed");
          blank.innerHTML = `<span class="scroll-blank-gap">______</span><span class="scroll-blank-hint">${escapeHtml(
            hintFor(meta, mode)
          )}</span>`;
        }
      };

      setContent(reveal);
      blank.addEventListener("click", (e) => {
        e.preventDefault();
        setContent(!blank.classList.contains("is-revealed"));
      });
      return blank;
    };

    const answerToHtml = (answerEl, mode, reveal) => {
      const liveSelects = [...answerEl.querySelectorAll(".lr-word-pick")];
      const clone = answerEl.cloneNode(true);
      clone.querySelectorAll(".lr-tense-tag, .ex-a-label").forEach((n) => n.remove());
      [...clone.querySelectorAll(".lr-word-pick")].forEach((sel, i) => {
        const form = liveSelects[i]?.value ?? sel.value;
        const slotId = sel.dataset.slot || "";
        const meta = metaForPick(slotId, form);
        sel.replaceWith(attachBlank(form, meta, mode, reveal));
      });
      clone.querySelectorAll("strong, em").forEach((n) => {
        n.replaceWith(document.createTextNode(n.textContent));
      });
      return clone.innerHTML.replace(/\s+/g, " ").trim();
    };

    const buildTrack = () => {
      const mode = hintMode ? hintMode.value : "vi";
      const reveal = !!(revealTog && revealTog.checked);
      const blocks = [];
      let lastPartTitle = "";

      mock.querySelectorAll(".ex-ielts-part").forEach((part) => {
        const partTitle =
          part.querySelector(".ex-ielts-part-title")?.textContent.trim() || "";

        if (partTitle && partTitle !== lastPartTitle) {
          blocks.push(
            `<p class="scroll-line scroll-line--part">${escapeHtml(partTitle)}</p>`
          );
          lastPartTitle = partTitle;
        }

        if (part.dataset.part === "2") {
          const cue = part.querySelector(".ex-cue-title")?.textContent.trim();
          const ans = part.querySelector(".lr-answer-text");
          if (cue) {
            blocks.push(
              `<p class="scroll-line scroll-line--q">${escapeHtml(cue)}</p>`
            );
          }
          if (ans) {
            blocks.push(
              `<p class="scroll-line scroll-line--a">${answerToHtml(ans, mode, reveal)}</p>`
            );
          }
          return;
        }

        part.querySelectorAll(".ex-qa").forEach((qa) => {
          const q = plainQuestion(qa);
          const ans = qa.querySelector(".lr-answer-text");
          if (q) {
            blocks.push(
              `<p class="scroll-line scroll-line--q">${escapeHtml(q)}</p>`
            );
          }
          if (ans) {
            blocks.push(
              `<p class="scroll-line scroll-line--a">${answerToHtml(ans, mode, reveal)}</p>`
            );
          }
        });
      });

      track.innerHTML = `<div class="scroll-pad scroll-pad--top"></div>${blocks.join(
        ""
      )}<div class="scroll-pad scroll-pad--bottom"></div>`;

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
    mock.querySelectorAll(".lr-word-pick").forEach((sel) => {
      sel.addEventListener("change", rebuild);
    });
  };

  initMockScrollRead();

  /** Per-lesson Scroll read (Review Exercise 2) — source = practice cards / Food examples */
  const initLessonScrollReads = () => {
    let slots = {};
    try {
      slots = JSON.parse(document.getElementById("lrWordSlots").textContent);
    } catch {
      /* no slots */
    }

    const hintFor = (meta, mode) => {
      const vi = (meta && meta.vi) || "";
      const ipa = (meta && meta.ipa) || "";
      if (mode === "struct") return "…";
      if (mode === "ipa") return ipa ? `/${ipa}/` : "…";
      if (mode === "both") {
        if (vi && ipa) return `${vi} · /${ipa}/`;
        return vi || (ipa ? `/${ipa}/` : "…");
      }
      return vi || (ipa ? `/${ipa}/` : "…");
    };

    const metaForPick = (slotId, form) => {
      const opts = slots[slotId] || [];
      return opts.find((o) => o.form === form) || { form, vi: "", ipa: "" };
    };

    const attachBlank = (form, meta, mode, reveal) => {
      const blank = document.createElement("span");
      blank.className = "scroll-blank";
      blank.dataset.answer = form;
      blank.title = "Click to peek answer";
      const setContent = (revealed) => {
        if (revealed) {
          blank.classList.add("is-revealed");
          blank.innerHTML = `<span class="scroll-blank-answer">${escapeHtml(form)}</span>`;
        } else {
          blank.classList.remove("is-revealed");
          blank.innerHTML = `<span class="scroll-blank-gap">______</span><span class="scroll-blank-hint">${escapeHtml(
            hintFor(meta, mode)
          )}</span>`;
        }
      };
      setContent(reveal);
      blank.addEventListener("click", (e) => {
        e.preventDefault();
        setContent(!blank.classList.contains("is-revealed"));
      });
      return blank;
    };

    const answerToHtml = (answerEl, mode, reveal) => {
      const liveSelects = [...answerEl.querySelectorAll(".lr-word-pick")];
      const clone = answerEl.cloneNode(true);
      clone.querySelectorAll(".lr-tense-tag, .ex-a-label, .lr-mm-tag-yes, .lr-mm-tag-no, .lr-practice-tag").forEach((n) => n.remove());
      [...clone.querySelectorAll(".lr-word-pick")].forEach((sel, i) => {
        const form = liveSelects[i]?.value ?? sel.value;
        const slotId = sel.dataset.slot || "";
        const meta = metaForPick(slotId, form);
        sel.replaceWith(attachBlank(form, meta, mode, reveal));
      });
      clone.querySelectorAll(".lr-cloze").forEach((el) => {
        const form = el.dataset.en || el.textContent.trim();
        const meta = { form, vi: el.dataset.vi || "", ipa: el.dataset.ipa || "" };
        el.replaceWith(attachBlank(form, meta, mode, reveal));
      });
      clone.querySelectorAll("strong, em").forEach((n) => {
        n.replaceWith(document.createTextNode(n.textContent));
      });
      return clone.innerHTML.replace(/\s+/g, " ").trim();
    };

    /** Split full IPA string `/wɛl, aɪ …/` into per-word tokens */
    const tokenizeIpa = (ipaFull) => {
      let s = (ipaFull || "").trim();
      if (!s) return [];
      s = s.replace(/^\/+/, "").replace(/\/+$/, "").trim();
      return s.split(/\s+/).filter(Boolean);
    };

    /**
     * Keep English HTML (blanks + words) and add yellow IPA above each token.
     * Generator turns hyphens into spaces before eng_to_ipa, so "mouth-watering"
     * becomes two IPA tokens — consume that many per EN word.
     * Part 2 often has a standalone em dash "—" as its own IPA token; consume it
     * when EN is punctuation-only. Periods/commas glued onto words stay 1:1.
     */
    const wrapHtmlWithWordIpa = (html, ipaFull) => {
      const tokens = tokenizeIpa(ipaFull);
      if (!tokens.length) return html;
      const box = document.createElement("div");
      box.innerHTML = html;
      let ti = 0;
      const peekIpa = () => tokens[ti] || "";
      const takeIpa = () => tokens[ti++] || "";

      /** EN core without leading/trailing punctuation (keep internal ' and -). */
      const enCore = (enText) =>
        String(enText || "")
          .replace(/^[^A-Za-z0-9'’\-]+/, "")
          .replace(/[^A-Za-z0-9'’\-]+$/, "");

      const isPunctOnly = (enText) => {
        const t = String(enText || "").trim();
        return t.length > 0 && !/[A-Za-z0-9]/.test(t);
      };

      /** Standalone IPA punct (em dash, etc.) — not phoneme letters. */
      const isIpaPunctOnly = (tok) =>
        /^[\s.,;:!?\-—–…/]+$/.test(String(tok || "").trim());

      /**
       * How many space-separated IPA tokens this EN word should consume.
       * Matches `_ipa_from_en` (hyphen → space; takeaway → take away).
       */
      const ipaSlotsForEn = (enText) => {
        if (isPunctOnly(enText)) return 0;
        const core = enCore(enText);
        if (!core) return 0;
        const lower = core.toLowerCase();
        // Pre-normalisations applied in scripts/_gen_food_review_exercise.py
        if (lower === "takeaway") return 2;
        const hyphenParts = core.split("-").filter(Boolean);
        return Math.max(1, hyphenParts.length);
      };

      const takeIpaForEn = (enText) => {
        const n = ipaSlotsForEn(enText);
        if (n <= 0) return "";
        const parts = [];
        for (let i = 0; i < n; i++) {
          const t = takeIpa();
          if (t) parts.push(t);
        }
        return parts.join(" ");
      };

      /** EN "—" / ";" alone: eat matching IPA punct token so the stream stays synced. */
      const syncPunctOnly = (enText) => {
        if (isIpaPunctOnly(peekIpa())) takeIpa();
      };

      const makeWord = (enText, ipaText) => {
        const span = document.createElement("span");
        span.className = "scroll-word";
        if (ipaText) {
          const ipaEl = document.createElement("span");
          ipaEl.className = "scroll-word-ipa";
          ipaEl.setAttribute("lang", "en-fonipa");
          ipaEl.setAttribute("aria-hidden", "true");
          ipaEl.textContent = ipaText;
          span.appendChild(ipaEl);
        }
        const enEl = document.createElement("span");
        enEl.className = "scroll-word-en";
        enEl.textContent = enText;
        span.appendChild(enEl);
        return span;
      };

      const wrapTextNode = (textNode) => {
        const raw = textNode.textContent;
        if (!raw || !raw.trim()) return;
        const parts = raw.split(/(\s+)/);
        const frag = document.createDocumentFragment();
        parts.forEach((part) => {
          if (!part) return;
          if (/^\s+$/.test(part)) {
            frag.appendChild(document.createTextNode(part));
            return;
          }
          if (isPunctOnly(part)) {
            syncPunctOnly(part);
            frag.appendChild(document.createTextNode(part));
            return;
          }
          frag.appendChild(makeWord(part, takeIpaForEn(part)));
        });
        textNode.parentNode.replaceChild(frag, textNode);
      };

      const visit = (node) => {
        if (node.nodeType === Node.TEXT_NODE) {
          wrapTextNode(node);
          return;
        }
        if (node.nodeType !== Node.ELEMENT_NODE) return;
        if (node.classList.contains("scroll-blank")) {
          const form = (node.dataset.answer || "").trim();
          const words = form ? form.split(/\s+/).filter(Boolean) : [""];
          const ipas = words.map((w) => {
            if (isPunctOnly(w)) {
              syncPunctOnly(w);
              return "";
            }
            return takeIpaForEn(w);
          });
          if (node.classList.contains("is-revealed") && words.length > 1) {
            const frag = document.createDocumentFragment();
            words.forEach((w, i) => {
              if (i) frag.appendChild(document.createTextNode(" "));
              if (isPunctOnly(w)) {
                frag.appendChild(document.createTextNode(w));
                return;
              }
              frag.appendChild(makeWord(w, ipas[i] || ""));
            });
            node.replaceWith(frag);
            return;
          }
          const ipaJoined = ipas.filter(Boolean).join(" ");
          if (ipaJoined) {
            const ipaEl = document.createElement("span");
            ipaEl.className = "scroll-word-ipa";
            ipaEl.setAttribute("lang", "en-fonipa");
            ipaEl.setAttribute("aria-hidden", "true");
            ipaEl.textContent = ipaJoined;
            node.classList.add("scroll-word");
            node.insertBefore(ipaEl, node.firstChild);
          }
          return;
        }
        if (node.classList.contains("scroll-word-ipa")) return;
        if (node.classList.contains("scroll-word")) return;
        [...node.childNodes].forEach(visit);
      };

      [...box.childNodes].forEach(visit);
      return box.innerHTML;
    };

    /**
     * Mark rising ↗ / falling ↘ on clause & sentence boundaries for practice.
     * Heuristic (Oxford rules): mid-clause (,;— / before but|because|…) → rise;
     * sentence end (.!?) → fall; last unmarked word → fall.
     */
    const wrapHtmlWithIntonation = (html) => {
      const box = document.createElement("div");
      box.innerHTML = html;
      const words = [];
      // Only strong clause starters (avoid false rise on "a while", "x and y", …)
      const RISE_NEXT =
        /^(but|because|although|though|whereas|which)$/i;

      const markEl = (el, tone) => {
        if (!el || el.classList.contains("scroll-tone")) return;
        el.classList.add("scroll-tone", `scroll-tone--${tone}`);
        if (!el.querySelector(":scope > .scroll-tone-mark")) {
          const m = document.createElement("span");
          m.className = `scroll-tone-mark scroll-tone-mark--${tone}`;
          m.setAttribute("aria-hidden", "true");
          m.textContent = tone === "rise" ? "↗" : "↘";
          el.appendChild(m);
        }
      };

      const pushToneWord = (frag, text, trail, lex) => {
        const span = document.createElement("span");
        span.className = lex
          ? "scroll-tone-word scroll-tone-word--lex"
          : "scroll-tone-word";
        span.textContent = text;
        frag.appendChild(span);
        words.push({ el: span, trail: trail || "" });
        return span;
      };

      const wrapTextNode = (textNode) => {
        const raw = textNode.textContent;
        if (!raw) return;
        const parts = raw.split(/(\s+)/);
        const frag = document.createDocumentFragment();
        parts.forEach((part) => {
          if (!part) return;
          if (/^\s+$/.test(part)) {
            frag.appendChild(document.createTextNode(part));
            return;
          }
          if (/^[.,;:!?…—–]+$/.test(part)) {
            if (words.length) words[words.length - 1].trail += part;
            frag.appendChild(document.createTextNode(part));
            return;
          }
          const m = part.match(
            /^([\p{L}\p{N}'’\u00C0-\u024F\-]+)([.,;:!?…—–]*)$/u
          );
          if (m) {
            pushToneWord(frag, m[1], m[2] || "", false);
            if (m[2]) frag.appendChild(document.createTextNode(m[2]));
            return;
          }
          pushToneWord(frag, part, "", false);
        });
        textNode.parentNode.replaceChild(frag, textNode);
      };

      const expandRevealedBlank = (node) => {
        const form = (node.dataset.answer || node.textContent || "").trim();
        if (!form) {
          words.push({ el: node, trail: "" });
          return;
        }
        const frag = document.createDocumentFragment();
        const parts = form.split(/(\s+)/);
        parts.forEach((part) => {
          if (!part) return;
          if (/^\s+$/.test(part)) {
            frag.appendChild(document.createTextNode(part));
            return;
          }
          if (/^[.,;:!?…—–]+$/.test(part)) {
            if (words.length) words[words.length - 1].trail += part;
            frag.appendChild(document.createTextNode(part));
            return;
          }
          const m = part.match(
            /^([\p{L}\p{N}'’\u00C0-\u024F\-]+)([.,;:!?…—–]*)$/u
          );
          if (m) {
            pushToneWord(frag, m[1], m[2] || "", true);
            if (m[2]) frag.appendChild(document.createTextNode(m[2]));
            return;
          }
          pushToneWord(frag, part, "", true);
        });
        node.replaceWith(frag);
      };

      const visit = (node) => {
        if (node.nodeType === Node.TEXT_NODE) {
          wrapTextNode(node);
          return;
        }
        if (node.nodeType !== Node.ELEMENT_NODE) return;
        if (node.classList.contains("scroll-tone-mark")) return;
        if (node.classList.contains("scroll-blank")) {
          // Revealed multi-word blanks must become per-word units — otherwise the
          // tone mark sits on a column-flex blank and looks mid-phrase when wrapped.
          if (node.classList.contains("is-revealed")) {
            expandRevealedBlank(node);
            return;
          }
          const ans = (node.dataset.answer || "").trim();
          const m = ans.match(/[.,;:!?…—–]+$/);
          words.push({ el: node, trail: m ? m[0] : "" });
          return;
        }
        if (node.classList.contains("scroll-word")) {
          const enOnly = node.querySelector(".scroll-word-en")
            ? node.querySelector(".scroll-word-en").textContent.trim()
            : (node.textContent || "").trim();
          const m = enOnly.match(/[.,;:!?…—–]+$/);
          words.push({ el: node, trail: m ? m[0] : "" });
          return;
        }
        [...node.childNodes].forEach(visit);
      };

      [...box.childNodes].forEach(visit);

      for (let i = 0; i < words.length; i++) {
        const trail = words[i].trail || "";
        const nextText = (
          words[i + 1]?.el?.querySelector?.(".scroll-word-en")?.textContent ||
          words[i + 1]?.el?.textContent ||
          ""
        )
          .replace(/\s+/g, " ")
          .trim();
        const nextCore = nextText.replace(/^[^A-Za-z]+/, "").split(/\s+/)[0] || "";

        if (/[.!?…]/.test(trail)) markEl(words[i].el, "fall");
        else if (/[,;:—–]/.test(trail)) markEl(words[i].el, "rise");
        else if (nextCore && RISE_NEXT.test(nextCore)) markEl(words[i].el, "rise");
      }

      if (words.length) {
        const last = words[words.length - 1];
        if (!last.el.classList.contains("scroll-tone")) markEl(last.el, "fall");
      }

      return box.innerHTML;
    };

    /**
     * Mark consonant→vowel links in red with "_" bridges (Oxford "How to Link Words").
     * Single-pass per word so a token that is both link-start and link-end
     * (e.g. it in makes_it_a) is not painted twice and scrambled.
     */
    const wrapHtmlWithLinking = (html) => {
      const box = document.createElement("div");
      box.innerHTML = html;
      const words = [];

      const wordCore = (raw) =>
        String(raw || "")
          .replace(/^[^A-Za-z'’]+/, "")
          .replace(/[^A-Za-z'’]+$/, "");

      const startsWithVowelSound = (raw) => {
        const w = wordCore(raw).toLowerCase();
        if (!w) return false;
        if (/^(uni|use|used|useful|usual|euro|one|once|u\.s)/.test(w)) return false;
        if (/^(hour|honest|honou?r|heir|herb)/.test(w)) return true;
        return /^[aeiou]/.test(w);
      };

      const endsWithConsonantSound = (raw) => {
        const w = wordCore(raw);
        if (!w) return false;
        const lower = w.toLowerCase();
        if (/'(ve|re|ll|d|m|s)$/i.test(w)) return true;
        if (
          /[bcdfghjklmnpqrstvwxyz]e$/i.test(lower) &&
          !/(ee|ie|oe|ue)$/i.test(lower)
        ) {
          return true;
        }
        return /[bcdfghjklmnpqrstvwxyz]$/i.test(lower);
      };

      const shouldLinkCV = (a, b) =>
        endsWithConsonantSound(a) && startsWithVowelSound(b);

      const endLinkLen = (raw) => {
        const w = wordCore(raw);
        if (!w) return 0;
        if (/[A-Za-z]'s$/i.test(w) || (/s$/i.test(w) && /'/i.test(w))) return 1;
        if (/'(ve|re|ll|d|m)$/i.test(w)) return 1;
        const lower = w.toLowerCase();
        if (
          /[bcdfghjklmnpqrstvwxyz]e$/i.test(lower) &&
          !/(ee|ie|oe|ue)$/i.test(lower)
        ) {
          return /se$/i.test(w) ? 2 : 1;
        }
        if (/[bcdfghjklmnpqrstvwxyz]$/i.test(w)) return 1;
        return 0;
      };

      const startLinkLen = (raw) => {
        const w = wordCore(raw);
        if (!w) return 0;
        if (/^(an|a)$/i.test(w)) return w.length;
        if (/^I'(ve|m|d|ll)$/i.test(w) || /^(I've|I'm|I'd|I'll)$/i.test(w)) {
          return w.length;
        }
        return 1;
      };

      const plainFromEl = (el) => {
        if (el.classList?.contains("scroll-blank")) {
          return (el.dataset.answer || el.textContent || "").trim();
        }
        const en = el.querySelector?.(".scroll-word-en");
        const src = en || el;
        const c = src.cloneNode(true);
        c.querySelectorAll(
          ".scroll-tone-mark, .scroll-link, .scroll-link-us, .scroll-word-ipa"
        ).forEach((n) => n.remove());
        return c.textContent.trim();
      };

      const textHost = (el) => {
        if (el.classList?.contains("scroll-blank")) return el;
        return el.querySelector?.(".scroll-word-en") || el;
      };

      const redSpan = (text) => {
        const span = document.createElement("span");
        span.className = "scroll-link";
        span.textContent = text;
        return span;
      };

      /** Rebuild host once: [startRed][middle][endRed] + keep tone marks. */
      const paintWordOnce = (el, startN, endN) => {
        const host = textHost(el);
        const toneMarks = [
          ...host.querySelectorAll(":scope > .scroll-tone-mark"),
        ];
        const raw = plainFromEl(el);
        if (!raw) return;

        const core = wordCore(raw);
        const idx = raw.toLowerCase().indexOf(core.toLowerCase());
        if (idx < 0) return;
        const before = raw.slice(0, idx);
        const word = raw.slice(idx, idx + core.length);
        const after = raw.slice(idx + core.length);

        let sN = Math.max(0, Math.min(startN || 0, word.length));
        let eN = Math.max(0, Math.min(endN || 0, word.length - sN));
        // If start+end would overlap, prefer end mark (rarer for short words)
        if (sN + eN > word.length) {
          eN = Math.max(0, word.length - sN);
        }

        const start = word.slice(0, sN);
        const mid = word.slice(sN, word.length - eN);
        const end = word.slice(word.length - eN);

        const frag = document.createDocumentFragment();
        if (before) frag.appendChild(document.createTextNode(before));
        if (start) frag.appendChild(redSpan(start));
        if (mid) frag.appendChild(document.createTextNode(mid));
        if (end) frag.appendChild(redSpan(end));
        if (after) frag.appendChild(document.createTextNode(after));
        toneMarks.forEach((m) => frag.appendChild(m));
        host.innerHTML = "";
        host.appendChild(frag);
        el.classList.add("scroll-link-word");
      };

      const insertBridge = (leftEl) => {
        if (!leftEl?.parentNode) return;
        if (
          leftEl.nextSibling?.classList?.contains?.("scroll-link-us")
        ) {
          return;
        }
        const us = document.createElement("span");
        us.className = "scroll-link-us";
        us.setAttribute("aria-hidden", "true");
        us.textContent = "_";
        let n = leftEl.nextSibling;
        while (n && n.nodeType === Node.TEXT_NODE && !/\S/.test(n.textContent)) {
          const next = n.nextSibling;
          n.remove();
          n = next;
        }
        if (n && n.nodeType === Node.TEXT_NODE) {
          n.textContent = n.textContent.replace(/^\s+/, "");
        }
        leftEl.parentNode.insertBefore(us, leftEl.nextSibling);
      };

      const wrapTextNode = (textNode) => {
        const raw = textNode.textContent;
        if (!raw || !raw.trim()) return;
        const parts = raw.split(/(\s+)/);
        const frag = document.createDocumentFragment();
        parts.forEach((part) => {
          if (!part) return;
          if (/^\s+$/.test(part)) {
            frag.appendChild(document.createTextNode(part));
            return;
          }
          if (/^[.,;:!?…—–]+$/.test(part)) {
            frag.appendChild(document.createTextNode(part));
            return;
          }
          const span = document.createElement("span");
          span.className = "scroll-link-word";
          span.textContent = part;
          frag.appendChild(span);
          words.push(span);
        });
        textNode.parentNode.replaceChild(frag, textNode);
      };

      const visit = (node) => {
        if (node.nodeType === Node.TEXT_NODE) {
          wrapTextNode(node);
          return;
        }
        if (node.nodeType !== Node.ELEMENT_NODE) return;
        if (
          node.classList.contains("scroll-tone-mark") ||
          node.classList.contains("scroll-link") ||
          node.classList.contains("scroll-link-us")
        ) {
          return;
        }
        if (node.classList.contains("scroll-blank")) {
          words.push(node);
          return;
        }
        if (
          node.classList.contains("scroll-word") ||
          node.classList.contains("scroll-tone-word") ||
          node.classList.contains("scroll-link-word")
        ) {
          words.push(node);
          return;
        }
        [...node.childNodes].forEach(visit);
      };

      [...box.childNodes].forEach(visit);

      const plains = words.map(plainFromEl);
      const startN = words.map(() => 0);
      const endN = words.map(() => 0);
      const bridgeAfter = words.map(() => false);

      for (let i = 0; i < words.length - 1; i++) {
        if (!shouldLinkCV(plains[i], plains[i + 1])) continue;
        endN[i] = endLinkLen(plains[i]);
        startN[i + 1] = startLinkLen(plains[i + 1]);
        bridgeAfter[i] = true;
      }

      words.forEach((el, i) => {
        if (startN[i] || endN[i]) paintWordOnce(el, startN[i], endN[i]);
      });
      words.forEach((el, i) => {
        if (bridgeAfter[i]) insertBridge(el);
      });

      return box.innerHTML;
    };

    const plainFromAnswer = (answerEl) => {
      if (answerEl.dataset.plain) return answerEl.dataset.plain;
      const liveSelects = [...answerEl.querySelectorAll(".lr-word-pick")];
      const clone = answerEl.cloneNode(true);
      clone.querySelectorAll(".lr-mm-tag-yes, .lr-mm-tag-no, .lr-practice-tag").forEach((n) => n.remove());
      [...clone.querySelectorAll(".lr-word-pick")].forEach((sel, i) => {
        const span = document.createElement("span");
        span.textContent = liveSelects[i]?.value ?? sel.value;
        sel.replaceWith(span);
      });
      return clone.textContent.replace(/\s+/g, " ").trim();
    };

    document.querySelectorAll(".lr-lesson-scroll").forEach((root) => {
      const source = document.querySelector(root.dataset.scrollSource || "");
      const track = root.querySelector(".ex-scroll-track");
      const viewport = root.querySelector(".ex-scroll-viewport");
      if (!source || !track || !viewport) return;

      const speedRange = root.querySelector(".js-scroll-speed");
      const speedVal = root.querySelector(".js-scroll-speed-val");
      const hintMode = root.querySelector(".js-scroll-hint");
      const revealTog = root.querySelector(".js-scroll-reveal");
      const showIpaTog = root.querySelector(".js-scroll-show-ipa");
      const showIpaOverTog = root.querySelector(".js-scroll-show-ipa-over");
      const showIntonationTog = root.querySelector(".js-scroll-show-intonation");
      const showLinkingTog = root.querySelector(".js-scroll-show-linking");
      const toneLegend = root.querySelector(".ex-scroll-tone-legend");
      const linkLegend = root.querySelector(".ex-scroll-link-legend");
      const btnPlay = root.querySelector(".js-scroll-play");
      const btnPause = root.querySelector(".js-scroll-pause");
      const btnRestart = root.querySelector(".js-scroll-restart");
      const btnCopy = root.querySelector(".js-scroll-copy");

      let playing = false;
      let offset = 0;
      let raf = 0;
      let lastTs = 0;
      let pxPerSec = speedRange ? Number(speedRange.value) : 32;

      const buildTrack = () => {
        const mode = hintMode ? hintMode.value : "vi";
        const reveal = !!(revealTog && revealTog.checked);
        const showIpa = !!(showIpaTog && showIpaTog.checked);
        const showIpaOver = !!(showIpaOverTog && showIpaOverTog.checked);
        const showIntonation = !!(showIntonationTog && showIntonationTog.checked);
        const showLinking = !!(showLinkingTog && showLinkingTog.checked);
        if (toneLegend) toneLegend.hidden = !showIntonation;
        if (linkLegend) linkLegend.hidden = !showLinking;
        root.classList.toggle("is-intonation", showIntonation);
        root.classList.toggle("is-linking", showLinking);
        const blocks = [];

        const resolveIpa = (ans, qaEl) =>
          (
            (ans && ans.dataset.ipaFull) ||
            (qaEl && qaEl.dataset.ipaFull) ||
            ""
          ).trim();

        const pushAnswer = (ans, qaEl) => {
          if (!ans) return;
          const ipa = resolveIpa(ans, qaEl);
          if (showIpa && !showIpaOver) {
            blocks.push(
              `<p class="scroll-line scroll-line--a scroll-line--a-ipa">${escapeHtml(
                ipa || plainFromAnswer(ans)
              )}</p>`
            );
            return;
          }
          let html = answerToHtml(ans, mode, reveal);
          if (showIpaOver && ipa) {
            html = wrapHtmlWithWordIpa(html, ipa);
          }
          if (showIntonation) {
            html = wrapHtmlWithIntonation(html);
          }
          if (showLinking) {
            html = wrapHtmlWithLinking(html);
          }
          const overlayClass =
            showIpaOver && ipa ? " scroll-line--a-overlay" : "";
          const toneClass = showIntonation ? " scroll-line--a-tone" : "";
          const linkClass = showLinking ? " scroll-line--a-link" : "";
          blocks.push(
            `<p class="scroll-line scroll-line--a${overlayClass}${toneClass}${linkClass}">${html}</p>`
          );
        };

        // Lesson 16 · Part 2: cue card + 5 labeled sections (no .lr-scroll-qa)
        source.querySelectorAll(".lr-p2-card").forEach((card) => {
          const cue =
            card.querySelector(".lr-cue-title") ||
            card.querySelector(".lr-food-ex-q");
          const qText = cue ? cue.textContent.replace(/\s+/g, " ").trim() : "";
          if (qText) {
            blocks.push(
              `<p class="scroll-line scroll-line--q">${escapeHtml(qText)}</p>`
            );
          }
          card.querySelectorAll(".lr-p2-sec .lr-answer-text").forEach((ans) => {
            pushAnswer(ans, null);
          });
        });

        source.querySelectorAll(".lr-scroll-qa").forEach((qa) => {
          // Skip if already covered via Part 2 card walk
          if (qa.closest(".lr-p2-card")) return;
          const cardQ = qa.closest(".lr-food-ex-card")?.querySelector(".lr-food-ex-q");
          const qEl =
            qa.querySelector(".lr-scroll-q") ||
            qa.querySelector(".lr-practice-q") ||
            cardQ;
          const ans =
            qa.querySelector(".lr-answer-text") ||
            qa.querySelector(".lr-practice-flow");
          if (!ans) return;
          // English question only — never append Thích / Không thích
          let qText = "";
          if (cardQ) qText = cardQ.textContent.replace(/\s+/g, " ").trim();
          else if (qEl) qText = qEl.textContent.replace(/\s+/g, " ").trim();
          if (qText) {
            blocks.push(`<p class="scroll-line scroll-line--q">${escapeHtml(qText)}</p>`);
          }
          pushAnswer(ans, qa);
        });

        track.innerHTML = `<div class="scroll-pad scroll-pad--top"></div>${blocks.join(
          ""
        )}<div class="scroll-pad scroll-pad--bottom"></div>`;
        const topPad = track.querySelector(".scroll-pad--top");
        const bottomPad = track.querySelector(".scroll-pad--bottom");
        if (topPad) topPad.style.height = `${Math.max(40, viewport.clientHeight * 0.42)}px`;
        if (bottomPad) bottomPad.style.height = `${Math.max(40, viewport.clientHeight * 0.55)}px`;
      };

      const applyTransform = () => {
        track.style.transform = `translate3d(0, ${-offset}px, 0)`;
      };
      const maxOffset = () =>
        Math.max(0, track.scrollHeight - viewport.clientHeight);

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

      const copyText = () => {
        const parts = [];
        source.querySelectorAll(".lr-p2-card").forEach((card) => {
          const cue =
            card.querySelector(".lr-cue-title") ||
            card.querySelector(".lr-food-ex-q");
          const qText = cue ? cue.textContent.replace(/\s+/g, " ").trim() : "";
          if (qText) parts.push(qText);
          card.querySelectorAll(".lr-p2-sec .lr-answer-text").forEach((ans) => {
            parts.push(plainFromAnswer(ans));
          });
        });
        source.querySelectorAll(".lr-scroll-qa").forEach((qa) => {
          if (qa.closest(".lr-p2-card")) return;
          const cardQ = qa.closest(".lr-food-ex-card")?.querySelector(".lr-food-ex-q");
          const ans =
            qa.querySelector(".lr-answer-text") ||
            qa.querySelector(".lr-practice-flow");
          if (!ans) return;
          // Clean English only — no Thích/Không thích, no IPA, no Vietnamese
          const qText = cardQ
            ? cardQ.textContent.replace(/\s+/g, " ").trim()
            : "";
          if (qText) parts.push(qText);
          parts.push(plainFromAnswer(ans));
        });
        return parts.filter(Boolean).join("\n\n");
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
      showIpaTog &&
        showIpaTog.addEventListener("change", () => {
          if (showIpaTog.checked && showIpaOverTog) showIpaOverTog.checked = false;
          rebuild();
        });
      showIpaOverTog &&
        showIpaOverTog.addEventListener("change", () => {
          if (showIpaOverTog.checked && showIpaTog) showIpaTog.checked = false;
          rebuild();
        });
      showIntonationTog &&
        showIntonationTog.addEventListener("change", rebuild);
      showLinkingTog && showLinkingTog.addEventListener("change", rebuild);
      source.querySelectorAll(".lr-word-pick").forEach((sel) => {
        sel.addEventListener("change", rebuild);
      });
      if (btnCopy) {
        btnCopy.addEventListener("click", async () => {
          const text = copyText();
          if (!text) return;
          try {
            await navigator.clipboard.writeText(text);
            btnCopy.textContent = "Copied!";
            setTimeout(() => {
              btnCopy.textContent = "Copy for NaturalReader";
            }, 2000);
          } catch {
            window.prompt("Copy for NaturalReader:", text);
          }
        });
      }
    });
  };

  initLessonScrollReads();

  /** Collapse / expand each Lesson article (default collapsed; open via click or #hash) */
  const initLessonCollapse = () => {
    const articles = [...document.querySelectorAll(".lr-core-lesson")];
    if (!articles.length) return;

    const setOpen = (article, open) => {
      article.classList.toggle("is-open", open);
      article.classList.toggle("is-collapsed", !open);
      const head = article.querySelector(".lr-core-lesson-head");
      if (head) head.setAttribute("aria-expanded", open ? "true" : "false");
    };

    articles.forEach((article) => {
      const head = article.querySelector(".lr-core-lesson-head");
      if (!head || article.querySelector(".lr-core-lesson-body")) return;

      const body = document.createElement("div");
      body.className = "lr-core-lesson-body";
      while (head.nextSibling) body.appendChild(head.nextSibling);
      article.appendChild(body);

      if (!head.querySelector(".lr-core-lesson-chevron")) {
        const chev = document.createElement("span");
        chev.className = "lr-core-lesson-chevron";
        chev.setAttribute("aria-hidden", "true");
        head.appendChild(chev);
      }
      head.setAttribute("role", "button");
      head.tabIndex = 0;
      head.setAttribute("aria-controls", article.id || "");

      const toggle = () => setOpen(article, !article.classList.contains("is-open"));
      head.addEventListener("click", (e) => {
        if (e.target.closest("a, button, input, select, label")) return;
        toggle();
      });
      head.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          toggle();
        }
      });

      setOpen(article, false);
    });

    const openFromHash = () => {
      const id = (location.hash || "").replace(/^#/, "");
      if (!id) return;
      const el = document.getElementById(id);
      if (!el) return;
      const article =
        el.closest(".lr-core-lesson") ||
        (el.classList.contains("lr-core-lesson") ? el : null);
      if (article) setOpen(article, true);
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    };
    openFromHash();
    window.addEventListener("hashchange", openFromHash);
  };

  initLessonCollapse();

  /** Horizontal mind map: SVG cubic bezier from measured node boxes */
  const initMindmaps = () => {
    document.querySelectorAll(".lr-mmap").forEach((wrap) => {
      const board = wrap.querySelector(".lr-mmap-board");
      const svg = wrap.querySelector(".lr-mmap-svg");
      const root = wrap.querySelector('[data-mmap-node="root"]');
      if (!board || !svg || !root) return;

      const NS = "http://www.w3.org/2000/svg";

      const pt = (el, side) => {
        const a = el.getBoundingClientRect();
        const b = board.getBoundingClientRect();
        const y = a.top + a.height / 2 - b.top;
        const x =
          side === "left"
            ? a.left - b.left
            : side === "right"
              ? a.right - b.left
              : a.left + a.width / 2 - b.left;
        return { x, y };
      };

      const cubic = (a, b) => {
        const dx = (b.x - a.x) * 0.52;
        return `M ${a.x} ${a.y} C ${a.x + dx} ${a.y}, ${b.x - dx} ${b.y}, ${b.x} ${b.y}`;
      };

      const pathEl = (d, color, width) => {
        const p = document.createElementNS(NS, "path");
        p.setAttribute("d", d);
        p.setAttribute("fill", "none");
        p.setAttribute("stroke", color);
        p.setAttribute("stroke-width", String(width));
        p.setAttribute("stroke-linecap", "round");
        p.setAttribute("opacity", "0.92");
        return p;
      };

      const draw = () => {
        const w = board.scrollWidth;
        const h = board.scrollHeight;
        svg.setAttribute("viewBox", `0 0 ${w} ${h}`);
        svg.setAttribute("width", String(w));
        svg.setAttribute("height", String(h));
        svg.replaceChildren();

        wrap.querySelectorAll(".lr-mmap-branch").forEach((branch) => {
          const left = branch.closest(".lr-mmap-col--left");
          const color =
            getComputedStyle(branch).getPropertyValue("--mmap-c").trim() ||
            "#7dd3fc";
          const tense = branch.querySelector('[data-mmap-node="tense"]');
          if (!tense) return;

          const fromRoot = left ? pt(root, "left") : pt(root, "right");
          const toTense = left ? pt(tense, "right") : pt(tense, "left");
          svg.appendChild(pathEl(cubic(fromRoot, toTense), color, 2.2));

          const tenseOut = left ? pt(tense, "left") : pt(tense, "right");
          branch.querySelectorAll(".lr-mmap-group").forEach((group) => {
            const fork = group.querySelector('[data-mmap-node="fork"]');
            if (!fork) return;
            const toFork = left ? pt(fork, "right") : pt(fork, "left");
            svg.appendChild(pathEl(cubic(tenseOut, toFork), color, 1.7));

            const forkOut = left ? pt(fork, "left") : pt(fork, "right");
            group.querySelectorAll('[data-mmap-node="leaf"]').forEach((leaf) => {
              const toLeaf = left ? pt(leaf, "right") : pt(leaf, "left");
              svg.appendChild(pathEl(cubic(forkOut, toLeaf), color, 1.35));
            });
          });
        });
      };

      const schedule = () => requestAnimationFrame(draw);
      schedule();
      if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(schedule);
      }
      window.addEventListener("resize", schedule);
      new ResizeObserver(schedule).observe(board);
      const shell = document.querySelector(".docs-shell");
      if (shell) {
        new MutationObserver(schedule).observe(shell, {
          attributes: true,
          attributeFilter: ["class"],
        });
      }
    });
  };

  initMindmaps();
})();
