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
  transition: none;
  cursor: grabbing;
}
.ex-flash-deck { touch-action: pan-y; }
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
  .ex-flash-stage { padding: 4px 0 8px; overflow: hidden; }
  .ex-flash-deck, .ex-flash-card {
    width: 100%;
    min-height: min(58dvh, 460px);
  }
  .ex-flash-peek { display: none !important; }
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

  const bindCardSwipe = (deckEl, { onBrowseNext, onBrowsePrev, canBrowse }) => {
    if (!deckEl || deckEl.dataset.swipeBound) return;
    deckEl.dataset.swipeBound = "1";
    const THRESH = 64;
    let startX = 0;
    let startY = 0;
    let dx = 0;
    let dy = 0;
    let tracking = false;
    let axis = null;
    let pid = null;
    let settled = false;

    const setShift = (x, animate) => {
      deckEl.classList.toggle("is-dragging", !animate && tracking);
      deckEl.style.transition = animate ? "transform 0.22s ease" : "none";
      deckEl.style.transform = x ? `translateX(${x}px)` : "";
    };

    const ignore = (t) => !!(t && t.closest && t.closest("button, a, input, textarea"));

    const finish = (dir) => {
      if (settled) return;
      settled = true;
      const width = Math.max(deckEl.getBoundingClientRect().width, 280);
      setShift(dir * (width + 40), true);
      window.setTimeout(() => {
        deckEl.style.transition = "none";
        deckEl.style.transform = "";
        if (dir < 0) onBrowseNext && onBrowseNext();
        else onBrowsePrev && onBrowsePrev();
      }, 200);
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
      setShift(dx, false);
    };

    const onUp = (e) => {
      if (!tracking || (e.pointerId != null && e.pointerId !== pid)) return;
      tracking = false;
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("pointerup", onUp);
      window.removeEventListener("pointercancel", onUp);
      if (axis === "x" && Math.abs(dx) >= THRESH && (!canBrowse || canBrowse())) finish(dx > 0 ? 1 : -1);
      else setShift(0, true);
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
    mount,
    bindCardSwipe,
  };
})();
