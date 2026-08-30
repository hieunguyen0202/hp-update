#!/usr/bin/env python3
"""Enrich english_words_by_lesson.json from LanGeek (EN definition, example, photo)."""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORDS_PATH = ROOT / "english_words_by_lesson.json"
VOCAB_PATH = ROOT / "english_vocab_data.json"
LOCALE = "en-VI"
USER_AGENT = "Mozilla/5.0 (compatible; hieu-portfolio/1.0)"


def norm_word(s: str) -> str:
    w = (s or "").strip().lower()
    if w.startswith("to ") and len(w) > 3:
        w = w[3:].strip()
    return w


def clean_vi_example(s: str) -> str:
    return re.sub(r"\*\*([^*]+)\*\*", r"\1", (s or "").strip())


def fetch_build_id() -> str:
    req = urllib.request.Request(
        f"https://langeek.co/{LOCALE}/vocab/subcategory/146/learn",
        headers={"User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8", errors="replace")
    m = re.search(r"/_next/static/([A-Za-z0-9_-]+)/_buildManifest", html)
    if not m:
        raise RuntimeError("Could not detect LanGeek build id")
    return m.group(1)


def fetch_lesson_cards(build_id: str, lesson_id: int) -> list[dict]:
    url = (
        f"https://langeek.co/_next/data/{build_id}/{LOCALE}/"
        f"vocab/subcategory/{lesson_id}/learn.json"
    )
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=45) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    sub = (
        data.get("pageProps", {})
        .get("initialState", {})
        .get("static", {})
        .get("subcategory", {})
    )
    return sub.get("cards") or []


def card_to_fields(card: dict) -> dict:
    mt = card.get("mainTranslation") or {}
    title = (mt.get("title") or "").strip()
    if not title:
        return {}

    def_en = (mt.get("translation") or "").strip()
    ex_en = ""
    ex_vi = ""
    examples = mt.get("examples") or []
    if examples:
        ex = examples[0]
        ex_en = (ex.get("example") or "").strip()
        loc = ex.get("localizedProperties") or {}
        ex_vi = clean_vi_example(loc.get("example") or "")

    photo = ""
    wp = mt.get("wordPhoto") or {}
    photo = (wp.get("photo") or "").strip()
    voice_us = (mt.get("titleVoice") or "").strip()

    return {
        "key": norm_word(title),
        "def_en": def_en,
        "ex_en": ex_en,
        "ex_vi": ex_vi,
        "photo": photo,
        "voice_us": voice_us,
    }


def lesson_ids_from_vocab() -> list[int]:
    data = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))
    ids: set[int] = set()
    for topic in data.get("topics", []):
        for lesson in topic.get("lessons", []):
            lid = lesson.get("id")
            if lid is not None:
                ids.add(int(lid))
    return sorted(ids)


def main() -> None:
    words_by_lesson = json.loads(WORDS_PATH.read_text(encoding="utf-8"))
    build_id = fetch_build_id()
    print("LanGeek build id:", build_id)

    lesson_ids = [int(k) for k in words_by_lesson.keys()]
    lesson_ids = sorted(set(lesson_ids) | set(lesson_ids_from_vocab()))

    enriched = 0
    missing = 0
    for i, lid in enumerate(lesson_ids, 1):
        key = str(lid)
        items = words_by_lesson.get(key)
        if not items:
            continue
        try:
            cards = fetch_lesson_cards(build_id, lid)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            print(f"WARN lesson {lid}: {e}")
            time.sleep(0.4)
            continue

        by_word: dict[str, dict] = {}
        for card in cards:
            fields = card_to_fields(card)
            if fields.get("key"):
                by_word[fields["key"]] = fields

        for item in items:
            k = norm_word(item.get("word", ""))
            src = by_word.get(k)
            if not src:
                missing += 1
                item.pop("def_en", None)
                item.pop("ex_en", None)
                item.pop("ex_vi", None)
                item.pop("photo", None)
                item.pop("voice_us", None)
                continue
            item["def_en"] = src["def_en"]
            item["ex_en"] = src["ex_en"]
            item["ex_vi"] = src["ex_vi"]
            item["photo"] = src["photo"]
            item["voice_us"] = src["voice_us"]
            if src["def_en"] or src["ex_en"]:
                enriched += 1

        if i % 20 == 0:
            print(f"  … {i}/{len(lesson_ids)} lessons")
        time.sleep(0.15)

    WORDS_PATH.write_text(
        json.dumps(words_by_lesson, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"Done — enriched {enriched} word entries, {missing} without LanGeek match in a lesson")


if __name__ == "__main__":
    main()
