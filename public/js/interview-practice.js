(() => {
  const DATA = window.INTERVIEW_DATA;
  if (!DATA?.lessons?.length) return;

  const TITLE_VI = {
    "Tell me about yourself": "Giới thiệu về bản thân",
    "Why do you want to work here?": "Vì sao muốn làm ở đây?",
    "Describe a challenging bug you fixed": "Bug khó đã fix",
    "How do you handle tight deadlines?": "Xử lý deadline gấp",
    "Tell me about a disagreement with a teammate": "Bất đồng với teammate",
    "How do you keep your skills up to date?": "Cập nhật kỹ năng",
    "What's your ideal team and work environment?": "Team & môi trường lý tưởng",
    "How do you prioritize multiple projects?": "Ưu tiên nhiều project",
    "What are your strengths and weaknesses?": "Điểm mạnh / điểm yếu",
    "Tell me about a project you're proud of": "Project tự hào",
    "How do you explain technical issues to non-technical people?": "Giải thích kỹ thuật cho non-tech",
    "What are your salary expectations?": "Expectation lương",
    "Explain your approach in a live coding interview": "Approach live coding",
    "Design a URL shortener": "Design URL shortener",
    "Do you have any questions for us?": "Câu hỏi ngược lại",
    "A recruiter screening call": "Recruiter screening call",
  };

  const MODE_META = {
    both: {
      label: "Chữ + dịch",
      hint: "Hiện chữ tiếng Anh và bản dịch.",
      banner: (r) =>
        `Lượt ${r}/3: nghe có chữ + dịch. Nghe hết bài, app tự tắt dịch rồi phát lượt kế.`,
    },
    text: {
      label: "Chỉ chữ",
      hint: "Ẩn dịch — chỉ còn tiếng Anh.",
      banner: (r) =>
        `Lượt ${r}/3: chỉ còn chữ tiếng Anh. Nghe hết bài, app tự ẩn chữ rồi phát lượt kế.`,
    },
    listen: {
      label: "Chỉ nghe",
      hint: "Ẩn chữ — luyện tới khi không cần sub.",
      banner: (r) =>
        `Lượt ${r}/3: chỉ nghe. Chạm vào đoạn chữ mờ nếu cần xem lại nhanh.`,
    },
  };

  const SPEEDS = [0.75, 1, 1.25, 1.5];
  const WPM = 145;

  const els = {
    lessonGrid: document.getElementById("ivLessonGrid"),
    qList: document.getElementById("ivQuestionList"),
    practice: document.getElementById("ivPractice"),
    banner: document.getElementById("ivBanner"),
    lessonPill: document.getElementById("ivLessonPill"),
    script: document.getElementById("ivScript"),
    seek: document.getElementById("ivSeek"),
    time: document.getElementById("ivTime"),
    play: document.getElementById("ivPlay"),
    speed: document.getElementById("ivSpeed"),
    btnSentence: document.getElementById("ivBtnSentence"),
    btnLesson: document.getElementById("ivBtnLesson"),
  };

  const state = {
    lesson: null,
    turns: [],
    index: 0,
    playing: false,
    round: 1,
    mode: "both",
    autoMode: true,
    speedIdx: 1,
    repeatSentence: false,
    repeatLesson: false,
    focus: false,
    tick: null,
    startedAt: 0,
    turnStartedAt: 0,
    elapsedBefore: 0,
  };

  const fmt = (sec) => {
    const s = Math.max(0, Math.floor(sec || 0));
    const m = Math.floor(s / 60);
    const r = s % 60;
    return `${m}:${String(r).padStart(2, "0")}`;
  };

  const estimateSec = (text) => {
    const words = String(text || "").trim().split(/\s+/).filter(Boolean).length;
    return Math.max(1.4, (words / WPM) * 60);
  };

  const totalDuration = () =>
    state.turns.reduce((n, t) => n + estimateSec(t.en) / SPEEDS[state.speedIdx], 0);

  const elapsedToIndex = (idx) => {
    let n = 0;
    for (let i = 0; i < idx; i++) n += estimateSec(state.turns[i].en) / SPEEDS[state.speedIdx];
    return n;
  };

  const pickVoice = (preferFemale) => {
    const voices = window.speechSynthesis?.getVoices?.() || [];
    const en = voices.filter((v) => /^en(-|_)/i.test(v.lang) || /english/i.test(v.name));
    if (!en.length) return null;
    const scored = en.map((v) => {
      let score = 0;
      if (/US|United States|en-US/i.test(`${v.lang} ${v.name}`)) score += 3;
      if (/GB|UK|en-GB/i.test(`${v.lang} ${v.name}`)) score += 1;
      if (preferFemale && /female|aria|samantha|jenny|zira|susan|karen|moira/i.test(v.name)) score += 4;
      if (!preferFemale && /male|guy|daniel|alex|david|fred|tom|google uk english male/i.test(v.name)) score += 4;
      return { v, score };
    });
    scored.sort((a, b) => b.score - a.score);
    return scored[0]?.v || en[0];
  };

  const buildTurns = (lesson) => {
    const turns = [];
    lesson.questions.forEach((q, qi) => {
      turns.push({
        kind: "q",
        qIndex: qi,
        who: "Interviewer",
        en: q.q_en,
        vi: q.q_vi,
        label: `${qi + 1}. ${q.q_en}`,
      });
      q.lines.forEach((line) => {
        turns.push({
          kind: "a",
          qIndex: qi,
          who: "Candidate",
          en: line.en,
          vi: line.vi,
        });
      });
    });
    return turns;
  };

  const stopSpeech = () => {
    try {
      window.speechSynthesis?.cancel();
    } catch (_) {}
    if (state.tick) {
      clearInterval(state.tick);
      state.tick = null;
    }
  };

  const setPlayingUI = (on) => {
    state.playing = on;
    if (els.play) els.play.textContent = on ? "❚❚" : "▶";
    if (els.play) els.play.setAttribute("aria-label", on ? "Pause" : "Play");
  };

  const updateProgress = () => {
    const total = totalDuration() || 1;
    let cur = elapsedToIndex(state.index);
    if (state.playing) {
      cur += (performance.now() - state.turnStartedAt) / 1000;
    } else {
      cur += state.elapsedBefore;
    }
    cur = Math.min(total, Math.max(0, cur));
    if (els.seek) {
      els.seek.max = String(total);
      els.seek.value = String(cur);
    }
    if (els.time) els.time.textContent = `${fmt(cur)} / ${fmt(total)}`;
  };

  const highlight = () => {
    const nodes = els.script?.querySelectorAll(".iv-turn") || [];
    nodes.forEach((node, i) => {
      node.classList.toggle("active", i === state.index);
      if (i === state.index) node.scrollIntoView({ block: "nearest", behavior: "smooth" });
    });
  };

  const renderScript = () => {
    if (!els.script) return;
    els.script.innerHTML = state.turns
      .map(
        (t, i) => `
      <div class="iv-turn${i === state.index ? " active" : ""}" data-i="${i}">
        <div class="iv-turn__who">${t.who}${t.kind === "q" ? ` · Q${t.qIndex + 1}` : ""}</div>
        <div class="iv-turn__en">${escapeHtml(t.en)}</div>
        <div class="iv-turn__vi">${escapeHtml(t.vi || "")}</div>
      </div>`
      )
      .join("");
  };

  const escapeHtml = (s) =>
    String(s)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");

  const applyMode = () => {
    if (!els.practice) return;
    els.practice.dataset.mode = state.mode;
    document.querySelectorAll(".iv-mode").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.mode === state.mode);
    });
    const meta = MODE_META[state.mode];
    if (els.banner && meta) els.banner.textContent = meta.banner(state.round);
  };

  const modeForRound = (round) => (round === 1 ? "both" : round === 2 ? "text" : "listen");

  const speakCurrent = () => {
    if (!window.speechSynthesis || !state.turns.length) return;
    stopSpeech();
    const turn = state.turns[state.index];
    if (!turn) return;

    const u = new SpeechSynthesisUtterance(turn.en);
    u.rate = SPEEDS[state.speedIdx];
    u.pitch = turn.kind === "q" ? 1.05 : 0.95;
    const voice = pickVoice(turn.kind === "q");
    if (voice) u.voice = voice;

    state.turnStartedAt = performance.now();
    state.elapsedBefore = 0;
    setPlayingUI(true);
    highlight();
    updateProgress();
    state.tick = setInterval(updateProgress, 200);

    u.onend = () => {
      if (state.tick) {
        clearInterval(state.tick);
        state.tick = null;
      }
      if (state.repeatSentence) {
        speakCurrent();
        return;
      }
      if (state.index >= state.turns.length - 1) {
        onLessonEnd();
        return;
      }
      state.index += 1;
      speakCurrent();
    };
    u.onerror = () => setPlayingUI(false);
    window.speechSynthesis.speak(u);
  };

  const onLessonEnd = () => {
    setPlayingUI(false);
    updateProgress();
    if (state.repeatLesson) {
      state.index = 0;
      speakCurrent();
      return;
    }
    if (state.autoMode && state.round < 3) {
      state.round += 1;
      state.mode = modeForRound(state.round);
      state.index = 0;
      applyMode();
      speakCurrent();
      return;
    }
    if (state.autoMode && state.round >= 3) {
      if (els.banner) {
        els.banner.textContent =
          "Xong 3 lượt. Bạn có thể bấm Play để luyện lại, hoặc Tắt luyện để về danh sách bài.";
      }
    }
  };

  const openPractice = (lessonId) => {
    const lesson = DATA.lessons.find((l) => l.id === lessonId);
    if (!lesson || !els.practice) return;
    state.lesson = lesson;
    state.turns = buildTurns(lesson);
    state.index = 0;
    state.round = 1;
    state.mode = "both";
    state.autoMode = true;
    state.repeatSentence = false;
    state.repeatLesson = false;
    state.elapsedBefore = 0;
    els.practice.classList.add("open");
    els.practice.setAttribute("aria-hidden", "false");
    document.body.classList.add("iv-lock");
    if (els.lessonPill) {
      const vi = TITLE_VI[lesson.title] || lesson.title;
      els.lessonPill.textContent = `Bài ${lesson.num}: ${vi}`;
    }
    renderScript();
    applyMode();
    updateProgress();
    els.btnSentence?.classList.toggle("active", false);
    els.btnLesson?.classList.toggle("active", false);
    // Warm voices then autoplay shortly
    window.speechSynthesis?.getVoices?.();
    setTimeout(() => speakCurrent(), 250);
  };

  const closePractice = () => {
    stopSpeech();
    setPlayingUI(false);
    els.practice?.classList.remove("open", "focus", "reveal-text");
    els.practice?.setAttribute("aria-hidden", "true");
    document.body.classList.remove("iv-lock");
    state.focus = false;
  };

  const renderHub = () => {
    if (els.lessonGrid) {
      els.lessonGrid.innerHTML = DATA.lessons
        .map((l) => {
          const vi = TITLE_VI[l.title] || "";
          return `
          <button type="button" class="iv-lesson-card" data-lesson="${l.id}">
            <div class="iv-lesson-card__top">
              <span class="iv-lesson-card__num">${String(l.num).padStart(2, "0")}</span>
              <span class="iv-lesson-card__cta">Luyện nghe →</span>
            </div>
            <h3>${escapeHtml(l.title)}</h3>
            <p>${escapeHtml(vi)} · ${l.questions.length} câu hỏi · đáp án mẫu + dịch</p>
          </button>`;
        })
        .join("");
    }

    if (els.qList) {
      const blocks = [];
      DATA.lessons.forEach((l) => {
        blocks.push(
          `<h3 id="${l.id}" style="margin:28px 0 10px;color:var(--accent);font-family:var(--mono);font-size:0.95rem;">${String(l.num).padStart(2, "0")}. ${escapeHtml(l.title)}</h3>`
        );
        l.questions.forEach((q, qi) => {
          const lines = q.lines
            .map(
              (line) => `
            <div class="iv-line">
              <div class="iv-line__en">${escapeHtml(line.en)}</div>
              <div class="iv-line__vi">${escapeHtml(line.vi || "")}</div>
            </div>`
            )
            .join("");
          blocks.push(`
            <details class="iv-q" id="${q.slug}">
              <summary>
                <div class="iv-q__meta"><span>Q${qi + 1}</span><span>${l.id}</span></div>
                <div class="iv-q__en">${escapeHtml(q.q_en)}</div>
                <div class="iv-q__vi">${escapeHtml(q.q_vi || "")}</div>
              </summary>
              <div class="iv-q__body">
                <div class="iv-q__actions">
                  <button type="button" class="iv-btn" data-speak-q="${l.id}:${qi}">Nghe câu hỏi</button>
                  <button type="button" class="iv-btn primary" data-speak-a="${l.id}:${qi}">Nghe đáp án mẫu</button>
                  <button type="button" class="iv-btn" data-open-lesson="${l.id}">Luyện cả bài</button>
                </div>
                ${lines}
              </div>
            </details>`);
        });
      });
      els.qList.innerHTML = blocks.join("");
    }
  };

  const speakText = (text, preferFemale = false) => {
    if (!window.speechSynthesis) return;
    stopSpeech();
    const u = new SpeechSynthesisUtterance(text);
    u.rate = SPEEDS[state.speedIdx];
    const voice = pickVoice(preferFemale);
    if (voice) u.voice = voice;
    window.speechSynthesis.speak(u);
  };

  const speakAnswer = (lessonId, qIndex) => {
    const lesson = DATA.lessons.find((l) => l.id === lessonId);
    const q = lesson?.questions?.[qIndex];
    if (!q) return;
    const text = q.lines.map((x) => x.en).join(" ");
    speakText(text, false);
  };

  // Events
  document.addEventListener("click", (e) => {
    const t = e.target.closest("[data-lesson],[data-open-lesson],[data-speak-q],[data-speak-a],.iv-mode,#ivClose,#ivFocus,#ivPlay,#ivBack5,#ivFwd5,#ivSpeed,#ivBtnSentence,#ivBtnLesson,.iv-turn");
    if (!t) return;

    if (t.matches("[data-lesson]") || t.matches("[data-open-lesson]")) {
      openPractice(t.dataset.lesson || t.dataset.openLesson);
      return;
    }
    if (t.matches("[data-speak-q]")) {
      const [lid, qi] = t.dataset.speakQ.split(":");
      const lesson = DATA.lessons.find((l) => l.id === lid);
      const q = lesson?.questions?.[Number(qi)];
      if (q) speakText(q.q_en, true);
      return;
    }
    if (t.matches("[data-speak-a]")) {
      const [lid, qi] = t.dataset.speakA.split(":");
      speakAnswer(lid, Number(qi));
      return;
    }
    if (t.id === "ivClose") {
      closePractice();
      return;
    }
    if (t.id === "ivFocus") {
      state.focus = !state.focus;
      els.practice?.classList.toggle("focus", state.focus);
      return;
    }
    if (t.classList.contains("iv-mode")) {
      state.mode = t.dataset.mode;
      state.autoMode = false;
      applyMode();
      return;
    }
    if (t.id === "ivPlay") {
      if (state.playing) {
        state.elapsedBefore += (performance.now() - state.turnStartedAt) / 1000;
        stopSpeech();
        setPlayingUI(false);
        updateProgress();
      } else {
        speakCurrent();
      }
      return;
    }
    if (t.id === "ivBack5") {
      const was = state.playing;
      stopSpeech();
      state.index = Math.max(0, state.index - 1);
      state.elapsedBefore = 0;
      highlight();
      updateProgress();
      if (was) speakCurrent();
      return;
    }
    if (t.id === "ivFwd5") {
      const was = state.playing;
      stopSpeech();
      state.index = Math.min(state.turns.length - 1, state.index + 1);
      state.elapsedBefore = 0;
      highlight();
      updateProgress();
      if (was) speakCurrent();
      return;
    }
    if (t.id === "ivSpeed") {
      state.speedIdx = (state.speedIdx + 1) % SPEEDS.length;
      els.speed.textContent = `${SPEEDS[state.speedIdx]}x`;
      updateProgress();
      if (state.playing) speakCurrent();
      return;
    }
    if (t.id === "ivBtnSentence") {
      state.repeatSentence = !state.repeatSentence;
      if (state.repeatSentence) state.repeatLesson = false;
      els.btnSentence.classList.toggle("active", state.repeatSentence);
      els.btnLesson.classList.toggle("active", false);
      return;
    }
    if (t.id === "ivBtnLesson") {
      state.repeatLesson = !state.repeatLesson;
      if (state.repeatLesson) state.repeatSentence = false;
      els.btnLesson.classList.toggle("active", state.repeatLesson);
      els.btnSentence.classList.toggle("active", false);
      return;
    }
    if (t.classList.contains("iv-turn") && state.mode === "listen") {
      els.practice?.classList.toggle("reveal-text");
    }
  });

  els.seek?.addEventListener("input", () => {
    const target = Number(els.seek.value || 0);
    let acc = 0;
    let idx = 0;
    for (let i = 0; i < state.turns.length; i++) {
      const d = estimateSec(state.turns[i].en) / SPEEDS[state.speedIdx];
      if (acc + d >= target) {
        idx = i;
        break;
      }
      acc += d;
      idx = i;
    }
    const was = state.playing;
    stopSpeech();
    state.index = idx;
    state.elapsedBefore = Math.max(0, target - elapsedToIndex(idx));
    highlight();
    updateProgress();
    if (was) speakCurrent();
  });

  document.addEventListener("keydown", (e) => {
    if (!els.practice?.classList.contains("open")) return;
    if (e.key === "Escape") closePractice();
    if (e.key === " ") {
      e.preventDefault();
      els.play?.click();
    }
  });

  // Chrome loads voices async
  window.speechSynthesis?.addEventListener?.("voiceschanged", () => {});

  renderHub();

  // Deep-link: ?lesson=le-1 or #le-1 / #slug
  const params = new URLSearchParams(location.search);
  const lessonParam = params.get("lesson");
  if (lessonParam) openPractice(lessonParam);
  else if (location.hash?.startsWith("#le-")) {
    const id = location.hash.slice(1);
    const node = document.getElementById(id);
    node?.scrollIntoView({ behavior: "smooth", block: "start" });
  }
})();
