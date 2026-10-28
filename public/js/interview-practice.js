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

  const VOICES = [
    { id: "en-US-AriaNeural", label: "Aria — US, nữ", short: "Aria" },
    { id: "en-US-GuyNeural", label: "Guy — US, nam", short: "Guy" },
    { id: "en-US-JennyNeural", label: "Jenny — US, nữ", short: "Jenny" },
    { id: "en-GB-SoniaNeural", label: "Sonia — UK, nữ", short: "Sonia" },
    { id: "en-GB-RyanNeural", label: "Ryan — UK, nam", short: "Ryan" },
    { id: "en-AU-NatashaNeural", label: "Natasha — AU, nữ", short: "Natasha" },
  ];

  const SPEEDS = [
    { rate: "-25%", pr: 0.75, label: "0.75×" },
    { rate: "+0%", pr: 1, label: "1×" },
    { rate: "+25%", pr: 1.25, label: "1.25×" },
    { rate: "+50%", pr: 1.5, label: "1.5×" },
  ];

  const MODE_META = {
    both: {
      banner: (r) =>
        `Lượt ${r}/3: nghe có chữ + dịch. Nghe hết bài, app tự tắt dịch rồi phát lượt kế.`,
    },
    text: {
      banner: (r) =>
        `Lượt ${r}/3: chỉ còn chữ tiếng Anh. Nghe hết bài, app tự ẩn chữ rồi phát lượt kế.`,
    },
    listen: {
      banner: (r) =>
        `Lượt ${r}/3: chỉ nghe. Chạm vào chữ mờ nếu cần xem lại nhanh.`,
    },
  };

  const els = {
    lessonGrid: document.getElementById("ivLessonGrid"),
    qList: document.getElementById("ivQuestionList"),
    practice: document.getElementById("ivPractice"),
    banner: document.getElementById("ivBanner"),
    karaoke: document.getElementById("ivKaraoke"),
    viBox: document.getElementById("ivViBox"),
    heading: document.getElementById("ivLessonHeading"),
    status: document.getElementById("ivStatus"),
    seek: document.getElementById("ivSeek"),
    time: document.getElementById("ivTime"),
    play: document.getElementById("ivPlay"),
    speed: document.getElementById("ivSpeed"),
    btnSentence: document.getElementById("ivBtnSentence"),
    btnLesson: document.getElementById("ivBtnLesson"),
    mute: document.getElementById("ivMute"),
    voiceToggle: document.getElementById("ivVoiceToggle"),
    voicePanel: document.getElementById("ivVoicePanel"),
    voiceA: document.getElementById("ivVoiceA"),
    voiceB: document.getElementById("ivVoiceB"),
    voiceLabel: document.getElementById("ivVoiceLabel"),
    audio: document.getElementById("ivAudio"),
  };

  const state = {
    lesson: null,
    textEn: "",
    textVi: "",
    words: [], // [{t,d,w, el}]
    wordIndex: -1,
    playing: false,
    loading: false,
    round: 1,
    mode: "both",
    autoMode: true,
    speedIdx: 1,
    repeatSentence: false,
    repeatLesson: false,
    focus: false,
    muted: false,
    voiceA: "en-US-AriaNeural",
    voiceB: "en-US-GuyNeural",
    audioUrl: null,
    cacheKey: "",
    raf: 0,
    sentenceRanges: [], // [{startWord, endWord, startTime, endTime, vi}]
  };

  const escapeHtml = (s) =>
    String(s)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");

  const fmt = (sec) => {
    const s = Math.max(0, Math.floor(sec || 0));
    return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
  };

  const shortVoice = (id) => VOICES.find((v) => v.id === id)?.short || id;

  const updateVoiceLabel = () => {
    if (!els.voiceLabel) return;
    els.voiceLabel.textContent = state.voiceB
      ? `${shortVoice(state.voiceA)} · ${shortVoice(state.voiceB)}`
      : shortVoice(state.voiceA);
  };

  const fillVoiceSelects = () => {
    if (!els.voiceA || !els.voiceB) return;
    els.voiceA.innerHTML = VOICES.map(
      (v) => `<option value="${v.id}">${v.label}</option>`
    ).join("");
    els.voiceB.innerHTML =
      `<option value="">Tắt</option>` +
      VOICES.map((v) => `<option value="${v.id}">${v.label}</option>`).join("");
    els.voiceA.value = state.voiceA;
    els.voiceB.value = state.voiceB;
    updateVoiceLabel();
  };

  const buildLessonText = (lesson) => {
    const viTitle = TITLE_VI[lesson.title] || lesson.title;
    const enParts = [`Lesson ${lesson.num}: ${lesson.title}`, ""];
    const viParts = [`Bài ${lesson.num}: ${viTitle}`, ""];
    const sentenceMeta = []; // parallel EN/VI blocks for VI box

    lesson.questions.forEach((q, qi) => {
      enParts.push(`${qi + 1}. ${q.q_en}`);
      viParts.push(`${qi + 1}. ${q.q_vi}`);
      sentenceMeta.push({ kind: "q", qi, en: q.q_en, vi: q.q_vi });
      q.lines.forEach((line) => {
        enParts.push(line.en);
        viParts.push(line.vi || "");
        sentenceMeta.push({ kind: "a", qi, en: line.en, vi: line.vi || "" });
      });
      enParts.push("");
      viParts.push("");
    });

    return {
      textEn: enParts.join("\n").trim(),
      textVi: viParts.join("\n").trim(),
      sentenceMeta,
      heading: `Lesson ${lesson.num}: ${lesson.title}`,
      viTitle: `Bài ${lesson.num}: ${viTitle}`,
    };
  };

  const tokenizeForDisplay = (text) => {
    // Keep whitespace/newlines; wrap word-like tokens
    const parts = [];
    const re = /([A-Za-z0-9]+(?:['’][A-Za-z0-9]+)?|[^\sA-Za-z0-9]+|\s+)/g;
    let m;
    while ((m = re.exec(text))) {
      const raw = m[0];
      if (/^[A-Za-z0-9]/.test(raw)) {
        parts.push({ type: "word", text: raw });
      } else {
        parts.push({ type: "other", text: raw });
      }
    }
    return parts;
  };

  const renderKaraokeShell = (textEn) => {
    if (!els.karaoke) return;
    const parts = tokenizeForDisplay(textEn);
    let html = "";
    parts.forEach((p) => {
      if (p.type === "word") {
        html += `<span class="iv-w" data-w="${escapeHtml(p.text)}">${escapeHtml(p.text)}</span>`;
      } else if (p.text.includes("\n")) {
        html += p.text.replaceAll("\n", "<br>");
      } else {
        html += escapeHtml(p.text);
      }
    });
    els.karaoke.innerHTML = html;
  };

  const mapWordsToSpans = (timelineWords) => {
    const spans = [...(els.karaoke?.querySelectorAll(".iv-w") || [])];
    const mapped = [];
    let cursor = 0;
    timelineWords.forEach((tw) => {
      const needle = String(tw.w || "").toLowerCase().replace(/[^\w']/g, "");
      let found = -1;
      for (let i = cursor; i < spans.length; i++) {
        const token = (spans[i].dataset.w || "")
          .toLowerCase()
          .replace(/[^\w']/g, "");
        if (token === needle || token.startsWith(needle) || needle.startsWith(token)) {
          found = i;
          break;
        }
      }
      if (found >= 0) {
        mapped.push({ ...tw, el: spans[found], spanIndex: found });
        cursor = found + 1;
      } else {
        mapped.push({ ...tw, el: null, spanIndex: -1 });
      }
    });
    return mapped;
  };

  const buildSentenceRanges = (mapped, sentenceMeta) => {
    // Approximate: each sentenceMeta.en maps to a contiguous span of timeline words
    const ranges = [];
    let searchFrom = 0;
    const hay = mapped.map((w) => String(w.w || "").toLowerCase()).join(" ");

    sentenceMeta.forEach((s) => {
      const tokens = String(s.en)
        .toLowerCase()
        .replace(/[^\w\s']/g, " ")
        .split(/\s+/)
        .filter(Boolean);
      if (!tokens.length) return;
      // find first token from searchFrom
      let start = -1;
      for (let i = searchFrom; i < mapped.length; i++) {
        const w = String(mapped[i].w || "")
          .toLowerCase()
          .replace(/[^\w']/g, "");
        if (w === tokens[0] || w.startsWith(tokens[0]) || tokens[0].startsWith(w)) {
          start = i;
          break;
        }
      }
      if (start < 0) return;
      let end = Math.min(mapped.length - 1, start + tokens.length - 1);
      // extend a bit if next words still in sentence
      for (let i = start; i < mapped.length && i < start + tokens.length + 2; i++) {
        end = i;
      }
      ranges.push({
        startWord: start,
        endWord: end,
        startTime: mapped[start].t,
        endTime: mapped[end].t + (mapped[end].d || 0),
        vi: s.vi,
        en: s.en,
        kind: s.kind,
      });
      searchFrom = end + 1;
    });
    state.sentenceRanges = ranges;
  };

  const setStatus = (msg, show = true) => {
    if (!els.status) return;
    els.status.hidden = !show;
    els.status.textContent = msg || "";
  };

  const applyMode = () => {
    if (!els.practice) return;
    els.practice.dataset.mode = state.mode;
    document.querySelectorAll(".iv-mode").forEach((btn) => {
      const on = btn.dataset.mode === state.mode;
      btn.classList.toggle("active", on);
      btn.setAttribute("aria-selected", on ? "true" : "false");
    });
    const meta = MODE_META[state.mode];
    if (els.banner && meta) els.banner.textContent = meta.banner(state.round);
    if (els.viBox) els.viBox.hidden = state.mode !== "both";
  };

  const modeForRound = (round) => (round === 1 ? "both" : round === 2 ? "text" : "listen");

  const highlightAt = (time) => {
    const words = state.words;
    if (!words.length) return;
    let idx = -1;
    for (let i = 0; i < words.length; i++) {
      const w = words[i];
      if (time + 0.02 >= w.t) idx = i;
      else break;
    }
    if (idx === state.wordIndex) {
      updateViBox(idx, time);
      return;
    }
    state.wordIndex = idx;
    words.forEach((w, i) => {
      if (!w.el) return;
      w.el.classList.remove("is-past", "is-active", "is-future");
      if (i < idx) w.el.classList.add("is-past");
      else if (i === idx) w.el.classList.add("is-active");
      else w.el.classList.add("is-future");
    });
    const active = words[idx]?.el;
    if (active) {
      active.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }
    updateViBox(idx, time);
  };

  const updateViBox = (wordIdx, time) => {
    if (!els.viBox || state.mode !== "both") return;
    const range =
      state.sentenceRanges.find(
        (r) => time >= r.startTime - 0.05 && time <= r.endTime + 0.15
      ) ||
      state.sentenceRanges.find(
        (r) => wordIdx >= r.startWord && wordIdx <= r.endWord
      );
    if (range?.vi) {
      els.viBox.textContent = range.vi;
      els.viBox.hidden = false;
    }
  };

  const updateProgress = () => {
    const a = els.audio;
    if (!a) return;
    const dur = a.duration && Number.isFinite(a.duration) ? a.duration : state.words.at(-1)
      ? state.words.at(-1).t + state.words.at(-1).d
      : 0;
    const cur = a.currentTime || 0;
    if (els.seek) {
      els.seek.max = String(dur || 1);
      els.seek.value = String(cur);
    }
    if (els.time) els.time.textContent = `${fmt(cur)} / ${fmt(dur)}`;
  };

  const tick = () => {
    if (!state.playing) return;
    const t = els.audio?.currentTime || 0;
    highlightAt(t);
    updateProgress();
    state.raf = requestAnimationFrame(tick);
  };

  const setPlayingUI = (on) => {
    state.playing = on;
    if (els.play) {
      els.play.textContent = on ? "❚❚" : "▶";
      els.play.setAttribute("aria-label", on ? "Pause" : "Play");
    }
  };

  const revokeAudio = () => {
    if (state.audioUrl) {
      URL.revokeObjectURL(state.audioUrl);
      state.audioUrl = null;
    }
  };

  const fetchTts = async (text) => {
    const key = `${state.voiceA}|${state.voiceB}|${SPEEDS[state.speedIdx].rate}|${text}`;
    if (key === state.cacheKey && els.audio?.src) return true;

    state.loading = true;
    setStatus("Đang tạo audio (Aria/Guy Neural)…");
    if (els.play) els.play.disabled = true;

    const body = new URLSearchParams({
      text,
      voice: state.voiceA,
      rate: SPEEDS[state.speedIdx].rate,
      timeline: "1",
    });
    if (state.voiceB) body.set("voice_b", state.voiceB);

    const res = await fetch("/api/tts", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });
    const data = await res.json();
    if (!res.ok || !data.ok) {
      throw new Error(data.error || "TTS failed");
    }

    const bin = Uint8Array.from(atob(data.audio), (c) => c.charCodeAt(0));
    revokeAudio();
    const url = URL.createObjectURL(new Blob([bin], { type: data.mime || "audio/mpeg" }));
    state.audioUrl = url;
    state.cacheKey = key;
    els.audio.src = url;
    els.audio.muted = state.muted;
    els.audio.playbackRate = 1; // rate baked into TTS request

    renderKaraokeShell(text);
    state.words = mapWordsToSpans(data.words || []);
    state.words.forEach((w) => w.el?.classList.add("is-future"));
    const built = buildLessonText(state.lesson);
    buildSentenceRanges(state.words, built.sentenceMeta);

    await new Promise((resolve, reject) => {
      const onReady = () => {
        cleanup();
        resolve();
      };
      const onErr = () => {
        cleanup();
        reject(new Error("Audio decode failed"));
      };
      const cleanup = () => {
        els.audio.removeEventListener("canplaythrough", onReady);
        els.audio.removeEventListener("error", onErr);
      };
      els.audio.addEventListener("canplaythrough", onReady, { once: true });
      els.audio.addEventListener("error", onErr, { once: true });
      els.audio.load();
    });

    state.loading = false;
    if (els.play) els.play.disabled = false;
    setStatus("", false);
    updateProgress();
    return true;
  };

  const playFrom = async (time = 0) => {
    if (!state.lesson) return;
    try {
      if (!els.audio.src || state.loading) {
        await fetchTts(state.textEn);
      }
      els.audio.currentTime = Math.max(0, time);
      els.audio.muted = state.muted;
      await els.audio.play();
      setPlayingUI(true);
      cancelAnimationFrame(state.raf);
      state.raf = requestAnimationFrame(tick);
    } catch (err) {
      setPlayingUI(false);
      setStatus(err.message || "Không phát được audio", true);
      if (els.play) els.play.disabled = false;
      state.loading = false;
    }
  };

  const pause = () => {
    els.audio?.pause();
    setPlayingUI(false);
    cancelAnimationFrame(state.raf);
    updateProgress();
  };

  const currentSentenceRange = () => {
    const t = els.audio?.currentTime || 0;
    return (
      state.sentenceRanges.find((r) => t >= r.startTime && t <= r.endTime + 0.2) ||
      state.sentenceRanges[0]
    );
  };

  const onEnded = () => {
    if (state.repeatSentence) {
      const r = currentSentenceRange();
      playFrom(r?.startTime || 0);
      return;
    }
    if (state.repeatLesson) {
      playFrom(0);
      return;
    }
    if (state.autoMode && state.round < 3) {
      state.round += 1;
      state.mode = modeForRound(state.round);
      applyMode();
      playFrom(0);
      return;
    }
    setPlayingUI(false);
    cancelAnimationFrame(state.raf);
    if (state.autoMode && state.round >= 3 && els.banner) {
      els.banner.textContent =
        "Xong 3 lượt. Bật Mute để luyện speaking (chữ vẫn chạy), hoặc Play để nghe lại.";
    }
    updateProgress();
  };

  const openPractice = async (lessonId) => {
    const lesson = DATA.lessons.find((l) => l.id === lessonId);
    if (!lesson || !els.practice) return;

    pause();
    revokeAudio();
    if (els.audio) els.audio.removeAttribute("src");
    state.cacheKey = "";
    state.lesson = lesson;
    state.wordIndex = -1;
    state.round = 1;
    state.mode = "both";
    state.autoMode = true;
    state.repeatSentence = false;
    state.repeatLesson = false;
    els.btnSentence?.classList.remove("active");
    els.btnLesson?.classList.remove("active");

    const built = buildLessonText(lesson);
    state.textEn = built.textEn;
    state.textVi = built.textVi;
    if (els.heading) els.heading.textContent = built.heading;
    if (els.viBox) {
      els.viBox.textContent = built.sentenceMeta[0]?.vi || built.viTitle;
      els.viBox.hidden = false;
    }

    els.practice.classList.add("open");
    els.practice.setAttribute("aria-hidden", "false");
    document.body.classList.add("iv-lock");
    applyMode();
    renderKaraokeShell(state.textEn);
    state.words = [];
    updateVoiceLabel();

    try {
      await fetchTts(state.textEn);
      await playFrom(0);
    } catch (err) {
      setStatus(err.message || "Lỗi TTS", true);
    }
  };

  const closePractice = () => {
    pause();
    revokeAudio();
    if (els.audio) els.audio.removeAttribute("src");
    state.cacheKey = "";
    els.practice?.classList.remove("open", "focus", "reveal-text");
    els.practice?.setAttribute("aria-hidden", "true");
    document.body.classList.remove("iv-lock");
    state.focus = false;
    els.voicePanel && (els.voicePanel.hidden = true);
  };

  const speakSnippet = async (text, preferB = false) => {
    // One-off listen for Q/A cards using same Neural voices
    try {
      const body = new URLSearchParams({
        text,
        voice: preferB && state.voiceB ? state.voiceB : state.voiceA,
        rate: SPEEDS[state.speedIdx].rate,
        timeline: "1",
      });
      const res = await fetch("/api/tts", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body,
      });
      const data = await res.json();
      if (!res.ok || !data.ok) throw new Error(data.error || "TTS failed");
      const bin = Uint8Array.from(atob(data.audio), (c) => c.charCodeAt(0));
      const url = URL.createObjectURL(new Blob([bin], { type: "audio/mpeg" }));
      const a = new Audio(url);
      a.onended = () => URL.revokeObjectURL(url);
      a.play();
    } catch (err) {
      console.warn(err);
    }
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

  // Audio events
  els.audio?.addEventListener("ended", onEnded);
  els.audio?.addEventListener("timeupdate", () => {
    if (!state.playing) {
      highlightAt(els.audio.currentTime || 0);
      updateProgress();
    }
  });

  document.addEventListener("click", (e) => {
    const t = e.target.closest(
      "[data-lesson],[data-open-lesson],[data-speak-q],[data-speak-a],.iv-mode,#ivClose,#ivFocus,#ivMute,#ivPlay,#ivBack5,#ivFwd5,#ivSpeed,#ivBtnSentence,#ivBtnLesson,#ivVoiceToggle,.iv-karaoke"
    );
    if (!t) return;

    if (t.matches("[data-lesson]") || t.matches("[data-open-lesson]")) {
      openPractice(t.dataset.lesson || t.dataset.openLesson);
      return;
    }
    if (t.matches("[data-speak-q]")) {
      const [lid, qi] = t.dataset.speakQ.split(":");
      const lesson = DATA.lessons.find((l) => l.id === lid);
      const q = lesson?.questions?.[Number(qi)];
      if (q) speakSnippet(q.q_en, false);
      return;
    }
    if (t.matches("[data-speak-a]")) {
      const [lid, qi] = t.dataset.speakA.split(":");
      const lesson = DATA.lessons.find((l) => l.id === lid);
      const q = lesson?.questions?.[Number(qi)];
      if (q) speakSnippet(q.lines.map((x) => x.en).join(" "), true);
      return;
    }
    if (t.id === "ivClose") return closePractice();
    if (t.id === "ivFocus") {
      state.focus = !state.focus;
      els.practice?.classList.toggle("focus", state.focus);
      return;
    }
    if (t.id === "ivMute") {
      state.muted = !state.muted;
      if (els.audio) els.audio.muted = state.muted;
      els.mute?.classList.toggle("active", state.muted);
      els.mute && (els.mute.textContent = state.muted ? "Unmute" : "Mute");
      // Keep highlighting: if muted mid-play, audio still runs with muted=true
      if (state.muted && !state.playing && els.audio?.src) {
        // Convenience: if paused, start muted playback so chữ vẫn chạy for speaking
        playFrom(els.audio.currentTime || 0);
      }
      return;
    }
    if (t.id === "ivVoiceToggle") {
      if (els.voicePanel) els.voicePanel.hidden = !els.voicePanel.hidden;
      return;
    }
    if (t.classList.contains("iv-mode")) {
      state.mode = t.dataset.mode;
      state.autoMode = false;
      applyMode();
      return;
    }
    if (t.id === "ivPlay") {
      if (state.playing) pause();
      else playFrom(els.audio?.currentTime || 0);
      return;
    }
    if (t.id === "ivBack5") {
      const next = Math.max(0, (els.audio?.currentTime || 0) - 5);
      if (state.playing) playFrom(next);
      else {
        els.audio.currentTime = next;
        highlightAt(next);
        updateProgress();
      }
      return;
    }
    if (t.id === "ivFwd5") {
      const dur = els.audio?.duration || 0;
      const next = Math.min(dur, (els.audio?.currentTime || 0) + 5);
      if (state.playing) playFrom(next);
      else {
        els.audio.currentTime = next;
        highlightAt(next);
        updateProgress();
      }
      return;
    }
    if (t.id === "ivSpeed") {
      state.speedIdx = (state.speedIdx + 1) % SPEEDS.length;
      els.speed.textContent = SPEEDS[state.speedIdx].label;
      // Rate is baked into Neural TTS — refetch
      const was = state.playing;
      const t0 = els.audio?.currentTime || 0;
      const ratio = t0 / (els.audio?.duration || 1);
      pause();
      state.cacheKey = "";
      fetchTts(state.textEn)
        .then(() => {
          const jump = ratio * (els.audio.duration || 0);
          if (was) playFrom(jump);
          else {
            els.audio.currentTime = jump;
            highlightAt(jump);
            updateProgress();
          }
        })
        .catch((err) => setStatus(err.message, true));
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
    if (t.classList.contains("iv-karaoke") && state.mode === "listen") {
      els.practice?.classList.toggle("reveal-text");
    }
  });

  els.seek?.addEventListener("input", () => {
    const t = Number(els.seek.value || 0);
    const was = state.playing;
    if (was) pause();
    els.audio.currentTime = t;
    highlightAt(t);
    updateProgress();
    if (was) playFrom(t);
  });

  const onVoiceChange = () => {
    state.voiceA = els.voiceA.value;
    state.voiceB = els.voiceB.value;
    updateVoiceLabel();
    if (!state.lesson) return;
    const was = state.playing;
    const t0 = els.audio?.currentTime || 0;
    const ratio = t0 / (els.audio?.duration || 1);
    pause();
    state.cacheKey = "";
    fetchTts(state.textEn)
      .then(() => {
        const jump = ratio * (els.audio.duration || 0);
        if (was) playFrom(jump);
        else {
          els.audio.currentTime = jump;
          highlightAt(jump);
          updateProgress();
        }
      })
      .catch((err) => setStatus(err.message, true));
  };
  els.voiceA?.addEventListener("change", onVoiceChange);
  els.voiceB?.addEventListener("change", onVoiceChange);

  document.addEventListener("keydown", (e) => {
    if (!els.practice?.classList.contains("open")) return;
    if (e.key === "Escape") closePractice();
    if (e.key === " ") {
      e.preventDefault();
      els.play?.click();
    }
    if (e.key === "m" || e.key === "M") els.mute?.click();
  });

  fillVoiceSelects();
  renderHub();

  const params = new URLSearchParams(location.search);
  const lessonParam = params.get("lesson");
  if (lessonParam) openPractice(lessonParam);
  else if (location.hash?.startsWith("#le-")) {
    document.getElementById(location.hash.slice(1))?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  }
})();
