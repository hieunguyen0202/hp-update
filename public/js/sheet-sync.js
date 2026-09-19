(() => {
  const CFG_URL = "flash-sheet-url";
  const CFG_SECRET = "flash-sheet-secret";
  const STYLE_ID = "flash-sheet-style";

  const injectCss = () => {
    if (document.getElementById(STYLE_ID)) return;
    const el = document.createElement("style");
    el.id = STYLE_ID;
    el.textContent = `
.ex-flash-sheet-panel {
  display: none;
  margin: 12px 0 0;
  padding: 14px 16px;
  border: 1px solid var(--border, rgba(148,163,184,.25));
  border-radius: 14px;
  background: rgba(255,255,255,.03);
  max-width: 42rem;
}
.ex-flash-sheet-panel.is-open { display: grid; gap: 10px; }
.ex-flash-sheet-panel h3 {
  margin: 0;
  font-size: 0.92rem;
  font-family: Outfit, sans-serif;
  font-weight: 600;
  color: var(--text, #e2e8f0);
}
.ex-flash-sheet-panel p,
.ex-flash-sheet-help {
  margin: 0;
  font-size: 0.82rem;
  line-height: 1.45;
  color: rgba(226,232,240,.68);
  font-family: Outfit, sans-serif;
}
.ex-flash-sheet-panel label {
  display: grid;
  gap: 4px;
  font-size: 0.75rem;
  font-family: "JetBrains Mono", monospace;
  color: rgba(226,232,240,.75);
}
.ex-flash-sheet-panel input {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid var(--border, rgba(148,163,184,.25));
  border-radius: 8px;
  background: rgba(2,6,23,.55);
  color: var(--text, #e2e8f0);
  padding: 8px 10px;
  font-size: 0.82rem;
  font-family: "JetBrains Mono", monospace;
}
.ex-flash-sheet-actions { display: flex; flex-wrap: wrap; gap: 8px; }
.ex-flash-swipe-hint {
  margin: 8px 0 0;
  text-align: center;
  font-size: 0.78rem;
  color: rgba(226,232,240,.5);
  font-family: Outfit, sans-serif;
}
.ex-flash-deck.is-dragging {
  cursor: grabbing;
}
.ex-flash-deck { touch-action: pan-y; user-select: none; }
.ex-flash-card {
  will-change: transform, opacity;
}
.ex-flash-peek--prev { display: none !important; }
.ex-flash-gold-badge {
  display: none;
  align-items: center;
  font-family: "JetBrains Mono", monospace;
  font-size: 0.75rem;
  color: #fbbf24;
  border: 1px solid rgba(251, 191, 36, 0.45);
  background: rgba(251, 191, 36, 0.12);
  border-radius: 999px;
  padding: 4px 10px;
}
.ex-flash--gold .ex-flash-gold-badge { display: inline-flex; }
.ex-flash { overflow: hidden; }
.ex-flash-grade--pareto { grid-template-columns: 1fr 1fr; }
@media (max-width: 640px) {
  .ex-flash {
    padding: 10px 8px 16px;
    margin-bottom: 24px;
    padding-bottom: max(16px, env(safe-area-inset-bottom));
  }
  .ex-flash-head { gap: 8px; margin-bottom: 10px; }
  .ex-flash-hint { font-size: 0.8rem; max-width: none; }
  .ex-flash-controls { gap: 6px; }
  .ex-flash-stats { width: 100%; font-size: 0.72rem; gap: 8px 12px; }
  .ex-flash .ex-btn { padding: 6px 10px; font-size: 0.72rem; }
  .ex-flash-stage { padding: 6px 16px 10px 6px; overflow: hidden; }
  .ex-flash-deck, .ex-flash-card {
    width: 100%;
    min-height: min(58dvh, 460px);
  }
  .ex-flash-peek, .ex-flash-peek--next {
    inset: 0 !important;
    width: 100%;
    height: 100%;
    transform: scale(0.96) translate3d(10px, 8px, 0);
  }
  .ex-flash-peek--prev { display: none !important; }
  .ex-flash-grade--pareto { grid-template-columns: 1fr 1fr; min-height: 52px; }
  .ex-flash-grade-btn { font-size: 0.9rem; padding: 14px 8px; min-height: 48px; }
  .ex-flash-front-body { padding: 40px 16px 20px; }
  .ex-flash-back-body { padding: 44px 14px 10px; gap: 8px; }
  .docs-main .ex-flash-term { font-size: clamp(1.4rem, 7vw, 2rem); }
  .ex-flash-photo img { max-width: min(100%, 220px); max-height: 132px; }
  .ex-flash-sheet-panel { max-width: none; }
}
@media (max-width: 640px) and (max-height: 720px) {
  .ex-flash-deck, .ex-flash-card { min-height: min(52dvh, 400px); }
  .ex-flash-photo img { max-height: 96px; }
}
`;
    document.head.appendChild(el);
  };

  const getConfig = () => ({
    url: String(localStorage.getItem(CFG_URL) || "").trim(),
    secret: String(localStorage.getItem(CFG_SECRET) || "").trim(),
  });

  const setConfig = (url, secret) => {
    localStorage.setItem(CFG_URL, String(url || "").trim());
    localStorage.setItem(CFG_SECRET, String(secret || "").trim());
  };

  const isConfigured = () => {
    const { url, secret } = getConfig();
    return /^https:\/\/script\.google\.com\//.test(url) && !!secret;
  };

  const request = async (body) => {
    const { url, secret } = getConfig();
    if (!url || !secret) {
      const err = new Error("Chưa cấu hình Web App URL / secret");
      err.code = "noconfig";
      throw err;
    }
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "text/plain;charset=utf-8" },
      body: JSON.stringify({ ...body, secret }),
    });
    const text = await res.text();
    let data = null;
    try {
      data = JSON.parse(text);
    } catch {
      throw new Error("Sheet không trả JSON — kiểm tra Deploy = Web app / Anyone");
    }
    if (!data || data.ok === false) {
      throw new Error((data && data.error) || "Sheet từ chối request");
    }
    return data;
  };

  const save = (deck, payload) => request({ action: "save", deck, payload });
  const load = (deck) => request({ action: "load", deck });
  const ping = () => request({ action: "ping" });

  const wordRef = (w) => ({
    id: w && w.id != null ? w.id : null,
    form: String((w && (w.form || w.hanzi)) || ""),
  });

  const resolver = (vocab) => {
    const byId = new Map();
    const byForm = new Map();
    (vocab || []).forEach((w) => {
      if (w && w.id != null) byId.set(String(w.id), w);
      const form = String((w && (w.form || w.hanzi)) || "").toLowerCase();
      if (form) byForm.set(form, w);
    });
    return (ref) => {
      if (ref == null) return null;
      if (typeof ref === "string") return byForm.get(ref.toLowerCase()) || null;
      if (ref.id != null && byId.has(String(ref.id))) return byId.get(String(ref.id));
      const form = String(ref.form || "").toLowerCase();
      return form ? byForm.get(form) || null : null;
    };
  };

  const snapshot = (deck, idx, classified) => ({
    version: 1,
    idx,
    deck: (deck || []).map(wordRef),
    gold: (classified.gold || []).map(wordRef),
    known: (classified.known || []).map(wordRef),
    trash: (classified.trash || []).map(wordRef),
  });

  const restore = (payload, vocab) => {
    const resolve = resolver(vocab);
    const mapList = (arr) => (Array.isArray(arr) ? arr.map(resolve).filter(Boolean) : []);
    const deck = mapList(payload && payload.deck);
    const gold = mapList(payload && payload.gold);
    const known = mapList(payload && payload.known);
    const trash = mapList(payload && payload.trash);
    let idx = Number(payload && payload.idx);
    if (!Number.isFinite(idx) || idx < 0) idx = gold.length + known.length + trash.length;
    if (idx > deck.length) idx = deck.length;
    return { deck, idx, gold, known, trash };
  };

  const wordKey = (w) => {
    if (w && w.id != null && w.id !== "") return `id:${w.id}`;
    return `form:${String((w && (w.form || w.hanzi)) || "").toLowerCase()}`;
  };

  const mergeGoldReview = (base, live) => {
    const pending = (live.deck || []).slice(live.idx || 0);
    const stillGold = [...(live.classified.gold || []), ...pending];
    const toKnown = live.classified.known || [];
    const toTrash = live.classified.trash || [];
    const moved = new Set([...stillGold, ...toKnown, ...toTrash].map(wordKey));
    const keep = (arr) => (arr || []).filter((w) => !moved.has(wordKey(w)));
    return {
      deck: base.deck && base.deck.length ? base.deck : live.deck || [],
      idx: base.idx || 0,
      gold: stillGold,
      known: [...keep(base.known), ...toKnown],
      trash: [...keep(base.trash), ...toTrash],
    };
  };

  const mount = ({ section, deckKey, vocab, getLive, applyLive, applyGoldReview, showMsg }) => {
    if (!section) return;
    injectCss();
    const controls = section.querySelector(".ex-flash-controls");
    if (!controls) return;
    if (document.getElementById("btnFlashSheetSave")) return;

    const addBtn = (id, label) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "ex-btn";
      btn.id = id;
      btn.textContent = label;
      const restart = document.getElementById("btnFlashRestart");
      controls.insertBefore(btn, restart || null);
      return btn;
    };

    const btnSave = addBtn("btnFlashSheetSave", "Lưu Sheet");
    const btnLoad = addBtn("btnFlashSheetLoad", "Tải Sheet");
    const btnGold = addBtn("btnFlashSheetGold", "Ôn phải học");
    btnGold.classList.add("primary");
    const btnCfg = addBtn("btnFlashSheetCfg", "Sheet…");

    const stats = section.querySelector(".ex-flash-stats");
    ensureMastery(section);
    if (stats && !document.getElementById("flashGoldMode")) {
      const badge = document.createElement("span");
      badge.id = "flashGoldMode";
      badge.className = "ex-flash-gold-badge";
      badge.textContent = "Ôn phải học";
      stats.appendChild(badge);
    }

    const panel = document.createElement("div");
    panel.className = "ex-flash-sheet-panel";
    panel.id = "flashSheetPanel";
    panel.innerHTML = `
      <h3>Google Sheet làm backend</h3>
      <p class="ex-flash-sheet-help">
        Tạo Sheet → Extensions → Apps Script → dán
        <code>scripts/google-sheet-progress.gs</code> → Deploy Web app (Anyone).
        Dán URL <code>/exec</code> và secret trùng với script. Không commit URL/secret lên git.
      </p>
      <label>Web App URL
        <input type="url" id="flashSheetUrl" placeholder="https://script.google.com/macros/s/…/exec" autocomplete="off">
      </label>
      <label>Secret
        <input type="password" id="flashSheetSecret" placeholder="trùng SECRET trong Apps Script" autocomplete="off">
      </label>
      <div class="ex-flash-sheet-actions">
        <button type="button" class="ex-btn primary" id="flashSheetSaveCfg">Lưu cấu hình</button>
        <button type="button" class="ex-btn" id="flashSheetPing">Thử kết nối</button>
      </div>
    `;
    const msg = section.querySelector(".ex-flash-msg");
    if (msg) section.insertBefore(panel, msg);
    else section.appendChild(panel);

    const fillCfg = () => {
      const cfg = getConfig();
      const urlEl = document.getElementById("flashSheetUrl");
      const secretEl = document.getElementById("flashSheetSecret");
      if (urlEl) urlEl.value = cfg.url;
      if (secretEl) secretEl.value = cfg.secret;
    };

    const keyOf = () => (typeof deckKey === "function" ? deckKey() : String(deckKey || "deck"));

    const needConfig = () => {
      if (isConfigured()) return false;
      panel.classList.add("is-open");
      fillCfg();
      showMsg("Dán Web App URL + secret rồi bấm Lưu cấu hình.", false);
      return true;
    };

    btnCfg.addEventListener("click", () => {
      panel.classList.toggle("is-open");
      if (panel.classList.contains("is-open")) fillCfg();
    });

    document.getElementById("flashSheetSaveCfg")?.addEventListener("click", () => {
      const url = document.getElementById("flashSheetUrl")?.value || "";
      const secret = document.getElementById("flashSheetSecret")?.value || "";
      setConfig(url, secret);
      if (!isConfigured()) {
        showMsg("URL phải là script.google.com/.../exec và secret không trống.", false);
        return;
      }
      showMsg("Đã lưu cấu hình Sheet trên trình duyệt này.", true);
    });

    document.getElementById("flashSheetPing")?.addEventListener("click", async () => {
      if (needConfig()) return;
      try {
        await ping();
        showMsg("Kết nối Google Sheet OK.", true);
      } catch (err) {
        showMsg(err.message || String(err), false);
      }
    });

    btnSave.addEventListener("click", async () => {
      if (needConfig()) return;
      const live = getLive();
      if (!live || !live.deck || !live.deck.length) {
        showMsg("Chưa có từ vựng để lưu.", false);
        return;
      }
      btnSave.disabled = true;
      try {
        let payload;
        if (live.mode === "gold") {
          const data = await load(keyOf());
          if (!data.found || !data.payload) {
            showMsg("Sheet chưa có bản Pareto đầy đủ. Sàng lọc đủ bộ rồi Lưu Sheet trước.", false);
            return;
          }
          const base = restore(data.payload, vocab);
          const merged = mergeGoldReview(base, live);
          payload = snapshot(merged.deck, merged.idx, {
            gold: merged.gold,
            known: merged.known,
            trash: merged.trash,
          });
        } else {
          payload = snapshot(live.deck, live.idx, live.classified);
        }
        payload.savedAt = new Date().toISOString();
        await save(keyOf(), payload);
        const nGold = (payload.gold || []).length;
        showMsg(
          live.mode === "gold"
            ? `Đã cập nhật nhóm Phải học trên Sheet (${nGold} từ).`
            : `Đã lưu ${keyOf()} lên Google Sheet.`,
          true
        );
      } catch (err) {
        showMsg(err.message || String(err), false);
      } finally {
        btnSave.disabled = false;
      }
    });

    btnLoad.addEventListener("click", async () => {
      if (needConfig()) return;
      btnLoad.disabled = true;
      try {
        const data = await load(keyOf());
        if (!data.found || !data.payload) {
          showMsg("Sheet chưa có dữ liệu cho bộ thẻ này.", false);
          return;
        }
        const next = restore(data.payload, vocab);
        if (!next.deck.length) {
          showMsg("JSON trên Sheet không khớp từ vựng trang này.", false);
          return;
        }
        applyLive(next);
        showMsg(
          `Đã tải từ Sheet — card ${Math.min(next.idx + 1, next.deck.length)}/${next.deck.length}.`,
          true
        );
      } catch (err) {
        showMsg(err.message || String(err), false);
      } finally {
        btnLoad.disabled = false;
      }
    });

    btnGold.addEventListener("click", async () => {
      if (needConfig()) return;
      if (typeof applyGoldReview !== "function") return;
      btnGold.disabled = true;
      try {
        const data = await load(keyOf());
        if (!data.found || !data.payload) {
          showMsg("Sheet chưa có dữ liệu. Phân loại rồi Lưu Sheet trước.", false);
          return;
        }
        const next = restore(data.payload, vocab);
        if (!next.gold.length) {
          showMsg("Sheet chưa có từ Phải học cho bộ thẻ này.", false);
          return;
        }
        applyGoldReview(next.gold);
        showMsg(`Ôn ${next.gold.length} từ phải học từ Sheet.`, true);
      } catch (err) {
        showMsg(err.message || String(err), false);
      } finally {
        btnGold.disabled = false;
      }
    });
  };

  const escapeHtml = (s) =>
    String(s ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");

  const escapeRegExp = (s) => String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

  const shuffle = (arr) => {
    const a = (arr || []).slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  };

  const termOf = (w) => String((w && (w.form || w.hanzi || w.word)) || "").trim();
  const stemOf = (w) => termOf(w).replace(/^to\s+/i, "").trim() || termOf(w);

  const exampleOf = (w) => {
    if (!w) return { en: "", vi: "", zh: "", py: "" };
    const ex = (w.examples && w.examples[0]) || null;
    return {
      en: String(w.ex_en || (ex && (ex.en || ex.zh)) || "").trim(),
      vi: String(w.ex_vi || (ex && ex.vi) || "").trim(),
      zh: String((ex && ex.zh) || "").trim(),
      py: String((ex && ex.py) || "").trim(),
    };
  };

  const clozeHtml = (w) => {
    const ex = exampleOf(w);
    const sentence = ex.zh || ex.en;
    const answer = termOf(w);
    const stem = stemOf(w);
    const vi = ex.vi;
    if (!sentence) {
      return {
        html: `Chọn từ đúng với nghĩa: <strong>${escapeHtml(w.vi || w.en || answer)}</strong>`,
        vi: "",
      };
    }
    const needles = [...new Set([answer, stem].filter(Boolean))].sort(
      (a, b) => b.length - a.length
    );
    let idx = -1;
    let len = 0;
    needles.forEach((p) => {
      if (idx >= 0) return;
      const cjk = /[\u3400-\u9fff]/.test(p);
      const re = cjk ? new RegExp(escapeRegExp(p)) : new RegExp(`\\b${escapeRegExp(p)}\\b`, "i");
      const m = sentence.match(re);
      if (m) {
        idx = sentence.search(re);
        len = m[0].length;
      }
    });
    if (idx < 0) {
      return {
        html: `${escapeHtml(sentence)} <span class="ex-cloze-blank">______</span>`,
        vi,
      };
    }
    return {
      html:
        escapeHtml(sentence.slice(0, idx)) +
        `<span class="ex-cloze-blank">______</span>` +
        escapeHtml(sentence.slice(idx + len)),
      vi,
    };
  };

  const paintMastery = (knownN, goldN) => {
    const known = Number(knownN || 0);
    const gold = Number(goldN || 0);
    const total = known + gold;
    const pct = total ? Math.round((known / total) * 100) : 0;
    const label = document.getElementById("flashMasteryLabel");
    const fill = document.getElementById("flashMasteryFill");
    const track = fill && fill.parentElement;
    if (label) label.textContent = total ? `${known}/${total} · ${pct}%` : "Chưa phân loại";
    if (fill) fill.style.width = `${pct}%`;
    if (track) track.setAttribute("aria-valuenow", String(pct));
  };

  const ensureMastery = (section) => {
    if (document.getElementById("flashMastery")) return;
    if (!section) return;
    const el = document.createElement("div");
    el.id = "flashMastery";
    el.className = "ex-flash-mastery";
    el.innerHTML = `
      <div class="ex-flash-mastery-row">
        <span>Tiến độ phải học → đã biết</span>
        <strong id="flashMasteryLabel">0/0</strong>
      </div>
      <div class="ex-flash-mastery-track" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
        <div class="ex-flash-mastery-fill" id="flashMasteryFill"></div>
      </div>
    `;
    const head = section.querySelector(".ex-flash-head");
    if (head) head.appendChild(el);
    else section.prepend(el);
  };

  const choiceLabel = (w) => {
    const term = termOf(w);
    const sub = w && w.pinyin ? w.pinyin : w && w.vi ? w.vi : "";
    return { term, sub };
  };

  const mountCloze = ({ section, deckKey, vocab, getLive, applyGrade, showMsg }) => {
    if (!section || document.getElementById("exCloze")) return;
    injectCss();
    const root = document.createElement("section");
    root.className = "ex-cloze";
    root.id = "exCloze";
    root.setAttribute("aria-label", "Điền chỗ trống");
    root.innerHTML = `
      <div class="ex-cloze-head">
        <div>
          <h2>Điền chỗ trống</h2>
          <p class="ex-cloze-hint">
            Chỉ ôn từ <strong>Phải học</strong> đã lưu trên Sheet. Câu ví dụ + 4 đáp án
            (nhiễu lấy từ nhóm <strong>Đã biết</strong> và từ khác). Đúng → Đã biết · Sai → vẫn Phải học.
            Mỗi câu tự lưu Sheet.
          </p>
        </div>
        <div class="ex-cloze-actions">
          <button type="button" class="ex-btn primary" id="btnClozeStart">Bắt đầu</button>
        </div>
      </div>
      <div class="ex-cloze-progress" id="clozeProgress" hidden>
        <div class="ex-cloze-progress-row">
          <span>Hoàn thành phải học → đã biết</span>
          <strong id="clozeProgressLabel">0/0</strong>
        </div>
        <div class="ex-cloze-progress-track" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
          <div class="ex-cloze-progress-fill" id="clozeProgressFill"></div>
        </div>
      </div>
      <div class="ex-cloze-board" id="clozeBoard"></div>
      <p class="ex-cloze-status" id="clozeStatus"></p>
    `;
    section.insertAdjacentElement("afterend", root);

    const nav = document.querySelector(".hsk-jump");
    if (nav && !nav.querySelector('[href="#exCloze"]')) {
      const a = document.createElement("a");
      a.href = "#exCloze";
      a.textContent = "Điền chỗ trống";
      nav.appendChild(a);
    }

    if (!document.getElementById("btnFlashCloze")) {
      const controls = section.querySelector(".ex-flash-controls");
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "ex-btn";
      btn.id = "btnFlashCloze";
      btn.textContent = "Điền chỗ trống";
      btn.addEventListener("click", () => {
        document.getElementById("exCloze")?.scrollIntoView({ behavior: "smooth", block: "start" });
      });
      const restart = document.getElementById("btnFlashRestart");
      if (controls) controls.insertBefore(btn, restart || null);
    }

    const board = document.getElementById("clozeBoard");
    const status = document.getElementById("clozeStatus");
    const btnStart = document.getElementById("btnClozeStart");
    const keyOf = () => (typeof deckKey === "function" ? deckKey() : String(deckKey || "deck"));
    const LETTERS = ["A", "B", "C", "D"];

    const setStatus = (text, kind) => {
      if (!status) return;
      status.textContent = text || "";
      status.classList.toggle("ok", kind === "ok");
      status.classList.toggle("bad", kind === "bad");
    };

    const paintSessionBar = (cleared, total) => {
      const wrap = document.getElementById("clozeProgress");
      const label = document.getElementById("clozeProgressLabel");
      const fill = document.getElementById("clozeProgressFill");
      if (wrap) wrap.hidden = !total;
      const pct = total ? Math.round((cleared / total) * 100) : 0;
      if (label) label.textContent = `${cleared}/${total} · ${pct}%`;
      if (fill) fill.style.width = `${pct}%`;
      if (fill && fill.parentElement) fill.parentElement.setAttribute("aria-valuenow", String(pct));
    };

    const openSheetPanel = () => {
      const panel = document.getElementById("flashSheetPanel");
      if (panel) {
        panel.classList.add("is-open");
        panel.scrollIntoView({ behavior: "smooth", block: "center" });
      }
      if (showMsg) showMsg("Dán Web App URL + secret rồi bấm Lưu cấu hình.", false);
    };

    const renderLock = () => {
      if (!board) return;
      board.innerHTML = `
        <div class="ex-cloze-lock">
          <p>Kết nối Google Sheet trước khi chơi. Trò này chỉ ôn các từ <strong>Phải học</strong> đã lưu.</p>
          <div class="ex-cloze-actions">
            <button type="button" class="ex-btn primary" id="btnClozeCfg">Mở cấu hình Sheet</button>
          </div>
        </div>`;
      document.getElementById("btnClozeCfg")?.addEventListener("click", openSheetPanel);
    };

    let state = null;
    let queue = [];
    let qIdx = 0;
    let startTotal = 0;
    let cleared = 0;
    let correctN = 0;
    let wrongN = 0;
    let busy = false;

    const uniquePush = (arr, w) => {
      const k = wordKey(w);
      if (!k || arr.some((x) => wordKey(x) === k)) return;
      arr.push(w);
    };

    const mergeLive = (base) => {
      const live = getLive && getLive();
      if (!live || !live.classified) return base;
      const gold = (base.gold || []).slice();
      const known = (base.known || []).slice();
      const knownKeys = new Set((live.classified.known || []).map(wordKey));
      (live.classified.gold || []).forEach((w) => uniquePush(gold, w));
      (live.classified.known || []).forEach((w) => uniquePush(known, w));
      return {
        ...base,
        gold: gold.filter((w) => !knownKeys.has(wordKey(w))),
        known,
        deck: live.deck && live.deck.length && live.mode !== "gold" ? live.deck : base.deck,
        idx: live.deck && live.deck.length && live.mode !== "gold" ? live.idx : base.idx,
        trash: live.classified.trash || base.trash || [],
      };
    };

    const persist = async () => {
      const payload = snapshot(state.deck, state.idx, {
        gold: state.gold,
        known: state.known,
        trash: state.trash,
      });
      payload.savedAt = new Date().toISOString();
      await save(keyOf(), payload);
    };

    const pickChoices = (answer) => {
      const used = new Set([wordKey(answer)]);
      const out = [];
      const take = (arr) => {
        shuffle(arr).forEach((w) => {
          if (out.length >= 3) return;
          const k = wordKey(w);
          if (!k || used.has(k) || !termOf(w)) return;
          used.add(k);
          out.push(w);
        });
      };
      const samePos = (arr) =>
        (arr || []).filter((w) => answer.pos && w.pos && String(w.pos) === String(answer.pos));
      take(samePos(state.known));
      take(state.known);
      take(samePos(vocab));
      take(vocab);
      const options = shuffle([answer, ...out.slice(0, 3)]);
      let i = 0;
      while (options.length < 4 && i < (vocab || []).length) {
        uniquePush(options, vocab[i]);
        i += 1;
      }
      return options.slice(0, 4);
    };

    const renderDone = () => {
      board.innerHTML = `
        <div class="ex-cloze-done">
          <p>Đã ôn ${startTotal} từ phải học.</p>
          <p class="ex-cloze-done-meta">Đúng <strong>${correctN}</strong> → Đã biết · Sai <strong>${wrongN}</strong> → vẫn Phải học</p>
          <div class="ex-cloze-actions">
            <button type="button" class="ex-btn primary" id="btnClozeAgain">Chơi lại</button>
            <button type="button" class="ex-btn" id="btnClozeFlash">Về flashcards</button>
          </div>
        </div>`;
      document.getElementById("btnClozeAgain")?.addEventListener("click", () => startGame());
      document.getElementById("btnClozeFlash")?.addEventListener("click", () => {
        section.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    };

    const renderQuestion = () => {
      const w = queue[qIdx];
      if (!w) {
        renderDone();
        return;
      }
      const { html, vi } = clozeHtml(w);
      const choices = pickChoices(w);
      board.innerHTML = `
        <div class="ex-cloze-card">
          <p class="ex-cloze-meta">Câu ${qIdx + 1}/${queue.length}</p>
          <p class="ex-cloze-q">${html}</p>
          <p class="ex-cloze-vi" id="clozeVi" hidden>${escapeHtml(vi)}</p>
          <div class="ex-cloze-choices">
            ${choices
              .map((opt, i) => {
                const lab = choiceLabel(opt);
                return `<button type="button" class="ex-cloze-choice" data-key="${escapeHtml(wordKey(opt))}">
                  <span class="ex-cloze-letter">${LETTERS[i]}</span>
                  <span>${escapeHtml(lab.term)}${
                    lab.sub && lab.sub !== lab.term
                      ? `<span class="ex-cloze-sub">${escapeHtml(lab.sub)}</span>`
                      : ""
                  }</span>
                </button>`;
              })
              .join("")}
          </div>
        </div>`;
      board.querySelectorAll(".ex-cloze-choice").forEach((btn) => {
        btn.addEventListener("click", () => onPick(btn, w));
      });
    };

    const onPick = async (btn, word) => {
      if (busy) return;
      busy = true;
      const ok = btn.getAttribute("data-key") === wordKey(word);
      board.querySelectorAll(".ex-cloze-choice").forEach((el) => {
        el.disabled = true;
        if (el.getAttribute("data-key") === wordKey(word)) el.classList.add("is-correct");
      });
      if (!ok) btn.classList.add("is-wrong");
      const blank = board.querySelector(".ex-cloze-blank");
      if (blank) {
        blank.textContent = termOf(word);
        blank.classList.add(ok ? "is-ok" : "is-bad");
      }
      const viEl = document.getElementById("clozeVi");
      if (viEl && viEl.textContent.trim()) viEl.hidden = false;

      const k = wordKey(word);
      state.gold = (state.gold || []).filter((w) => wordKey(w) !== k);
      state.known = (state.known || []).filter((w) => wordKey(w) !== k);
      if (ok) {
        state.known.push(word);
        cleared += 1;
        correctN += 1;
      } else {
        state.gold.push(word);
        wrongN += 1;
      }
      if (typeof applyGrade === "function") applyGrade(word, ok);
      paintSessionBar(cleared, startTotal);
      paintMastery(state.known.length, state.gold.length);
      setStatus(ok ? "Đúng — chuyển sang Đã biết, đang lưu Sheet…" : "Sai — vẫn Phải học, đang lưu Sheet…", ok ? "ok" : "bad");
      try {
        await persist();
        setStatus(ok ? "Đúng · đã lưu Sheet." : "Sai · đã lưu Sheet.", ok ? "ok" : "bad");
      } catch (err) {
        setStatus(err.message || "Lưu Sheet thất bại.", "bad");
      }
      window.setTimeout(() => {
        qIdx += 1;
        busy = false;
        renderQuestion();
      }, 900);
    };

    const startGame = async () => {
      if (!isConfigured()) {
        renderLock();
        openSheetPanel();
        return;
      }
      btnStart.disabled = true;
      setStatus("Đang tải từ phải học trên Sheet…");
      try {
        const data = await load(keyOf());
        if (!data.found || !data.payload) {
          board.innerHTML = `<div class="ex-cloze-empty"><p>Sheet chưa có dữ liệu cho bộ này. Phân loại flashcards rồi <strong>Lưu Sheet</strong> trước.</p></div>`;
          setStatus("Chưa có dữ liệu Sheet.", "bad");
          return;
        }
        state = mergeLive(restore(data.payload, vocab));
        queue = shuffle(state.gold || []);
        if (!queue.length) {
          board.innerHTML = `<div class="ex-cloze-empty"><p>Không còn từ <strong>Phải học</strong>. Sàng lọc flashcards hoặc ôn bộ khác.</p></div>`;
          paintMastery(state.known.length, 0);
          paintSessionBar(0, 0);
          setStatus("Hết từ phải học.", "ok");
          return;
        }
        qIdx = 0;
        startTotal = queue.length;
        cleared = 0;
        correctN = 0;
        wrongN = 0;
        busy = false;
        paintSessionBar(0, startTotal);
        paintMastery(state.known.length, state.gold.length);
        setStatus(`Ôn ${startTotal} từ phải học.`);
        renderQuestion();
      } catch (err) {
        setStatus(err.message || String(err), "bad");
        renderLock();
      } finally {
        btnStart.disabled = false;
      }
    };

    btnStart.addEventListener("click", () => startGame());
    if (!isConfigured()) renderLock();
    else {
      board.innerHTML = `<div class="ex-cloze-empty"><p>Bấm <strong>Bắt đầu</strong> để ôn các từ phải học từ Google Sheet.</p></div>`;
    }
  };

  const bindCardSwipe = (deckEl, { onGradeLeft, onGradeRight, onTap, onBrowseNext, onBrowsePrev }) => {
    if (!deckEl || deckEl.dataset.swipeBound) return;
    deckEl.dataset.swipeBound = "1";
    const THRESH = 72;
    const TAP_MAX = 12;
    const gradeLeft = onGradeLeft || onBrowsePrev;
    const gradeRight = onGradeRight || onBrowseNext;
    let startX = 0;
    let startY = 0;
    let dx = 0;
    let dy = 0;
    let tracking = false;
    let axis = null;
    let pid = null;
    let settled = false;

    const cardEl = () => deckEl.querySelector("#flashCard");
    const peekNextEl = () =>
      deckEl.querySelector(".ex-flash-peek--next") ||
      deckEl.querySelector(".ex-flash-peek:not(.ex-flash-peek--prev)");
    const washKnownEl = () => deckEl.querySelector(".ex-flash-wash--known");
    const washGoldEl = () => deckEl.querySelector(".ex-flash-wash--gold");

    const paint = (x, animate) => {
      const card = cardEl();
      const peek = peekNextEl();
      const washKnown = washKnownEl();
      const washGold = washGoldEl();
      const ease = animate
        ? "transform 0.32s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.32s ease"
        : "none";
      deckEl.classList.toggle("is-dragging", !animate && tracking);

      const setWash = (el, op) => {
        if (!el) return;
        el.style.transition = animate ? "opacity 0.22s ease" : "none";
        el.style.opacity = op;
      };

      if (!x) {
        [card, peek].forEach((el) => {
          if (!el) return;
          el.style.transition = ease;
          el.style.transform = "";
          el.style.opacity = "";
        });
        setWash(washKnown, "");
        setWash(washGold, "");
        return;
      }

      const width = Math.max(deckEl.getBoundingClientRect().width, 1);
      const p = Math.min(1, Math.abs(x) / (width * 0.62));
      const pWash = Math.min(1, Math.abs(x) / (width * 0.38));
      const goingLeft = x < 0;

      if (card) {
        card.style.transition = ease;
        card.style.transform = `translate3d(${x}px, ${Math.abs(x) * 0.035}px, 0) rotate(${x * 0.055}deg)`;
        card.style.opacity = String(1 - 0.18 * p);
      }
      if (peek) {
        peek.style.transition = ease;
        peek.style.opacity = "1";
        peek.style.transform = `scale(${0.94 + 0.06 * p}) translate3d(${16 * (1 - p)}px, ${10 * (1 - p)}px, 0)`;
      }
      if (goingLeft) {
        setWash(washKnown, String(pWash));
        setWash(washGold, "0");
      } else {
        setWash(washGold, String(pWash));
        setWash(washKnown, "0");
      }
    };

    const ignore = (t) =>
      !!(
        t &&
        t.closest &&
        t.closest(
          ".ex-flash-speak, .ex-flash-grade-btn, .ex-flash-example-speak, .ex-flash-backnav, a, input, textarea"
        )
      );

    const finish = (dir) => {
      if (settled) return;
      settled = true;
      const width = Math.max(deckEl.getBoundingClientRect().width, 280);
      paint(dir * width * 1.18, true);
      deckEl.style.pointerEvents = "none";
      window.setTimeout(() => {
        deckEl.classList.remove("is-dragging");
        if (dir < 0) gradeLeft && gradeLeft();
        else gradeRight && gradeRight();
      }, 300);
    };

    const onMove = (e) => {
      if (!tracking || e.pointerId !== pid) return;
      dx = e.clientX - startX;
      dy = e.clientY - startY;
      if (axis == null && (Math.abs(dx) > 8 || Math.abs(dy) > 8)) {
        axis = Math.abs(dx) > Math.abs(dy) * 1.15 ? "x" : "y";
      }
      if (axis !== "x") return;
      if (e.cancelable) e.preventDefault();
      paint(dx, false);
    };

    const onUp = (e) => {
      if (!tracking || (e.pointerId != null && e.pointerId !== pid)) return;
      tracking = false;
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("pointerup", onUp);
      window.removeEventListener("pointercancel", onUp);
      const isSwipe = axis === "x" && Math.abs(dx) >= THRESH;
      if (isSwipe) {
        finish(dx > 0 ? 1 : -1);
      } else {
        paint(0, true);
        if (axis !== "x" && Math.abs(dx) < TAP_MAX && Math.abs(dy) < TAP_MAX && onTap) {
          onTap();
        }
      }
      axis = null;
      pid = null;
    };

    deckEl.addEventListener("pointerdown", (e) => {
      if (e.pointerType === "mouse" && e.button !== 0) return;
      if (ignore(e.target)) return;
      tracking = true;
      settled = false;
      axis = null;
      pid = e.pointerId;
      startX = e.clientX;
      startY = e.clientY;
      dx = dy = 0;
      window.addEventListener("pointermove", onMove, { passive: false });
      window.addEventListener("pointerup", onUp);
      window.addEventListener("pointercancel", onUp);
    });
  };

  window.SheetBackend = {
    getConfig,
    setConfig,
    isConfigured,
    save,
    load,
    ping,
    snapshot,
    restore,
    mergeGoldReview,
    wordRef,
    wordKey,
    paintMastery,
    mount,
    mountCloze,
    bindCardSwipe,
  };
})();
