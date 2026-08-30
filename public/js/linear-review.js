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
})();
