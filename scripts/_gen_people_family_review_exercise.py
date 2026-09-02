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

_food_spec = importlib.util.spec_from_file_location(
    "food_rev", Path(__file__).with_name("_gen_food_review_exercise.py")
)
_food = importlib.util.module_from_spec(_food_spec)
assert _food_spec and _food_spec.loader
_food_spec.loader.exec_module(_food)
mind_map_html = _food.mind_map_html

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
    "family_idiom": [
        {"form": "blood is thicker than water", "vi": "máu mủ ruột thịt"},
        {"form": "like two peas in a pod", "vi": "giống nhau như đúc"},
        {"form": "the apple of someone's eye", "vi": "người được cưng chiều"},
        {"form": "black sheep of the family", "vi": "thành viên cá biệt"},
        {"form": "like father, like son", "vi": "con nhà tông không giống lông cũng giống cánh"},
    ],
}

GRAMMAR_MINDMAP_LEFT = [
    {
        "id": "gerunds-yes",
        "color": "#6ee7b7",
        "name": "Gerunds & YES",
        "name_vi": "Lesson 4 · thích",
        "speaking": True,
        "forks": [
            {
                "label": "Cấu trúc",
                "leaves": [
                    ("Verb", "I like / love / enjoy + <strong>V-ing</strong>"),
                    ("Adj", "I'm keen on / interested in + N/V-ing"),
                    ("NP", "I'm a big fan of + N/V-ing"),
                ],
            },
            {
                "label": "FAVOURITE",
                "leaves": [
                    "My favourite … is/are + who/when/where",
                    "Family: My favourite thing is having dinner with my parents",
                ],
            },
        ],
    },
]

GRAMMAR_MINDMAP_RIGHT = [
    {
        "id": "gerunds-no",
        "color": "#fca5a5",
        "name": "NO + prefer",
        "name_vi": "Lesson 4 · không thích",
        "forks": [
            {
                "label": "Phủ định",
                "leaves": [
                    "No, not really · I don't enjoy + V-ing",
                    "I'm not keen on …",
                ],
            },
            {
                "label": "Mở rộng",
                "leaves": [
                    ("HARDLY EVER", "I hardly ever + V"),
                    ("prefer", "prefer V-ing <strong>to</strong> V-ing"),
                    ("rather than", "prefer to V <strong>rather than</strong> V"),
                ],
            },
        ],
    },
    {
        "id": "reasons-cond",
        "color": "#a78bfa",
        "name": "Reasons & Type 2",
        "name_vi": "Lesson 5",
        "speaking": True,
        "forks": [
            {
                "label": "Lý do",
                "leaves": [
                    ("Clause", "because / This is because + <strong>S + V</strong>"),
                    ("Noun", "because of + <strong>noun phrase</strong>"),
                ],
            },
            {
                "label": "Chọn loại",
                "leaves": [
                    "if I <strong>had</strong> to choose one, I <strong>would</strong> go for…",
                    "it would have to be … / I would opt for …",
                    "would = chưa chắc · will = chắc chắn hơn",
                ],
            },
        ],
    },
]


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
    cards = []
    for title, url, vi_use, ex in GRAMMAR_REFS:
        cards.append(
            f"""        <a class="lr-grammar-card lr-grammar-card--link" href="{esc(url)}" target="_blank" rel="noopener noreferrer">
          <strong>{esc(title)}</strong>
          <p>{esc(vi_use)}</p>
          <p class="lr-grammar-ex"><em>e.g.</em> {esc(ex)}</p>
          <span class="lr-card-cta">Read on DOL English ↗</span>
        </a>"""
        )
    return "\n".join(cards)


def grammar_mind_map_section() -> str:
    return mind_map_html(
        "grammarMindmap",
        "Sơ đồ tư duy ngữ pháp People & Family",
        "People & Family",
        "Lesson 4 & 5",
        GRAMMAR_MINDMAP_LEFT,
        GRAMMAR_MINDMAP_RIGHT,
        note="Trái = <strong>thích</strong> · Phải = <strong>không thích + lý do + chọn loại</strong>. <span class='lr-mmap-star'>★</span> = công thức trong mock test.",
        extra_class=" lr-mmap--lesson3",
        min_width="1180px",
    )


def speaking_lessons_html() -> str:
    rows = []
    for v in SPEAKING_VIDEOS:
        rows.append(
            f"""        <li class="lr-lesson-card">
          <div class="lr-lesson-head">
            <strong>{esc(v["title"])}</strong>
            <a class="lr-video-link" href="{esc(v["youtube"])}" target="_blank" rel="noopener noreferrer">Watch video ↗</a>
            <span class="lr-lesson-why">{esc(v["why"])}</span>
          </div>
          <details class="lr-lesson-notes">
            <summary>Family practice — example sentence</summary>
            <p class="lr-catchup-hint">Xem video trước, sau đó đọc câu mẫu và tự nói lại — áp dụng công thức Lesson 4 &amp; 5.</p>
            <p class="lr-food-ex"><strong>Family:</strong> {esc(v["family"])}</p>
          </details>
        </li>"""
        )
    return "\n".join(rows)


def lesson_highlights_html() -> str:
    l4_practice = f"""
            <div class="lr-practice-chain lr-chain lr-practice-chain--yes" data-ex-en="Yes, definitely. I'm keen on {{activity}} because it gives me the chance to relax with my family.">
              <p class="lr-practice-q">Do you like spending time with your family?</p>
              <p class="lr-chain-flow lr-practice-flow">Yes, definitely. I'm keen on {slot_select("activity", 0)} because it gives me the chance to relax with my family.</p>
              <p class="lr-practice-en lr-chain-ex-text"></p>
            </div>
            <div class="lr-practice-chain lr-chain lr-practice-chain--no" data-ex-en="No, not really. I hardly ever visit my extended family. I prefer staying at home rather than going to big parties.">
              <p class="lr-practice-q">Do you like large family parties?</p>
              <p class="lr-chain-flow lr-practice-flow">No, not really. I <strong>hardly ever</strong> visit my {slot_select("family_type", 1)}. I <strong>prefer staying</strong> at home <strong>rather than</strong> going to big parties.</p>
              <p class="lr-practice-en lr-chain-ex-text"></p>
            </div>"""
    l5_practice = f"""
            <div class="lr-practice-chain lr-chain" data-ex-en="Well, I love all kinds of family activities, but if I had to choose one, I would opt for {{activity}}. This is because it helps us strengthen our bond.">
              <p class="lr-practice-q">What kind of family activities do you like most?</p>
              <p class="lr-chain-flow lr-practice-flow">Well, I love all kinds of family activities, but if I <strong>had</strong> to choose one, I <strong>would opt for</strong> {slot_select("activity", 3)}. <strong>This is because</strong> it helps us strengthen our bond.</p>
              <p class="lr-practice-en lr-chain-ex-text"></p>
            </div>"""
    return f"""
      <div class="lr-core-lessons">
        <article class="lr-core-lesson" id="lesson4-formulas">
          <header class="lr-core-lesson-head">
            <h3>Lesson 4 · Do you like X?</h3>
            <p class="lr-formula"><strong>Công thức:</strong> Yes/No + FAVOURITE / HARDLY EVER + prefer</p>
          </header>
          <p class="lr-mm-hint">YES → love/enjoy + V-ing · FAVOURITE · NO → hardly ever · prefer V-ing to V-ing</p>
          <details class="lr-formula-details" open>
            <summary>Thực hành dropdown · Family</summary>
{l4_practice}
          </details>
        </article>
        <article class="lr-core-lesson" id="lesson5-formulas">
          <header class="lr-core-lesson-head">
            <h3>Lesson 5 · What kind of X do you like most?</h3>
            <p class="lr-formula"><strong>Công thức:</strong> if I had to choose… + because / because of</p>
          </header>
          <p class="lr-mm-hint">Loại gì? → I would opt for… → This is because + S + V</p>
          <details class="lr-formula-details" open>
            <summary>Thực hành dropdown · Family</summary>
{l5_practice}
          </details>
        </article>
      </div>"""


def family_lang_html() -> str:
    items = []
    for en, vi in FAMILY_IDIOMS:
        items.append(
            f'<li><mark class="lr-idiom-mark">{esc(en)}</mark>'
            f' <span class="lr-idiom-vi">— {esc(vi)}</span></li>'
        )
    practice = (
        f'My little brother is {slot_select("family_idiom", 2)} — he really '
        f'{slot_select("relationship", 1)} our dad. People say we are '
        f'{slot_select("family_idiom", 1)}.'
    )
    return f"""        <article class="lr-idiom-card">
          <h3>Family idioms</h3>
          <p class="lr-idiom-hint">Chọn 1–2 idiom phù hợp Part 2/3 — không nhồi hết.</p>
          <ul class="lr-idiom-list">{"".join(items)}</ul>
        </article>
        <div class="lr-idiom-practice">
          <p class="lr-chain-ex-label">Try combining (dropdown)</p>
          <p class="lr-idiom-practice-text">{practice}</p>
          <p class="lr-ref">Nguồn: <a href="https://www.dolenglish.vn/blog/family-ielts-speaking" target="_blank" rel="noopener noreferrer">DOL — Family IELTS Speaking</a> · <a href="https://zim.vn/ielts-speaking-part-1-family-and-friends-1" target="_blank" rel="noopener noreferrer">ZIM — Family &amp; Friends</a></p>
        </div>"""


def vocab_chains_html(words: list[dict]) -> str:
    chains = [
        {
            "title": "Family types (describe)",
            "flow": "nuclear family → parents → siblings → upbringing",
            "slots": ["family_type", "relative", "life_stage"],
            "ex_en": (
                "I come from a {family_type} — I live with my {relative}, "
                "and my {life_stage} shaped who I am today."
            ),
            "ex_vi": (
                "Tôi đến từ {family_type} — sống với {relative}, "
                "và {life_stage} định hình con người tôi."
            ),
            "tense": "Present Simple · describe",
        },
        {
            "title": "Time with family (habit)",
            "flow": "get on well → activity together → family gathering",
            "slots": ["relationship", "activity", "gathering"],
            "ex_en": (
                "I {relationship} my parents, and we enjoy {activity} "
                "during every {gathering}."
            ),
            "ex_vi": (
                "Tôi {relationship} bố mẹ, và chúng tôi thích {activity} "
                "mỗi {gathering}."
            ),
            "tense": "Present Simple · habit",
        },
        {
            "title": "Admire a member (Part 2)",
            "flow": "look up to → trait → take after → influence",
            "slots": ["relationship", "trait_pos", "life_stage"],
            "ex_en": (
                "I really {relationship} my mother — she is so {trait_pos}, "
                "and I think my {life_stage} values come from her."
            ),
            "ex_vi": (
                "Tôi {relationship} mẹ — bà rất {trait_pos}, "
                "và giá trị {life_stage} của tôi đến từ bà."
            ),
            "tense": "Present Simple · Part 2",
        },
        {
            "title": "Preference (Lesson 4)",
            "flow": "prefer small gatherings → hardly ever big parties → close-knit",
            "slots": ["activity", "family_type"],
            "ex_en": (
                "I <strong>prefer</strong> {activity} <strong>to</strong> loud parties, "
                "and I hardly ever see my whole {family_type} at once."
            ),
            "ex_vi": (
                "Tôi <strong>thích</strong> {activity} <strong>hơn</strong> tiệc ồn ào, "
                "và hiếm khi gặp cả {family_type}."
            ),
            "tense": "prefer V-ing to V-ing · hardly ever",
        },
    ]
    parts = []
    for chain in chains:
        text = chain["flow"]
        for sid in chain["slots"]:
            text = text.replace("{" + sid + "}", slot_select(sid), 1)
        parts.append(
            f"""        <div class="lr-chain" data-ex-en="{esc(chain["ex_en"])}" data-ex-vi="{esc(chain["ex_vi"])}">
          <h4>{esc(chain["title"])}</h4>
          <p class="lr-chain-flow">{text}</p>
          <div class="lr-chain-ex">
            <p class="lr-chain-ex-label">Example sentence</p>
            <p class="lr-chain-ex-text"></p>
            <p class="lr-chain-ex-vi"></p>
            <span class="lr-tense-tag">{esc(chain["tense"])}</span>
          </div>
        </div>"""
        )
    chips = []
    for w in words[:48]:
        ipa = f' <span class="ipa">/{esc(w["ipa"])}/</span>' if w.get("ipa") else ""
        vi = f' — {esc(w["vi"])}' if w.get("vi") else ""
        chips.append(f'<li><mark class="vocab">{esc(w["form"])}</mark>{ipa}{vi}</li>')
    return (
        "\n".join(parts)
        + f"""
        <details class="lr-vocab-bank">
          <summary>Vocabulary bank ({len(words)} words · B1/B2 focus)</summary>
          <ul class="ex-vocab-list">{"".join(chips)}</ul>
        </details>"""
    )


def speaking_mock_html() -> str:
    p1 = [
        (
            "Do you have a large or small family?",
            "Bạn có gia đình đông hay ít người?",
            (
                "I'd say I come from a fairly large family. Besides my "
                f'{slot_select("relative", 0)}, I have many cousins in my '
                f'{slot_select("family_type", 1)}. '
                '<span class="lr-tense-tag">Present Simple</span>'
            ),
        ),
        (
            "How much time do you spend with your family?",
            "Bạn dành bao nhiêu thời gian cho gia đình?",
            (
                "Honestly, not as much as I'd like <strong>because of</strong> my busy schedule, "
                "but I try to see them every weekend. We usually enjoy "
                f'{slot_select("activity", 0)}. '
                '<span class="lr-tense-tag">because of + noun · try to + V</span>'
            ),
        ),
        (
            "What do you like to do together as a family?",
            "Gia đình bạn thích làm gì cùng nhau?",
            (
                'Yes, definitely — I <strong>love</strong> '
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
                '<span class="lr-tense-tag">Present Simple · personality</span>'
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
                '<span class="lr-tense-tag">Present Simple · although</span>'
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
                "For me, family comes first <strong>because of</strong> the bond we share, "
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

    p2_idx = len(p1) + 1
    p3_start = p2_idx + 1
    lines = []
    lines.append('        <div class="ex-ielts-part lr-mock-part" data-part="1">')
    lines.append('          <h2 class="ex-ielts-part-title">Part 1 · Interview</h2>')
    lines.append(
        '          <p class="ex-ielts-part-hint">Yes/No + reasons · pick vocabulary from dropdowns · Lesson 4 &amp; 5 grammar tags.</p>'
    )
    for i, (q, qvi, ans) in enumerate(p1, 1):
        lines.append('          <div class="ex-qa">')
        lines.append(f'            <p class="ex-q"><span class="ex-role">Examiner</span> {esc(q)}</p>')
        lines.append(f'            <p class="ex-q-vi">{esc(qvi)}</p>')
        lines.append(f'            <p class="ex-sent lr-answer" data-sent="{i}">')
        lines.append('              <span class="ex-a-label">You</span>')
        lines.append(f'              <span class="ex-en lr-answer-text">{ans}</span>')
        lines.append("            </p></div>")
    lines.append("        </div>")

    lines.append('        <div class="ex-ielts-part lr-mock-part" data-part="2">')
    lines.append('          <h2 class="ex-ielts-part-title">Part 2 · Long turn</h2>')
    lines.append('          <div class="ex-cue-card">')
    lines.append(
        '            <p class="ex-cue-title">Describe a family member you admire. You should say:</p>'
    )
    lines.append("            <ul>")
    for b in [
        "who they are",
        "what they look like",
        "what they are like",
        "and explain why you admire them",
    ]:
        lines.append(f"              <li>{esc(b)}</li>")
    lines.append("            </ul></div>")
    lines.append('          <div class="ex-qa">')
    lines.append(f'            <p class="ex-sent lr-answer" data-sent="{p2_idx}">')
    lines.append('              <span class="ex-a-label">You</span>')
    lines.append(f'              <span class="ex-en lr-answer-text">{p2_en}</span>')
    lines.append("            </p></div></div>")

    lines.append('        <div class="ex-ielts-part lr-mock-part" data-part="3">')
    lines.append('          <h2 class="ex-ielts-part-title">Part 3 · Discussion</h2>')
    for j, (q, qvi, ans) in enumerate(p3, p3_start):
        lines.append('          <div class="ex-qa">')
        lines.append(f'            <p class="ex-q"><span class="ex-role">Examiner</span> {esc(q)}</p>')
        lines.append(f'            <p class="ex-q-vi">{esc(qvi)}</p>')
        lines.append(f'            <p class="ex-sent lr-answer" data-sent="{j}">')
        lines.append('              <span class="ex-a-label">You</span>')
        lines.append(f'              <span class="ex-en lr-answer-text">{ans}</span>')
        lines.append("            </p></div>")
    lines.append("        </div>")
    return "\n".join(lines)


def scroll_read_html() -> str:
    return """
        <section class="ex-scroll lr-scroll-read" id="exScroll" aria-label="Scroll reading teleprompter">
          <div class="ex-scroll-head">
            <div>
              <h3>Scroll read · speaking</h3>
              <p class="ex-scroll-hint">Đọc theo chữ cuộn kiểu teleprompter (VOA-style). Từ trong dropdown bị ẩn — hiện nghĩa VI hoặc IPA để bạn tự nhớ và nói ra tiếng Anh. Câu hỏi + câu trả lời cuộn theo Part 1 / 2 / 3.</p>
            </div>
          </div>
          <div class="ex-scroll-toolbar">
            <button type="button" class="ex-btn primary" id="btnScrollPlay">▶ Play</button>
            <button type="button" class="ex-btn" id="btnScrollPause">Pause</button>
            <button type="button" class="ex-btn" id="btnScrollRestart">⟲ Restart</button>
            <label class="ex-voice">Speed
              <input id="scrollSpeed" type="range" min="12" max="90" step="1" value="32">
              <span id="scrollSpeedVal">32</span> px/s
            </label>
            <label class="ex-voice">Hint
              <select id="scrollHintMode" aria-label="Hint mode for hidden words">
                <option value="vi" selected>Nghĩa VI</option>
                <option value="ipa">IPA</option>
                <option value="both">VI + IPA</option>
              </select>
            </label>
            <label class="ex-toggle"><input type="checkbox" id="scrollReveal"> Hiện từ EN</label>
          </div>
          <div class="ex-scroll-stage">
            <div class="ex-scroll-focus" aria-hidden="true"></div>
            <div class="ex-scroll-viewport" id="scrollViewport">
              <div class="ex-scroll-track" id="scrollTrack"></div>
            </div>
          </div>
        </section>"""


def mock_practice_refs_html() -> str:
    return """
        <aside class="lr-practice-refs" aria-label="Speaking practice references">
          <h3 class="lr-practice-refs-title">Luyện nói với TTS</h3>
          <ol class="lr-practice-steps">
            <li>Chọn từ trong dropdown → chỉnh câu trả lời theo ý bạn.</li>
            <li>Bấm <strong>Copy current answers</strong> — clipboard gồm <em>câu hỏi + câu trả lời</em> theo Part 1 / 2 / 3.</li>
            <li>Mở <a href="https://www.naturalreaders.com/online/" target="_blank" rel="noopener noreferrer">NaturalReader Online</a> (hoặc TTS khác) → paste → nghe và lặp lại để luyện phát âm &amp; nhịp nói.</li>
            <li>Hoặc dùng <strong>Scroll read · speaking</strong> bên dưới — teleprompter cuộn chữ, từ dropdown bị ẩn (gợi ý VI/IPA) để bạn tự nói.</li>
          </ol>
          <div class="lr-ref-grid">
            <a class="lr-ref-card" href="https://www.dolenglish.vn/blog/speaking-test-ielts" target="_blank" rel="noopener noreferrer">
              <strong>DOL — Speaking Test IELTS Part 1, 2 &amp; 3</strong>
              <span>Cấu trúc thi (11–14 phút), mục đích từng part, đề mẫu full test</span>
              <span class="lr-card-cta">Đọc hướng dẫn ↗</span>
            </a>
            <a class="lr-ref-card" href="https://www.naturalreaders.com/online/" target="_blank" rel="noopener noreferrer">
              <strong>NaturalReader Online</strong>
              <span>Text-to-speech miễn phí — paste Q&amp;A đã copy để nghe examiner + câu trả lời</span>
              <span class="lr-card-cta">Mở NaturalReader ↗</span>
            </a>
            <a class="lr-ref-card" href="https://www.dolenglish.vn/blog/family-ielts-speaking" target="_blank" rel="noopener noreferrer">
              <strong>DOL — IELTS Speaking Family</strong>
              <span>Chủ đề Family thực tế, câu hỏi Part 1/2/3 và gợi ý trả lời</span>
              <span class="lr-card-cta">Xem chủ đề Family ↗</span>
            </a>
            <a class="lr-ref-card" href="https://ielts.idp.com/vietnam/about/news-and-articles/article-talk-about-your-family" target="_blank" rel="noopener noreferrer">
              <strong>IDP — Talk about your family</strong>
              <span>Từ vựng &amp; mẹo nói về gia đình trong IELTS Speaking</span>
              <span class="lr-card-cta">Đọc bài IDP ↗</span>
            </a>
          </div>
        </aside>"""


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

    body = f"""    <aside class="docs-sidebar" id="docsSidebar" data-nav="english" data-docs-root="../../" data-active="people-family">
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
        <p class="lede">Sau khi hoàn thành B2, ôn tập theo <a href="https://www.dolenglish.vn/blog/linearthinking-trong-speaking" target="_blank" rel="noopener noreferrer">Linear Thinking</a>: ngữ pháp (gerunds &amp; preferences, because/conditional 2) → mental model → cấu trúc Speaking → từ vựng B1/B2 → mock IELTS Part 1/2/3 với dropdown từ thay thế.</p>
        <nav class="lr-toc" aria-label="On this page">
          <a href="#natural-vlog">0 · Real talk</a>
          <a href="#grammar">1 · Grammar</a>
          <a href="#mental-model">2 · Mental model</a>
          <a href="#structures">3 · Structures</a>
          <a href="#lessons">4 · Lesson highlights</a>
          <a href="#family-lang">5 · Idioms &amp; phrases</a>
          <a href="#vocab-chains">6 · Vocab chains</a>
          <a href="#mock-test">7 · Mock test</a>
        </nav>
        <div class="ex-toolbar lr-toolbar lr-toolbar--hero">
          <label class="ex-toggle"><input type="checkbox" id="togVi" /> Vietnamese</label>
        </div>
      </header>

{natural_vlog_html()}

      <section class="lr-section" id="grammar">
        <h2>1 · Grammar foundations</h2>
        <p class="lr-section-hint">Hai chủ điểm từ <a href="https://www.dolenglish.vn/blog/ngu-phap-ielts" target="_blank" rel="noopener noreferrer">DOL — Ngữ pháp IELTS</a>, gắn Lesson 4 (<em>Do you like X?</em>) và Lesson 5 (<em>What kind of X…?</em>).</p>
        <div class="lr-grammar-list">
{grammar_section()}
        </div>
        <p class="lr-ref">Tham khảo thêm: <a href="https://www.dolenglish.vn/blog/linearthinking-trong-hoc-ngu-phap-grammar" target="_blank" rel="noopener noreferrer">Linear Thinking trong Grammar</a> · <a href="https://www.dolenglish.vn/blog/family-ielts-speaking" target="_blank" rel="noopener noreferrer">DOL — IELTS Speaking Family</a></p>
      </section>

      <section class="lr-section" id="mental-model">
        <h2>2 · Mental model — Grammar for family speaking</h2>
        <p class="lr-section-hint">Sơ đồ tư duy 2 chủ điểm ngữ pháp — gerunds/prefer (Lesson 4) và because/conditional 2 (Lesson 5). <span class="lr-mmap-star">★</span> = dùng trong mock test.</p>
{grammar_mind_map_section()}
      </section>

      <section class="lr-section" id="structures">
        <h2>3 · Speaking structures (family + grammar)</h2>
        <p class="lr-section-hint">Xem video gốc trước, sau đó mở <strong>Family practice</strong>. Playlist: <a href="https://www.youtube.com/playlist?list=PLD6t6ckHsruYoalxbzcjX1TNn4h7ShiRk" target="_blank" rel="noopener noreferrer">Oxford Online English · Spoken English Lessons</a>.</p>
        <ul class="lr-lesson-list">
{speaking_lessons_html()}
        </ul>
      </section>

      <section class="lr-section" id="lessons">
        <h2>4 · Core formulas — Lesson 4 &amp; 5</h2>
        <p class="lr-section-hint">Công thức <strong>IELTS Nguyễn Huyền</strong> — <strong>Lesson 4</strong> (Do you like X?) trước, <strong>Lesson 5</strong> (What kind of X…) sau. Chọn <strong>1–2 nhánh</strong>, không nhồi hết.</p>
{lesson_highlights_html()}
      </section>

      <section class="lr-section" id="family-lang">
        <h2>5 · Family lang · idioms &amp; phrases</h2>
        <p class="lr-section-hint">IELTS đánh giá <strong>Lexical Resource</strong> — chọn 1–2 idiom phù hợp ngữ cảnh (không nhồi).</p>
        <div class="lr-idiom-grid">
{family_lang_html()}
        </div>
      </section>

      <section class="lr-section" id="vocab-chains">
        <h2>6 · Vocabulary — idea chains (Level 3)</h2>
        <p class="lr-section-hint">Học từ theo <a href="https://www.dolenglish.vn/blog/linearthinking-trong-hoc-tu-vung-vocab" target="_blank" rel="noopener noreferrer">dòng ideas</a>, không liệt kê. Chọn từ trong dropdown — bên dưới mỗi chain có <strong>Example sentence</strong> ghép từ + ngữ pháp đã học.</p>
{vocab_chains_html(words)}
      </section>

      <section class="lr-section lr-mock" id="mock-test">
        <h2>7 · IELTS Speaking mock — People &amp; Family</h2>
        <p class="lr-section-hint">Part 1 / 2 / 3 thực chiến. Dùng dropdown để đổi từ — không cần nhồi hết từ vào một câu.</p>
{mock_practice_refs_html()}
        <div class="ex-toolbar lr-toolbar">
          <button type="button" class="ex-btn primary" id="btnCopyAnswer">Copy current answers</button>
        </div>
        <section class="ex-passage ex-ielts lr-mock-passage" id="mockPassage" data-tts-root>
{speaking_mock_html()}
        </section>
{scroll_read_html()}
      </section>

      <script type="application/json" id="lrWordSlots">{slots_json}</script>
    </article>"""

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
{body}
  </div>
  <script src="{home}js/docs.js?v=lr24"></script>
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
