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
      const word = sel.value.trim();
      const mark =
        word && word !== "—"
          ? `<mark class="vocab">${word}</mark>`
          : "";
      out = out.split(`{${slot}}`).join(mark);
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
        const blocks = [];

        source.querySelectorAll(".lr-scroll-qa").forEach((qa) => {
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
          blocks.push(
            `<p class="scroll-line scroll-line--a">${answerToHtml(ans, mode, reveal)}</p>`
          );
          if (showIpa) {
            const ipa = qa.dataset.ipaFull || "";
            if (ipa) {
              blocks.push(
                `<p class="scroll-line scroll-line--ipa">${escapeHtml(ipa)}</p>`
              );
            }
          }
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
        source.querySelectorAll(".lr-scroll-qa").forEach((qa) => {
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
      showIpaTog && showIpaTog.addEventListener("change", rebuild);
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
