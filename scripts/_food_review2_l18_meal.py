"""L18 Describe a meal / food — grammar trees + Part 2 examples (Food Review Exercise 2).

Sentence frames from ZIM Food topic; ideas/lexical inspired by ECE / IDP / Aland / ISE / Study4.
Answers follow Lesson 16 five-part frame (not verbatim sample copies).
"""
from __future__ import annotations

from typing import Callable


def lesson18_meal_food_grammar_html(
    *,
    lesson_grammar_tree_html: Callable,
    g_mark: Callable[[str], str],
) -> str:
    tree_basic = lesson_grammar_tree_html(
        "L18 · Thông tin cơ bản",
        "THÔNG TIN CƠ BẢN",
        [
            {
                "label_html": f'{g_mark("What · When · Where · Who")}',
                "openers": [
                    "I'd like to recount a meal that left a mark on me",
                    "It was during… / a couple of years ago / last Tet",
                    "I was with my family / friends at…",
                ],
                "details_label": "1 câu đánh giá",
                "details": [
                    "Although…, which made it a perfect moment for those who…",
                    "It stood out because it wasn't just about food",
                    "a full-on feast · festive vibe · in high spirits",
                ],
            },
            {
                "label_html": f'{g_mark("Mở cố định")}',
                "openers": [
                    "I'm going to talk about + X which + paraphrase",
                    "So, if I had to talk about a meal / dish…",
                ],
                "details_label": "Lexical mở",
                "details": [
                    "memorable / special / unusual meal",
                    "traditional dish · foreign cuisine I'd like to try",
                ],
            },
        ],
        footer=[
            "What · When/Where · Who → 1 evaluation sentence",
            "Reuse L16 open/close frames",
        ],
    )
    tree_describe = lesson_grammar_tree_html(
        "L18 · Mô tả món (ZIM)",
        "MÔ TẢ MÓN ĂN",
        [
            {
                "label_html": f'{g_mark("Thành phần")}',
                "openers": [
                    "This dish consists of…",
                    "One of the ingredients in this dish is…",
                    "It is topped with… / served with… / garnished with…",
                ],
                "details_label": "Ví dụ khung",
                "details": [
                    "grilled… topped with… and served with…",
                    "fresh basil / herbs which add a burst of freshness",
                    "simmered for hours · cooked from scratch · homemade",
                ],
            },
            {
                "label_html": f'{g_mark("Hương vị · Kết cấu")}',
                "openers": [
                    "The flavors in this dish are…",
                    "The taste of this dish is…",
                    "The texture of this dish is…",
                    "This food item has a subtle hint of…",
                ],
                "details_label": "Band lexical",
                "details": [
                    "a perfect balance of sweet and savory",
                    "exquisite · layers of flavors · mouth-watering aroma",
                    "velvety smooth · crisp and refreshing · creamy / rich",
                ],
            },
        ],
        footer=[
            "ZIM frames: consists of · flavors · taste · texture · subtle hint",
        ],
    )
    tree_contrast = lesson_grammar_tree_html(
        "L18 · So sánh + Highlight",
        "SO SÁNH · ĐIỂM NHẤN",
        [
            {
                "label_html": f'{g_mark("So sánh / tương phản")}',
                "openers": [
                    "Compared to…, this dish…",
                    "In contrast to…, this food item…",
                    "While some people prefer…, I personally…",
                ],
                "details_label": "Dùng khi",
                "details": [
                    "lighter / more refreshing than the previous course",
                    "crisp salad ↔ rich creamy soup",
                    "bland porridge ↔ savory homemade spaghetti",
                ],
            },
            {
                "label_html": f'{g_mark("Highlight")}',
                "openers": [
                    "What sets this dish apart is…",
                    "The highlight of this meal is…",
                    "The thing that made the meal special wasn't the food alone…",
                ],
                "details_label": "Idea",
                "details": [
                    "unique combination of spices · explosion of flavor",
                    "family bond · festive vibe · pulled at my heartstrings",
                    "a treat for the taste buds + tradition / culture",
                ],
            },
        ],
        footer=None,
    )
    tree_feel = lesson_grammar_tree_html(
        "L18 · Cảm nhận + Kết",
        "CẢM NHẬN · KẾT",
        [
            {
                "label_html": f'{g_mark("Cảm nhận")}',
                "openers": [
                    "Last time / That meal stood out because…",
                    "It helped me unwind / recharge / lift my spirits",
                    "I would recommend… to anyone who…",
                ],
                "details_label": "Lexical",
                "details": [
                    "left a mark on me · ring in the new year",
                    "in high spirits · chew the fat · fortify family ties",
                    "culinary experience · broaden my palate",
                ],
            },
            {
                "label_html": f'{g_mark("Kết cố định")}',
                "openers": [
                    "So, if I had to talk about a memorable meal…, it would have to be…",
                    "So, if I had to talk about a dish…, it would have to be…",
                ],
                "details_label": "Nhắc lại",
                "details": [
                    "name the meal / dish clearly in the closing line",
                ],
            },
        ],
        footer=None,
    )
    return f"""
          <div class="lr-grammar-notes lr-lex-boost-wrap" id="lesson18-meal-grammar">
            <h4 class="lr-grammar-notes-title">Grammar note · L18 Describe a meal / food</h4>
            <p class="lr-freq-hint">Khung 5 phần cố định · Cốt lõi dùng khung câu <strong>ZIM</strong> (<code>consists of</code> · <code>flavors</code> · <code>taste</code> · <code>texture</code> · <code>Compared to</code> · <code>What sets … apart</code>). Lexical gợi ý từ ECE / IDP / Aland / ISE — <em>không copy nguyên bài mẫu</em>.</p>
            <div class="lr-g-tree-grid lr-g-tree-grid--l17">
{tree_basic}
{tree_describe}
{tree_contrast}
{tree_feel}
            </div>
          </div>"""


def food_lesson18_examples_html(
    *,
    phrase_pick: Callable,
    food_p2_cards_html: Callable,
) -> str:
    cards_data: list[dict] = []

    cards_data.append({
        "cue": "Describe a memorable meal you had",
        "fw": "L18 Meal",
        "bullets": [
            "what the meal was",
            "where you had it",
            "who you were with",
            "and explain why it was memorable",
        ],
        "source": "ECE-style · Memorable meal · nhấn: consists of + festive vibe",
        "choice": "Bữa cơm Tết ở quê bà",
        "secs": [
            (
                "Mở đầu",
                f'{phrase_pick("p2_open", 0)} a memorable meal which left a mark on me during Tet a couple of years ago.',
                "Tôi sẽ nói về một bữa ăn đáng nhớ để lại dấu ấn với tôi vào dịp Tết vài năm trước.",
            ),
            (
                "Thông tin cơ bản",
                "I'd like to recount a full-on feast at my grandmother's house in the countryside. "
                "The whole family had gathered there to ring in the new year. "
                "Although the table looked crowded, the festive vibe made it a perfect moment for those who rarely see each other during the year.",
                "Kể lại bữa tiệc thịnh soạn ở nhà bà · ring in the new year · Although…, which makes it…",
            ),
            (
                "Cốt lõi ★",
                "This meal consisted of bánh chưng, boiled chicken, pickled onions and a variety of home-cooked dishes my grandma had spent days preparing. "
                "One of the ingredients that stood out was fresh herbs, which added a burst of freshness to every plate. "
                "The flavors in this meal were a perfect balance of savory and slightly sweet, with a subtle hint of pepper and fish sauce. "
                "Compared to ordinary weekday dinners, this feast felt much richer and warmer. "
                "What set the meal apart was not only a treat for the taste buds, but the joy of being together — everyone was in high spirits, sharing stories and enjoying the festive vibe. "
                "I remember my grandmother making a short speech to kick things off, and that moment really pulled at my heartstrings.",
                "★ ZIM: consists of · flavors · subtle hint · Compared to · What sets … apart + ECE lexical.",
            ),
            (
                "Cảm nhận",
                "That meal stood out because it reminded me of family, tradition and culture. "
                f'{phrase_pick("p2_feel", 1)} valuing quality time over fancy restaurants.',
                "stood out · tradition · recommend to anyone who…",
            ),
            (
                "Kết",
                f'{phrase_pick("p2_close", 0)} a memorable meal I have had, {phrase_pick("p2_close_tail", 0)} that Tet feast at my grandma\'s house.',
                "So, if I had to talk about…, it would have to be…",
            ),
        ],
        "notes": [
            "left a mark on me · recount · full-on feast · ring in the new year",
            "This dish/meal consists of… · The flavors… are… · subtle hint of…",
            "Compared to… · What sets … apart · treat for the taste buds",
            "in high spirits · festive vibe · pulled at my heartstrings",
        ],
    })

    cards_data.append({
        "cue": "Describe a special meal you have had",
        "fw": "L18 Meal",
        "bullets": [
            "where you had it",
            "who you had it with",
            "what you ate",
            "and explain why it was special for you",
        ],
        "source": "IDP-style · Special meal · nhấn: taste / texture + contrast",
        "choice": "Spaghetti mẹ nấu sau khi ốm",
        "secs": [
            (
                "Mở đầu",
                f'{phrase_pick("p2_open", 1)} a special homemade meal which I had right after recovering from a digestive problem.',
                "Tôi muốn nói về bữa ăn đặc biệt nấu nhà ngay sau khi hồi phục rối loạn tiêu hóa.",
            ),
            (
                "Thông tin cơ bản",
                "It took place at home about two years ago. I had only been able to eat bland porridge for a week, so I was craving something savory. "
                "My mother made spaghetti with beef and mushroom for lunch. "
                "Although it was a basic Italian dish, it instantly made my mood improve.",
                "When/where/who · bland porridge → craving · Although…",
            ),
            (
                "Cốt lõi ★",
                "This dish consisted of ground beef, sliced mushrooms, chopped garlic and onions, all served with tomato sauce and topped with Parmesan cheese. "
                "One of the ingredients I loved most was the fresh mushrooms, which added a soft bite to every forkful. "
                "In contrast to the bland porridge I had eaten all week, this food item was rich and comforting. "
                "The taste of this dish was exquisite — savory beef mixed with a little cheesy flavor. "
                "The texture was velvety smooth because of the creamy tomato sauce that coated every bite. "
                "What set this meal apart was how appetizing and nutritious it felt after days without proper protein and fat.",
                "★ ZIM: consists of · In contrast to · taste · texture · What sets … apart.",
            ),
            (
                "Cảm nhận",
                "We had a quiet lunch together, and the meal helped me recharge after feeling weak. "
                f'{phrase_pick("p2_feel", 2)} it was cooked with care when I needed comfort food the most.',
                "recharge · comfort food · what makes it meaningful…",
            ),
            (
                "Kết",
                f'{phrase_pick("p2_close", 0)} a special meal I have had, {phrase_pick("p2_close_tail", 0)} my mum\'s spaghetti after that long week of porridge.',
                "So, if I had to talk about…, it would have to be…",
            ),
        ],
        "notes": [
            "bland porridge · digestive · topped with · homemade meal",
            "In contrast to… · The taste… is… · The texture… is…",
            "exquisite · velvety smooth · What sets this meal apart",
            "comfort food · recharge",
        ],
    })

    cards_data.append({
        "cue": "Describe a food of another country you would like to try",
        "fw": "L18 Meal",
        "bullets": [
            "what the food is",
            "where it is from",
            "how you know about it",
            "and explain why you would like to try it",
        ],
        "source": "Study4 / exam-style · Foreign food · nhấn: highlight + broaden palate",
        "choice": "Korean soft tofu stew (sundubu-jjigae)",
        "secs": [
            (
                "Mở đầu",
                f'{phrase_pick("p2_open", 0)} a Korean dish which I have never tried but really want to give a shot.',
                "Tôi sẽ nói về một món Hàn tôi chưa từng thử nhưng rất muốn thử một lần.",
            ),
            (
                "Thông tin cơ bản",
                "It's called sundubu-jjigae — a soft tofu stew that originates from Korea. "
                "I first saw it on a food vlog, and later a friend who studied in Seoul kept recommending it. "
                "Although it looks spicy in every photo, the bubbling red broth makes it a perfect comfort food for rainy evenings.",
                "Name · origin · how I know · Although…",
            ),
            (
                "Cốt lõi ★",
                "From what I have researched, this dish consists of soft tofu, seafood or minced meat, kimchi and a gochugaru broth, often served with a raw egg on top. "
                "One of the ingredients that fascinates me is the silken tofu, which should add a burst of creaminess to the spicy soup. "
                "The flavors are said to be a bold balance of spicy, savory and slightly sour. "
                "Compared to the milder soups I usually eat in Vietnam, this food item seems much more intense. "
                "What sets this dish apart is the unique combination of chili heat and soft texture — an explosion of flavor in one bowl. "
                "The highlight for me would be tasting that contrast: fiery broth with gentle tofu.",
                "★ ZIM frames + broaden palate / culinary experience lexical.",
            ),
            (
                "Cảm nhận",
                "I want to try it because it would help me step out of my comfort zone and broaden my palate. "
                "If the dish doesn't suit my taste, I might not give it another shot — but I still love diving into new culinary experiences. "
                f'{phrase_pick("p2_feel", 1)} exploring Asian street-food flavours.',
                "comfort zone · broaden my palate · culinary experiences · recommend…",
            ),
            (
                "Kết",
                f'{phrase_pick("p2_close", 0)} a food of another country I would like to try, {phrase_pick("p2_close_tail", 0)} Korean sundubu-jjigae.',
                "So, if I had to talk about…, it would have to be…",
            ),
        ],
        "notes": [
            "give it a shot · originates from · bubbling broth",
            "This dish consists of… · Compared to… · What sets this dish apart",
            "explosion of flavor · The highlight of…",
            "broaden my palate · culinary experience · step out of my comfort zone",
        ],
    })

    return f"""
        <div class="lr-food-examples" id="food-examples-l18">
          <h3 class="lr-core-subtitle">Ví dụ L18 Describe a meal / food (bài nói đủ 5 phần)</h3>
          <p class="lr-mm-hint">Cốt lõi dùng khung <strong>ZIM</strong> (<em>consists of · flavors · taste · texture · Compared to · What sets … apart</em>). Chỉ <em>nhấn</em> khác nhau: <strong>Tết</strong> = festive highlight · <strong>Spaghetti</strong> = contrast taste/texture · <strong>Sundubu</strong> = foreign dish + palate. Idea/lexical tham khảo ECE · IDP · Aland · ISE · Study4 — viết lại theo 5 phần.</p>
{food_p2_cards_html(cards_data)}
        </div>"""
