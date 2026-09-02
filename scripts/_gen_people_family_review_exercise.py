#!/usr/bin/env python3
"""Generate People & Family · Linear Thinking review exercise (capstone after B2).

Grammar focus (2 topics, tied to Lesson 4 & 5):
  1. Gerunds & preferences (like/enjoy/prefer/hardly ever)
  2. Because vs because of + Conditional Type 2 (if I had to choose…)
"""
from __future__ import annotations

import html as htmlmod
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "blog" / "english" / "people-family" / "review-exercise"

_spec = importlib.util.spec_from_file_location(
    "gen_ex", Path(__file__).with_name("_gen_english_exercises.py")
)
_gen = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_gen)

esc = _gen.esc
collect_words = _gen.collect_words
TOPICS = _gen.TOPICS

GRAMMAR_REFS = [
    (
        "Gerunds, verb patterns & preferences",
        "https://www.dolenglish.vn/blog/ngu-phap-ielts",
        "Lesson 4 · Do you like X? — like/love/enjoy + V-ing, keen on, prefer…to…",
        "I enjoy spending time with my family / I prefer cooking to eating out",
    ),
    (
        "Because / because of & Conditional Type 2",
        "https://www.dolenglish.vn/blog/ngu-phap-ielts",
        "Lesson 5 · What kind of X…? — if I had to choose, I would… + lý do",
        "…because it helps me relax / because of my busy schedule / if I had to choose one, I would go for…",
    ),
]

SPEAKING_VIDEOS = [
    {
        "title": "Talking About Your Family",
        "why": "Immediate vs extended family, relationship vocabulary",
        "youtube": "https://www.youtube.com/watch?v=vXI2lRCnTKw",
        "family": "There are six people in my immediate family — my parents, my younger brother, my wife and our son.",
    },
    {
        "title": "Likes and Dislikes",
        "why": "Lesson 4 formulas — love/enjoy/keen on, hardly ever, prefer",
        "youtube": "https://www.youtube.com/watch?v=Da6MVHpabQY",
        "family": "I'm a big fan of family gatherings, but I hardly ever visit my extended family because of my busy work schedule.",
    },
    {
        "title": "How to Describe a Person",
        "why": "Part 2 — admire a family member (appearance + personality)",
        "youtube": "https://www.youtube.com/watch?v=7bdRcIpN1jU",
        "family": "My mum is quite tall and slim, with short dark hair. She's really caring and supportive.",
    },
    {
        "title": "Compare and Contrast",
        "why": "prefer…rather than… / equally / just as — family vs friends",
        "youtube": "https://www.youtube.com/watch?v=EOsxooAh9_4",
        "family": "Family and friends are equally important to me, but I prefer sharing personal problems with my sister rather than with colleagues.",
    },
]

FAMILY_IDIOMS = [
    ("blood is thicker than water", "máu mủ ruột thịt — gia đình quan trọng hơn"),
    ("like two peas in a pod", "giống nhau như đúc"),
    ("the apple of someone's eye", "người được cưng chiều nhất"),
    ("black sheep of the family", "thành viên cá biệt trong gia đình"),
    ("bring home the bacon", "kiếm tiền nuôi gia đình"),
    ("like father, like son", "con nhà tông không giống lông cũng giống cánh"),
    ("break one's neck", "cố gắng hết sức (cha mẹ vì con)"),
    ("when the blood sheds, the heart aches", "máu chảy ruột mềm"),
]

WORD_SLOTS: dict[str, list[dict]] = {
    "family_type": [
        {"form": "nuclear family", "vi": "gia đình hạt nhân"},
        {"form": "extended family", "vi": "đại gia đình"},
        {"form": "blended family", "vi": "gia đình tái hợp"},
        {"form": "close-knit family", "vi": "gia đình gắn kết"},
    ],
    "relative": [
        {"form": "my younger brother", "vi": "em trai"},
        {"form": "my older sister", "vi": "chị gái"},
        {"form": "my grandparents", "vi": "ông bà"},
        {"form": "my cousins", "vi": "anh em họ"},
        {"form": "my mother-in-law", "vi": "mẹ chồng/vợ"},
    ],
    "activity": [
        {"form": "having dinner together", "vi": "ăn tối cùng nhau"},
        {"form": "watching movies at home", "vi": "xem phim ở nhà"},
        {"form": "going on weekend trips", "vi": "đi chơi cuối tuần"},
        {"form": "cooking traditional food", "vi": "nấu món truyền thống"},
        {"form": "playing board games", "vi": "chơi board game"},
    ],
    "trait_pos": [
        {"form": "supportive", "vi": "hay hỗ trợ"},
        {"form": "caring", "vi": "chu đáo, quan tâm"},
        {"form": "reliable", "vi": "đáng tin cậy"},
        {"form": "open-minded", "vi": "cởi mở"},
        {"form": "hard-working", "vi": "chăm chỉ"},
    ],
    "trait_neg": [
        {"form": "overprotective", "vi": "bảo bọc quá mức"},
        {"form": "strict", "vi": "nghiêm khắc"},
        {"form": "stubborn", "vi": "cứng đầu"},
        {"form": "talkative", "vi": "hay nói"},
    ],
    "relationship": [
        {"form": "get on well with", "vi": "hòa thuận với"},
        {"form": "take after", "vi": "giống (người thân)"},
        {"form": "look up to", "vi": "ngưỡng mộ"},
        {"form": "rely on", "vi": "dựa vào"},
        {"form": "keep in touch with", "vi": "giữ liên lạc"},
    ],
    "life_stage": [
        {"form": "childhood", "vi": "thời thơ ấu"},
        {"form": "adolescence", "vi": "tuổi dậy thì"},
        {"form": "upbringing", "vi": "sự nuôi dưỡng"},
        {"form": "family background", "vi": "xuất thân gia đình"},
    ],
    "gathering": [
        {"form": "family gathering", "vi": "buổi họp mặt gia đình"},
        {"form": "special occasion", "vi": "dịp đặc biệt"},
        {"form": "Tet holiday", "vi": "Tết"},
        {"form": "wedding ceremony", "vi": "lễ cưới"},
    ],
    "society": [
        {"form": "traditional values", "vi": "giá trị truyền thống"},
        {"form": "gender roles", "vi": "vai trò giới tính"},
        {"form": "nuclear households", "vi": "hộ gia đình nhỏ"},
        {"form": "aging population", "vi": "dân số già hóa"},
    ],
}


def collect_review_words() -> list[dict]:
    topic = next(t for t in TOPICS["topics"] if t["slug"] == "people-family")
    by_level: dict[str, list[dict]] = {}
    for level in ("A1", "A2", "B1", "B2"):
        lessons = [l for l in topic["lessons"] if l["level"] == level]
        by_level[level] = collect_words([l["id"] for l in lessons])
    return by_level["B1"] + by_level["B2"] + by_level["A2"][:15] + by_level["A1"][:8]


def slot_select(slot_id: str, default_idx: int = 0) -> str:
    opts = WORD_SLOTS[slot_id]
    idx = min(default_idx, len(opts) - 1)
    options = "\n".join(
        f'<option value="{esc(o["form"])}"{" selected" if i == idx else ""}>'
        f'{esc(o["form"])} — {esc(o["vi"])}</option>'
        for i, o in enumerate(opts)
    )
    return (
        f'<select class="lr-word-pick" data-slot="{esc(slot_id)}" data-kind="vocab" '
        f'aria-label="Choose vocabulary">{options}</select>'
    )


def grammar_section() -> str:
    parts = []
    for title, url, hint, ex in GRAMMAR_REFS:
        parts.append(
            f"""        <a class="lr-grammar-card lr-grammar-card--link" href="{esc(url)}" target="_blank" rel="noopener noreferrer">
          <h3>{esc(title)}</h3>
          <p class="lr-grammar-hint">{esc(hint)}</p>
          <p class="lr-grammar-ex"><em>{esc(ex)}</em></p>
          <span class="lr-grammar-cta">Đọc trên DOL English →</span>
        </a>"""
        )
    return "\n".join(parts)


def mind_map_html() -> str:
    return """
      <div class="lr-mmap lr-mmap--grammar" id="grammarMindmap" aria-label="Sơ đồ tư duy ngữ pháp People & Family" style="--mmap-min:920px">
        <p class="lr-mmap-scroll-hint">Vuốt ngang nếu sơ đồ rộng hơn màn hình</p>
        <div class="lr-mmap-viewport">
          <div class="lr-mmap-board">
            <svg class="lr-mmap-svg" aria-hidden="true"></svg>
            <div class="lr-mmap-root" data-mmap-node="root">
              <div class="lr-mmap-root-title">People &amp; Family</div>
              <div class="lr-mmap-root-sub">Lesson 4 &amp; 5</div>
            </div>
            <div class="lr-mmap-col lr-mmap-col--right">
              <div class="lr-mmap-branch" data-mmap-branch="gerunds" style="--mmap-c:#22d3ee">
                <div class="lr-mmap-tense lr-mmap-tense--starred" data-mmap-node="tense">
                  <span class="lr-mmap-num">1</span><strong>Gerunds &amp; preferences</strong>
                  <span class="lr-mmap-star" title="Lesson 4 · Do you like X?">★</span>
                </div>
                <div class="lr-mmap-forks">
                  <div class="lr-mmap-group">
                    <span class="lr-mmap-fork" data-mmap-node="fork">Yes</span>
                    <ul class="lr-mmap-leaves">
                      <li class="lr-mmap-leaf" data-mmap-node="leaf"><span class="lr-mmap-k">Verb</span> I + like/love/enjoy + <strong>V-ing</strong></li>
                      <li class="lr-mmap-leaf" data-mmap-node="leaf"><span class="lr-mmap-k">Adj</span> I'm keen on / interested in + N/V-ing</li>
                      <li class="lr-mmap-leaf" data-mmap-node="leaf"><span class="lr-mmap-k">Noun</span> I'm a big fan of + N/V-ing</li>
                      <li class="lr-mmap-leaf" data-mmap-node="leaf"><span class="lr-mmap-k">FAVOURITE</span> My favourite … is/are + who/when/where</li>
                    </ul>
                  </div>
                  <div class="lr-mmap-group">
                    <span class="lr-mmap-fork" data-mmap-node="fork">No</span>
                    <ul class="lr-mmap-leaves">
                      <li class="lr-mmap-leaf" data-mmap-node="leaf">No, not really / I don't enjoy + V-ing</li>
                      <li class="lr-mmap-leaf" data-mmap-node="leaf"><span class="lr-mmap-k">HARDLY EVER</span> I hardly ever + V</li>
                      <li class="lr-mmap-leaf" data-mmap-node="leaf"><span class="lr-mmap-k">prefer</span> prefer V-ing <strong>to</strong> V-ing</li>
                      <li class="lr-mmap-leaf" data-mmap-node="leaf">prefer to V <strong>rather than</strong> V (bare)</li>
                    </ul>
                  </div>
                </div>
              </div>
              <div class="lr-mmap-branch" data-mmap-branch="reasons" style="--mmap-c:#a78bfa">
                <div class="lr-mmap-tense lr-mmap-tense--starred" data-mmap-node="tense">
                  <span class="lr-mmap-num">2</span><strong>Reasons &amp; hypothetical choice</strong>
                  <span class="lr-mmap-star" title="Lesson 5 · What kind of X…?">★</span>
                </div>
                <div class="lr-mmap-forks">
                  <div class="lr-mmap-group">
                    <span class="lr-mmap-fork" data-mmap-node="fork">Lý do</span>
                    <ul class="lr-mmap-leaves">
                      <li class="lr-mmap-leaf" data-mmap-node="leaf"><span class="lr-mmap-k">Clause</span> because / This is because + <strong>S + V</strong></li>
                      <li class="lr-mmap-leaf" data-mmap-node="leaf"><span class="lr-mmap-k">Noun</span> because of + <strong>noun phrase</strong></li>
                      <li class="lr-mmap-leaf" data-mmap-node="leaf">V-ing làm chủ ngữ: Spending time with family <strong>is</strong> relaxing</li>
                    </ul>
                  </div>
                  <div class="lr-mmap-group">
                    <span class="lr-mmap-fork" data-mmap-node="fork">Chọn loại (L5)</span>
                    <ul class="lr-mmap-leaves">
                      <li class="lr-mmap-leaf" data-mmap-node="leaf">I like … most.</li>
                      <li class="lr-mmap-leaf" data-mmap-node="leaf">if I <strong>had</strong> to choose one, I <strong>would</strong> go for…</li>
                      <li class="lr-mmap-leaf" data-mmap-node="leaf">it would have to be … / I would opt for …</li>
                      <li class="lr-mmap-leaf" data-mmap-node="leaf"><span class="lr-mmap-k">Modal</span> would = chưa chắc · will = chắc chắn hơn</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>"""


def videos_html() -> str:
    items = []
    for v in SPEAKING_VIDEOS:
        vid = re.search(r"v=([\w-]+)", v["youtube"])
        embed = f'https://www.youtube.com/embed/{vid.group(1)}' if vid else v["youtube"]
        items.append(
            f"""        <li class="lr-lesson-item">
          <div class="lr-lesson-head">
            <h3>{esc(v["title"])}</h3>
            <p class="lr-lesson-why">{esc(v["why"])}</p>
          </div>
          <div class="lr-lesson-embed">
            <iframe src="{esc(embed)}" title="{esc(v["title"])}" loading="lazy" allowfullscreen></iframe>
          </div>
          <p class="lr-lesson-practice"><strong>Family practice:</strong> {esc(v["family"])}</p>
          <p class="ex-vi lr-lesson-vi"><strong>VI:</strong> (đọc lại câu trên bằng tiếng Việt khi bật Vietnamese)</p>
        </li>"""
        )
    return "\n".join(items)


def lesson_highlights_html() -> str:
    return """
        <div class="lr-formula-grid">
          <article class="lr-formula-card" id="lesson-4">
            <h3>Lesson 4 · Do you like X?</h3>
            <p class="lr-formula-q">Do you like spending time with your family?</p>
            <table class="lr-table">
              <thead><tr><th>Yes</th><th>No + HARDLY EVER + prefer</th></tr></thead>
              <tbody>
                <tr><td>Yes, definitely — I <strong>love enjoying</strong> → I <strong>love spending</strong> time with my family.</td>
                    <td>No, not really. I <strong>hardly ever</strong> visit relatives. I <strong>prefer staying</strong> at home <strong>to going</strong> to big parties.</td></tr>
              </tbody>
            </table>
            <details class="lr-example">
              <summary>Model answer (family)</summary>
              <p>Yes, absolutely. I'm a big fan of family gatherings. <strong>My favourite thing</strong> is having dinner with my parents at the weekend because it helps me unwind and forget work pressure.</p>
              <p class="ex-vi">Vâng, chắc chắn. Tôi rất thích các buổi sum họp gia đình. Điều tôi thích nhất là ăn tối với bố mẹ vào cuối tuần vì điều đó giúp tôi thư giãn và quên áp lực công việc.</p>
            </details>
          </article>
          <article class="lr-formula-card" id="lesson-5">
            <h3>Lesson 5 · What kind of X do you like most?</h3>
            <p class="lr-formula-q">What kind of family activities do you like most?</p>
            <table class="lr-table">
              <thead><tr><th>Loại gì?</th><th>Lý do</th></tr></thead>
              <tbody>
                <tr><td>I love all kinds of activities, but if I <strong>had</strong> to choose one, I <strong>would opt for</strong> cooking together.</td>
                    <td><strong>This is because</strong> it gives us a chance to talk and strengthen our bond.</td></tr>
              </tbody>
            </table>
            <details class="lr-example">
              <summary>Model answer (family)</summary>
              <p>Well, I love all kinds of family activities, but if I had to choose one, it would have to be going on short trips together. This is because travelling helps us create shared memories and understand each other better.</p>
              <p class="ex-vi">Tôi thích mọi hoạt động gia đình, nhưng nếu phải chọn một, đó sẽ là những chuyến đi ngắn cùng nhau. Điều này là vì du lịch giúp chúng tôi tạo kỷ niệm chung và hiểu nhau hơn.</p>
            </details>
            <p class="lr-note-tip"><strong>prefer:</strong> prefer V-ing <strong>to</strong> V-ing · prefer to V <strong>rather than</strong> V (bare infinitive)</p>
          </article>
        </div>"""


def idioms_html() -> str:
    rows = []
    for en, vi in FAMILY_IDIOMS:
        rows.append(f"<tr><td><strong>{esc(en)}</strong></td><td>{esc(vi)}</td></tr>")
    return f"""
        <table class="lr-table lr-table--idioms">
          <thead><tr><th>Idiom / phrase</th><th>Nghĩa</th></tr></thead>
          <tbody>{"".join(rows)}</tbody>
        </table>
        <p class="lr-ref">Nguồn: <a href="https://www.dolenglish.vn/blog/family-ielts-speaking" target="_blank" rel="noopener noreferrer">DOL — Family IELTS Speaking</a> · <a href="https://ielts.idp.com/vietnam/about/news-and-articles/article-talk-about-your-family" target="_blank" rel="noopener noreferrer">IDP — Talk about your family</a></p>"""


def vocab_chains_html(words: list[dict]) -> str:
    chains = [
        ("nuclear family", "parents", "siblings", "upbringing"),
        ("extended family", "cousins", "grandparents", "family gathering"),
        ("get on well with", "supportive", "rely on", "keep in touch"),
        ("look up to", "take after", "role model", "influence"),
    ]
    parts = ['<div class="lr-chain-grid">']
    for chain in chains:
        chips = " → ".join(f'<span class="lr-chain-chip">{esc(w)}</span>' for w in chain)
        parts.append(f'<div class="lr-chain">{chips}</div>')
    parts.append("</div>")
    chips = []
    for w in words[:48]:
        ipa = f' <span class="ipa">/{esc(w["ipa"])}/</span>' if w.get("ipa") else ""
        vi = f' — {esc(w["vi"])}' if w.get("vi") else ""
        chips.append(f'<li><mark class="vocab">{esc(w["form"])}</mark>{ipa}{vi}</li>')
    parts.append(
        f"""<details class="lr-vocab-bank">
          <summary>Vocabulary bank ({len(words)} words · B1/B2 focus)</summary>
          <ul class="ex-vocab-list">{"".join(chips)}</ul>
        </details>"""
    )
    return "\n".join(parts)


def speaking_mock_html() -> str:
    p1 = [
        (
            "Do you have a large or small family?",
            "Bạn có gia đình đông hay ít người?",
            (
                "I'd say I come from a fairly large family. Besides my "
                f'{slot_select("relative", 0)}, I have many cousins in my '
                f'{slot_select("family_type", 1)}. '
                '<span class="lr-tense-tag">There are… · family types</span>'
            ),
        ),
        (
            "How much time do you spend with your family?",
            "Bạn dành bao nhiêu thời gian cho gia đình?",
            (
                "Honestly, not as much as I'd like because of my busy schedule, "
                "but I try to see them every weekend. We usually enjoy "
                f'{slot_select("activity", 0)}. '
                '<span class="lr-tense-tag">because of + noun · try to + V</span>'
            ),
        ),
        (
            "What do you like to do together as a family?",
            "Gia đình bạn thích làm gì cùng nhau?",
            (
                "Yes, definitely — I <strong>love</strong> "
                f'{slot_select("activity", 2)} because it gives us the chance to relax together. '
                '<span class="lr-tense-tag">love + V-ing · because + S + V</span>'
            ),
        ),
        (
            "Do you get along well with your family?",
            "Bạn có hòa thuận với gia đình không?",
            (
                "Yes, absolutely. I "
                f'{slot_select("relationship", 0)} most of my relatives, especially my parents. '
                "They're really "
                f'{slot_select("trait_pos", 1)} and '
                f'{slot_select("trait_pos", 2)}. '
                '<span class="lr-tense-tag">get on well · personality adj</span>'
            ),
        ),
        (
            "Who are you closest to in your family?",
            "Bạn thân nhất với ai trong gia đình?",
            (
                "Definitely my older sister. I "
                f'{slot_select("relationship", 3)} her whenever I have problems, and I really '
                f'{slot_select("relationship", 2)} her because she has been my role model since '
                f'{slot_select("life_stage", 0)}. '
                '<span class="lr-tense-tag">rely on · look up to</span>'
            ),
        ),
        (
            "Do you prefer spending time with family or friends?",
            "Bạn thích ở với gia đình hay bạn bè hơn?",
            (
                "That's tough — both matter. I "
                "<strong>prefer sharing</strong> personal news with my family "
                "<strong>rather than</strong> posting online, but I "
                f'<strong>prefer going</strong> out with friends <strong>to</strong> staying home sometimes. '
                '<span class="lr-tense-tag">prefer V-ing to V-ing</span>'
            ),
        ),
        (
            "What kind of family activities do you like most?",
            "Bạn thích loại hoạt động gia đình nào nhất?",
            (
                "Well, I love all kinds of activities, but if I <strong>had</strong> to choose one, "
                f'I <strong>would opt for</strong> {slot_select("activity", 3)}. '
                "<strong>This is because</strong> it reminds me of my "
                f'{slot_select("life_stage", 2)}. '
                '<span class="lr-tense-tag">Conditional 2 · because clause</span>'
            ),
        ),
        (
            "Is family important in your country?",
            "Gia đình có quan trọng ở nước bạn không?",
            (
                "Yes, definitely. Most people still respect "
                f'{slot_select("society", 0)}, although '
                f'{slot_select("society", 2)} are becoming more common in big cities. '
                '<span class="lr-tense-tag">although · society vocab</span>'
            ),
        ),
    ]

    p2_en = (
        "I'd like to talk about a family member I really admire — my mother. "
        f"She's quite tall and slim, with short dark hair, and she's incredibly "
        f'{slot_select("trait_pos", 0)}. '
        f"What I admire most is that she always "
        f'{slot_select("relationship", 1)} her own parents — she is patient and '
        f'{slot_select("trait_pos", 4)}. '
        f"When I was in {slot_select('life_stage', 1)}, she would "
        f"encourage me to study hard without being too "
        f'{slot_select("trait_neg", 0)}. '
        f"One special moment was during a {slot_select('gathering', 0)} last "
        f"{slot_select('gathering', 2)} — the whole family cooked together, and "
        "<strong>what I enjoyed most</strong> was seeing everyone laugh. "
        "Looking back, she has had a huge influence on who I am today."
    )

    p3 = [
        (
            "How have families changed in your country?",
            "Gia đình ở nước bạn đã thay đổi thế nào?",
            (
                "I think they've changed quite a bit. More "
                f'{slot_select("society", 2)} live in cities, and '
                f'{slot_select("society", 1)} are less rigid than before. '
                '<span class="lr-tense-tag">Present Perfect · society</span>'
            ),
        ),
        (
            "Should husbands and wives have different roles?",
            "Vợ chồng có nên có vai trò khác nhau không?",
            (
                "Not necessarily. Couples should share household chores and support each other. "
                f'In modern families, both partners may {slot_select("relationship", 4)} '
                "their careers equally. "
                '<span class="lr-tense-tag">modal · equality</span>'
            ),
        ),
        (
            "Which are more important: family or friends?",
            "Gia đình hay bạn bè quan trọng hơn?",
            (
                "For me, family comes first because of the bond we share, "
                "but close friends are equally valuable. "
                '<span class="lr-tense-tag">because of · comparison</span>'
            ),
        ),
        (
            "What role do grandparents play?",
            "Ông bà đóng vai trò gì trong gia đình?",
            (
                "They often help raise grandchildren and pass down "
                f'{slot_select("society", 0)}. Many children '
                f'{slot_select("relationship", 1)} their grandparents in personality. '
                '<span class="lr-tense-tag">take after · traditions</span>'
            ),
        ),
    ]

    def part_block(title: str, qs: list, part_id: str) -> str:
        cards = []
        for i, (en, vi, ans) in enumerate(qs, 1):
            cards.append(
                f"""          <article class="lr-mock-q" id="{part_id}-q{i}">
            <h4>Q{i}. {esc(en)}</h4>
            <p class="ex-vi lr-mock-vi">{esc(vi)}</p>
            <div class="lr-mock-answer">{ans}</div>
          </article>"""
            )
        return f"""        <div class="lr-mock-part" id="{part_id}">
          <h3>{esc(title)}</h3>
{chr(10).join(cards)}
        </div>"""

    p2_block = f"""        <div class="lr-mock-part" id="part2">
          <h3>Part 2 · Cue card</h3>
          <p class="lr-mock-cue"><strong>Describe a family member you admire.</strong> You should say who they are, what they look like, what they are like, and explain why you admire them.</p>
          <p class="ex-vi lr-mock-vi">Mô tả một thành viên gia đình bạn ngưỡng mộ — ai, ngoại hình, tính cách, vì sao.</p>
          <article class="lr-mock-q" id="part2-answer">
            <div class="lr-mock-answer">{p2_en}</div>
          </article>
        </div>"""

    return (
        part_block("Part 1 · Family & friends", p1, "part1")
        + "\n"
        + p2_block
        + "\n"
        + part_block("Part 3 · Discussion", p3, "part3")
    )


def natural_vlog_html() -> str:
    return """
      <section class="lr-section lr-vlog-section" id="natural-vlog">
        <h2>0 · Real talk — Family life vlog</h2>
        <p class="lr-section-hint">Văn nói tự sự kiểu TikTok / daily vlog — không phải IELTS script. Nghe nhịp tự nhiên với filler. Bật <strong>Vietnamese</strong> ở trên để xem bản dịch.</p>
        <blockquote class="lr-vlog" cite="family-vlog">
          <p class="lr-vlog-text"><mark class="lr-filler">So</mark> um today I wanted to talk about my family, <mark class="lr-filler">like</mark> nothing fancy, just <mark class="lr-filler">kind of</mark> a real update — <mark class="lr-filler">you know</mark> how everyone always asks "how's your family?" and you're <mark class="lr-filler">like</mark> where do I even start?</p>
          <p class="lr-vlog-text"><mark class="lr-filler">Yeah</mark> we're a pretty typical Vietnamese family, I guess — my parents still live in the same house I grew up in, my sister moved to another city for work, and <mark class="lr-filler">honestly</mark> we don't see each other as much as we used to, which <mark class="lr-filler">kind of</mark> sucks sometimes.</p>
          <p class="lr-vlog-text">But whenever we do meet up, it's always the same vibe — mum cooks way too much food, dad asks the same questions about my job, and my sister and I just sit there <mark class="lr-filler">like</mark> okay, this is home, <mark class="lr-filler">I mean</mark> it's chaotic but in a good way.</p>
          <p class="lr-vlog-text"><mark class="lr-filler">I think</mark> what I miss most is those random Sunday lunches, not the big holidays or anything — just <mark class="lr-filler">like</mark> sitting on the floor, eating rice, complaining about traffic, <mark class="lr-filler">you know</mark>? Super normal stuff that you don't appreciate until you're not there every week.</p>
          <p class="lr-vlog-text"><mark class="lr-filler">Anyway</mark> if you're watching this and you still live with your family, <mark class="lr-filler">like</mark> enjoy it while you can — call your parents, eat the extra portion, don't scroll through your phone the whole time. <mark class="lr-filler">Trust me</mark> on that one.</p>
          <p class="ex-vi lr-vlog-vi">Hôm nay mình muốn nói về gia đình — không phải kiểu formal, chỉ update thật thôi. Kiểu ai cũng hỏi "gia đình thế nào?" mà không biết bắt đầu từ đâu. Gia đình mình khá điển hình kiểu Việt: bố mẹ vẫn ở nhà cũ, chị gái ra thành phố khác làm, gặp nhau ít hơn trước — hơi buồn. Nhưng mỗi lần gặp vẫn y chang: mẹ nấu quá nhiều, bố hỏi lại công việc, hai chị em ngồi đó kiểu "ừ, đây là nhà" — hơi hỗn nhưng ấm. Mình nhớ nhất những bữa trưa Chủ nhật bình thường: ngồi sàn, ăn cơm, than phiền kẹt xe — chuyện nhỏ mà đi xa mới thấy quý. Nếu bạn còn sống với gia đình thì tận hưởng đi: gọi bố mẹ, ăn thêm miếng, đừng cắm điện thoại suốt bữa.</p>
        </blockquote>
        <p class="lr-note-tip">Tip: Giọng hơi trầm, nói nhanh nhẹ ở filler — <em>kind of</em> → <em>kinda</em>, <em>you know</em> rút gọn nhẹ cuối câu.</p>
      </section>"""


def build_page() -> str:
    words = collect_review_words()
    home = "../../../../"
    slots_json = json.dumps(WORD_SLOTS, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Review Exercise · People &amp; Family — The Quiet Corner</title>
  <meta name="description" content="Linear Thinking review: gerunds &amp; preferences, reasons &amp; conditionals, and IELTS Speaking mock for People &amp; Family.">
  <link rel="icon" href="{home}favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{home}css/docs.css?v=lr24">
</head>
<body class="docs lr-body">
  <div class="cursor" id="cursor"></div>
  <div class="cursor-ring" id="cursorRing"></div>
  <canvas id="matrix-canvas"></canvas>
  <div class="grid-bg"></div>
  <header class="docs-topbar">
    <button class="docs-menu-btn" id="docsMenuBtn" type="button">menu</button>
    <button class="docs-sidebar-toggle" id="docsSidebarToggle" type="button" aria-expanded="true" title="Thu thanh điều hướng">nav ◂</button>
    <a class="docs-brand" href="{home}"><span>✦</span> The Quiet Corner <span>✦</span></a>
    <nav class="docs-series">
      <a href="{home}blog/web-security/">DevSecOps</a>
      <a href="{home}blog/kubestronaut/">Kubestronaut</a>
      <a class="active" href="../../">English</a>
      <a href="{home}blog/tech-hub/">Tech Hub</a>
    </nav>
    <span class="docs-topbar-spacer"></span>
    <a class="docs-top-link" href="{home}#blogs">blogs</a>
  </header>
  <div class="docs-shell docs-shell--wide">
    <aside class="docs-sidebar" id="docsSidebar" data-nav="english" data-docs-root="../../" data-active="people-family">
      <div class="docs-nav-label">English</div>
      <ul class="docs-nav" id="docsNav">
        <li><a href="../../">All topics</a></li>
        <li><a href="../">People &amp; Family</a></li>
        <li><a class="active" href="./">Review Exercise</a></li>
      </ul>
    </aside>
    <article class="docs-main lr-page">
      <div class="docs-breadcrumb">
        <a href="{home}">Home</a><span>›</span>
        <a href="{home}#blogs">Blogs</a><span>›</span>
        <a href="../../">English</a><span>›</span>
        <a href="../">People &amp; Family</a><span>›</span>
        <span>Review Exercise</span>
      </div>

      <header class="lr-hero">
        <p class="lr-hero-badge">Linear Thinking · Capstone</p>
        <h1>People &amp; Family — Review Exercise</h1>
        <p class="lede">Sau B2, ôn theo <a href="https://www.dolenglish.vn/blog/linearthinking-trong-speaking" target="_blank" rel="noopener noreferrer">Linear Thinking</a>: <strong>2 chủ điểm ngữ pháp</strong> (gerunds &amp; preferences · because/conditional 2) gắn <strong>Lesson 4 &amp; 5</strong> → sơ đồ tư duy → video → mock IELTS Part 1/2/3 (dropdown từ B1/B2).</p>
        <nav class="lr-toc" aria-label="On this page">
          <a href="#natural-vlog">0 · Real talk</a>
          <a href="#grammar">1 · Grammar</a>
          <a href="#mental-model">2 · Mind map</a>
          <a href="#videos">3 · Videos</a>
          <a href="#lessons">4 · Lesson highlights</a>
          <a href="#family-lang">5 · Idioms</a>
          <a href="#vocab-chains">6 · Vocab chains</a>
          <a href="#practice">7 · Practice</a>
          <a href="#mock-test">8 · Mock test</a>
        </nav>
        <div class="ex-toolbar lr-toolbar lr-toolbar--hero">
          <label class="ex-toggle"><input type="checkbox" id="togVi" /> Vietnamese</label>
        </div>
      </header>

{natural_vlog_html()}

      <section class="lr-section" id="grammar">
        <h2>1 · Grammar foundations (2 chủ điểm)</h2>
        <p class="lr-section-hint">Chọn từ <a href="https://www.dolenglish.vn/blog/ngu-phap-ielts" target="_blank" rel="noopener noreferrer">DOL — Ngữ pháp IELTS</a> và <a href="https://ielts-fighter.com/tin-tuc/grammar_c16.html" target="_blank" rel="noopener noreferrer">IELTS Fighter — Grammar</a>, gắn Lesson 4 (<em>Do you like X?</em>) và Lesson 5 (<em>What kind of X…?</em>).</p>
        <div class="lr-grammar-list">
{grammar_section()}
        </div>
      </section>

      <section class="lr-section" id="mental-model">
        <h2>2 · Mind map — Grammar for family speaking</h2>
        <p class="lr-section-hint">Hai nhánh chính: <strong>thích / không thích</strong> (gerund &amp; prefer) và <strong>lý do / chọn loại</strong> (because · conditional 2). <span class="lr-mmap-star">★</span> = công thức Lesson 4 &amp; 5.</p>
{mind_map_html()}
      </section>

      <section class="lr-section" id="videos">
        <h2>3 · Video — Spoken English Lessons</h2>
        <p class="lr-section-hint">Playlist <a href="https://www.youtube.com/playlist?list=PLD6t6ckHsruYoalxbzcjX1TNn4h7ShiRk" target="_blank" rel="noopener noreferrer">Oxford Online English · Spoken English Lessons</a> — family, likes/dislikes, describe a person, compare.</p>
        <ul class="lr-lesson-list">
{videos_html()}
        </ul>
      </section>

      <section class="lr-section" id="lessons">
        <h2>4 · Core formulas — Lesson 4 &amp; 5</h2>
        <p class="lr-section-hint">Công thức <strong>IELTS Nguyễn Huyền</strong> áp dụng cho chủ đề People &amp; Family.</p>
{lesson_highlights_html()}
      </section>

      <section class="lr-section" id="family-lang">
        <h2>5 · Idioms &amp; phrases — Family</h2>
        <p class="lr-section-hint">Dùng 1–2 idiom trong Part 2/3 — không nhồi hết.</p>
{idioms_html()}
      </section>

      <section class="lr-section" id="vocab-chains">
        <h2>6 · Vocab chains (B1/B2)</h2>
        <p class="lr-section-hint">Chuỗi từ theo chủ đề — kết hợp dropdown trong mock test bên dưới.</p>
{vocab_chains_html(words)}
      </section>

      <section class="lr-section" id="practice">
        <h2>7 · Practice — People &amp; Family</h2>
        <p class="lr-section-hint">Tham khảo câu hỏi &amp; bài mẫu: <a href="https://www.dolenglish.vn/blog/family-ielts-speaking" target="_blank" rel="noopener noreferrer">DOL</a> · <a href="https://zim.vn/ielts-speaking-part-1-family-and-friends-1" target="_blank" rel="noopener noreferrer">ZIM</a> · <a href="https://ielts.idp.com/vietnam/about/news-and-articles/article-talk-about-your-family" target="_blank" rel="noopener noreferrer">IDP</a>.</p>
        <div class="lr-practice-grid">
          <article class="lr-practice-card">
            <h3>Part 1 warm-up</h3>
            <ol>
              <li>Do you have a large or small family?</li>
              <li>How much time do you spend with your family?</li>
              <li>What do you like to do together as a family?</li>
              <li>Do you get along well with your family?</li>
              <li>Who are you closest to in your family?</li>
            </ol>
            <p class="lr-practice-tip">Dùng <strong>Yes/No + FAVOURITE</strong> hoặc <strong>hardly ever + prefer</strong> (Lesson 4).</p>
          </article>
          <article class="lr-practice-card">
            <h3>Part 2 cue cards</h3>
            <ul>
              <li>Describe a family member you admire</li>
              <li>Describe a family member who has influenced you</li>
              <li>Describe a happy family event</li>
            </ul>
            <p class="lr-practice-tip">Kết hợp Lesson 06 (describe a person) + idioms nhẹ.</p>
          </article>
          <article class="lr-practice-card">
            <h3>Part 3 discussion</h3>
            <ul>
              <li>How have families changed in your country?</li>
              <li>Should husbands and wives have different roles?</li>
              <li>Family or friends — which is more important?</li>
              <li>What role do grandparents play?</li>
            </ul>
            <p class="lr-practice-tip">Dùng <strong>if I had to choose</strong> + <strong>because/because of</strong> (Lesson 5).</p>
          </article>
        </div>
      </section>

      <section class="lr-section" id="mock-test">
        <h2>8 · Mock IELTS Speaking — dropdown từ vựng</h2>
        <p class="lr-section-hint">Đổi từ trong dropdown để luyện paraphrase. Grammar tags gắn Lesson 4 &amp; 5.</p>
        <div class="lr-mock">
{speaking_mock_html()}
        </div>
      </section>

      <p class="lr-ref lr-ref--footer">Nguồn: IELTS Nguyễn Huyền (Lesson 4 &amp; 5) · DOL · ZIM · IDP · Oxford Online English playlist.</p>
    </article>
  </div>
  <script>
    window.LR_WORD_SLOTS = {slots_json};
  </script>
  <script src="{home}js/docs.js"></script>
  <script src="{home}js/linear-review.js?v=lr24"></script>
</body>
</html>"""


def patch_topic_index() -> None:
    path = ROOT / "public" / "blog" / "english" / "people-family" / "index.html"
    text = path.read_text(encoding="utf-8")
    if 'id="review"' in text:
        return
    review_section = """
      <section class="vocab-level vocab-level--review" id="review">
        <div class="vocab-level__head">
          <span class="vocab-level__badge vocab-level__badge--review">Review</span>
          <h2>Linear Thinking · Capstone exercise</h2>
        </div>
        <p class="vocab-level__desc">Sau B2 — ôn ngữ pháp (gerunds &amp; preferences, because/conditional 2), mind map, Lesson 4/5, và mock IELTS Part 1/2/3 (từ vựng B1/B2, dropdown thay từ).</p>
        <div class="vocab-lesson-grid">
          <a class="vocab-lesson-card vocab-lesson-card--review" href="review-exercise/">
            <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 72 72' fill='none'%3E%3Crect width='72' height='72' rx='14' fill='%231a1033'/%3E%3Ccircle cx='36' cy='36' r='22' stroke='%23a78bfa' stroke-width='2.5'/%3E%3Cpath d='M36 20v16l10 8' stroke='%2322d3ee' stroke-width='2.5' stroke-linecap='round'/%3E%3Cpath d='M22 48h28' stroke='%23e4e4e7' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E" alt="" width="72" height="72" loading="lazy">
            <span>Review Exercise</span>
          </a>
        </div>
      </section>
"""
    marker = '      <div class="docs-pager">'
    if marker in text:
        text = text.replace(marker, review_section + "\n" + marker)
        path.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(build_page(), encoding="utf-8")
    patch_topic_index()
    print("Wrote", OUT / "index.html")


if __name__ == "__main__":
    main()
