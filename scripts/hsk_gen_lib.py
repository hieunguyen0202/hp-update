"""Shared helpers to emit HSK lesson data JS."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def hanzi_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def build_matchers(vocab: list[dict]) -> list[tuple[str, str]]:
    matchers: list[tuple[str, str]] = []
    for w in vocab:
        forms = w.get("match") or [w["hanzi"]]
        for form in forms:
            matchers.append((form, w["id"]))
    matchers.sort(key=lambda x: len(x[0]), reverse=True)
    return matchers


def _norm_para(item: tuple | dict) -> dict:
    """Accept (zh,py,en), (zh,py,en,vi), (speaker,zh,py,en,vi), or dict."""
    if isinstance(item, dict):
        return item
    if len(item) == 3:
        zh, py, en = item
        return {"zh": zh, "py": py, "en": en}
    if len(item) == 4:
        zh, py, en, vi = item
        return {"zh": zh, "py": py, "en": en, "vi": vi}
    if len(item) == 5:
        speaker, zh, py, en, vi = item
        return {"speaker": speaker, "zh": zh, "py": py, "en": en, "vi": vi}
    raise ValueError(f"Bad paragraph tuple length: {len(item)}")


def tokenize(
    text: str,
    matchers: list[tuple[str, str]],
    blocked_if_inside: dict[str, tuple[str, ...]] | None = None,
    *,
    extra_matchers: list[tuple[str, str]] | None = None,
    emotion_forms: list[str] | None = None,
) -> list[dict]:
    """Longest-match tokenize.

    Priority when same length: emotion > lesson vocab > extra.
    Tokens may include ``new``, ``extra``, or ``emotion`` keys.
    """
    blocked_if_inside = blocked_if_inside or {}
    ranked: list[tuple[str, str, str]] = []  # form, kind, id
    for form in emotion_forms or []:
        if form:
            ranked.append((form, "emotion", form))
    for form, vid in matchers:
        ranked.append((form, "new", vid))
    for form, eid in extra_matchers or []:
        ranked.append((form, "extra", eid))
    ranked.sort(key=lambda x: (-len(x[0]), 0 if x[1] == "emotion" else 1 if x[1] == "new" else 2))

    tokens: list[dict] = []
    i = 0
    n = len(text)
    plain: list[str] = []

    def flush() -> None:
        nonlocal plain
        if plain:
            tokens.append({"t": "".join(plain)})
            plain = []

    while i < n:
        matched = False
        for form, kind, vid in ranked:
            if not text.startswith(form, i):
                continue
            if kind == "new":
                blocked = blocked_if_inside.get(vid, ())
                if any(text.startswith(b, i) for b in blocked if b != form):
                    continue
            flush()
            tok: dict = {"t": form}
            if kind == "new":
                tok["new"] = vid
            elif kind == "extra":
                tok["extra"] = vid
            else:
                tok["emotion"] = True
            tokens.append(tok)
            i += len(form)
            matched = True
            break
        if not matched:
            plain.append(text[i])
            i += 1
    flush()
    return tokens


def emit_lesson(
    *,
    lesson: int,
    title: str,
    title_py: str,
    title_en: str,
    vocab: list[dict],
    paras: list,
    blocked_if_inside: dict[str, tuple[str, ...]] | None = None,
    ignore_missing: set[str] | None = None,
    extras: list[dict] | None = None,
    emotions: list[dict] | None = None,
) -> dict:
    matchers = build_matchers(vocab)
    extras = extras or []
    emotions = emotions or []
    extra_matchers = sorted(
        [(e["hanzi"], e["id"]) for e in extras if e.get("hanzi")],
        key=lambda x: len(x[0]),
        reverse=True,
    )
    emotion_forms = sorted(
        [e["hanzi"] for e in emotions if e.get("hanzi")],
        key=len,
        reverse=True,
    )
    by_extra = {e["id"]: e for e in extras}

    paragraphs = []
    used: set[str] = set()
    used_extra: set[str] = set()
    used_emotion: set[str] = set()
    total = 0
    for raw in paras:
        p = _norm_para(raw)
        zh = p["zh"]
        toks = tokenize(
            zh,
            matchers,
            blocked_if_inside,
            extra_matchers=extra_matchers,
            emotion_forms=emotion_forms,
        )
        for t in toks:
            if t.get("new"):
                used.add(t["new"])
            if t.get("extra"):
                used_extra.add(t["extra"])
            if t.get("emotion"):
                used_emotion.add(t["t"])
        total += hanzi_count(zh)
        out_p = {
            "tokens": toks,
            "py": p.get("py") or "",
            "en": p.get("en") or "",
            "zh": zh,
        }
        if p.get("vi"):
            out_p["vi"] = p["vi"]
        if p.get("speaker"):
            out_p["speaker"] = p["speaker"]
        paragraphs.append(out_p)

    ignore_missing = ignore_missing or set()
    missing = [w["id"] for w in vocab if w["id"] not in used and w["id"] not in ignore_missing]
    payload = {
        "lesson": lesson,
        "title": title,
        "title_py": title_py,
        "title_en": title_en,
        "level": f"HSK 1 → Lesson {lesson}",
        "hanzi_count": total,
        "vocab": [{k: v for k, v in w.items() if k != "match"} for w in vocab],
        "extras": extras,
        "emotions": emotions,
        "script": paragraphs,
    }
    out = ROOT / "public" / "js" / f"hsk-lesson-{lesson}-data.js"
    out.parent.mkdir(parents=True, exist_ok=True)
    body = (
        f"/* Generated by scripts/_gen_hsk_lesson_{lesson}.py — do not edit by hand. */\n"
        f"window.HSK_LESSON_{lesson} = "
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + f";\nwindow.HSK_LESSON = window.HSK_LESSON_{lesson};\n"
    )
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out}")
    print(f"hanzi_count={total}")
    print(f"paragraphs={len(paragraphs)}")
    print(f"vocab={len(vocab)} used={len(used)}")
    print(f"extras used={sorted(used_extra)} / {len(extras)}")
    print(f"emotions used={sorted(used_emotion)}")
    if missing:
        print("MISSING highlights:", missing)
    unused_extra = [e["id"] for e in extras if e["id"] not in used_extra]
    if unused_extra:
        print("UNUSED extras:", unused_extra)
    return payload
