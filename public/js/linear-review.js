(() => {
  const body = document.body;
  const togVi = document.getElementById("togVi");
  if (togVi) {
    togVi.addEventListener("change", () => {
      body.classList.toggle("ex-show-vi", togVi.checked);
    });
  }

  /** Sync visible answer text when user changes vocab dropdown */
  const picks = document.querySelectorAll(".lr-word-pick");
  picks.forEach((sel) => {
    sel.addEventListener("change", () => {
      sel.classList.add("lr-word-pick--changed");
    });
  });

  const plainAnswer = (root) => {
    const clone = root.cloneNode(true);
    clone.querySelectorAll(".lr-tense-tag").forEach((n) => n.remove());
    clone.querySelectorAll(".lr-word-pick").forEach((sel) => {
      const span = document.createElement("span");
      span.className = "vocab";
      span.textContent = sel.value;
      sel.replaceWith(span);
    });
    clone.querySelectorAll("strong, em").forEach((n) => {
      n.replaceWith(document.createTextNode(n.textContent));
    });
    return clone.textContent.replace(/\s+/g, " ").trim();
  };

  const allAnswersText = () =>
    [...document.querySelectorAll(".lr-answer-text")]
      .map(plainAnswer)
      .filter(Boolean)
      .join("\n\n");

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
