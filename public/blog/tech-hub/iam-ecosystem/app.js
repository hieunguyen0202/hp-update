(() => {
  const slides = Array.from(document.querySelectorAll(".slide"));
  const progressBar = document.getElementById("progressBar");
  const currentEl = document.getElementById("currentSlide");
  const totalEl = document.getElementById("totalSlides");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");

  let index = 0;
  let animating = false;

  totalEl.textContent = String(slides.length);

  function revealAnims(slide) {
    const items = slide.querySelectorAll(".anim");
    items.forEach((el) => el.classList.remove("in"));
    items.forEach((el) => {
      const delay = Number(el.dataset.d || 0) * 90;
      window.setTimeout(() => el.classList.add("in"), delay + 40);
    });
  }

  function goTo(nextIndex) {
    if (animating) return;
    if (nextIndex < 0 || nextIndex >= slides.length || nextIndex === index) {
      updateChrome();
      return;
    }

    animating = true;
    const current = slides[index];
    const next = slides[nextIndex];

    current.classList.add("leaving");
    current.classList.remove("active");

    window.setTimeout(() => {
      current.classList.remove("leaving");
      index = nextIndex;
      next.classList.add("active");
      revealAnims(next);
      updateChrome();
      history.replaceState(null, "", `#${index + 1}`);
      animating = false;
    }, 220);
  }

  function updateChrome() {
    currentEl.textContent = String(index + 1);
    progressBar.style.width = `${((index + 1) / slides.length) * 100}%`;
    prevBtn.disabled = index === 0;
    nextBtn.disabled = index === slides.length - 1;
  }

  function next() { goTo(index + 1); }
  function prev() { goTo(index - 1); }

  prevBtn.addEventListener("click", prev);
  nextBtn.addEventListener("click", next);

  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight" || e.key === " " || e.key === "PageDown") {
      e.preventDefault();
      next();
    } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
      e.preventDefault();
      prev();
    } else if (e.key === "Home") {
      e.preventDefault();
      goTo(0);
    } else if (e.key === "End") {
      e.preventDefault();
      goTo(slides.length - 1);
    } else if (e.key.toLowerCase() === "f") {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen?.();
      } else {
        document.exitFullscreen?.();
      }
    }
  });

  let touchX = null;
  document.addEventListener("touchstart", (e) => {
    touchX = e.changedTouches[0].screenX;
  }, { passive: true });

  document.addEventListener("touchend", (e) => {
    if (touchX == null) return;
    const dx = e.changedTouches[0].screenX - touchX;
    if (Math.abs(dx) > 50) {
      if (dx < 0) next();
      else prev();
    }
    touchX = null;
  }, { passive: true });

  const fromHash = Number((location.hash || "").replace("#", "")) - 1;
  if (!Number.isNaN(fromHash) && fromHash >= 0 && fromHash < slides.length) {
    slides.forEach((s) => s.classList.remove("active"));
    index = fromHash;
    slides[index].classList.add("active");
  }

  revealAnims(slides[index]);
  updateChrome();
})();
