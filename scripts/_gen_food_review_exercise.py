#!/usr/bin/env python3
"""Generate Food & Drink · Linear Thinking review exercise (capstone after B2).

Flow: Grammar refs → tense mental model → speaking structures → lesson highlights
      → vocab idea chains → IELTS Speaking mock (Part 1/2/3) with word dropdowns.
"""
from __future__ import annotations

import html as htmlmod
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "blog" / "english" / "food-drink" / "review-exercise"

_spec = importlib.util.spec_from_file_location(
    "gen_ex", Path(__file__).with_name("_gen_english_exercises.py")
)
_gen = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_gen)

esc = _gen.esc
collect_words = _gen.collect_words
TOPICS = _gen.TOPICS
BRAND = "✦ The Quiet Corner ✦"

GRAMMAR_REFS = [
    (
        "Present Simple & Present Continuous",
        "https://ielts-fighter.com/grammarvocabulary/present-simple-present-continuous-state-verbs_mt1458272845.html",
        "Thói quen ăn uống, sở thích, xu hướng hiện tại",
        "I usually have… / I'm trying a low-carb diet",
    ),
    (
        "Past Simple & Past Continuous · used to · would",
        "https://ielts-fighter.com/grammarvocabulary/past-simple-past-continuous-use-to-would_mt1458275537.html",
        "Kỷ niệm ẩm thực, món từng thích, đang nấu thì…",
        "When I was a child, I would… / I was cooking when…",
    ),
    (
        "Future Simple & near future",
        "https://ielts-fighter.com/grammarvocabulary/the-future-simple-the-near-future_mt1458293272.html",
        "Kế hoạch nấu ăn, dự đoán thói quen ăn",
        "I'm going to cook… / Food will become…",
    ),
    (
        "Future Perfect · Continuous · be about to",
        "https://ielts-fighter.com/grammarvocabulary/future-perfect-future-perfect-continuous-future-continuous-be-about-to_mt1458293628.html",
        "Dự đoán dài hạn về ẩm thực",
        "By next year I will have tried…",
    ),
    (
        "Past Perfect & Past Perfect Continuous",
        "https://ielts-fighter.com/grammarvocabulary/past-perfect-past-perfect-continuous_mt1458293093.html",
        "Kể chuyện bữa ăn (trước / trong khi / sau)",
        "I had never tried… before I visited…",
    ),
    (
        "Present Perfect & Present Perfect Continuous",
        "https://ielts-fighter.com/grammarvocabulary/present-perfect-present-perfect-continuous_mt1458292833.html",
        "Kinh nghiệm ẩm thực đến nay",
        "I've always liked… / I've been eating more…",
    ),
]

SPEAKING_LESSONS = [
    ("lesson-03-do-you-like-x", "Do you like X? — Yes/No + reasons", "Part 1 food questions"),
    ("lesson-02-reasons-like-dislike", "Reasons like / dislike", "Because / This is because + S+V"),
    ("lesson-34-how-to-talk-about-the-past-in-english", "Talk about the past", "Childhood food, used to"),
    ("lesson-57-how-to-use-the-past-perfect-tense-in-english-english-grammar", "Past Perfect", "Before that meal, I had never…"),
    ("lesson-15-how-to-tell-a-story-in-english-using-past-tense", "Tell a story (past)", "Part 2 meal narrative"),
    ("lesson-23-future-in-english-how-to-talk-about-the-future", "Talk about the future", "Diet plans, food trends"),
    ("lesson-61-how-to-add-emphasis-in-english-improve-your-spoken-english", "Add emphasis", "What I enjoy most is…"),
]

# Hand-curated interchangeable vocab slots (B1/B2 heavy)
WORD_SLOTS: dict[str, list[dict]] = {
    "morning_drink": [
        {"form": "latte", "vi": "cà phê latte"},
        {"form": "espresso", "vi": "espresso"},
        {"form": "cappuccino", "vi": "cappuccino"},
        {"form": "herbal tea", "vi": "trà thảo mộc"},
        {"form": "smoothie", "vi": "sinh tố"},
    ],
    "soft_drink": [
        {"form": "mineral water", "vi": "nước khoáng"},
        {"form": "lemonade", "vi": "nước chanh"},
        {"form": "soda", "vi": "nước ngọt có ga"},
        {"form": "sparkling water", "vi": "nước có ga"},
    ],
    "alcohol": [
        {"form": "wine", "vi": "rượu vang"},
        {"form": "beer", "vi": "bia"},
        {"form": "cider", "vi": "rượu táo"},
        {"form": "gin", "vi": "gin"},
        {"form": "booze", "vi": "đồ có cồn (thân mật)"},
    ],
    "favourite_food": [
        {"form": "cheesecake", "vi": "bánh phô mai"},
        {"form": "pasta", "vi": "mì Ý"},
        {"form": "curry", "vi": "cà ri"},
        {"form": "steak", "vi": "bít tết"},
        {"form": "sushi", "vi": "sushi"},
    ],
    "dislike_food": [
        {"form": "fast food", "vi": "đồ ăn nhanh"},
        {"form": "junk food", "vi": "đồ ăn vặt không lành mạnh"},
        {"form": "processed food", "vi": "đồ chế biến sẵn"},
    ],
    "healthy_item": [
        {"form": "vegetable salad", "vi": "salad rau"},
        {"form": "low-carb diet", "vi": "chế độ ít carb"},
        {"form": "gluten-free diet", "vi": "chế độ không gluten"},
        {"form": "fruit salad", "vi": "salad trái cây"},
    ],
    "cook_verb": [
        {"form": "grill", "vi": "nướng"},
        {"form": "roast", "vi": "quay"},
        {"form": "marinate", "vi": "ướp"},
        {"form": "chop", "vi": "thái nhỏ"},
        {"form": "stir", "vi": "đảo"},
    ],
    "ingredient": [
        {"form": "herb", "vi": "thảo mộc"},
        {"form": "spice", "vi": "gia vị"},
        {"form": "garlic", "vi": "tỏi"},
        {"form": "ginger", "vi": "gừng"},
    ],
    "b2_drink": [
        {"form": "mojito", "vi": "mojito"},
        {"form": "margarita", "vi": "margarita"},
        {"form": "martini", "vi": "martini"},
        {"form": "ginger ale", "vi": "ginger ale"},
    ],
    "b2_bread": [
        {"form": "bagel", "vi": "bánh bagel"},
        {"form": "baguette", "vi": "bánh mì Pháp"},
        {"form": "croissant", "vi": "bánh sừng bò"},
    ],
}


def collect_review_words() -> list[dict]:
    topic = next(t for t in TOPICS["topics"] if t["slug"] == "food-drink")
    by_level: dict[str, list[dict]] = {}
    for level in ("A1", "A2", "B1", "B2"):
        lessons = [l for l in topic["lessons"] if l["level"] == level]
        by_level[level] = collect_words([l["id"] for l in lessons])
    # ~70% B1+B2, ~20% A2, ~10% A1 for display chips
    return (
        by_level["B1"]
        + by_level["B2"]
        + by_level["A2"][:18]
        + by_level["A1"][:9]
    )


def slot_select(slot_id: str, default_idx: int = 0) -> str:
    opts = WORD_SLOTS[slot_id]
    idx = min(default_idx, len(opts) - 1)
    options = "\n".join(
        f'<option value="{esc(o["form"])}"{" selected" if i == idx else ""}>'
        f'{esc(o["form"])} — {esc(o["vi"])}</option>'
        for i, o in enumerate(opts)
    )
    return (
        f'<select class="lr-word-pick" data-slot="{esc(slot_id)}" '
        f'aria-label="Choose vocabulary">'
        f"{options}</select>"
    )


def grammar_section() -> str:
    cards = []
    for title, url, vi_use, ex in GRAMMAR_REFS:
        cards.append(
            f"""        <li class="lr-grammar-card">
          <a href="{esc(url)}" target="_blank" rel="noopener noreferrer">
            <strong>{esc(title)}</strong>
          </a>
          <p>{esc(vi_use)}</p>
          <p class="lr-grammar-ex"><em>e.g.</em> {esc(ex)}</p>
        </li>"""
        )
    return "\n".join(cards)


def mental_model_html() -> str:
    return """
      <div class="lr-model lr-model--tenses">
        <div class="lr-model-root">Food &amp; habits · Tense map</div>
        <div class="lr-model-branches">
          <div class="lr-branch lr-branch--blue">
            <span class="lr-branch-label">Present</span>
            <ul>
              <li><strong>Simple</strong> — facts, habits, preferences<br><em>I usually have rice. / Fast food is convenient.</em></li>
              <li><strong>Continuous</strong> — now, changing trends<br><em>I'm trying a low-carb diet. / People are eating more plant-based food.</em></li>
              <li><strong>Perfect</strong> — experience until now<br><em>I've tried sushi. / I've always liked spicy food.</em></li>
              <li><strong>Perfect Continuous</strong> — duration until now<br><em>I've been cooking at home more lately.</em></li>
            </ul>
          </div>
          <div class="lr-branch lr-branch--green">
            <span class="lr-branch-label">Past</span>
            <ul>
              <li><strong>Simple</strong> — finished events<br><em>Last Sunday I grilled kebab in the garden.</em></li>
              <li><strong>Continuous</strong> — background action<br><em>I was chopping vegetables when my friend arrived.</em></li>
              <li><strong>Perfect</strong> — earlier past<br><em>I had never tried lobster before that trip.</em></li>
              <li><strong>used to / would</strong> — past habits<br><em>I would eat fast food every day as a teenager.</em></li>
            </ul>
          </div>
          <div class="lr-branch lr-branch--orange">
            <span class="lr-branch-label">Future</span>
            <ul>
              <li><strong>will / going to</strong> — plans &amp; predictions<br><em>I'm going to cook pasta tonight. / People will eat healthier.</em></li>
              <li><strong>Future Perfect</strong> — completed by a deadline<br><em>By next year I will have tried ten new cuisines.</em></li>
              <li><strong>be about to</strong> — immediate future<br><em>I'm about to order takeout.</em></li>
            </ul>
          </div>
        </div>
        <p class="lr-model-note">Linear Thinking rule: pick <strong>one time frame</strong> per sentence — don't mix tenses without a clear link (when / before / after).</p>
      </div>"""


def speaking_lessons_html() -> str:
    rows = []
    for slug, title, why in SPEAKING_LESSONS:
        rows.append(
            f"""        <li>
          <strong>{esc(title)}</strong>
          <code class="lr-path">IELTS/SPEAKING/spoken-english-lessons/{esc(slug)}.md</code>
          <span class="lr-lesson-why">{esc(why)}</span>
        </li>"""
        )
    rows.append(
        """        <li>
          <strong>Lesson 2 — Reasons like / dislike</strong>
          <code class="lr-path">IELTS/SPEAKING/lesson-2-reasons-like-dislike.md</code>
          <span class="lr-lesson-why">Yes/No + because (food likes &amp; dislikes)</span>
        </li>"""
    )
    rows.append(
        """        <li>
          <strong>Lesson 3 — Do you like X?</strong>
          <code class="lr-path">IELTS/SPEAKING/lesson-3-do-you-like-x.md</code>
          <span class="lr-lesson-why">Part 1 formula for food questions</span>
        </li>"""
    )
    return "\n".join(rows)


def lesson_highlights_html() -> str:
    return """
      <div class="lr-highlight-grid">
        <article class="lr-highlight-card">
          <h3>Lesson 3 · Do you like X?</h3>
          <p class="lr-formula"><strong>Yes/No</strong> + <strong>Reasons</strong></p>
          <ul>
            <li><mark>Yes, definitely.</mark> / <mark>No, not really.</mark></li>
            <li><mark>I'm keen on</mark> / <mark>I'm a big fan of</mark> + noun</li>
            <li><mark>This is because</mark> + S + V</li>
            <li><mark>It gives me the chance to</mark> + V</li>
          </ul>
          <p class="lr-food-ex"><strong>Food:</strong> Do you like cooking? → <em>Yes, definitely. I'm keen on cooking because it gives me the chance to try new recipes.</em></p>
        </article>
        <article class="lr-highlight-card">
          <h3>Lesson 2 · Reasons</h3>
          <p class="lr-formula">Like → <strong>entertaining</strong> or <strong>educational</strong> (+ health)</p>
          <ul>
            <li><mark>It's a great way to</mark> unwind / relax</li>
            <li><mark>It helps me</mark> recharge my batteries</li>
            <li>Dislike → <mark>can lead to</mark> health problems</li>
            <li><mark>not my cup of tea</mark> · <mark>can't stand</mark></li>
          </ul>
          <p class="lr-food-ex"><strong>Food:</strong> Why dislike fast food? → <em>Because it can lead to obesity and it's not my cup of tea.</em></p>
        </article>
      </div>"""


def vocab_chains_html(words: list[dict]) -> str:
    chains = [
        (
            "Morning routine (Time process)",
            "wake up → sip {morning_drink} → grab {b2_bread} → check nutrition",
            ["morning_drink", "b2_bread"],
        ),
        (
            "Eating out (Cause → Effect)",
            "order {favourite_food} → share with friends → feel satisfied → sometimes order {b2_drink}",
            ["favourite_food", "b2_drink"],
        ),
        (
            "Healthy choice (Problem → Solution)",
            "avoid {dislike_food} → follow {healthy_item} → {cook_verb} at home with {ingredient}",
            ["dislike_food", "healthy_item", "cook_verb", "ingredient"],
        ),
        (
            "Weekend drinks (Advantage / Disadvantage)",
            "Advantage: enjoy {alcohol} on special occasions · Disadvantage: need time to sober up → prefer {soft_drink}",
            ["alcohol", "soft_drink"],
        ),
    ]
    parts = []
    for title, template, slot_ids in chains:
        text = template
        for sid in slot_ids:
            text = text.replace("{" + sid + "}", slot_select(sid), 1)
        parts.append(
            f"""        <div class="lr-chain">
          <h4>{esc(title)}</h4>
          <p class="lr-chain-flow">{text}</p>
        </div>"""
        )
    chips = []
    for w in words[:48]:
        ipa = f' <span class="ipa">/{esc(w["ipa"])}/</span>' if w.get("ipa") else ""
        vi = f' — {esc(w["vi"])}' if w.get("vi") else ""
        chips.append(
            f'<li><mark class="vocab">{esc(w["form"])}</mark>{ipa}{vi}</li>'
        )
    return (
        "\n".join(parts)
        + f"""
        <details class="lr-vocab-bank">
          <summary>Vocabulary bank ({len(words)} words · B1/B2 focus)</summary>
          <ul class="ex-vocab-list">{"".join(chips)}</ul>
        </details>"""
    )


def speaking_mock_html() -> str:
    """IELTS Part 1 / 2 / 3 with grammar + interchangeable vocab slots."""
    p1 = [
        (
            "Do you like cooking?",
            "Bạn có thích nấu ăn không?",
            (
                'Yes, definitely. <strong>I\'m keen on</strong> cooking because it gives me the chance to '
                f'{slot_select("cook_verb")} fresh food at home. '
                f'I usually add {slot_select("ingredient")} and follow a simple recipe. '
                '<span class="lr-tense-tag">Present Simple</span>'
            ),
        ),
        (
            "What's your favourite food or drink?",
            "Món ăn hoặc đồ uống yêu thích của bạn là gì?",
            (
                'Well, I would say I <strong>have a sweet tooth</strong>, so I love '
                f'{slot_select("favourite_food")}. '
                f'In the morning I often drink {slot_select("morning_drink")}. '
                '<span class="lr-tense-tag">Present Simple · habit</span>'
            ),
        ),
        (
            "Do you have a healthy diet?",
            "Bạn có chế độ ăn lành mạnh không?",
            (
                'I think so. I <strong>used to</strong> eat unhealthily, but now '
                f'I\'m trying {slot_select("healthy_item")}. '
                f'I hardly ever buy {slot_select("dislike_food")} anymore. '
                '<span class="lr-tense-tag">used to · Present Continuous</span>'
            ),
        ),
        (
            "Have you always liked the same food?",
            "Bạn có luôn thích cùng một loại đồ ăn không?",
            (
                'Not really. The food I liked as a child and what I enjoy now are '
                '<strong>totally different</strong>. '
                f'<strong>I\'ve tried</strong> many new dishes — last month I even tasted '
                f'{slot_select("b2_bread")} with {slot_select("b2_drink")}. '
                '<span class="lr-tense-tag">Present Perfect · Past Simple</span>'
            ),
        ),
        (
            "Do you often eat out?",
            "Bạn có thường ăn ngoài không?",
            (
                'Sometimes. I <strong>prefer</strong> home-cooked food, but on weekends '
                f'I might order {slot_select("favourite_food")} or grab '
                f'{slot_select("soft_drink")} with friends. '
                '<span class="lr-tense-tag">Present Simple · preference</span>'
            ),
        ),
    ]

    p2_en = (
        "I'm going to describe a meal I really enjoyed. "
        f"It was last month when my family cooked together. "
        f"First, we decided to {slot_select('cook_verb', 2)} meat and prepare "
        f"{slot_select('healthy_item', 1)} on the side. "
        f"I was {slot_select('cook_verb', 4)} sauce while my mom chopped vegetables — "
        "<strong>Past Continuous</strong> for background. "
        f"Before that day, I <strong>had never tried</strong> that recipe, so everything felt new. "
        f"We finished with {slot_select('favourite_food', 0)} and shared "
        f"{slot_select('alcohol', 0)} for a toast. "
        "What I enjoyed most was spending time together — not just the food."
    )

    p3 = [
        (
            "How have eating habits changed in your country?",
            "Thói quen ăn uống ở nước bạn đã thay đổi thế nào?",
            (
                'I think they <strong>have changed quite a bit</strong>. '
                'Young people are eating more fast food, while others '
                f'are following {slot_select("healthy_item", 2)}. '
                '<strong>More people have been cooking</strong> at home since the pandemic. '
                '<span class="lr-tense-tag">Present Perfect · Continuous</span>'
            ),
        ),
        (
            "Is fast food popular where you live?",
            "Đồ ăn nhanh có phổ biến nơi bạn sống không?",
            (
                'Yes, definitely — it\'s convenient, but it\'s extremely <strong>unhealthy</strong>. '
                f'Eating too much {slot_select("dislike_food")} '
                '<strong>can lead to</strong> obesity and heart problems. '
                '<span class="lr-tense-tag">Modal · general truth</span>'
            ),
        ),
        (
            "Will people's diets be healthier in the future?",
            "Chế độ ăn của mọi người sẽ lành mạnh hơn trong tương lai không?",
            (
                'I hope so. I believe more people <strong>will choose</strong> organic food '
                f'and <strong>will reduce</strong> {slot_select("dislike_food", 1)}. '
                f'By 2030 many families <strong>will have adopted</strong> balanced meal plans. '
                '<span class="lr-tense-tag">Future Simple · Future Perfect</span>'
            ),
        ),
    ]

    lines = []
    lines.append('        <div class="ex-ielts-part lr-mock-part" data-part="1">')
    lines.append('          <h2 class="ex-ielts-part-title">Part 1 · Interview</h2>')
    lines.append('          <p class="ex-ielts-part-hint">Yes/No + reasons · pick vocabulary from dropdowns · one tense per idea.</p>')
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
    lines.append('            <p class="ex-cue-title">Describe a meal you enjoyed. You should say:</p>')
    lines.append("            <ul>")
    for b in ["when it was", "who you were with", "what you ate", "and explain why you enjoyed it"]:
        lines.append(f"              <li>{esc(b)}</li>")
    lines.append("            </ul></div>")
    lines.append('          <div class="ex-qa">')
    lines.append('            <p class="ex-sent lr-answer" data-sent="6">')
    lines.append('              <span class="ex-a-label">You</span>')
    lines.append(f'              <span class="ex-en lr-answer-text">{p2_en}</span>')
    lines.append("            </p></div></div>")

    lines.append('        <div class="ex-ielts-part lr-mock-part" data-part="3">')
    lines.append('          <h2 class="ex-ielts-part-title">Part 3 · Discussion</h2>')
    for j, (q, qvi, ans) in enumerate(p3, 7):
        lines.append('          <div class="ex-qa">')
        lines.append(f'            <p class="ex-q"><span class="ex-role">Examiner</span> {esc(q)}</p>')
        lines.append(f'            <p class="ex-q-vi">{esc(qvi)}</p>')
        lines.append(f'            <p class="ex-sent lr-answer" data-sent="{j}">')
        lines.append('              <span class="ex-a-label">You</span>')
        lines.append(f'              <span class="ex-en lr-answer-text">{ans}</span>')
        lines.append("            </p></div>")
    lines.append("        </div>")
    return "\n".join(lines)


def build_page() -> str:
    words = collect_review_words()
    home = "../../../"
    slots_json = json.dumps(WORD_SLOTS, ensure_ascii=False)

    body = f"""    <aside class="docs-sidebar" id="docsSidebar" data-nav="english" data-docs-root="../../" data-active="food-drink">
      <div class="docs-nav-label">English</div>
      <ul class="docs-nav" id="docsNav">
        <li><a href="../../">All topics</a></li>
        <li><a href="../">Food &amp; Drink</a></li>
        <li><a class="active" href="./">Review Exercise</a></li>
      </ul>
    </aside>
    <article class="docs-main lr-page">
      <div class="docs-breadcrumb">
        <a href="{home}">Home</a><span>›</span>
        <a href="{home}#blogs">Blogs</a><span>›</span>
        <a href="../../">English</a><span>›</span>
        <a href="../">Food &amp; Drink</a><span>›</span>
        <span>Review Exercise</span>
      </div>

      <header class="lr-hero">
        <p class="lr-hero-badge">Linear Thinking · Capstone</p>
        <h1>Food &amp; Drink — Review Exercise</h1>
        <p class="lede">Sau khi hoàn thành B2, ôn tập theo <a href="https://www.dolenglish.vn/blog/linearthinking-trong-speaking" target="_blank" rel="noopener noreferrer">Linear Thinking</a>: ngữ pháp (6 thì) → mental model → cấu trúc Speaking → từ vựng B1/B2 → mock IELTS Part 1/2/3 với dropdown từ thay thế.</p>
        <nav class="lr-toc" aria-label="On this page">
          <a href="#grammar">1 · Grammar</a>
          <a href="#mental-model">2 · Mental model</a>
          <a href="#structures">3 · Structures</a>
          <a href="#lessons">4 · Lesson highlights</a>
          <a href="#vocab-chains">5 · Vocab chains</a>
          <a href="#mock-test">6 · Mock test</a>
        </nav>
      </header>

      <section class="lr-section" id="grammar">
        <h2>1 · Grammar foundations</h2>
        <p class="lr-section-hint">Đọc lý thuyết cơ bản trước khi luyện nói. Mỗi thì gắn với ngữ cảnh Food &amp; Drink.</p>
        <ul class="lr-grammar-list">
{grammar_section()}
        </ul>
        <p class="lr-ref">Tham khảo thêm: <a href="https://www.dolenglish.vn/blog/linearthinking-trong-hoc-ngu-phap-grammar" target="_blank" rel="noopener noreferrer">Linear Thinking trong Grammar</a> · <a href="https://www.dolenglish.vn/blog/ielts-speaking-food" target="_blank" rel="noopener noreferrer">DOL — IELTS Speaking Food</a></p>
      </section>

      <section class="lr-section" id="mental-model">
        <h2>2 · Mental model — Tenses for Food speaking</h2>
        <p class="lr-section-hint">Gom 6 nhóm thì thành 3 nhánh thời gian — chọn <strong>một nhánh</strong> cho mỗi câu trả lời.</p>
{mental_model_html()}
      </section>

      <section class="lr-section" id="structures">
        <h2>3 · Speaking structures (food + tenses)</h2>
        <p class="lr-section-hint">Các bài trong <code>IELTS/SPEAKING/spoken-english-lessons</code> liên quan chủ đề Food và thì.</p>
        <ul class="lr-lesson-list">
{speaking_lessons_html()}
        </ul>
      </section>

      <section class="lr-section" id="lessons">
        <h2>4 · Core formulas — Lesson 2 &amp; 3</h2>
        <p class="lr-section-hint">Cấu trúc trọng tâm trước khi ghép từ mới.</p>
{lesson_highlights_html()}
      </section>

      <section class="lr-section" id="vocab-chains">
        <h2>5 · Vocabulary — idea chains (Level 3)</h2>
        <p class="lr-section-hint">Học từ theo <a href="https://www.dolenglish.vn/blog/linearthinking-trong-hoc-tu-vung-vocab" target="_blank" rel="noopener noreferrer">dòng ideas</a>, không liệt kê. Chọn từ trong dropdown — các lựa chọn cùng nhóm có thể thay thế nhau.</p>
{vocab_chains_html(words)}
      </section>

      <section class="lr-section lr-mock" id="mock-test">
        <h2>6 · IELTS Speaking mock — Food</h2>
        <p class="lr-section-hint">Part 1 / 2 / 3 thực chiến. Dùng dropdown để đổi từ (vd. <em>booze</em> → <em>cider</em> → <em>gin</em>) — không cần nhồi hết từ vào một câu.</p>
        <div class="ex-toolbar lr-toolbar">
          <label class="ex-toggle"><input type="checkbox" id="togVi" /> Vietnamese</label>
          <button type="button" class="ex-btn primary" id="btnCopyAnswer">Copy current answers</button>
        </div>
        <section class="ex-passage ex-ielts lr-mock-passage" id="mockPassage" data-tts-root>
{speaking_mock_html()}
        </section>
      </section>

      <script type="application/json" id="lrWordSlots">{slots_json}</script>
    </article>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Review Exercise · Food &amp; Drink — The Quiet Corner</title>
  <meta name="description" content="Linear Thinking review: grammar, mental models, and IELTS Speaking mock for Food &amp; Drink (B1/B2 focus).">
  <link rel="icon" href="{home}favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{home}css/docs.css?v=lr1">
</head>
<body class="docs lr-body">
  <div class="cursor" id="cursor"></div>
  <div class="cursor-ring" id="cursorRing"></div>
  <canvas id="matrix-canvas"></canvas>
  <div class="grid-bg"></div>
  <header class="docs-topbar">
    <button class="docs-menu-btn" id="docsMenuBtn" type="button">menu</button>
    <a class="docs-brand" href="{home}">{BRAND}</a>
    <nav class="docs-series">
      <a href="{home}blog/web-security/">DevSecOps</a>
      <a href="{home}blog/kubestronaut/">Kubestronaut</a>
      <a class="active" href="../../">English</a>
      <a href="{home}blog/tech-hub/">Tech Hub</a>
    </nav>
    <span class="docs-topbar-spacer"></span>
    <a class="docs-top-link" href="{home}#blogs">blogs</a>
  </header>
  <div class="docs-shell">
{body}
  </div>
  <script src="{home}js/docs.js"></script>
  <script src="{home}js/linear-review.js?v=lr1"></script>
</body>
</html>"""


def patch_topic_index() -> None:
    path = ROOT / "public" / "blog" / "english" / "food-drink" / "index.html"
    text = path.read_text(encoding="utf-8")
    if "review-exercise/" in text:
        return
    review_section = """
      <section class="vocab-level vocab-level--review" id="review">
        <div class="vocab-level__head">
          <span class="vocab-level__badge vocab-level__badge--review">Review</span>
          <h2>Linear Thinking · Capstone exercise</h2>
        </div>
        <p class="vocab-level__desc">Sau B2 — ôn ngữ pháp (6 thì), mental model, cấu trúc Speaking, và mock IELTS Part 1/2/3 (từ vựng B1/B2, dropdown thay từ).</p>
        <div class="vocab-lesson-grid">
          <a class="vocab-lesson-card vocab-lesson-card--review" href="review-exercise/">
            <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 72 72' fill='none'%3E%3Crect width='72' height='72' rx='14' fill='%231a1033'/%3E%3Ccircle cx='36' cy='36' r='22' stroke='%23a78bfa' stroke-width='2.5'/%3E%3Cpath d='M36 20v16l10 8' stroke='%2322d3ee' stroke-width='2.5' stroke-linecap='round'/%3E%3Cpath d='M22 48h28' stroke='%23e4e4e7' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E" alt="" width="72" height="72" loading="lazy">
            <span>Review Exercise</span>
          </a>
        </div>
      </section>
"""
    # Insert before closing article or after B2 section
    marker = '      <section class="vocab-level" id="b2">'
    if marker not in text:
        text = text.replace("    </article>", review_section + "\n    </article>")
    else:
        # After B2 section closes (find next section or end)
        b2_end = text.find("</section>", text.find('id="b2"'))
        if b2_end > 0:
            insert_at = b2_end + len("</section>")
            text = text[:insert_at] + "\n" + review_section + text[insert_at:]
    path.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(build_page(), encoding="utf-8")
    patch_topic_index()
    print("Wrote", OUT / "index.html")
    print("Patched food-drink/index.html with Review section")


if __name__ == "__main__":
    main()
