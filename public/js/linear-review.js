(() => {
  const body = document.body;
  const togVi = document.getElementById("togVi");
  if (togVi) {
    togVi.addEventListener("change", () => {
      body.classList.toggle("ex-show-vi", togVi.checked);
    });
  }

  /** Fill {slot} placeholders in a chain example from dropdowns in the same chain */
  const fillChainTemplate = (template, chain) => {
    if (!template) return "";
    let out = template;
    chain.querySelectorAll(".lr-word-pick").forEach((sel) => {
      const slot = sel.dataset.slot;
      if (!slot) return;
      const word = sel.value;
      const mark = `<mark class="vocab">${word}</mark>`;
      out = out.split(`{${slot}}`).join(mark);
    });
    return out;
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
    });
  });

  initChainExamples();

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
})();
