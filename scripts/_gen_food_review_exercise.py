#!/usr/bin/env python3
"""Generate Food & Drink · Linear Thinking review exercise (capstone after B2).

Flow: Grammar refs → tense mental model → speaking structures → lesson highlights
      → phrase drills (Lesson-3 frames × Pareto gold words)
      → IELTS Speaking mock (Part 1/2/3) with word dropdowns.
"""
from __future__ import annotations

import html as htmlmod
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "blog" / "english" / "food-drink" / "review-exercise"
OUT2 = ROOT / "public" / "blog" / "english" / "food-drink" / "review-exercise-2"

_spec = importlib.util.spec_from_file_location(
    "gen_ex", Path(__file__).with_name("_gen_english_exercises.py")
)
_gen = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_gen)

_seg_spec = importlib.util.spec_from_file_location(
    "food_segments", Path(__file__).with_name("_food_speaking_segments.py")
)
_seg_mod = importlib.util.module_from_spec(_seg_spec)
assert _seg_spec and _seg_spec.loader
_seg_spec.loader.exec_module(_seg_mod)
SPEAKING_SEGMENTS = _seg_mod.SPEAKING_SEGMENTS

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
    {
        "slug": "lesson-34-how-to-talk-about-the-past-in-english",
        "title": "Talk about the past",
        "why": "Childhood food, used to, past habits",
        "youtube": "https://www.youtube.com/watch?v=rZS5qlCGCIY",
        "model": [
            ("Past Simple", "finished events — <em>Last Sunday I grilled kebab.</em>"),
            ("Past Continuous", "background action — <em>I was chopping vegetables when…</em>"),
            ("used to / would", "past habits — <em>When I was a child, I would eat fast food every day.</em>"),
            ("Time anchors", "when I was younger · last year · as a teenager"),
        ],
        "food": "When I was a child, I <strong>used to</strong> hate vegetables, but now I love a good <em>vegetable salad</em>.",
    },
    {
        "slug": "lesson-57-how-to-use-the-past-perfect-tense-in-english-english-grammar",
        "title": "Past Perfect",
        "why": "Earlier past before another past event",
        "youtube": "https://www.youtube.com/watch?v=iKi4Jy6r-0s",
        "model": [
            ("Form", "had + past participle"),
            ("Earlier past", "event A happened <strong>before</strong> event B (both in the past)"),
            ("Never before", "<em>I had never tried lobster before that trip.</em>"),
            ("Timeline", "had tried → then visited → then tasted"),
        ],
        "food": "Before that dinner, I <strong>had never tasted</strong> blue cheese — so the flavour shocked me.",
    },
    {
        "slug": "lesson-15-how-to-tell-a-story-in-english-using-past-tense",
        "title": "Tell a story (past tense)",
        "why": "Part 2 meal narrative — 4-step structure",
        "youtube": "https://www.youtube.com/watch?v=m04lQ5BUAn0",
        "model": [
            ("1 · Background", "who / when / where / what — set the scene"),
            ("2 · Goal", "what did people want? — <em>We had to finish cooking before guests arrived.</em>"),
            ("3 · Tension", "problems, difficulties, foreshadowing"),
            ("4 · Ending", "resolve tension + retrospective comment — <em>Looking back, it was stressful but fun.</em>"),
        ],
        "food": "It was last month… We wanted to <strong>roast</strong> ribs, but the oven broke — tension — we <strong>grilled</strong> outside instead.",
    },
    {
        "slug": "lesson-23-future-in-english-how-to-talk-about-the-future",
        "title": "Talk about the future",
        "why": "Diet plans, food trends, predictions",
        "youtube": "https://www.youtube.com/watch?v=0anZBvnj6LM",
        "model": [
            ("Present Continuous", "fixed plan with when/where — <em>I'm meeting friends for lunch on Saturday.</em>"),
            ("going to / planning to", "intention, not fully fixed — <em>I'm planning to try a low-carb diet.</em>"),
            ("Present Simple", "timetables — <em>The cooking class starts at 11:30.</em>"),
            ("will / won't", "predictions — <em>People will eat more plant-based food.</em>"),
            ("may / might", "uncertainty — <em>I might order takeout tonight.</em>"),
        ],
        "food": "Next month I'm <strong>going to</strong> cook more at home, and I <strong>will probably</strong> cut down on fast food.",
    },
    {
        "slug": "lesson-61-how-to-add-emphasis-in-english-improve-your-spoken-english",
        "title": "Add emphasis",
        "why": "Highlight what matters most in your answer",
        "youtube": "https://www.youtube.com/watch?v=P-PSlizktNU",
        "model": [
            ("What…is", "<em>What I enjoy most is</em> trying new cuisines."),
            ("It was…that", "cleft — <em>It was the fresh herbs that made the dish special.</em>"),
            ("do/does + V", "<em>I do like</em> spicy food, but not every day."),
            ("so / really / absolutely", "degree — <em>I absolutely love</em> homemade pasta."),
            ("Stress", "put emphasis on the key word when speaking"),
        ],
        "food": "<strong>What I enjoy most</strong> about cooking is the chance to experiment with <em>spices</em> and <em>herbs</em>.",
    },
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
        {"form": "pastry", "vi": "bánh ngọt"},
        {"form": "cereal", "vi": "ngũ cốc"},
    ],
    "meat": [
        {"form": "bacon", "vi": "thịt xông khói"},
        {"form": "veal", "vi": "thịt bê"},
        {"form": "rib", "vi": "sườn"},
        {"form": "lobster", "vi": "tôm hùm"},
        {"form": "beefsteak", "vi": "bít tết"},
    ],
    "seafood": [
        {"form": "seafood", "vi": "hải sản"},
        {"form": "crab", "vi": "thịt cua"},
        {"form": "oyster", "vi": "hàu"},
        {"form": "shellfish", "vi": "hải sản có vỏ"},
    ],
    "cheese": [
        {"form": "blue cheese", "vi": "phô mai xanh"},
        {"form": "Cheddar", "vi": "phô mai cheddar"},
        {"form": "goat cheese", "vi": "phô mai dê"},
        {"form": "Swiss cheese", "vi": "phô mai Thụy Sĩ"},
    ],
    "fruit": [
        {"form": "pomegranate", "vi": "lựu"},
        {"form": "papaya", "vi": "đu đủ"},
        {"form": "cranberry", "vi": "nam việt quất"},
        {"form": "nectarine", "vi": "quả xuân đào"},
        {"form": "coconut", "vi": "dừa"},
    ],
    "sauce": [
        {"form": "soy sauce", "vi": "nước tương"},
        {"form": "ketchup", "vi": "tương cà"},
        {"form": "mustard", "vi": "mù tạt"},
        {"form": "mayonnaise", "vi": "sốt mayonnaise"},
    ],
    "dessert": [
        {"form": "cheesecake", "vi": "bánh phô mai"},
        {"form": "cupcake", "vi": "bánh nướng nhỏ"},
        {"form": "donut", "vi": "bánh rán"},
        {"form": "pudding", "vi": "bánh pudding"},
        {"form": "popsicle", "vi": "kem que"},
    ],
    "cuisine": [
        {"form": "cuisine", "vi": "ẩm thực"},
        {"form": "kebab", "vi": "kebab"},
        {"form": "curry", "vi": "cà ri"},
        {"form": "pasta", "vi": "mì Ý"},
    ],
    "diet_term": [
        {"form": "calorie", "vi": "calo"},
        {"form": "nutrition", "vi": "dinh dưỡng"},
        {"form": "plant-based", "vi": "thuần chay"},
        {"form": "sugar-free", "vi": "không đường"},
    ],
    "kitchen_tool": [
        {"form": "blender", "vi": "máy xay"},
        {"form": "wok", "vi": "wok"},
        {"form": "frying pan", "vi": "chảo rán"},
        {"form": "barbecue", "vi": "bếp nướng"},
    ],
    # Idioms · phrases · slang (Lexical Resource — IELTS band)
    "idiom_taste": [
        {"form": "someone who has a sweet tooth", "vi": "người thích đồ ngọt"},
        {"form": "a bit of a foodie", "vi": "hơi sành ăn"},
        {"form": "not very fussy about food", "vi": "không kén ăn"},
        {"form": "quite health-conscious", "vi": "khá chú ý sức khỏe"},
    ],
    "idiom_ease": [
        {"form": "a piece of cake", "vi": "dễ như ăn bánh"},
        {"form": "as easy as pie", "vi": "dễ như ăn bánh"},
        {"form": "like taking candy from a baby", "vi": "dễ ợt"},
        {"form": "sells like hotcakes", "vi": "bán chạy như tảo nước"},
    ],
    "idiom_enjoy": [
        {"form": "melt in my mouth", "vi": "tan trong miệng"},
        {"form": "the icing on the cake", "vi": "phần thưởng thêm"},
        {"form": "food for thought", "vi": "điều đáng suy ngẫm"},
        {"form": "the spice of life", "vi": "gia vị của cuộc sống (variety)"},
    ],
    "idiom_social": [
        {"form": "chew the fat", "vi": "tám chuyện phiếm"},
        {"form": "bring home the bacon", "vi": "kiếm tiền nuôi gia đình"},
        {"form": "cool as a cucumber", "vi": "bình tĩnh như dưa chuột"},
        {"form": "in a pickle", "vi": "trong tình thế khó"},
    ],
    "idiom_health": [
        {"form": "watch what I eat", "vi": "chú ý thức ăn"},
        {"form": "bite off more than I can chew", "vi": "tham lam quá sức"},
        {"form": "sticks to my ribs", "vi": "no lâu, ấm bụng"},
        {"form": "take health claims with a grain of salt", "vi": "hoài nghi quảng cáo sức khỏe"},
    ],
    "phrase_food": [
        {"form": "grab a bite", "vi": "ăn vội một miếng"},
        {"form": "dine out", "vi": "ăn ngoài"},
        {"form": "treat yourself", "vi": "tự thưởng cho bản thân"},
        {"form": "comfort food", "vi": "đồ ăn an ủi"},
        {"form": "guilty pleasure", "vi": "thú thích tội lỗi"},
        {"form": "home-cooked meal", "vi": "bữa ăn nấu ở nhà"},
    ],
    "slang_food": [
        {"form": "pig out", "vi": "ăn thả ga (slang)"},
        {"form": "scarf down", "vi": "nuốt vội (slang)"},
        {"form": "splash out on food", "vi": "chi đậm cho đồ ăn"},
        {"form": "grab takeaway", "vi": "mua đồ mang về"},
        {"form": "booze", "vi": "uống có cồn (informal)"},
    ],
    # Lesson 2 · interchangeable benefit phrases (dropdown in practice cards)
    "relax_phrase": [
        {"form": "unwind and recharge their batteries", "vi": "thư giãn và nạp lại năng lượng"},
        {"form": "relax and clear their head", "vi": "thư giãn và giải tỏa đầu óc"},
        {"form": "reduce stress after a long day", "vi": "giảm căng thẳng sau ngày dài"},
        {"form": "escape from the hustle and bustle of the city", "vi": "thoát khỏi sự hối hả thành phố"},
        {"form": "temporarily forget all the pressures from their work", "vi": "tạm quên áp lực công việc"},
    ],
    "relax_followup": [
        {"form": "Being in the kitchen also helps them temporarily forget all the pressures from their work.", "vi": "Ở trong bếp cũng giúp họ tạm quên áp lực công việc."},
        {"form": "Cooking at home also gives them a chance to escape from reality for a while.", "vi": "Nấu ở nhà cũng cho họ cơ hội thoát khỏi thực tại một lúc."},
        {"form": "It also helps them express their inner feelings through food.", "vi": "Nó cũng giúp họ thể hiện cảm xúc qua món ăn."},
        {"form": "—", "vi": "không thêm câu"},
    ],
    "health_phrase": [
        {"form": "stay healthy and prevent various health problems", "vi": "giữ khỏe và phòng bệnh"},
        {"form": "keep fit and burn excess calories", "vi": "giữ dáng và đốt calo thừa"},
        {"form": "strengthen their muscles and maintain a healthy weight", "vi": "tăng cơ và duy trì cân nặng"},
        {"form": "improve their health and keep in shape", "vi": "cải thiện sức khỏe và giữ dáng"},
    ],
    "health_followup": [
        {"form": "It also helps them strengthen their muscles.", "vi": "Nó cũng giúp tăng cơ bắp."},
        {"form": "Eating vegetables can also prevent problems such as high blood pressure.", "vi": "Ăn rau cũng có thể phòng cao huyết áp."},
        {"form": "—", "vi": "không thêm câu"},
    ],
    "edu_phrase": [
        {"form": "learn how to manage my diet better and make healthier choices", "vi": "học cách quản lý chế độ ăn tốt hơn"},
        {"form": "enrich my knowledge about nutrition and cooking", "vi": "làm giàu kiến thức dinh dưỡng và nấu ăn"},
        {"form": "learn skills such as money management and problem-solving", "vi": "học kỹ năng như quản lý tiền và giải quyết vấn đề"},
        {"form": "widen my horizons by exploring different food cultures", "vi": "mở rộng tầm nhìn qua ẩm thực đa dạng"},
    ],
    # Dislike · Lesson 2/3 reasons (contextual — for Không thích dropdowns)
    "dislike_feel": [
        {"form": "makes me exhausted", "vi": "khiến tôi kiệt sức"},
        {"form": "makes me bored", "vi": "khiến tôi chán"},
        {"form": "makes me stressed", "vi": "khiến tôi căng thẳng"},
        {"form": "makes them exhausted", "vi": "khiến họ kiệt sức"},
        {"form": "makes them bored and frustrated", "vi": "khiến họ chán và bực"},
    ],
    "dislike_duty": [
        {"form": "have to deal with the same tasks every day", "vi": "phải làm việc lặp lại mỗi ngày"},
        {"form": "have to spend hours preparing ingredients", "vi": "phải mất hàng giờ chuẩn bị nguyên liệu"},
        {"form": "have to clean up a messy kitchen afterwards", "vi": "phải dọn bếp lộn xộn sau đó"},
        {"form": "have to deal with difficult customers", "vi": "phải đối phó khách khó tính"},
    ],
    "dislike_no_benefit": [
        {"form": "It doesn't give me the chance to try anything new", "vi": "Không cho tôi cơ hội thử điều mới"},
        {"form": "It doesn't help me relax", "vi": "Không giúp tôi thư giãn"},
        {"form": "It doesn't help me enrich my knowledge", "vi": "Không giúp làm giàu kiến thức"},
        {"form": "It doesn't give me the opportunity to widen my horizons", "vi": "Không cho cơ hội mở rộng tầm nhìn"},
        {"form": "It doesn't help me learn useful skills", "vi": "Không giúp học kỹ năng hữu ích"},
    ],
    "soft_dislike": [
        {"form": "isn't my cup of tea", "vi": "không phải sở thích của tôi"},
        {"form": "isn't really my thing", "vi": "không phải gu của tôi"},
        {"form": "doesn't appeal to me", "vi": "không hấp dẫn tôi"},
        {"form": "is not something I'm keen on", "vi": "không phải thứ tôi thích"},
    ],
    "taste_complaint": [
        {"form": "they don't give me richer flavours", "vi": "không mang lại hương vị phong phú"},
        {"form": "they taste too bland", "vi": "chúng quá nhạt"},
        {"form": "they don't help me enjoy my meals", "vi": "không giúp thưởng thức bữa ăn"},
        {"form": "the texture feels strange to me", "vi": "cảm giác kết cấu lạ"},
    ],
    "unhealthy_food": [
        {"form": "fast food", "vi": "đồ ăn nhanh"},
        {"form": "junk food", "vi": "đồ ăn vặt không lành mạnh"},
        {"form": "greasy take-away", "vi": "đồ mang về nhiều dầu"},
        {"form": "fried snacks", "vi": "đồ chiên"},
        {"form": "sugary soft drinks", "vi": "nước ngọt có đường"},
    ],
    "health_outcome": [
        {"form": "various health problems, such as diabetes, heart attack, high blood pressure or even cancer", "vi": "nhiều vấn đề SK: tiểu đường, đau tim, huyết áp cao, ung thư"},
        {"form": "obesity and high blood pressure", "vi": "béo phì và huyết áp cao"},
        {"form": "serious problems such as stroke or heart disease", "vi": "vấn đề nghiêm trọng như đột quỵ hoặc bệnh tim"},
        {"form": "a shorter life expectancy over time", "vi": "tuổi thọ ngắn hơn theo thời gian"},
    ],
    "convenience_benefit": [
        {"form": "it helps me unwind after a long day", "vi": "giúp thư giãn sau ngày dài"},
        {"form": "it saves me a lot of time", "vi": "tiết kiệm nhiều thời gian"},
        {"form": "it's convenient when I'm too busy to cook", "vi": "tiện khi tôi quá bận để nấu"},
    ],
    "food_taste_reason": [
        {"form": "they wake up my taste buds", "vi": "chúng đánh thức vị giác của tôi"},
        {"form": "they make every meal more exciting", "vi": "chúng làm mọi bữa ăn thú vị hơn"},
        {"form": "the flavours are so rich and memorable", "vi": "hương vị rất đậm và đáng nhớ"},
        {"form": "I'm a bit of a foodie when it comes to spices", "vi": "tôi hơi sành ăn với đồ cay"},
    ],
    "social_benefit": [
        {"form": "a great way to escape from reality for a while", "vi": "cách tuyệt để thoát thực tại một lúc"},
        {"form": "a great way to unwind with friends", "vi": "cách tuyệt để thư giãn với bạn"},
        {"form": "a chance to try something new together", "vi": "cơ hội thử món mới cùng nhau"},
        {"form": "a great way to grab a bite and catch up", "vi": "cách tuyệt để ăn vội và tám chuyện"},
    ],
    "job_benefit": [
        {"form": "gives me the chance to challenge myself", "vi": "cho cơ hội thử thách bản thân"},
        {"form": "helps me learn how to work effectively in a team", "vi": "giúp học làm việc nhóm hiệu quả"},
        {"form": "pushes me to become more confident and independent", "vi": "đẩy tôi tự tin và độc lập hơn"},
    ],
    # Food-only benefits (NEVER reuse job_benefit in Food Qs)
    "food_benefit": [
        {"form": "helps me explore new flavours", "vi": "giúp tôi khám phá hương vị mới"},
        {"form": "helps me strengthen my muscles when I cook and stay active", "vi": "giúp tăng cơ khi nấu và vận động"},
        {"form": "gives me richer flavours in every dish", "vi": "mang lại hương vị phong phú hơn"},
        {"form": "makes every meal more memorable", "vi": "làm mọi bữa ăn đáng nhớ hơn"},
        {"form": "helps me burn a few extra calories", "vi": "giúp đốt thêm một ít calo"},
        {"form": "wakes up my taste buds", "vi": "đánh thức vị giác của tôi"},
    ],
    "food_health_threat": [
        {"form": "pose a threat to my health", "vi": "gây đe dọa đến sức khỏe"},
        {"form": "take a heavy toll on my health", "vi": "gây hậu quả nặng nề cho sức khỏe"},
        {"form": "can shorten my life expectancy", "vi": "có thể làm giảm tuổi thọ"},
        {"form": "can lead to various stomach problems", "vi": "có thể dẫn đến nhiều vấn đề về dạ dày"},
        {"form": "can lead to obesity and high blood pressure", "vi": "có thể dẫn đến béo phì và huyết áp cao"},
    ],
    "allergy_risk": [
        {"form": "can lead to allergies", "vi": "có thể gây dị ứng"},
        {"form": "can cause food poisoning if it isn't fresh", "vi": "có thể ngộ độc nếu không tươi"},
        {"form": "might not be safe for people with shellfish allergies", "vi": "có thể không an toàn nếu dị ứng shellfish"},
    ],
    # Lesson 3 · Favourite tactic
    "hardly_ever_action": [
        {"form": "cook", "vi": "nấu ăn"},
        {"form": "cook at home", "vi": "nấu ở nhà"},
        {"form": "eat spicy dishes", "vi": "ăn món cay"},
        {"form": "eat this kind of food", "vi": "ăn loại đồ ăn này"},
        {"form": "eat out", "vi": "ăn ngoài"},
        {"form": "order take-away", "vi": "gọi đồ mang về"},
    ],
    "prefer_rather_than": [
        {"form": "to cook at home rather than eat out", "vi": "nấu ở nhà hơn là ăn ngoài"},
        {"form": "to eat home-cooked meals rather than grab take-away", "vi": "ăn đồ nấu nhà hơn gọi mang về"},
        {"form": "to have mild dishes rather than spicy food", "vi": "ăn món dịu hơn món cay"},
        {"form": "home-cooked food rather than eating out", "vi": "đồ nấu nhà hơn ăn ngoài"},
        {"form": "to grab a bite at home rather than dine out", "vi": "ăn vội ở nhà hơn ăn nhà hàng"},
    ],
    "stomach_problem": [
        {"form": "various stomach problems", "vi": "nhiều vấn đề về dạ dày"},
        {"form": "heartburn and indigestion", "vi": "ợ nóng và khó tiêu"},
        {"form": "stomach pain after meals", "vi": "đau bụng sau bữa ăn"},
    ],
    # Lesson 5 · What kind of X do you like most?
    "kind_choice_food": [
        {"form": "home-cooked food", "vi": "đồ ăn nấu ở nhà"},
        {"form": "street food", "vi": "đồ ăn đường phố"},
        {"form": "seafood", "vi": "hải sản"},
        {"form": "plant-based meals", "vi": "bữa ăn thực vật"},
        {"form": "comfort food", "vi": "đồ ăn an ủi"},
    ],
    "kind_choice_cuisine": [
        {"form": "Vietnamese cuisine", "vi": "ẩm thực Việt"},
        {"form": "Japanese cuisine", "vi": "ẩm thực Nhật"},
        {"form": "Italian cuisine", "vi": "ẩm thực Ý"},
        {"form": "Korean cuisine", "vi": "ẩm thực Hàn"},
        {"form": "Mediterranean cuisine", "vi": "ẩm thực Địa Trung Hải"},
    ],
    "kind_choice_restaurant": [
        {"form": "casual local eateries", "vi": "quán bình dân gần nhà"},
        {"form": "family-run restaurants", "vi": "nhà hàng gia đình"},
        {"form": "buffet restaurants", "vi": "nhà hàng buffet"},
        {"form": "fine-dining places", "vi": "nhà hàng cao cấp"},
        {"form": "open-air food courts", "vi": "khu ẩm thực ngoài trời"},
    ],
    "kind_choice_drink": [
        {"form": "fresh fruit juice", "vi": "nước ép trái cây tươi"},
        {"form": "herbal tea", "vi": "trà thảo mộc"},
        {"form": "iced coffee", "vi": "cà phê đá"},
        {"form": "smoothie bowls", "vi": "sinh tố dạng bát"},
        {"form": "sparkling water", "vi": "nước có ga"},
    ],
    "kind_choice_fruit": [
        {"form": "tropical fruit like mango and papaya", "vi": "trái nhiệt đới như xoài và đu đủ"},
        {"form": "citrus fruit such as oranges and tangerines", "vi": "cam quýt như cam và quýt"},
        {"form": "berries", "vi": "quả mọng"},
        {"form": "bananas", "vi": "chuối"},
        {"form": "watermelon in summer", "vi": "dưa hấu mùa hè"},
    ],
    "kind_choice_snack": [
        {"form": "nuts and seeds", "vi": "hạt và hạt giống"},
        {"form": "fresh fruit", "vi": "trái cây tươi"},
        {"form": "yoghurt with granola", "vi": "sữa chua với granola"},
        {"form": "rice crackers", "vi": "bánh gạo"},
        {"form": "dark chocolate in small amounts", "vi": "sô-cô-la đen lượng nhỏ"},
    ],
    "kind_choice_dessert": [
        {"form": "fruit-based desserts", "vi": "tráng miệng từ trái cây"},
        {"form": "cheesecake", "vi": "bánh phô mai"},
        {"form": "homemade pudding", "vi": "pudding tự làm"},
        {"form": "ice cream", "vi": "kem"},
        {"form": "mochi", "vi": "bánh mochi"},
    ],
    "kind_choice_method": [
        {"form": "grilled dishes", "vi": "món nướng"},
        {"form": "steamed dishes", "vi": "món hấp"},
        {"form": "stir-fried dishes", "vi": "món xào"},
        {"form": "slow-cooked stews", "vi": "món hầm chậm"},
        {"form": "fresh salads", "vi": "salad tươi"},
    ],
    "kind_choice_street": [
        {"form": "pho and spring rolls", "vi": "phở và gỏi cuốn"},
        {"form": "grilled skewers", "vi": "xiên nướng"},
        {"form": "banh mi", "vi": "bánh mì"},
        {"form": "sticky rice", "vi": "xôi"},
        {"form": "fresh summer rolls", "vi": "gỏi cuốn tươi"},
    ],
    "kind_choice_meal": [
        {"form": "a light breakfast", "vi": "bữa sáng nhẹ"},
        {"form": "a proper sit-down lunch", "vi": "bữa trưa ngồi ăn tử tế"},
        {"form": "an early dinner at home", "vi": "bữa tối sớm ở nhà"},
        {"form": "brunch at the weekend", "vi": "brunch cuối tuần"},
        {"form": "a late supper after work", "vi": "bữa khuya sau giờ làm"},
    ],
    "kind_lex_adj": [
        {"form": "mouth-watering and packed with flavour", "vi": "cực ngon và đầy hương vị"},
        {"form": "wholesome and freshly prepared", "vi": "lành mạnh và mới chế biến"},
        {"form": "light on the stomach but still filling", "vi": "dễ tiêu mà vẫn no"},
        {"form": "comforting without being too greasy", "vi": "an ủi mà không quá nhiều dầu"},
        {"form": "trendy yet still affordable", "vi": "hợp mốt mà vẫn vừa túi tiền"},
    ],
    "kind_lex_reason": [
        {"form": "much healthier than restaurant food", "vi": "lành mạnh hơn nhiều so với đồ nhà hàng"},
        {"form": "made from scratch with fresh ingredients", "vi": "làm từ đầu với nguyên liệu tươi"},
        {"form": "a great way to stick to a balanced diet", "vi": "cách tuyệt để giữ chế độ ăn cân bằng"},
        {"form": "full of nutrients without taking a heavy toll on my health", "vi": "đầy dinh dưỡng mà không hại sức khỏe"},
        {"form": "the kind of food that really hits the spot after a long day", "vi": "đúng gu sau một ngày dài"},
    ],
    "kind_followup": [
        {"form": "I try not to eat out too often.", "vi": "Tôi cố gắng không ăn ngoài quá thường xuyên."},
        {"form": "I try to cut down on processed snacks.", "vi": "Tôi cố gắng giảm đồ ăn vặt chế biến sẵn."},
        {"form": "I also get the chance to grab a bite without feeling heavy afterwards.", "vi": "Tôi cũng được ăn vội mà không bị nặng bụng."},
        {"form": "It helps me keep fit and burn a few extra calories.", "vi": "Giúp tôi giữ dáng và đốt thêm calo."},
        {"form": "I try using seasonal ingredients whenever I can.", "vi": "Tôi cố thử dùng nguyên liệu theo mùa khi có thể."},
    ],
    # Lesson 6 · Do you prefer X or Y?
    "prefer_pair_home": [
        {"form": "eating at home to eating out", "vi": "ăn ở nhà hơn ăn ngoài (X to Y)"},
        {"form": "eating at home rather than eating out", "vi": "ăn ở nhà hơn là ăn ngoài"},
        {"form": "cooking at home to ordering takeaway", "vi": "nấu ở nhà hơn gọi mang về"},
    ],
    "prefer_pair_sweet": [
        {"form": "savoury dishes to sweet desserts", "vi": "món mặn hơn món ngọt"},
        {"form": "sweet snacks rather than savoury ones", "vi": "đồ ngọt hơn đồ mặn"},
        {"form": "fruit-based desserts to heavy cakes", "vi": "tráng miệng trái cây hơn bánh nặng"},
    ],
    "prefer_pair_social": [
        {"form": "eating with my family to eating alone", "vi": "ăn với gia đình hơn ăn một mình"},
        {"form": "sharing a meal with friends rather than dining on my own", "vi": "chia sẻ bữa với bạn hơn ăn một mình"},
        {"form": "cooking with someone to cooking by myself", "vi": "nấu cùng ai đó hơn nấu một mình"},
    ],
    "prefer_pair_health": [
        {"form": "wholesome home-cooked meals to fast food", "vi": "bữa nấu nhà lành mạnh hơn fast food"},
        {"form": "fresh ingredients rather than processed snacks", "vi": "nguyên liệu tươi hơn đồ chế biến sẵn"},
        {"form": "a balanced diet to greasy takeaway", "vi": "chế độ ăn cân bằng hơn đồ mang về nhiều dầu"},
    ],
    "prefer_pair_drink": [
        {"form": "herbal tea to coffee", "vi": "trà thảo mộc hơn cà phê"},
        {"form": "fresh juice rather than soft drinks", "vi": "nước ép hơn nước ngọt"},
        {"form": "drinking water to sugary drinks", "vi": "uống nước hơn đồ ngọt"},
    ],
    "prefer_pair_taste": [
        {"form": "mild dishes to spicy food", "vi": "món dịu hơn món cay"},
        {"form": "spicy food rather than bland meals", "vi": "món cay hơn món nhạt"},
        {"form": "grilled dishes to deep-fried food", "vi": "món nướng hơn đồ chiên ngập dầu"},
    ],
    "prefer_it_takes": [
        {"form": "it takes me about an hour to cook a proper meal from scratch", "vi": "mất khoảng một giờ để nấu bữa tử tế từ đầu"},
        {"form": "it can take several hours to prepare a traditional feast", "vi": "có thể mất vài giờ để chuẩn bị tiệc truyền thống"},
        {"form": "it only takes a few minutes to grab a bite from a street stall", "vi": "chỉ mất vài phút để ăn vội ở quán đường phố"},
        {"form": "it only takes several seconds to order takeaway on an app", "vi": "chỉ mất vài giây để gọi mang về trên app"},
    ],
    "prefer_feeling": [
        {"form": "sitting around the table with my family and tasting freshly cooked dishes", "vi": "ngồi quanh bàn với gia đình, thưởng thức món mới nấu"},
        {"form": "cooking slowly and smelling the spices in the kitchen", "vi": "nấu chậm và ngửi mùi gia vị trong bếp"},
        {"form": "sharing a hot pot and chatting over food", "vi": "ăn lẩu chung và tám chuyện bên bàn ăn"},
        {"form": "sipping tea after a light homemade meal", "vi": "nhấp trà sau bữa ăn nhà nhẹ"},
    ],
    "prefer_have_someone": [
        {"form": "have someone to share the meal with", "vi": "có ai đó để chia sẻ bữa ăn"},
        {"form": "have someone to try new dishes with", "vi": "có ai đó để thử món mới cùng"},
        {"form": "have someone to help me in the kitchen", "vi": "có ai đó giúp tôi trong bếp"},
        {"form": "have someone to send food recommendations to", "vi": "có ai đó để gửi gợi ý món ăn"},
    ],
    "prefer_function": [
        {"form": "my body functions more effectively throughout the day", "vi": "cơ thể tôi hoạt động hiệu quả hơn cả ngày"},
        {"form": "my brain functions better when I eat a balanced breakfast", "vi": "não hoạt động tốt hơn khi tôi ăn sáng cân bằng"},
        {"form": "my body cannot function normally if nutrients are in short supply", "vi": "cơ thể không hoạt động bình thường nếu thiếu dinh dưỡng"},
        {"form": "I function better at work after a wholesome lunch", "vi": "tôi làm việc hiệu quả hơn sau bữa trưa lành mạnh"},
    ],
    "prefer_contrast": [
        {"form": "while eating out is often more time-consuming and expensive", "vi": "trong khi ăn ngoài thường tốn thời gian và đắt hơn"},
        {"form": "whereas fast food can pose a threat to my health", "vi": "trong khi fast food có thể đe dọa sức khỏe"},
        {"form": "while cooking alone feels quieter and a bit lonely", "vi": "trong khi nấu một mình yên hơn và hơi cô đơn"},
        {"form": "whereas sugary drinks take a heavy toll on my health over time", "vi": "trong khi đồ ngọt dần gây hại nặng cho sức khỏe"},
    ],
    "prefer_send": [
        {"form": "send photos of my homemade dishes to my friends", "vi": "gửi ảnh món tự nấu cho bạn bè"},
        {"form": "send a recipe to my sister", "vi": "gửi công thức cho chị/em gái"},
        {"form": "send food recommendations to colleagues", "vi": "gửi gợi ý quán ăn cho đồng nghiệp"},
        {"form": "send a grocery list to my roommate", "vi": "gửi danh sách đi chợ cho bạn cùng phòng"},
    ],
}

# ── Mind map helpers (shared: Section 2 tenses + Lesson 2/3) ───────────────

def tip(en: str, vi: str) -> dict:
    """Phrase leaf with Vietnamese hover tooltip (no HTML in en)."""
    return {"en": en, "vi": vi}


def tip_html(html_en: str, vi: str) -> dict:
    """Phrase leaf with raw HTML + Vietnamese hover tooltip."""
    return {"html": html_en, "vi": vi}


def _mmap_leaf_html(leaf) -> str:
    if isinstance(leaf, dict) and leaf.get("vi"):
        body = leaf["html"] if leaf.get("html") is not None else esc(leaf.get("en", ""))
        return (
            f'                <li class="lr-mmap-leaf lr-tip" data-mmap-node="leaf" '
            f'data-tip="{esc(leaf["vi"])}" title="{esc(leaf["vi"])}">'
            f'<span class="lr-tip-text">{body}</span></li>'
        )
    if isinstance(leaf, tuple):
        label, body = leaf
        return (
            f'                <li class="lr-mmap-leaf" data-mmap-node="leaf">'
            f'<span class="lr-mmap-k">{esc(label)}</span> {body}</li>'
        )
    return f'                <li class="lr-mmap-leaf" data-mmap-node="leaf">{leaf}</li>'


def _mmap_branch_html(node: dict) -> str:
    if node.get("flow"):
        return _lesson_flow_branch_html(node)
    color = esc(node["color"])
    star = (
        '<span class="lr-mmap-star" title="Có trong Section 3 · Speaking structures — xem kỹ">★</span>'
        if node.get("speaking")
        else ""
    )
    num = node.get("hana_num")
    num_html = (
        f'<span class="lr-mmap-num" title="Khớp timeline #{num}">{num}</span>'
        if num
        else ""
    )
    branch_id = f' id="mmap-tn-{num}"' if num else ""
    name_vi = (
        f'<span>{esc(node["name_vi"])}</span>' if node.get("name_vi") else ""
    )
    forks = []
    for fork in node["forks"]:
        leaves = "\n".join(_mmap_leaf_html(leaf) for leaf in fork["leaves"])
        forks.append(
            f"""              <div class="lr-mmap-group">
                <span class="lr-mmap-fork" data-mmap-node="fork">{esc(fork["label"])}</span>
                <ul class="lr-mmap-leaves">
{leaves}
                </ul>
              </div>"""
        )
    extra = " lr-mmap-tense--starred" if node.get("speaking") else ""
    return f"""          <div class="lr-mmap-branch" data-mmap-branch="{esc(node["id"])}"{branch_id} style="--mmap-c:{color}">
            <div class="lr-mmap-tense{extra}" data-mmap-node="tense">
              {num_html}<strong>{esc(node["name"])}</strong>{star}
              {name_vi}
            </div>
            <div class="lr-mmap-forks">
{chr(10).join(forks)}
            </div>
          </div>"""


def _lesson_flow_branch_html(node: dict) -> str:
    color = esc(node["color"])
    name_vi = (
        f'<span>{esc(node["name_vi"])}</span>' if node.get("name_vi") else ""
    )
    branches = []
    for br in node["branches"]:
        pattern_html = ""
        if br.get("patterns"):
            pattern_html = (
                f'<p class="lr-flow-patterns">{br["patterns"]}</p>'
            )
        leaves = "\n".join(_mmap_leaf_html(leaf) for leaf in br["leaves"])
        branches.append(
            f"""              <div class="lr-flow-branch" data-mmap-node="fork">
                <span class="lr-flow-branch-label">{esc(br["label"])}</span>
                {pattern_html}
                <ul class="lr-mmap-leaves">
{leaves}
                </ul>
              </div>"""
        )
    link_html = ""
    if node.get("link"):
        link_html = f'<p class="lr-flow-link">{node["link"]}</p>'
    return f"""          <div class="lr-mmap-branch lr-mmap-branch--flow" data-mmap-branch="{esc(node["id"])}" style="--mmap-c:{color}">
            <div class="lr-mmap-tense" data-mmap-node="tense">
              <strong>{esc(node["name"])}</strong>
              {name_vi}
            </div>
            <div class="lr-flow-pipeline">
              <div class="lr-flow-step lr-flow-step--opener" data-mmap-node="fork">
                <span class="lr-flow-step-label">① Mở</span>
                <span class="lr-flow-step-body">{node["opener"]}</span>
              </div>
              <div class="lr-flow-because" data-mmap-node="fork">because</div>
              <div class="lr-flow-branches">
{chr(10).join(branches)}
              </div>
              {link_html}
            </div>
          </div>"""


def mind_map_html(
    map_id: str,
    aria_label: str,
    root_title: str,
    root_sub: str,
    left: list[dict],
    right: list[dict],
    *,
    note: str = "",
    extra_class: str = "",
    min_width: str = "1240px",
) -> str:
    left_html = "\n".join(_mmap_branch_html(n) for n in left)
    right_html = "\n".join(_mmap_branch_html(n) for n in right)
    note_html = f'\n        <p class="lr-mmap-note">{note}</p>' if note else ""
    return f"""
      <div class="lr-mmap{extra_class}" id="{esc(map_id)}" aria-label="{esc(aria_label)}" style="--mmap-min:{esc(min_width)}">
        <p class="lr-mmap-scroll-hint">Vuốt ngang nếu sơ đồ rộng hơn màn hình</p>
        <div class="lr-mmap-viewport">
          <div class="lr-mmap-board">
            <svg class="lr-mmap-svg" aria-hidden="true"></svg>
            <div class="lr-mmap-col lr-mmap-col--left">
{left_html}
            </div>
            <div class="lr-mmap-root" data-mmap-node="root">
              <span class="lr-mmap-root-title">{root_title}</span>
              <span class="lr-mmap-root-sub">{root_sub}</span>
            </div>
            <div class="lr-mmap-col lr-mmap-col--right">
{right_html}
            </div>
          </div>
        </div>{note_html}
      </div>"""


def _tense_forks(struct: list[tuple], signals: list[str]) -> list[dict]:
    return [
        {"label": "Cấu trúc", "leaves": list(struct)},
        {"label": "Dấu hiệu nhận biết", "leaves": signals},
    ]


# 6 nhóm IELTS Fighter · ★ = xuất hiện Section 3 speaking catch-up
TENSE_MINDMAP_LEFT = [
    {
        "id": "past-ppc",
        "color": "#a78bfa",
        "name": "Past Perfect Continuous",
        "name_vi": "QK hoàn thành tiếp diễn",
        "hana_num": 12,
        "forks": _tense_forks(
            [
                ("Khẳng định", "S + had been + V-ing"),
                ("Phủ định", "S + hadn't been + V-ing"),
                ("Nghi vấn", "Had + S + been + V-ing?"),
            ],
            ["for, since (đến một mốc trong quá khứ)", "had been cooking for hours when…"],
        ),
    },
    {
        "id": "past-perfect",
        "color": "#c4b5fd",
        "name": "Past Perfect",
        "name_vi": "Quá khứ hoàn thành",
        "hana_num": 11,
        "speaking": True,
        "forks": _tense_forks(
            [
                ("Khẳng định", "S + had + V₃"),
                ("Phủ định", "S + had + not + V₃"),
                ("Nghi vấn", "Had + S + V₃?"),
            ],
            [
                "before, after, by the time, already",
                "Food: I <strong>had never tried</strong> lobster before that trip.",
            ],
        ),
    },
    {
        "id": "past-cont",
        "color": "#67e8f9",
        "name": "Past Continuous",
        "name_vi": "Quá khứ tiếp diễn",
        "hana_num": 10,
        "speaking": True,
        "forks": _tense_forks(
            [
                ("Khẳng định", "S + was/were + V-ing"),
                ("Phủ định", "S + was/were + not + V-ing"),
                ("Nghi vấn", "Was/Were + S + V-ing?"),
            ],
            [
                "while, when · at this time yesterday",
                "Food: I <strong>was chopping</strong> vegetables when…",
            ],
        ),
    },
    {
        "id": "past-simple",
        "color": "#5eead4",
        "name": "Past Simple",
        "name_vi": "Quá khứ đơn",
        "hana_num": 9,
        "speaking": True,
        "forks": _tense_forks(
            [
                ("Khẳng định", "S + V(ed / cột 2)"),
                ("Phủ định", "S + did + not + V"),
                ("Nghi vấn", "Did + S + V?"),
            ],
            [
                "yesterday, last week, ago, in 2000",
                "Food: Last Sunday I <strong>grilled</strong> kebab.",
            ],
        ),
    },
    {
        "id": "used-to",
        "color": "#34d399",
        "name": "used to / would",
        "name_vi": "Thói quen quá khứ",
        "speaking": True,
        "forks": _tense_forks(
            [
                ("Khẳng định", "S + used to + V · S + would + V"),
                ("Phủ định", "S + didn't use to + V"),
                ("Nghi vấn", "Did + S + use to + V?"),
            ],
            [
                "when I was a child · as a teenager",
                "don't … any more ≈ used to",
                "Food: I <strong>would eat</strong> fast food every day.",
            ],
        ),
    },
]

TENSE_MINDMAP_RIGHT = [
    {
        "id": "pres-simple",
        "color": "#93c5fd",
        "name": "Present Simple",
        "name_vi": "Hiện tại đơn",
        "hana_num": 1,
        "speaking": True,
        "forks": _tense_forks(
            [
                ("Khẳng định", "S + V(s/es)"),
                ("Phủ định", "S + do/does + not + V"),
                ("Nghi vấn", "Do/Does + S + V?"),
            ],
            [
                "always, usually, often · every day/week",
                "timetables: The class <strong>starts</strong> at 11:30",
                "Food: I <strong>usually</strong> have rice.",
            ],
        ),
    },
    {
        "id": "pres-cont",
        "color": "#60a5fa",
        "name": "Present Continuous",
        "name_vi": "Hiện tại tiếp diễn",
        "hana_num": 2,
        "speaking": True,
        "forks": _tense_forks(
            [
                ("Khẳng định", "S + am/is/are + V-ing"),
                ("Phủ định", "S + am/is/are + not + V-ing"),
                ("Nghi vấn", "Am/Is/Are + S + V-ing?"),
            ],
            [
                "now, at the moment · fixed future plan (when/where)",
                "Food: I'm <strong>trying</strong> a low-carb diet.",
                "Food: I'm <strong>meeting</strong> friends for lunch Saturday.",
            ],
        ),
    },
    {
        "id": "pres-perfect",
        "color": "#38bdf8",
        "name": "Present Perfect",
        "name_vi": "Hiện tại hoàn thành",
        "hana_num": 3,
        "speaking": True,
        "forks": _tense_forks(
            [
                ("Khẳng định", "S + have/has + V₃"),
                ("Phủ định", "S + have/has + not + V₃"),
                ("Nghi vấn", "Have/Has + S + V₃?"),
            ],
            [
                "ever, never, already, yet · for/since (no time)",
                "Food: <strong>Have you ever tried</strong> sushi?",
                "+ time → switch to Past Simple",
            ],
        ),
    },
    {
        "id": "pres-ppc",
        "color": "#7dd3fc",
        "name": "Present Perfect Continuous",
        "name_vi": "HT hoàn thành tiếp diễn",
        "hana_num": 4,
        "speaking": True,
        "forks": _tense_forks(
            [
                ("Khẳng định", "S + have/has been + V-ing"),
                ("Phủ định", "S + haven't/hasn't been + V-ing"),
                ("Nghi vấn", "Have/Has + S + been + V-ing?"),
            ],
            [
                "for, since, lately, recently",
                "Food: I've <strong>been cooking</strong> at home more lately.",
            ],
        ),
    },
    {
        "id": "going-to-will",
        "color": "#fbbf24",
        "name": "going to / will",
        "name_vi": "Tương lai gần",
        "hana_num": 5,
        "speaking": True,
        "forks": _tense_forks(
            [
                ("Kế hoạch", "S + am/is/are going to + V"),
                ("Dự đoán", "S + will / won't + V"),
                ("Gần", "may / might + V (không chắc)"),
            ],
            [
                "tonight, tomorrow, next week",
                "Food: I'm <strong>going to cook</strong> pasta tonight.",
                "Food: People <strong>will eat</strong> more plant-based food.",
            ],
        ),
    },
    {
        "id": "future-cont",
        "color": "#fb923c",
        "name": "Future Continuous",
        "name_vi": "Tương lai tiếp diễn",
        "hana_num": 6,
        "forks": _tense_forks(
            [
                ("Khẳng định", "S + will be + V-ing"),
                ("Phủ định", "S + won't be + V-ing"),
                ("Nghi vấn", "Will + S + be + V-ing?"),
            ],
            ["this time tomorrow, at 7pm next Friday"],
        ),
    },
    {
        "id": "future-perf",
        "color": "#f97316",
        "name": "Future Perfect",
        "name_vi": "Tương lai hoàn thành",
        "hana_num": 7,
        "forks": _tense_forks(
            [
                ("Khẳng định", "S + will have + V₃"),
                ("Phủ định", "S + won't have + V₃"),
                ("Nghi vấn", "Will + S + have + V₃?"),
            ],
            [
                "by next year, by 2030, by the time",
                "Food: By next year I <strong>will have tried</strong> ten cuisines.",
            ],
        ),
    },
    {
        "id": "future-ppc",
        "color": "#fb7185",
        "name": "Future Perfect Continuous",
        "name_vi": "TL hoàn thành tiếp diễn",
        "hana_num": 8,
        "forks": _tense_forks(
            [
                ("Khẳng định", "S + will have been + V-ing"),
                ("Phủ định", "S + won't have been + V-ing"),
                ("Nghi vấn", "Will + S + have been + V-ing?"),
            ],
            [
                "by … · for + period (đến mốc tương lai)",
                "By June I will have been living here for 5 years.",
            ],
        ),
    },
    {
        "id": "be-about-to",
        "color": "#fdba74",
        "name": "be about to",
        "name_vi": "Sắp xảy ra ngay",
        "forks": [
            {
                "label": "Cấu trúc",
                "leaves": [
                    ("Khẳng định", "S + am/is/are about to + V"),
                    ("Phủ định", "S + am/is/are not about to + V"),
                ],
            },
            {
                "label": "Dấu hiệu",
                "leaves": ["about to, on the point of", "Food: I'm <strong>about to order</strong> takeout."],
            },
        ],
    },
]

# Cách đọc -ed · Past Simple / V₃ (video: How to pronounce -ed)
ED_MINDMAP_LEFT = [
    {
        "id": "ed-id",
        "color": "#a78bfa",
        "name": "/ɪd/",
        "name_vi": "thêm 1 âm tiết",
        "forks": [
            {
                "label": "Quy tắc",
                "leaves": [
                    "Root kết thúc bằng âm <strong>/t/</strong> hoặc <strong>/d/</strong>",
                    "Đọc <code>/ɪd/</code> — đây là trường hợp <strong>có thêm âm tiết</strong>",
                ],
            },
            {
                "label": "Âm đứng trước /ɪd/",
                "leaves": [
                    ("/t/", "wanted · part → <code>/ˈpɑːtɪd/</code> · test → <code>/ˈtestɪd/</code>"),
                    ("/d/", "decided · end → <code>/ˈendɪd/</code> · need → <code>/ˈniːdɪd/</code>"),
                ],
            },
            {
                "label": "Food",
                "leaves": [
                    "I <strong>tasted</strong> <code>/ˈteɪstɪd/</code> the soup.",
                    "We <strong>needed</strong> <code>/ˈniːdɪd/</code> more salt.",
                    "They <strong>roasted</strong> <code>/ˈrəʊstɪd/</code> the ribs.",
                ],
            },
        ],
    },
    {
        "id": "ed-adj",
        "color": "#c4b5fd",
        "name": "Irregular adjectives",
        "name_vi": "luôn /ɪd/ — ngoại lệ",
        "forks": [
            {
                "label": "Quy tắc",
                "leaves": [
                    "Tính từ này <strong>luôn</strong> đọc <code>/ɪd/</code>",
                    "Dù root <em>không</em> kết thúc /t/ hay /d/",
                ],
            },
            {
                "label": "Học thuộc",
                "leaves": [
                    ("naked", "<code>/ˈneɪkɪd/</code>"),
                    ("wicked", "<code>/ˈwɪkɪd/</code>"),
                    ("jagged", "<code>/ˈdʒæɡɪd/</code>"),
                    ("rugged", "<code>/ˈrʌɡɪd/</code>"),
                ],
            },
        ],
    },
]

ED_MINDMAP_RIGHT = [
    {
        "id": "ed-t",
        "color": "#fb7185",
        "name": "/t/",
        "name_vi": "unvoiced + unvoiced",
        "forks": [
            {
                "label": "Quy tắc",
                "leaves": [
                    "Root kết thúc bằng phụ âm <strong>unvoiced</strong> (không phải /t/)",
                    "<em>we match unvoiced with unvoiced</em> → <code>/t/</code>",
                    "<strong>Không</strong> thêm âm tiết",
                ],
            },
            {
                "label": "Âm đứng trước /t/",
                "leaves": [
                    ("/p/", "helped · clap → <code>/klæpt/</code>"),
                    ("/k/", "asked · kick → <code>/kɪkt/</code>"),
                    ("/f/", "sniffed · laughed"),
                    ("/s/", "missed · dance → <code>/dɑːnst/</code>"),
                    ("/ʃ/", "washed → <code>/wɒʃt/</code>"),
                    ("/tʃ/", "matched"),
                    ("/θ/", "unearthed"),
                ],
            },
            {
                "label": "Food",
                "leaves": [
                    "I <strong>chopped</strong> <code>/tʃɒpt/</code> the herbs.",
                    "We <strong>cooked</strong> <code>/kʊkt/</code> pasta.",
                    "She <strong>sliced</strong> <code>/slaɪst/</code> the fruit.",
                ],
            },
        ],
    },
    {
        "id": "ed-d",
        "color": "#2dd4bf",
        "name": "/d/",
        "name_vi": "voiced + voiced",
        "forks": [
            {
                "label": "Quy tắc",
                "leaves": [
                    "Root kết thúc bằng âm <strong>voiced</strong> (không phải /d/) — nguyên âm + phụ âm hữu thanh",
                    "<em>we match voiced with voiced</em> → <code>/d/</code>",
                    "<strong>Không</strong> thêm âm tiết",
                ],
            },
            {
                "label": "Âm đứng trước /d/",
                "leaves": [
                    ("/b v z g/", "robbed · lived · amazed · rigged"),
                    ("/n m ŋ/", "fined · climbed · winged"),
                    ("/dʒ ð l r/", "judged · soothed · called · remembered"),
                    ("nguyên âm", "love → <code>/lʌvd/</code> · dine → <code>/daɪnd/</code> · comply → <code>/kəmˈplaɪd/</code>"),
                ],
            },
            {
                "label": "Food",
                "leaves": [
                    "I <strong>grilled</strong> <code>/ɡrɪld/</code> kebab.",
                    "We <strong>loved</strong> <code>/lʌvd/</code> the pho.",
                    "They <strong>fried</strong> <code>/fraɪd/</code> the eggs.",
                ],
            },
        ],
    },
]

# Lesson 2 · flow mind map — trái = DISLIKE, phải = LIKE
# Leaves: tip(en, vi) → hover hiện nghĩa VI (không hiện sẵn để tránh rối)
LESSON2_MINDMAP_LEFT = [
    {
        "id": "dis-fun",
        "color": "#fca5a5",
        "name": "Không giải trí",
        "name_vi": "not entertaining",
        "flow": True,
        "opener": "I don't like this · I can't stand … · It's not my cup of tea",
        "branches": [
            {
                "label": "Nhánh 1 · It's + adj",
                "leaves": [
                    tip(
                        "It's + not + interesting / entertaining / exciting / thrilling / relaxing",
                        "Không thú vị / giải trí / hấp dẫn / hồi hộp / thư giãn",
                    ),
                    tip(
                        "It's + boring / terrible / scary / difficult / stressful / noisy",
                        "Nhàm chán / tệ / đáng sợ / khó / căng thẳng / ồn ào",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · It makes me + adj",
                "patterns": (
                    "It makes me + bored / tired / stressed / exhausted · "
                    "I have to + deal with the same tasks every day"
                ),
                "leaves": [
                    tip("not my cup of tea", "không phải sở thích của tôi"),
                    tip("can't stand", "không chịu nổi"),
                    tip("I can't bear", "tôi không thể chịu nổi"),
                    tip("I have to do lots of homework", "tôi phải làm rất nhiều bài tập"),
                    tip(
                        "I have to memorise long lists of new words",
                        "tôi phải học thuộc danh sách dài từ mới",
                    ),
                    tip(
                        "I have to deal with difficult customers",
                        "tôi phải đối phó với khách hàng khó tính",
                    ),
                    tip(
                        "I have to deal with the same tasks and the same clients every day",
                        "tôi phải xử lý cùng công việc và cùng khách hàng mỗi ngày",
                    ),
                ],
            },
        ],
    },
    {
        "id": "dis-edu",
        "color": "#f87171",
        "name": "Không giáo dục",
        "name_vi": "not educational",
        "flow": True,
        "opener": "I don't think … · To be honest, I don't enjoy …",
        "branches": [
            {
                "label": "Nhánh 1 · It's + not + adj",
                "leaves": [
                    tip(
                        "It's + not + educational / useful / practical",
                        "Không mang tính giáo dục / hữu ích / thực tế",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · doesn't + V",
                "patterns": (
                    "<code>doesn't</code> + V nguyên mẫu · "
                    "It doesn't give me the chance to … · "
                    "It doesn't help me learn skills such as …"
                ),
                "leaves": [
                    tip("It doesn't help me relax", "Nó không giúp tôi thư giãn"),
                    tip(
                        "It doesn't give me the chance to challenge myself",
                        "Nó không cho tôi cơ hội thử thách bản thân",
                    ),
                    tip(
                        "It doesn't help me learn skills such as problem-solving",
                        "Nó không giúp tôi học kỹ năng như giải quyết vấn đề",
                    ),
                    tip(
                        "It doesn't give me the opportunity to widen my horizons",
                        "Nó không cho tôi cơ hội mở rộng tầm nhìn",
                    ),
                    tip(
                        "It doesn't help me enrich my knowledge",
                        "Nó không giúp tôi làm giàu vốn kiến thức",
                    ),
                    tip(
                        "It doesn't give me the chance to try anything new",
                        "Nó không cho tôi cơ hội thử điều gì mới",
                    ),
                ],
            },
        ],
    },
    {
        "id": "dis-health",
        "color": "#ef4444",
        "name": "Hại sức khỏe",
        "name_vi": "bad for health",
        "flow": True,
        "opener": "No, definitely not because … · I avoid …",
        "branches": [
            {
                "label": "Nhánh 1 · not good / harmful",
                "leaves": [
                    tip_html(
                        "not good <strong>for</strong> your health",
                        "không tốt cho sức khỏe của bạn",
                    ),
                    tip_html(
                        "harmful / detrimental <strong>to</strong> your health",
                        "có hại / bất lợi cho sức khỏe của bạn",
                    ),
                    tip("It's + unhealthy", "Nó không lành mạnh"),
                ],
            },
            {
                "label": "Nhánh 2 · can lead to …",
                "patterns": "Consuming too much … can lead to …",
                "leaves": [
                    tip("diabetes", "bệnh tiểu đường"),
                    tip("high blood pressure", "huyết áp cao"),
                    tip("stroke", "đột quỵ"),
                    tip("heart attack", "đau tim / nhồi máu cơ tim"),
                    tip("cancer", "ung thư"),
                    tip("obesity", "béo phì"),
                ],
            },
        ],
    },
]

LESSON2_MINDMAP_RIGHT = [
    {
        "id": "like-fun",
        "color": "#67e8f9",
        "name": "Giải trí",
        "name_vi": "entertainment",
        "flow": True,
        "opener": "I love this · I think … · I'm keen on …",
        "branches": [
            {
                "label": "Nhánh 1 · It's + adj",
                "leaves": [
                    tip(
                        "It's + relaxing / exciting / thrilling / entertaining / interesting …",
                        "Thư giãn / thú vị / hồi hộp / giải trí / hấp dẫn…",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · Starter + V",
                "patterns": (
                    "It helps me + V · It's a great way to + V · "
                    "It gives me the chance to + V · "
                    "I also get the opportunity to + V"
                ),
                "leaves": [
                    tip("reduce stress", "giảm căng thẳng"),
                    tip("relax / unwind", "thư giãn"),
                    tip("clear my head", "giải tỏa đầu óc"),
                    tip("recharge my batteries", "nạp lại năng lượng"),
                    tip(
                        "express my inner feelings",
                        "thổ lộ / giải bày cảm xúc bên trong",
                    ),
                    tip("escape from reality", "thoát khỏi thực tại"),
                    tip(
                        "escape from the hustle and bustle of the city",
                        "thoát khỏi sự hối hả và nhộn nhịp của thành phố",
                    ),
                    tip(
                        "temporarily forget all the pressures from my work",
                        "tạm thời quên đi tất cả áp lực từ công việc của tôi",
                    ),
                    tip(
                        "temporarily forget all the pressures or worries from your daily life",
                        "tạm thời quên đi tất cả áp lực và lo lắng từ cuộc sống hàng ngày",
                    ),
                    tip("being in nature", "ở giữa thiên nhiên"),
                ],
            },
        ],
    },
    {
        "id": "like-edu",
        "color": "#5eead4",
        "name": "Giáo dục",
        "name_vi": "educational",
        "flow": True,
        "opener": "I love this · I think it's useful · Yes, because …",
        "branches": [
            {
                "label": "Nhánh 1 · It's + adj",
                "leaves": [
                    tip(
                        "It's + educational / useful / practical",
                        "Mang tính giáo dục / hữu ích / thực tế",
                    ),
                    tip(
                        "learn skills such as … ↔ learn how to + V",
                        "học kỹ năng như … ↔ học cách + V",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · Starter + V",
                "patterns": (
                    "It helps me + V · It gives me the chance to + V · "
                    "I also get the opportunity to + V"
                ),
                "leaves": [
                    tip("meet different people", "gặp gỡ nhiều người khác nhau"),
                    tip(
                        "meet people from all walks of life",
                        "gặp gỡ người từ mọi tầng lớp xã hội",
                    ),
                    tip(
                        "explore different parts of the world",
                        "khám phá những khu vực khác nhau của thế giới",
                    ),
                    tip(
                        "explore different cultures and traditions",
                        "khám phá những văn hóa và truyền thống khác nhau",
                    ),
                    tip("widen my horizons", "mở rộng tầm nhìn"),
                    tip("enrich my knowledge", "làm giàu vốn kiến thức"),
                    tip(
                        "challenge myself / push myself to the limit",
                        "thử thách bản thân / đẩy bản thân tới giới hạn cao nhất",
                    ),
                    tip(
                        "become more confident and independent",
                        "trở nên tự tin và độc lập hơn",
                    ),
                    tip(
                        "become a better version of myself",
                        "trở thành một phiên bản tốt hơn của bản thân",
                    ),
                    tip(
                        "become a more well-rounded person",
                        "trở thành một con người toàn diện hơn",
                    ),
                    tip(
                        "develop my imagination and creativity",
                        "phát triển trí tưởng tượng và sáng tạo của tôi",
                    ),
                    tip(
                        "learn how to deal with difficult situations more effectively",
                        "học cách xử lý tình huống khó hiệu quả hơn",
                    ),
                    tip(
                        "learn how to manage my money / budgets better",
                        "học cách quản lý tiền bạc / ngân sách tốt hơn",
                    ),
                    tip(
                        "learn how to curb stress more effectively",
                        "học cách kiểm soát căng thẳng hiệu quả hơn",
                    ),
                    tip(
                        "learn how to work as a team / work effectively in a team environment",
                        "học cách làm việc nhóm / làm việc hiệu quả trong môi trường nhóm",
                    ),
                    tip(
                        "learn how to think more independently",
                        "học cách suy nghĩ độc lập hơn",
                    ),
                ],
            },
        ],
    },
    {
        "id": "like-health",
        "color": "#34d399",
        "name": "Sức khỏe",
        "name_vi": "health",
        "flow": True,
        "opener": "I love this · Yes, because it's a great way to …",
        "branches": [
            {
                "label": "Nhánh 1 · It's a great way to",
                "leaves": [
                    tip(
                        "It's a great way to + keep fit / stay healthy / keep in shape",
                        "Đây là cách tuyệt vời để giữ dáng / khỏe mạnh",
                    ),
                    tip("It's + good for your health", "Tốt cho sức khỏe của bạn"),
                ],
            },
            {
                "label": "Nhánh 2 · Cụm V",
                "patterns": (
                    "It helps me + V · It also helps me + V · "
                    "Eating … can also prevent …"
                ),
                "leaves": [
                    tip(
                        "keep fit / stay healthy / keep in shape",
                        "giữ dáng / khỏe mạnh",
                    ),
                    tip("improve my health", "cải thiện sức khỏe"),
                    tip("strengthen my muscles", "tăng cường cơ bắp"),
                    tip("burn excess calories", "đốt calo thừa"),
                    tip("maintain a healthy weight", "duy trì một cân nặng phù hợp"),
                    tip(
                        "prevent various health problems such as high blood pressure",
                        "tránh các vấn đề về sức khỏe như cao huyết áp",
                    ),
                    tip(
                        "prevent stroke / heart attack / cancer",
                        "tránh đột quỵ / đau tim / ung thư",
                    ),
                ],
            },
        ],
    },
]

# §6 · Food phrase drills — mind map (structures + idea lists, Food-specific)
FOOD_PHRASE_MINDMAP_LEFT = [
    {
        "id": "food-dis-health",
        "color": "#f87171",
        "name": "Không lành mạnh",
        "name_vi": "unhealthy food",
        "flow": True,
        "opener": "🕐 MỞ · No, definitely not because … · I avoid … · It's not my cup of tea",
        "branches": [
            {
                "label": "Nhánh 1 · not good / harmful",
                "leaves": [
                    "not good <strong>for</strong> your health",
                    "harmful / detrimental <strong>to</strong> your health",
                    "It's + unhealthy · not practical for a daily diet",
                    "<mark class=\"vocab\">take-away</mark> every night",
                    "too much <mark class=\"vocab\">soda</mark> / <mark class=\"vocab\">soft drink</mark>",
                    "<mark class=\"vocab\">energy drink</mark> late at night",
                ],
            },
            {
                "label": "Nhánh 2 · can lead to …",
                "patterns": "Consuming too much … can lead to …",
                "leaves": [
                    "fast food / greasy <mark class=\"vocab\">take-away</mark>",
                    "too much <mark class=\"vocab\">bacon</mark> → high salt intake",
                    "fried <mark class=\"vocab\">meatball</mark>s → feel heavy",
                    "sugary <mark class=\"vocab\">soft drink</mark>s → health problems",
                    "obesity · high blood pressure · diabetes",
                ],
            },
        ],
    },
    {
        "id": "food-dis-soft",
        "color": "#fca5a5",
        "name": "Không thích · soft no",
        "name_vi": "dislike",
        "flow": True,
        "opener": "🕐 MỞ · I don't think … · To be honest, I don't enjoy … · I can't stand …",
        "branches": [
            {
                "label": "Nhánh 1 · It's + not + adj",
                "leaves": [
                    "It's + not + useful / practical / worth it",
                    "<mark class=\"vocab\">veal</mark> is not really my cup of tea",
                    "<mark class=\"vocab\">Jell-O</mark> — texture feels strange",
                    "greasy <mark class=\"vocab\">take-away</mark> every night",
                ],
            },
            {
                "label": "Nhánh 2 · doesn't + V",
                "patterns": (
                    "<code>doesn't</code> + V nguyên mẫu · "
                    "It doesn't give me the chance to … · It doesn't help me …"
                ),
                "leaves": [
                    "plain <mark class=\"vocab\">chicken breast</mark> doesn't give richer flavours",
                    "skipping the <mark class=\"vocab\">yolk</mark> doesn't help me feel satisfied",
                    "counting every <mark class=\"vocab\">calorie</mark> doesn't help a healthy relationship with food",
                    "<mark class=\"vocab\">alcoholic</mark> drinks aren't necessary every dinner",
                ],
            },
        ],
    },
]

FOOD_PHRASE_MINDMAP_RIGHT = [
    {
        "id": "food-like-healthy",
        "color": "#34d399",
        "name": "Ăn lành mạnh",
        "name_vi": "healthy eating",
        "flow": True,
        "opener": "🕐 MỞ · To be honest, I'm keen on … · I'm a big fan of … · Yes, because …",
        "branches": [
            {
                "label": "Nhánh 1 · It's + adj / nutritious",
                "leaves": [
                    "It's + healthy / nutritious / practical",
                    "<mark class=\"vocab\">plant-based</mark> diet",
                    "<mark class=\"vocab\">low-carb diet</mark> / <mark class=\"vocab\">sugar-free</mark> options",
                    "<mark class=\"vocab\">ripe</mark> fruit makes salad taste better",
                    "<mark class=\"vocab\">white meat</mark> as a lighter choice",
                ],
            },
            {
                "label": "Nhánh 2 · helps / chance / opportunity",
                "patterns": (
                    "It helps me + V · It gives me the chance to + V · "
                    "I also get the opportunity to + V"
                ),
                "leaves": [
                    "<mark class=\"vocab\">smoothie</mark> every morning → stay full until lunch",
                    "<mark class=\"vocab\">fruit salad</mark> → add more vitamins",
                    "pay attention to <mark class=\"vocab\">nutrition</mark> → more energetic",
                    "cooking with <mark class=\"vocab\">garlic</mark> → flavour without too much salt",
                    "<mark class=\"vocab\">mineral water</mark> on my desk → drink more water",
                    "<mark class=\"vocab\">citrus</mark> fruit → top choice for breakfast",
                ],
            },
        ],
    },
    {
        "id": "food-like-enjoy",
        "color": "#67e8f9",
        "name": "Thích · tận hưởng",
        "name_vi": "enjoy food",
        "flow": True,
        "opener": "🕐 MỞ · I love … · I think … · Whenever I have free time, I really love to …",
        "branches": [
            {
                "label": "Nhánh 1 · It's + adj",
                "leaves": [
                    "It's + relaxing / exciting / entertaining / mouth-watering",
                    "<mark class=\"vocab\">cheesecake</mark> after a long day → so relaxing",
                    "trying <mark class=\"vocab\">oyster</mark> for the first time → exciting",
                    "mixing <mark class=\"vocab\">nonalcoholic cocktail</mark>s at home → entertaining",
                    "<mark class=\"vocab\">pancake</mark>s with berries on Sunday → interesting",
                ],
            },
            {
                "label": "Nhánh 2 · Phrases + social",
                "patterns": (
                    "<mark class=\"vocab\">grab a bite</mark> · <mark class=\"vocab\">dine out</mark> · "
                    "<mark class=\"vocab\">comfort food</mark> · <mark class=\"vocab\">home-cooked meal</mark>"
                ),
                "leaves": [
                    "<mark class=\"vocab\">grab a bite</mark> with friends → helps me unwind",
                    "<mark class=\"vocab\">dining out</mark> on Friday → try new restaurants",
                    "<mark class=\"vocab\">comfort food</mark> → forget work stress",
                    "<mark class=\"vocab\">home-cooked meal</mark> → practise cooking",
                    "<mark class=\"vocab\">guilty pleasure</mark> — snack khuya, thỉnh thoảng vẫn thích",
                    "<mark class=\"vocab\">cheeseburger</mark> · <mark class=\"vocab\">bacon</mark> · <mark class=\"vocab\">rib</mark>",
                ],
            },
        ],
    },
    {
        "id": "food-like-cook",
        "color": "#5eead4",
        "name": "Nấu ăn · tại nhà",
        "name_vi": "cooking",
        "flow": True,
        "opener": "🕐 MỞ · I'm keen on … · What I like most about … is that …",
        "branches": [
            {
                "label": "Nhánh 1 · What I like most about …",
                "leaves": [
                    "What I like most about a <mark class=\"vocab\">home-cooked meal</mark> is a warm experience",
                    "a fresh <mark class=\"vocab\">loaf</mark> at the weekend",
                    "warm <mark class=\"vocab\">bread roll</mark> with soup on rainy days",
                ],
            },
            {
                "label": "Nhánh 2 · Ingredients & dishes",
                "patterns": "It helps me + V · I also get the opportunity to + V",
                "leaves": [
                    "<mark class=\"vocab\">garlic</mark> · <mark class=\"vocab\">lime</mark> · fresh <mark class=\"vocab\">berry</mark>",
                    "<mark class=\"vocab\">shellfish</mark> when fresh · <mark class=\"vocab\">oyster</mark>",
                    "<mark class=\"vocab\">pomegranate</mark> seeds in salad — nice crunch",
                    "<mark class=\"vocab\">cantaloupe</mark> chilled in summer",
                    "<mark class=\"vocab\">macadamia nut</mark> instead of chips",
                    "<mark class=\"vocab\">tangerine</mark> after lunch — little reset",
                ],
            },
        ],
        "link": "🔗 Kết: <code>so / that's why / but I still / I avoid …</code> — chốt hoặc giới hạn (xem Bước 2 bên dưới)",
    },
]

# Lesson 3 · flow — trái = NO, phải = YES
LESSON3_MINDMAP_LEFT = [
    {
        "id": "no-flow",
        "color": "#fca5a5",
        "name": "NO",
        "name_vi": "phủ định",
        "flow": True,
        "opener": "No, definitely not · No, absolutely not · No, not really · Well, not really",
        "branches": [
            {
                "label": "Nhánh 1 · Verb",
                "leaves": [
                    tip(
                        "I don't like / love / enjoy + V-ing",
                        "Tôi không thích / yêu / tận hưởng + V-ing",
                    ),
                    tip(
                        "Food: I don't like fast food / eating too much dessert",
                        "Food: Tôi không thích đồ ăn nhanh / ăn quá nhiều món ngọt",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · Adj / NP",
                "leaves": [
                    tip("I'm not keen on …", "Tôi không hứng thú với …"),
                    tip("I'm not interested in …", "Tôi không quan tâm đến …"),
                    tip("I'm not a big fan of …", "Tôi không phải fan của …"),
                ],
            },
            {
                "label": "Nhánh 3 · hardly ever (chiến thuật Favourite)",
                "patterns": (
                    "<code>I hardly ever</code> + V nguyên mẫu · "
                    "mềm hóa NO: gần như không bao giờ làm việc đó"
                ),
                "leaves": [
                    tip(
                        "I hardly ever + V",
                        "Tôi hiếm khi / hầu như không bao giờ + V",
                    ),
                    tip(
                        "I hardly ever cook / eat spicy dishes / eat out",
                        "Hiếm khi nấu / ăn món cay / ăn ngoài",
                    ),
                    tip(
                        "No, not really. I hardly ever … because …",
                        "Không thật sự. Tôi hiếm khi … vì …",
                    ),
                ],
            },
        ],
        "link": "→ <strong>because</strong> + Lesson 2 <em>Không thích</em> (trái) · có thể + <em>prefer … rather than</em>",
    },
]

LESSON3_MINDMAP_RIGHT = [
    {
        "id": "yes-flow",
        "color": "#6ee7b7",
        "name": "YES",
        "name_vi": "khẳng định",
        "flow": True,
        "opener": "Yes, definitely · Yes, absolutely",
        "branches": [
            {
                "label": "Nhánh 1 · Verb",
                "leaves": [
                    tip("I like / love / enjoy + V-ing", "Tôi thích / yêu / tận hưởng + V-ing"),
                    tip(
                        "Food: I enjoy cooking / trying new cuisine",
                        "Food: Tôi thích nấu ăn / thử ẩm thực mới",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · Adj / NP",
                "leaves": [
                    tip("I'm keen on … · I'm interested in …", "Tôi thích / quan tâm đến …"),
                    tip("I'm a big fan of …", "Tôi là fan của …"),
                    tip("This is because + S + V", "Đây là vì + S + V"),
                ],
            },
            {
                "label": "Nhánh 3 · prefer … rather than …",
                "patterns": (
                    "<code>prefer to V + rather than + V</code> (nguyên mẫu) · "
                    "<code>prefer + V-ing + to + V-ing</code>"
                ),
                "leaves": [
                    tip(
                        "I prefer to cook at home rather than eat out",
                        "Tôi thích nấu ở nhà hơn là ăn ngoài (to V · rather than · V)",
                    ),
                    tip(
                        "I prefer reading to watching TV",
                        "Tôi thích đọc hơn xem TV (V-ing · to · V-ing)",
                    ),
                    tip(
                        "I prefer home-cooked food rather than eating out",
                        "Tôi thích đồ nấu nhà hơn ăn ngoài (NP · rather than · V-ing)",
                    ),
                ],
            },
        ],
        "link": "→ <strong>because</strong> + Lesson 2 <em>Thích</em> (phải)",
    },
    {
        "id": "reasons-flow",
        "color": "#fcd34d",
        "name": "Reasons",
        "name_vi": "lý do",
        "flow": True,
        "opener": "because · This is because · because of",
        "branches": [
            {
                "label": "Nhánh 1 · Mệnh đề",
                "leaves": [
                    tip("because + S + V", "because + mệnh đề"),
                    tip("This is because + S + V", "This is because + mệnh đề"),
                    tip(
                        "because it is not good for my health",
                        "vì nó không tốt cho sức khỏe (mệnh đề)",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · Danh từ / mở rộng",
                "patterns": (
                    "because of + noun / NP · "
                    "It gives me the chance to + V · "
                    "It's a great way to + V · can lead to …"
                ),
                "leaves": [
                    tip(
                        "because of its harmful effects on my health",
                        "vì tác hại của nó với sức khỏe",
                    ),
                    tip("It gives me the chance to + V", "Cho tôi cơ hội + V"),
                    tip("I also get the opportunity to + V", "Tôi cũng có cơ hội + V"),
                    tip("It also helps me + V", "Nó cũng giúp tôi + V"),
                    tip(
                        "can lead to various health problems",
                        "có thể dẫn đến nhiều vấn đề sức khỏe",
                    ),
                ],
            },
            {
                "label": "Nhánh 3 · Lexical Food (ý theo topic)",
                "patterns": (
                    "Chỉ dùng cụm <strong>Food / health</strong> — "
                    "không ghép ý job/team vào câu Food"
                ),
                "leaves": [
                    tip(
                        "strengthen my muscles / burn excess calories",
                        "tăng cường cơ bắp / đốt calo thừa",
                    ),
                    tip(
                        "grab a bite (to eat) · dine out",
                        "ăn vội một miếng · ăn ngoài",
                    ),
                    tip(
                        "have a sweet tooth",
                        "thích đồ ngọt (có ‘răng ngọt’)",
                    ),
                    tip(
                        "pose a threat to (my) health",
                        "gây đe dọa đến sức khỏe",
                    ),
                    tip(
                        "shorten one's / my life expectancy",
                        "làm giảm tuổi thọ",
                    ),
                    tip(
                        "take a heavy toll on (my) health",
                        "gây ảnh hưởng nghiêm trọng / hậu quả nặng nề cho sức khỏe",
                    ),
                    tip(
                        "wake up my taste buds · richer flavours",
                        "đánh thức vị giác · hương vị phong phú hơn",
                    ),
                ],
            },
        ],
    },
]

# Lesson 5 · What kind of X do you like most? — trái = Loại gì?, phải = Lý do
LESSON5_MINDMAP_LEFT = [
    {
        "id": "kind-flow",
        "color": "#93c5fd",
        "name": "Loại gì?",
        "name_vi": "What kind?",
        "flow": True,
        "opener": "Well, … · Honestly, …",
        "branches": [
            {
                "label": "Nhánh 1 · Direct",
                "leaves": [
                    tip("I like … most.", "Tôi thích … nhất."),
                    tip(
                        "Food: I like home-cooked food most.",
                        "Food: Tôi thích đồ nấu nhà nhất.",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · Soft choose (hay dùng nhất)",
                "patterns": (
                    "<code>I love all kinds of …, but if I had to choose one, "
                    "it would have to be…</code>"
                ),
                "leaves": [
                    tip(
                        "I love all kinds of food, but if I had to choose one, it would have to be…",
                        "Tôi thích mọi loại đồ ăn, nhưng nếu phải chọn một thì sẽ là…",
                    ),
                    tip(
                        "… I would go for …",
                        "… tôi sẽ chọn … (go for)",
                    ),
                    tip(
                        "… I would opt for …",
                        "… tôi sẽ chọn … (opt for — formal hơn)",
                    ),
                ],
            },
            {
                "label": "Nhánh 3 · Food kinds (gợi ý chọn)",
                "leaves": [
                    tip(
                        "home-cooked food · street food · seafood",
                        "đồ nấu nhà · đồ đường phố · hải sản",
                    ),
                    tip(
                        "Vietnamese / Japanese / Italian cuisine",
                        "ẩm thực Việt / Nhật / Ý",
                    ),
                    tip(
                        "grilled · steamed · fruit-based desserts",
                        "nướng · hấp · tráng miệng từ trái cây",
                    ),
                ],
            },
        ],
        "link": "→ <strong>because / This is because</strong> + Lý do (phải)",
    },
]

LESSON5_MINDMAP_RIGHT = [
    {
        "id": "kind-reason-flow",
        "color": "#fcd34d",
        "name": "Lý do",
        "name_vi": "Reason",
        "flow": True,
        "opener": "because · This is because · because of",
        "branches": [
            {
                "label": "Nhánh 1 · Mệnh đề / NP",
                "leaves": [
                    tip("because / This is because + S + V", "because + mệnh đề"),
                    tip("because of + noun / NP", "because of + danh từ / cụm DT"),
                    tip(
                        "This is because home-cooked food is much healthier than restaurant food",
                        "Vì đồ nấu nhà lành mạnh hơn nhiều so với đồ nhà hàng",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · Mở rộng (try / compare)",
                "patterns": (
                    "<code>try not to + V</code> · <code>try to + V</code> · "
                    "<code>try + V-ing</code> · so sánh <em>healthier than</em>"
                ),
                "leaves": [
                    tip(
                        "I try not to eat out too often",
                        "Tôi cố gắng không ăn ngoài quá thường xuyên",
                    ),
                    tip(
                        "I try to stick to a balanced diet",
                        "Tôi cố gắng giữ chế độ ăn cân bằng",
                    ),
                    tip(
                        "You should try using seasonal ingredients",
                        "Bạn nên thử dùng nguyên liệu theo mùa (try + V-ing)",
                    ),
                ],
            },
            {
                "label": "Nhánh 3 · Lexical Food (collocation hay)",
                "patterns": (
                    "Giống nhánh clothes: <em>out of fashion / trendy</em> — "
                    "ở đây dùng cụm Food band 7+"
                ),
                "leaves": [
                    tip(
                        "mouth-watering · packed with flavour",
                        "cực ngon · đầy hương vị",
                    ),
                    tip(
                        "wholesome · freshly prepared · from scratch",
                        "lành mạnh · mới chế biến · làm từ đầu",
                    ),
                    tip(
                        "hits the spot · light on the stomach",
                        "đúng gu / thỏa mãn · dễ tiêu",
                    ),
                    tip(
                        "stick to a balanced diet · cut down on processed food",
                        "giữ chế độ ăn cân bằng · giảm đồ chế biến sẵn",
                    ),
                    tip(
                        "comfort food · guilty pleasure · signature dish",
                        "đồ ăn an ủi · thú thích ‘tội lỗi’ · món đặc trưng",
                    ),
                    tip(
                        "farm-to-table · culinary tradition",
                        "từ nông trại tới bàn ăn · truyền thống ẩm thực",
                    ),
                ],
            },
        ],
        "link": "→ ghép Lesson 2 reasons nếu cần dài thêm 1 câu",
    },
]

# Lesson 6 · Do you prefer X or Y? — trái = Chọn X/Y, phải = Lý do
LESSON6_MINDMAP_LEFT = [
    {
        "id": "prefer-xy-flow",
        "color": "#c4b5fd",
        "name": "Chọn X / Y",
        "name_vi": "Prefer",
        "flow": True,
        "opener": "Well, … · Honestly, …",
        "branches": [
            {
                "label": "Nhánh 1 · I prefer X",
                "patterns": "X thường là <strong>V-ing</strong> / NP",
                "leaves": [
                    tip("I prefer + V-ing / NP", "Tôi thích hơn + V-ing / danh từ"),
                    tip(
                        "Food: I prefer eating at home",
                        "Food: Tôi thích ăn ở nhà hơn",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · I prefer X to Y",
                "patterns": "<code>prefer + V-ing + to + V-ing</code> (cùng form)",
                "leaves": [
                    tip(
                        "I prefer eating at home to eating out",
                        "Tôi thích ăn ở nhà hơn ăn ngoài",
                    ),
                    tip(
                        "I prefer cooking myself to ordering takeaway",
                        "Tôi thích tự nấu hơn gọi mang về",
                    ),
                ],
            },
            {
                "label": "Nhánh 3 · I prefer X rather than Y",
                "patterns": (
                    "<code>prefer to V rather than V</code> · "
                    "hoặc NP / V-ing + rather than …"
                ),
                "leaves": [
                    tip(
                        "I prefer to cook at home rather than eat out",
                        "Tôi thích nấu ở nhà hơn là ăn ngoài",
                    ),
                    tip(
                        "I prefer wholesome meals rather than fast food",
                        "Tôi thích bữa lành mạnh hơn fast food",
                    ),
                ],
            },
        ],
        "link": "→ <strong>because</strong> + Lý do (ưu điểm X · while · nhược điểm Y)",
    },
]

LESSON6_MINDMAP_RIGHT = [
    {
        "id": "prefer-reason-flow",
        "color": "#fcd34d",
        "name": "Lý do",
        "name_vi": "Reason",
        "flow": True,
        "opener": "because · This is because · while / whereas",
        "branches": [
            {
                "label": "Nhánh 1 · Ưu điểm X / Nhược điểm Y",
                "leaves": [
                    tip(
                        "Ưu điểm của X → healthier / more interesting / safer",
                        "Nêu điểm mạnh của lựa chọn X",
                    ),
                    tip(
                        "Nhược điểm của Y → time-consuming / pose a threat to health",
                        "Nêu điểm yếu của Y",
                    ),
                    tip(
                        "X …, while / whereas Y …",
                        "Đối chiếu trực tiếp X và Y",
                    ),
                ],
            },
            {
                "label": "Nhánh 2 · Cấu trúc slide (Food)",
                "patterns": "Áp dụng đúng ngữ cảnh Food — không copy ví dụ letters/cinema",
                "leaves": [
                    tip(
                        "It takes + time (+ for sb) + to V",
                        "Tốn bao nhiêu thời gian (cho ai) để làm gì",
                    ),
                    tip(
                        "love the feeling of + V-ing",
                        "Thích cảm giác làm gì",
                    ),
                    tip(
                        "have someone to + V",
                        "Có ai đó để làm gì",
                    ),
                    tip(
                        "send sth to sb",
                        "Gửi cái gì cho ai (ảnh món / recipe…)",
                    ),
                    tip(
                        "function (v) — body / brain / nutrients",
                        "Hoạt động (cơ thể / não / khi đủ dinh dưỡng)",
                    ),
                ],
            },
            {
                "label": "Nhánh 3 · Lexical Food (trong contrast)",
                "leaves": [
                    tip(
                        "more time-consuming · grab a bite",
                        "tốn thời gian hơn · ăn vội một miếng",
                    ),
                    tip(
                        "pose a threat to health · take a heavy toll on health",
                        "đe dọa sức khỏe · gây hậu quả nặng cho SK",
                    ),
                    tip(
                        "have a sweet tooth · strengthen my muscles",
                        "thích đồ ngọt · tăng cường cơ bắp",
                    ),
                    tip(
                        "hits the spot · from scratch · balanced diet",
                        "đúng gu · nấu từ đầu · chế độ ăn cân bằng",
                    ),
                ],
            },
        ],
        "link": "→ thêm 1 ví dụ cụ thể (Ví dụ) để chốt đoạn",
    },
]


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


def slot_select(slot_id: str, default_idx: int = 0, *, kind: str = "vocab") -> str:
    opts = WORD_SLOTS[slot_id]
    idx = min(default_idx, len(opts) - 1)
    extra_cls = " lr-idiom-pick" if kind == "idiom" else ""
    options = "\n".join(
        f'<option value="{esc(o["form"])}" title="{esc(o["vi"])}"'
        f'{" selected" if i == idx else ""}>{esc(o["form"])}</option>'
        for i, o in enumerate(opts)
    )
    return (
        f'<select class="lr-word-pick{extra_cls}" data-slot="{esc(slot_id)}" '
        f'data-kind="{esc(kind)}" title="Hover option · nghĩa VI" '
        f'aria-label="Choose {"idiom or phrase" if kind == "idiom" else "vocabulary"}">'
        f"{options}</select>"
    )


def idiom_pick(slot_id: str, default_idx: int = 0) -> str:
    return slot_select(slot_id, default_idx, kind="idiom")


def phrase_pick(slot_id: str, default_idx: int = 0) -> str:
    return slot_select(slot_id, default_idx, kind="phrase")


# 12 thì văn nói thực tế — Hana's Lexis (timeline quá khứ → hiện tại → tương lai)
HANA_TIMELINE_ZONES = [
    {
        "id": "past",
        "label": "Quá khứ",
        "label_en": "Past",
        "tenses": [
            {
                "num": 9,
                "id": "past-simple",
                "name": "Past Simple",
                "name_vi": "Quá khứ đơn",
                "color": "#f87171",
                "examples": [
                    ("I went to bed at 10pm yesterday.", None),
                ],
                "uses": [
                    "Đã xảy ra xong, kết thúc rồi — có thời điểm rõ ràng",
                    "Hành động ngắn, một mảnh trong câu chuyện quá khứ",
                ],
            },
            {
                "num": 10,
                "id": "past-continuous",
                "name": "Past Continuous",
                "name_vi": "Quá khứ tiếp diễn",
                "color": "#fb923c",
                "examples": [
                    (
                        "I was going to bed at 10pm yesterday but then my friend came over "
                        "so I had to stay up and talk to her.",
                        None,
                    ),
                    (
                        "I was watching movie with my friend when you called me.",
                        None,
                    ),
                ],
                "uses": [
                    "Hành động trong quá khứ <strong>đang kéo dài</strong>",
                    "Bị hành động khác chen vào → không kết thúc được việc đang làm",
                ],
                "tip": (
                    "Hành động <strong>cắt ngang</strong> (chen vào) → chỉ dùng "
                    "<strong>quá khứ đơn</strong> (came over, called me)."
                ),
            },
            {
                "num": 11,
                "id": "past-perfect",
                "name": "Past Perfect",
                "name_vi": "Quá khứ hoàn thành",
                "color": "#c084fc",
                "examples": [
                    (
                        "She had broken up with her ex-boyfriend before she started "
                        "dating her new boyfriend.",
                        None,
                    ),
                ],
                "uses": [
                    "Một hành động xảy ra <strong>trước</strong> một hành động khác trong quá khứ",
                    "Thường đi với <em>before / after / by the time</em>",
                ],
            },
            {
                "num": 12,
                "id": "past-ppc",
                "name": "Past Perfect Continuous",
                "name_vi": "QK hoàn thành tiếp diễn",
                "color": "#a78bfa",
                "examples": [
                    (
                        "She had been trying to break up with her ex-bf before she "
                        "started dating a new one.",
                        None,
                    ),
                ],
                "uses": [
                    "Chuyện đã xảy ra trước trong quá khứ, nhưng <strong>kéo dài</strong>",
                    "Cố gắng chia tay — chưa chắc đã kết thúc hay chưa",
                ],
                "tip": (
                    "Khác <strong>quá khứ hoàn thành</strong>: had broken up = "
                    "<strong>đã chia tay xong</strong> rồi."
                ),
            },
        ],
    },
    {
        "id": "present",
        "label": "Hiện tại",
        "label_en": "Present",
        "tenses": [
            {
                "num": 1,
                "id": "pres-simple",
                "name": "Present Simple",
                "name_vi": "Hiện tại đơn",
                "color": "#34d399",
                "examples": [
                    ("The sun rises in the east.", None),
                    ("I love eating spicy food.", None),
                    ("The bus runs at 8am every morning.", None),
                    ("My friend hates reading.", None),
                ],
                "uses": [
                    "Sự kiện xảy ra thường xuyên, thói quen",
                    "Sự thật chân lý hiển nhiên",
                    "Sở thích bản thân; chuyện của người khác",
                    "Lịch trình cố định, không thay đổi",
                ],
            },
            {
                "num": 2,
                "id": "pres-continuous",
                "name": "Present Continuous",
                "name_vi": "Hiện tại tiếp diễn",
                "color": "#60a5fa",
                "examples": [
                    ("I'm eating pears right now.", "đang ăn lê ngay lúc nói"),
                    (
                        "I'm traveling to Vegas at the end of this month.",
                        "đã có kế hoạch đi Vegas cuối tháng",
                    ),
                ],
                "uses": [
                    "Hành động <strong>đang diễn ra</strong> tại thời điểm mình nói",
                    "Nhấn mạnh tính chất <strong>kéo dài</strong> của hành động",
                    "Dự định tương lai gần — đã có <strong>kế hoạch</strong>",
                ],
                "tip": (
                    "Gần <strong>going to</strong> nhưng going to nhấn mạnh "
                    "<strong>ý định</strong> hơn. Việc <strong>bộc phát</strong>, "
                    "mới nghĩ ra → dùng <strong>will</strong>."
                ),
            },
            {
                "num": 3,
                "id": "pres-perfect",
                "name": "Present Perfect",
                "name_vi": "Hiện tại hoàn thành",
                "color": "#38bdf8",
                "examples": [
                    ("I've graduated.", "đã tốt nghiệp — không nói khi nào"),
                    (
                        "I have lived in Vietnam for 20 years.",
                        "và hiện tại vẫn còn sống ở Việt Nam",
                    ),
                    (
                        "I have lived in Vietnam since 1990.",
                        "và hiện tại vẫn còn sống ở Việt Nam",
                    ),
                    (
                        "I've been to Europe 3 times.",
                        "đã làm nhiều lần trong quá khứ",
                    ),
                ],
                "uses": [
                    "Hành động quá khứ <strong>không có thời điểm xác định</strong>",
                    "Bắt đầu trong quá khứ, <strong>kéo dài tới hiện tại</strong> (for / since)",
                    "Kinh nghiệm / số lần đã làm (ever, times)",
                ],
            },
            {
                "num": 4,
                "id": "pres-ppc",
                "name": "Present Perfect Continuous",
                "name_vi": "HT hoàn thành tiếp diễn",
                "color": "#7dd3fc",
                "examples": [
                    (
                        "I've been working at this company for 20 years.",
                        None,
                    ),
                    (
                        "I've been working at this company since I graduated from high school.",
                        None,
                    ),
                ],
                "uses": [
                    "Hành động quá khứ kéo dài đến hiện tại — "
                    "<strong>khả năng tiếp tục</strong> trong tương lai",
                ],
                "tip": (
                    "<em>I've worked at this company for 20 years</em> → có thể "
                    "đổi việc sau này, không nhấn mạnh vẫn đang làm."
                ),
            },
        ],
    },
    {
        "id": "future",
        "label": "Tương lai",
        "label_en": "Future",
        "tenses": [
            {
                "num": 5,
                "id": "future-will",
                "name": "Future Simple (will)",
                "name_vi": "Tương lai đơn",
                "color": "#fbbf24",
                "examples": [
                    ("I will go to Vegas.", "quyết định / lời hứa / bộc phát"),
                ],
                "uses": [
                    "Quyết định lúc đang nói, <strong>mới nghĩ ra</strong>",
                    "Lời hứa, dự đoán không chắc chắn",
                ],
            },
            {
                "num": 6,
                "id": "future-continuous",
                "name": "Future Continuous",
                "name_vi": "Tương lai tiếp diễn",
                "color": "#fb923c",
                "examples": [
                    (
                        "This time tomorrow I will be lying on the beach.",
                        "đúng lúc đó ngày mai sẽ đang nằm trên bãi",
                    ),
                ],
                "uses": [
                    "Hành động trong tương lai mang tính <strong>kéo dài</strong>",
                    "Nhìn từ hiện tại vào một mốc tương lai (this time tomorrow…)",
                ],
            },
            {
                "num": 7,
                "id": "future-perfect",
                "name": "Future Perfect",
                "name_vi": "Tương lai hoàn thành",
                "color": "#f97316",
                "examples": [
                    (
                        "She will have dated her boyfriend for 5 years by May of next year.",
                        "đến tháng 5 năm sau sẽ tròn 5 năm yêu",
                    ),
                ],
                "uses": [
                    "Diễn tả sự <strong>hoàn thành</strong> trước một mốc trong tương lai",
                    "Thường có <em>by … / by the time …</em>",
                ],
            },
            {
                "num": 8,
                "id": "future-ppc",
                "name": "Future Perfect Continuous",
                "name_vi": "TL hoàn thành tiếp diễn",
                "color": "#fb7185",
                "examples": [
                    (
                        "I will have been eating 5 meals by 6pm tonight.",
                        "đến 6h tối nay sẽ đã ăn đủ 5 bữa (kéo dài)",
                    ),
                ],
                "uses": [
                    "Hoàn thành trong tương lai <strong>và có kéo dài</strong> "
                    "trước mốc thời gian",
                ],
            },
        ],
    },
]


HANA_TENSE_BY_NUM: dict[int, dict] = {
    t["num"]: t for zone in HANA_TIMELINE_ZONES for t in zone["tenses"]
}

# Hội thoại Food — 12 thì, theo mốc hiện tại → quá khứ → tương lai
FOOD_TENSE_DIALOGUE = [
    {
        "act": "Hiện tại",
        "act_hint": "Thói quen & việc đang diễn ra",
        "lines": [
            {
                "speaker": "Lan",
                "num": 1,
                "phrase": "I usually eat",
                "text": "Honestly, I usually eat quite healthy — lots of vegetables, not much fried food.",
                "vi": "Thật ra tôi thường ăn khá lành mạnh — nhiều rau, ít đồ chiên.",
            },
            {
                "speaker": "Tom",
                "num": 2,
                "phrase": "I'm trying",
                "text": "Same here, though I'm trying to cut sugar this month.",
                "vi": "Tôi cũng vậy, dù tháng này tôi đang cố giảm đường.",
            },
            {
                "speaker": "Lan",
                "num": 3,
                "phrase": "I've tried",
                "text": "I've tried almost every street food stall on this street since I moved here.",
                "vi": "Tôi đã thử gần hết các quán ăn đường phố trên phố này từ khi chuyển đến đây.",
            },
            {
                "speaker": "Tom",
                "num": 4,
                "phrase": "I've been cooking",
                "text": "I've been cooking at home a lot lately — it's cheaper and I control the ingredients.",
                "vi": "Dạo này tôi nấu ở nhà nhiều — rẻ hơn và tôi kiểm soát được nguyên liệu.",
            },
        ],
    },
    {
        "act": "Quá khứ",
        "act_hint": "Chuyện đã xong & hành động chen ngang",
        "lines": [
            {
                "speaker": "Lan",
                "num": 9,
                "phrase": "I ate",
                "text": "Last Sunday I ate way too much at my cousin's wedding buffet.",
                "vi": "Chủ nhật tuần trước tôi ăn quá nhiều ở tiệc buffet đám cưới của anh họ.",
            },
            {
                "speaker": "Tom",
                "num": 10,
                "phrase": "I was making",
                "text": "Ha! I was making spring rolls when you sent me that photo from the party.",
                "vi": "Ha! Tôi đang cuốn nem khi bạn gửi ảnh từ bữa tiệc cho tôi.",
            },
            {
                "speaker": "Lan",
                "num": 11,
                "phrase": "I'd already had",
                "text": "Yeah, and I'd already had a big lunch before the ceremony, so I wasn't even hungry.",
                "vi": "Ừ, và tôi đã ăn trưa no trước lễ rồi nên chẳng đói chút nào.",
            },
            {
                "speaker": "Tom",
                "num": 12,
                "phrase": "had been baking",
                "text": "My neighbour had been baking bread every morning for years before she opened her bakery.",
                "vi": "Hàng xóm tôi đã nướng bánh mì mỗi sáng suốt nhiều năm trước khi mở tiệm bánh.",
            },
        ],
    },
    {
        "act": "Tương lai",
        "act_hint": "Kế hoạch & mốc thời gian phía trước",
        "lines": [
            {
                "speaker": "Lan",
                "num": 5,
                "phrase": "I'll cook",
                "text": "I'll cook Vietnamese food for you this Saturday — you pick the dish.",
                "vi": "Thứ Bảy này tôi sẽ nấu món Việt cho bạn — bạn chọn món nhé.",
            },
            {
                "speaker": "Tom",
                "num": 6,
                "phrase": "I'll be having",
                "text": "Deal! This time tomorrow I'll be having lunch with my parents at that new vegetarian place.",
                "vi": "Được! Đúng giờ này ngày mai tôi sẽ đang ăn trưa với bố mẹ ở quán chay mới kia.",
            },
            {
                "speaker": "Lan",
                "num": 7,
                "phrase": "I will have tried",
                "text": "By December I will have tried every night-market dish in this district.",
                "vi": "Đến tháng 12 tôi sẽ đã thử hết các món chợ đêm trong quận này.",
            },
            {
                "speaker": "Tom",
                "num": 8,
                "phrase": "I will have been working",
                "text": "And by 6 pm I will have been working without a proper meal — I'll be starving!",
                "vi": "Và đến 6 giờ tối tôi sẽ đã làm việc cả ngày không ăn bữa nào đàng hoàng — chắc đói lắm!",
            },
        ],
    },
]


def _hl_tense_phrase(text: str, phrase: str, num: int) -> str:
    meta = HANA_TENSE_BY_NUM[num]
    label = f"#{num} · {meta['name_vi']}"
    color = esc(meta["color"])
    idx = text.find(phrase)
    if idx < 0:
        return esc(text)
    before = esc(text[:idx])
    mid = esc(phrase)
    after = esc(text[idx + len(phrase) :])
    return (
        f'{before}<mark class="lr-tn lr-tn--{num}" data-tn="{num}" '
        f'style="--tn-c:{color}" title="{esc(label)}">{mid}</mark>{after}'
    )


def _hana_tense_legend_html() -> str:
    chips = []
    for num in sorted(HANA_TENSE_BY_NUM):
        t = HANA_TENSE_BY_NUM[num]
        chips.append(
            f'<a class="lr-tn-chip" href="#hana-{esc(t["id"])}" '
            f'style="--tn-c:{esc(t["color"])}" title="{esc(t["name"])}">'
            f'<span class="lr-tn-chip-num">{num}</span>'
            f'<span class="lr-tn-chip-label">{esc(t["name_vi"])}</span></a>'
        )
    return (
        '<div class="lr-tn-legend" aria-label="Chú thích số thì 1–12">'
        + "\n".join(chips)
        + "</div>"
    )


def _food_tense_dialogue_html() -> str:
    acts = []
    for act in FOOD_TENSE_DIALOGUE:
        lines_html = []
        for line in act["lines"]:
            num = line["num"]
            meta = HANA_TENSE_BY_NUM[num]
            body = _hl_tense_phrase(line["text"], line["phrase"], num)
            lines_html.append(
                f"""            <div class="lr-ftd-line" data-tn="{num}">
              <span class="lr-ftd-num" style="--tn-c:{esc(meta['color'])}">{num}</span>
              <div class="lr-ftd-bubble">
                <span class="lr-ftd-speaker">{esc(line['speaker'])}</span>
                <p class="lr-ftd-text">{body}</p>
                <p class="lr-ftd-vi">{esc(line.get('vi', ''))}</p>
                <span class="lr-ftd-tag" style="--tn-c:{esc(meta['color'])}">{esc(meta['name_vi'])}</span>
              </div>
            </div>"""
            )
        acts.append(
            f"""        <section class="lr-ftd-act">
          <header class="lr-ftd-act-head">
            <h4>{esc(act['act'])}</h4>
            <span>{esc(act['act_hint'])}</span>
          </header>
          <div class="lr-ftd-lines">
{chr(10).join(lines_html)}
          </div>
        </section>"""
        )
    return f"""
      <div class="lr-ftd-wrap" id="foodTenseDialogue">
        <h3 class="lr-subsection-title">Hội thoại Food — 12 thì trong thực tế</h3>
        <p class="lr-ftd-intro">
          Sau khi đọc use case, đọc hội thoại này: cùng chủ đề ẩm thực, đi từ
          <strong>hiện tại</strong> → <strong>quá khứ</strong> → <strong>tương lai</strong>.
          Phần <mark class="lr-tn-sample">highlight</mark> = cụm động từ đang dùng thì đó;
          số <strong>1–12</strong> khớp sơ đồ ngữ pháp phía trên và timeline bên dưới.
        </p>
        {_hana_tense_legend_html()}
        <div class="lr-ftd-dialogue" aria-label="Hội thoại minh họa 12 thì chủ đề food">
{chr(10).join(acts)}
        </div>
      </div>"""


def _ttimeline_card_html(tense: dict) -> str:
    color = esc(tense["color"])
    ex_items = []
    for ex in tense["examples"]:
        if isinstance(ex, tuple):
            en, gloss = ex
            gloss_html = (
                f'<span class="lr-ttimeline-gloss">→ {esc(gloss)}</span>'
                if gloss
                else ""
            )
            ex_items.append(
                f'<li><q>{esc(en)}</q>{gloss_html}</li>'
            )
        else:
            ex_items.append(f"<li><q>{esc(ex)}</q></li>")
    uses = "\n".join(
        f"<li>{u}</li>" for u in tense["uses"]
    )
    tip = tense.get("tip")
    tip_html = (
        f'<p class="lr-ttimeline-tip"><strong>Phân biệt:</strong> {tip}</p>'
        if tip
        else ""
    )
    return f"""            <article class="lr-ttimeline-card" id="hana-{esc(tense['id'])}" style="--tt-c:{color}">
              <header class="lr-ttimeline-card-head">
                <span class="lr-ttimeline-num">{tense['num']}</span>
                <div>
                  <strong>{esc(tense['name'])}</strong>
                  <span class="lr-ttimeline-vi">{esc(tense['name_vi'])}</span>
                </div>
              </header>
              <div class="lr-ttimeline-body">
                <p class="lr-ttimeline-label">Ví dụ</p>
                <ul class="lr-ttimeline-ex">
{chr(10).join(ex_items)}
                </ul>
                <p class="lr-ttimeline-label">Khi nào dùng (đời thường)</p>
                <ul class="lr-ttimeline-use">
{uses}
                </ul>
                {tip_html}
              </div>
            </article>"""


def hana_timeline_html() -> str:
    zones_html = []
    for zone in HANA_TIMELINE_ZONES:
        cards = "\n".join(
            _ttimeline_card_html(t) for t in zone["tenses"]
        )
        zones_html.append(
            f"""        <section class="lr-ttimeline-zone lr-ttimeline-zone--{esc(zone['id'])}" aria-label="{esc(zone['label'])}">
          <div class="lr-ttimeline-zone-head">
            <span class="lr-ttimeline-zone-label">{esc(zone['label'])}</span>
            <span class="lr-ttimeline-zone-en">{esc(zone['label_en'])}</span>
          </div>
          <div class="lr-ttimeline-cards">
{cards}
          </div>
        </section>"""
        )
    return f"""
      <div class="lr-ttimeline-wrap">
        <p class="lr-ttimeline-intro">
          Tóm tắt từ video
          <a href="https://www.youtube.com/watch?v=0mhWAFhs7KQ" target="_blank" rel="noopener noreferrer">Các thì tiếng Anh thật sự dùng trong văn nói</a>
          (Hana's Lexis) — tập trung <strong>use case thực tế</strong>, không học thuộc dấu hiệu khô khan.
        </p>
        <div class="lr-ttimeline" id="hanaTenseTimeline" aria-label="Timeline 12 thì văn nói — quá khứ đến tương lai">
          <div class="lr-ttimeline-axis" aria-hidden="true">
            <span class="lr-ttimeline-axis-past">◀ Quá khứ</span>
            <span class="lr-ttimeline-axis-now">Bây giờ</span>
            <span class="lr-ttimeline-axis-future">Tương lai ▶</span>
          </div>
{chr(10).join(zones_html)}
        </div>
        <p class="lr-ttimeline-note">
          Số trên mỗi thẻ khớp badge <strong>1–12</strong> trên sơ đồ ngữ pháp phía trên
          và highlight trong hội thoại Food bên dưới.
          Quá khứ (9→12) · hiện tại (1→4) · tương lai (5→8).
        </p>
      </div>"""


def mental_model_html() -> str:
    fighter_map = mind_map_html(
        "tenseMindmap",
        "Sơ đồ tư duy 6 nhóm thì — Food speaking",
        "6 nhóm thì",
        "Food &amp; habits",
        TENSE_MINDMAP_LEFT,
        TENSE_MINDMAP_RIGHT,
        note=(
            'Badge <strong>1–12</strong> khớp timeline + hội thoại bên dưới '
            '(<em>used to / would</em>, <em>be about to</em> không có số). '
            '<span class="lr-mmap-star">★</span> = có trong '
            '<strong>Section 3 · Speaking structures</strong>. '
            "Chọn <strong>một thì</strong> cho mỗi câu; chỉ trộn khi có mốc "
            "(when / before / after / by the time)."
        ),
        extra_class=" lr-mmap--tenses",
        min_width="1380px",
    )
    ed_map = mind_map_html(
        "edMindmap",
        "Sơ đồ tư duy cách đọc -ed — Past Simple / V₃",
        "-ed",
        "Past Simple · V₃",
        ED_MINDMAP_LEFT,
        ED_MINDMAP_RIGHT,
        note=(
            "Nghe <strong>âm cuối của root</strong> (không nhìn chính tả). "
            "Ngoại trừ <strong>/t/</strong> và <strong>/d/</strong> → không thêm âm tiết. "
            "Nguồn: "
            '<a href="https://www.youtube.com/watch?v=vv7cBMCBUdk" target="_blank" rel="noopener noreferrer">'
            "How to pronounce -ed</a>."
        ),
        extra_class=" lr-mmap--ed",
        min_width="1280px",
    )
    return (
        fighter_map
        + """
        <h3 class="lr-subsection-title" id="ed-ending">Cách đọc <em>-ed</em> — Past Simple / V₃</h3>
        <p class="lr-section-hint lr-section-hint--sub">Khi nói thì quá khứ đơn và V₃ động từ có quy tắc, đuôi <strong>-ed</strong> có 3 cách đọc. Quyết định theo <em>âm cuối của root</em>, không theo chữ cái.</p>"""
        + ed_map
        + """
        <h3 class="lr-subsection-title">Văn nói thực tế — timeline 12 thì</h3>
        <p class="lr-section-hint lr-section-hint--sub">Sơ đồ tiếp theo: cách người bản xứ <em>thật sự</em> chọn thì khi nói — theo tình huống, không theo bảng dấu hiệu.</p>"""
        + hana_timeline_html()
        + _food_tense_dialogue_html()
    )


def grammar_section() -> str:
    cards = []
    for title, url, vi_use, ex in GRAMMAR_REFS:
        cards.append(
            f"""        <a class="lr-grammar-card lr-grammar-card--link" href="{esc(url)}" target="_blank" rel="noopener noreferrer">
          <strong>{esc(title)}</strong>
          <p>{esc(vi_use)}</p>
          <p class="lr-grammar-ex"><em>e.g.</em> {esc(ex)}</p>
          <span class="lr-card-cta">Read on IELTS Fighter ↗</span>
        </a>"""
        )
    return "\n".join(cards)


def _render_transcript_segment(seg: dict) -> str:
    title = seg.get("title", "")
    is_food = seg.get("food")
    if is_food:
        label = f"Food practice — {esc(title)}" if title else "Food practice"
        extra_class = " lr-segment--food"
    else:
        label = f"Transcript — {esc(title)}" if title else "Transcript"
        extra_class = ""
    lines_html = "\n".join(
        f'                <div class="lr-dialogue-line">'
        f'<span class="lr-speaker">{esc(line["speaker"])}</span>'
        f'<span class="lr-dialogue-text">{line["text"]}</span></div>'
        for line in seg["lines"]
    )
    return f"""            <div class="lr-segment lr-segment--transcript{extra_class}">
              <p class="lr-seg-label">{label}</p>
              <div class="lr-dialogue">
{lines_html}
              </div>
            </div>"""


def _hl_phrase(text: str, parts: list[str]) -> str:
    out = esc(text)
    for part in parts:
        out = out.replace(esc(part), f'<mark class="lr-hl">{esc(part)}</mark>', 1)
    return out


def _render_note_segment(seg: dict) -> str:
    title = esc(seg.get("title", "Note"))
    intro = seg.get("intro", "")
    intro_html = f'<p class="lr-note-intro">{intro}</p>\n' if intro else ""
    tip = seg.get("tip", "")
    tip_html = f'<p class="lr-note-tip">{tip}</p>\n' if tip else ""

    items = seg.get("items", [])
    items_verbatim = seg.get("items_verbatim")
    speaker = seg.get("speaker")

    if speaker and items_verbatim:
        lines_html = "\n".join(
            f'                <p class="lr-verbatim-line">{esc(t)}</p>'
            for t in items_verbatim
        )
        body = f"""              <div class="lr-verbatim-block">
                <span class="lr-speaker">{esc(speaker)}</span>
{lines_html}
              </div>"""
    elif seg.get("formula"):
        rows = []
        for item in items:
            if isinstance(item, tuple) and len(item) == 2:
                label, body = item
                rows.append(
                    f"                <li><strong>{esc(label)}</strong> — {body}</li>"
                )
            else:
                rows.append(f"                <li>{item}</li>")
        items_html = "\n".join(rows)
        body = f"""              <ul class="lr-mini-model lr-note-list">
{items_html}
              </ul>"""
    else:
        display = items if items else (items_verbatim or [])
        items_html = "\n".join(f"                <li>{item}</li>" for item in display)
        body = f"""              <ul class="lr-note-list">
{items_html}
              </ul>"""

    exchange_html = ""
    for ex in seg.get("exchange", []):
        q = _hl_phrase(ex["q"], ex.get("q_hl", []))
        a = _hl_phrase(ex["a"], ex.get("a_hl", []))
        exchange_html += f"""              <div class="lr-note-exchange">
                <p class="lr-exchange-line">{q}</p>
                <p class="lr-exchange-line">{a}</p>
              </div>
"""

    visual_html = seg.get("visual_html", "")
    visual_block = f"{visual_html}\n" if visual_html else ""
    if visual_html and not items and not items_verbatim and not seg.get("formula") and not speaker:
        body = ""

    return f"""            <div class="lr-segment lr-segment--note{' lr-segment--food-note' if seg.get('food') else ''}{' lr-segment--viz' if visual_html else ''}">
              <h4 class="lr-note-title">{title}</h4>
{intro_html}{visual_block}{body}
{exchange_html}{tip_html}            </div>"""


def speaking_segments_html(slug: str) -> str:
    segments = SPEAKING_SEGMENTS.get(slug, [])
    if not segments:
        return ""
    parts = []
    for seg in segments:
        if seg["type"] == "transcript":
            parts.append(_render_transcript_segment(seg))
        elif seg["type"] == "note":
            parts.append(_render_note_segment(seg))
    return "\n".join(parts)


def speaking_lessons_html() -> str:
    rows = []
    for lesson in SPEAKING_LESSONS:
        slug = lesson["slug"]
        title = lesson["title"]
        why = lesson["why"]
        yt = lesson["youtube"]
        food_ex = lesson["food"]
        timeline = speaking_segments_html(slug)
        rows.append(
            f"""        <li class="lr-lesson-card">
          <div class="lr-lesson-head">
            <strong>{esc(title)}</strong>
            <a class="lr-video-link" href="{esc(yt)}" target="_blank" rel="noopener noreferrer">Watch video ↗</a>
            <span class="lr-lesson-why">{esc(why)}</span>
          </div>
          <details class="lr-lesson-notes">
            <summary>Video catch-up — transcript &amp; notes</summary>
            <p class="lr-catchup-hint">Transcript lấy <strong>nguyên văn</strong> từ phụ đề YouTube. Sau mỗi slide grammar có khối <strong>Food practice</strong> — hội thoại + ví dụ cùng cấu trúc, chủ đề ẩm thực.</p>
            <div class="lr-video-timeline">
{timeline}
            </div>
            <p class="lr-food-ex"><strong>Food:</strong> {food_ex}</p>
          </details>
        </li>"""
        )
    return "\n".join(rows)


def cloze(en: str, vi: str, ipa: str = "") -> str:
    """Cloze span for Scroll-read only — no hover tip (paragraph tip is on the whole line)."""
    return (
        f'<span class="lr-cloze" data-en="{esc(en)}" data-vi="{esc(vi)}" '
        f'data-ipa="{esc(ipa)}">{esc(en)}</span>'
    )


def lesson_scroll_read_html(uid: str, *, title: str, source_sel: str) -> str:
    """Per-lesson teleprompter: structure blanks + VI/IPA hints + copy EN for NaturalReader."""
    return f"""
        <section class="ex-scroll lr-scroll-read lr-lesson-scroll" id="scroll-{esc(uid)}" data-scroll-uid="{esc(uid)}" data-scroll-source="{esc(source_sel)}" aria-label="{esc(title)}">
          <div class="ex-scroll-head">
            <div>
              <h3>Scroll read · speaking · {esc(title)}</h3>
              <p class="ex-scroll-hint">Teleprompter luyện nói — chỉ tiếng Anh. Tắt <strong>Hiện từ EN</strong> để thấy khung + gợi ý VI. Bật <strong>Hiện IPA đoạn</strong> để cả đoạn <em>answer</em> chuyển sang IPA (câu hỏi vẫn giữ tiếng Anh, màu vàng). <strong>Copy</strong> = Q + A tiếng Anh sạch (NaturalReader).</p>
            </div>
            <button type="button" class="ex-btn primary js-scroll-copy">Copy for NaturalReader</button>
          </div>
          <div class="ex-scroll-toolbar">
            <button type="button" class="ex-btn primary js-scroll-play">▶ Play</button>
            <button type="button" class="ex-btn js-scroll-pause">Pause</button>
            <button type="button" class="ex-btn js-scroll-restart">⟲ Restart</button>
            <label class="ex-voice">Speed
              <input class="js-scroll-speed" type="range" min="12" max="90" step="1" value="32">
              <span class="js-scroll-speed-val">32</span> px/s
            </label>
            <label class="ex-voice">Hint
              <select class="js-scroll-hint" aria-label="Hint mode">
                <option value="vi" selected>Nghĩa VI</option>
                <option value="ipa">IPA từ</option>
                <option value="both">VI + IPA</option>
                <option value="struct">Chỉ cấu trúc</option>
              </select>
            </label>
            <label class="ex-toggle"><input type="checkbox" class="js-scroll-reveal"> Hiện từ EN</label>
            <label class="ex-toggle"><input type="checkbox" class="js-scroll-show-ipa"> Hiện IPA đoạn</label>
          </div>
          <div class="ex-scroll-stage">
            <div class="ex-scroll-focus" aria-hidden="true"></div>
            <div class="ex-scroll-viewport">
              <div class="ex-scroll-track"></div>
            </div>
          </div>
        </section>"""


def _pair_answer_html(
    *,
    kind: str,
    en_html: str,
    vi: str,
    plain: str,
    ipa: str,
    q: str,
    ex_en: str = "",
) -> str:
    """One answer line — Thích / Không thích / Mẫu (Lesson 5). Whole-paragraph VI tooltip."""
    tags = {
        "yes": ("Thích", "lr-mm-tag-yes"),
        "no": ("Không thích", "lr-mm-tag-no"),
        "sample": ("Mẫu", "lr-mm-tag-yes"),
        "alt": ("Khác", "lr-mm-tag-no"),
    }
    tag, tag_cls = tags.get(kind, ("Mẫu", "lr-mm-tag-yes"))
    chain = " lr-practice-chain lr-chain" if ex_en else ""
    ex_attr = f' data-ex-en="{esc(ex_en)}"' if ex_en else ""
    return f"""              <div class="lr-scroll-qa{chain}" data-ipa-full="{esc(ipa)}"{ex_attr}>
                <p class="lr-scroll-q" hidden>{esc(q)}</p>
                <p class="lr-food-ex-line lr-tip lr-answer-text" data-tip="{esc(vi)}" title="{esc(vi)}" data-plain="{esc(plain)}">
                  <span class="{tag_cls}">{tag}</span>
                  <span class="lr-tip-text">{en_html}</span>
                </p>
                <p class="lr-practice-en lr-chain-ex-text" hidden></p>
              </div>"""


def _ex_chip_notes_html(chips: list | None) -> str:
    """Structure / vocab chips under an example card — hover for VI tooltip."""
    if not chips:
        return ""
    # en → vi (for hover); also split "A · B" into two chips
    chip_vi = {
        "It takes + time (+ for sb) + to V": "Tốn bao nhiêu thời gian (cho ai) để làm gì",
        "while / whereas": "trong khi / trong khi đó (đối chiếu)",
        "love the feeling of + V-ing": "Thích cảm giác làm gì",
        "pose a threat to (my) health": "Gây đe dọa đến sức khỏe",
        "have a sweet tooth": "Thích đồ ngọt (có ‘răng ngọt’)",
        "function (v) — body / brain / nutrients": "Hoạt động (cơ thể / não / khi đủ dinh dưỡng)",
        "have someone to + V": "Có ai đó để làm gì",
        "send sth to sb": "Gửi cái gì cho ai",
        "grab a bite": "Ăn vội một miếng",
        "shorten one's / my life expectancy": "Làm giảm tuổi thọ",
        "try not to + V": "Cố gắng không làm gì",
        "try to + V": "Cố gắng làm gì",
        "try + V-ing": "Thử làm theo cách nào đó",
        "take a heavy toll on (my) health": "Gây hậu quả nặng nề cho sức khỏe",
        "I hardly ever + V": "Hiếm khi / hầu như không bao giờ + V",
        "prefer … rather than …": "Thích … hơn là …",
        "prefer to V rather than V": "prefer to V rather than V (nguyên mẫu)",
        "can lead to …": "Có thể dẫn đến …",
        "because / because of": "because + mệnh đề · because of + danh từ",
        "culinary tradition": "Truyền thống ẩm thực",
        "wholesome": "Lành mạnh, bổ dưỡng",
        "freshly prepared": "Mới chế biến",
        "from scratch": "Làm từ đầu / từ nguyên liệu thô",
        "light on the stomach": "Dễ tiêu / không nặng bụng",
        "stick to a balanced diet": "Giữ chế độ ăn cân bằng",
        "hits the spot": "Đúng gu / thỏa mãn đúng lúc",
        "burn excess calories": "Đốt calo thừa",
        "signature dish": "Món đặc trưng",
        "mouth-watering": "Cực ngon / kích thích vị giác",
    }
    expanded: list[tuple[str, str]] = []
    for c in chips:
        if not c:
            continue
        if isinstance(c, dict):
            expanded.append((c.get("en", ""), c.get("vi", "")))
            continue
        for part in str(c).split(" · "):
            en = part.strip()
            if not en:
                continue
            expanded.append((en, chip_vi.get(en, "")))
    items = "".join(
        f'<li class="lr-tip" data-tip="{esc(vi)}" title="{esc(vi)}">'
        f"<mark>{esc(en)}</mark></li>"
        if vi
        else f"<li><mark>{esc(en)}</mark></li>"
        for en, vi in expanded
        if en
    )
    return f"""
            <ul class="lr-ex-chips" aria-label="Cấu trúc trong ví dụ">
{items}
            </ul>"""


def food_lesson5_examples_html() -> str:
    """Lesson 5 · What kind of X? — 10 Food Qs with soft-choose + reason (IELTS length)."""
    items: list[dict] = []

    def add(
        q: str,
        en_html: str,
        vi: str,
        plain: str,
        ipa: str,
        ex: str,
        *,
        alt_html: str = "",
        alt_vi: str = "",
        alt_plain: str = "",
        alt_ipa: str = "",
        alt_ex: str = "",
        notes: list[str] | None = None,
    ) -> None:
        items.append(
            {
                "q": q,
                "html": en_html,
                "vi": vi,
                "plain": plain,
                "ipa": ipa,
                "ex": ex,
                "alt_html": alt_html,
                "alt_vi": alt_vi,
                "alt_plain": alt_plain,
                "alt_ipa": alt_ipa,
                "alt_ex": alt_ex,
                "notes": notes or [],
            }
        )

    # 1 — slide example
    t1 = (
        "Well, I love all kinds of food, but if I had to choose one, I would opt for "
        "{kind_choice_food}. This is because I think it's {kind_lex_reason}. "
        "{kind_followup}"
    )
    add(
        "What kind of food do you like to eat most?",
        t1.format(
            kind_choice_food=phrase_pick("kind_choice_food", 0),
            kind_lex_reason=phrase_pick("kind_lex_reason", 0),
            kind_followup=phrase_pick("kind_followup", 0),
        ),
        "Chà, tôi thích mọi loại đồ ăn, nhưng nếu phải chọn một thì tôi sẽ chọn đồ nấu nhà. Vì tôi nghĩ nó lành mạnh hơn đồ nhà hàng. Tôi cố không ăn ngoài quá thường xuyên.",
        "Well, I love all kinds of food, but if I had to choose one, I would opt for home-cooked food. This is because I think it's much healthier than restaurant food. I try not to eat out too often.",
        "/wel aɪ lʌv ɔːl kaɪndz əv fuːd…/",
        t1,
        alt_html=(
            "I like {kind_choice_food} most because it is {kind_lex_adj}. "
            "{kind_followup}".format(
                kind_choice_food=phrase_pick("kind_choice_food", 1),
                kind_lex_adj=phrase_pick("kind_lex_adj", 0),
                kind_followup=phrase_pick("kind_followup", 2),
            )
        ),
        alt_vi="Tôi thích đồ đường phố nhất vì cực ngon và đầy hương vị. Tôi cũng được ăn vội mà không nặng bụng.",
        alt_plain="I like street food most because it is mouth-watering and packed with flavour. I also get the chance to grab a bite without feeling heavy afterwards.",
        alt_ipa="/aɪ laɪk striːt fuːd məʊst…/",
        alt_ex="I like {kind_choice_food} most because it is {kind_lex_adj}. {kind_followup}",
        notes=["try not to + V", "grab a bite"],
    )

    # 2 cuisine
    t2 = (
        "Well, I love all kinds of cuisine, but if I had to choose one, I would go for "
        "{kind_choice_cuisine}. This is because the dishes are {kind_lex_adj}. "
        "Exploring this culinary tradition also helps me enrich my knowledge about food culture."
    )
    add(
        "What kind of cuisine do you like most?",
        t2.format(
            kind_choice_cuisine=phrase_pick("kind_choice_cuisine", 0),
            kind_lex_adj=phrase_pick("kind_lex_adj", 1),
        ),
        "Tôi thích mọi kiểu ẩm thực, nhưng nếu phải chọn thì sẽ là ẩm thực Việt vì món lành mạnh, mới chế biến. Khám phá truyền thống ẩm thực cũng giúp làm giàu kiến thức.",
        "Well, I love all kinds of cuisine, but if I had to choose one, I would go for Vietnamese cuisine. This is because the dishes are wholesome and freshly prepared. Exploring this culinary tradition also helps me enrich my knowledge about food culture.",
        "/wel aɪ lʌv ɔːl kaɪndz əv kwɪˈziːn…/",
        t2,
        notes=["culinary tradition", "wholesome · freshly prepared"],
    )

    # 3 restaurants
    t3 = (
        "I love all kinds of restaurants, but if I had to choose one, it would have to be "
        "{kind_choice_restaurant}. This is because the food there is {kind_lex_reason}. "
        "{kind_followup}"
    )
    add(
        "What kinds of restaurants do you like most?",
        t3.format(
            kind_choice_restaurant=phrase_pick("kind_choice_restaurant", 0),
            kind_lex_reason=phrase_pick("kind_lex_reason", 1),
            kind_followup=phrase_pick("kind_followup", 0),
        ),
        "Tôi thích nhiều loại nhà hàng, nhưng nếu phải chọn thì sẽ là quán bình dân gần nhà vì đồ ăn làm từ đầu với nguyên liệu tươi. Tôi cố không ăn ngoài quá thường xuyên.",
        "I love all kinds of restaurants, but if I had to choose one, it would have to be casual local eateries. This is because the food there is made from scratch with fresh ingredients. I try not to eat out too often.",
        "/aɪ lʌv ɔːl kaɪndz əv ˈrestrɒnts…/",
        t3,
        notes=["from scratch", "try not to + V"],
    )

    # 4 drinks
    t4 = (
        "Well, I love all kinds of drinks, but if I had to choose one, I would opt for "
        "{kind_choice_drink}. This is because it's {kind_lex_adj}. "
        "I try to cut down on sugary soft drinks as well."
    )
    add(
        "What kind of drinks do you like most?",
        t4.format(
            kind_choice_drink=phrase_pick("kind_choice_drink", 0),
            kind_lex_adj=phrase_pick("kind_lex_adj", 2),
        ),
        "Tôi thích nhiều loại đồ uống, nhưng nếu phải chọn thì nước ép trái cây tươi vì dễ tiêu mà vẫn no. Tôi cũng cố giảm nước ngọt có đường.",
        "Well, I love all kinds of drinks, but if I had to choose one, I would opt for fresh fruit juice. This is because it's light on the stomach but still filling. I try to cut down on sugary soft drinks as well.",
        "/wel aɪ lʌv ɔːl kaɪndz əv drɪŋks…/",
        t4,
        notes=["try to + V", "light on the stomach"],
    )

    # 5 fruit
    t5 = (
        "I like {kind_choice_fruit} most because they are {kind_lex_adj}. "
        "Eating fruit regularly is {kind_lex_reason}."
    )
    add(
        "What kind of fruit do you like most?",
        t5.format(
            kind_choice_fruit=phrase_pick("kind_choice_fruit", 0),
            kind_lex_adj=phrase_pick("kind_lex_adj", 1),
            kind_lex_reason=phrase_pick("kind_lex_reason", 2),
        ),
        "Tôi thích trái nhiệt đới như xoài và đu đủ nhất vì lành mạnh, mới. Ăn trái cây đều đặn là cách tuyệt để giữ chế độ ăn cân bằng.",
        "I like tropical fruit like mango and papaya most because they are wholesome and freshly prepared. Eating fruit regularly is a great way to stick to a balanced diet.",
        "/aɪ laɪk ˈtrɒpɪkl fruːt…/",
        t5,
        notes=["stick to a balanced diet"],
    )

    # 6 snacks
    t6 = (
        "Well, I love all kinds of snacks, but if I had to choose one, I would go for "
        "{kind_choice_snack}. This is because they are {kind_lex_reason}. "
        "{kind_followup}"
    )
    add(
        "What kinds of snacks do you like most?",
        t6.format(
            kind_choice_snack=phrase_pick("kind_choice_snack", 0),
            kind_lex_reason=phrase_pick("kind_lex_reason", 3),
            kind_followup=phrase_pick("kind_followup", 1),
        ),
        "Tôi thích nhiều loại snack, nhưng nếu phải chọn thì hạt vì đầy dinh dưỡng mà không hại sức khỏe. Tôi cố giảm đồ ăn vặt chế biến sẵn.",
        "Well, I love all kinds of snacks, but if I had to choose one, I would go for nuts and seeds. This is because they are full of nutrients without taking a heavy toll on my health. I try to cut down on processed snacks.",
        "/wel aɪ lʌv ɔːl kaɪndz əv snæks…/",
        t6,
        notes=["take a heavy toll on (my) health", "try to + V"],
    )

    # 7 desserts / sweet tooth
    t7 = (
        "To be honest, I have a bit of a sweet tooth, so if I had to choose one, "
        "it would have to be {kind_choice_dessert}. This is because they are "
        "{kind_lex_adj}. Still, I try not to overdo it."
    )
    add(
        "What kind of desserts do you like most?",
        t7.format(
            kind_choice_dessert=phrase_pick("kind_choice_dessert", 0),
            kind_lex_adj=phrase_pick("kind_lex_adj", 3),
        ),
        "Thành thật thì tôi hơi thích đồ ngọt, nên nếu phải chọn thì sẽ là tráng miệng từ trái cây vì an ủi mà không quá nhiều dầu. Vẫn cố không ăn quá đà.",
        "To be honest, I have a bit of a sweet tooth, so if I had to choose one, it would have to be fruit-based desserts. This is because they are comforting without being too greasy. Still, I try not to overdo it.",
        "/tuː bi ˈɒnɪst aɪ hæv ə bɪt əv ə swiːt tuːθ…/",
        t7,
        notes=["have a sweet tooth", "try not to + V"],
    )

    # 8 cooking methods / dishes
    t8 = (
        "I love all kinds of cooking styles, but if I had to choose one, I would opt for "
        "{kind_choice_method}. This is because they are {kind_lex_reason}. "
        "{kind_followup}"
    )
    add(
        "What kind of dishes do you like most?",
        t8.format(
            kind_choice_method=phrase_pick("kind_choice_method", 0),
            kind_lex_reason=phrase_pick("kind_lex_reason", 4),
            kind_followup=phrase_pick("kind_followup", 3),
        ),
        "Tôi thích nhiều kiểu chế biến, nhưng nếu phải chọn thì món nướng vì đúng gu sau ngày dài. Giúp giữ dáng và đốt thêm calo.",
        "I love all kinds of cooking styles, but if I had to choose one, I would opt for grilled dishes. This is because they are the kind of food that really hits the spot after a long day. It helps me keep fit and burn a few extra calories.",
        "/aɪ lʌv ɔːl kaɪndz əv ˈkʊkɪŋ staɪlz…/",
        t8,
        notes=["hits the spot", "burn excess calories"],
    )

    # 9 street food
    t9 = (
        "Well, I love all kinds of street food, but if I had to choose one, I would go for "
        "{kind_choice_street}. This is because they are {kind_lex_adj}. "
        "Trying local signature dishes is also a great way to experience culinary tradition."
    )
    add(
        "What kinds of street food do you like most?",
        t9.format(
            kind_choice_street=phrase_pick("kind_choice_street", 0),
            kind_lex_adj=phrase_pick("kind_lex_adj", 0),
        ),
        "Tôi thích nhiều món đường phố, nhưng nếu phải chọn thì phở và gỏi cuốn vì cực ngon, đầy hương vị. Thử món đặc trưng địa phương cũng là cách trải nghiệm truyền thống ẩm thực.",
        "Well, I love all kinds of street food, but if I had to choose one, I would go for pho and spring rolls. This is because they are mouth-watering and packed with flavour. Trying local signature dishes is also a great way to experience culinary tradition.",
        "/wel aɪ lʌv ɔːl kaɪndz əv striːt fuːd…/",
        t9,
        notes=["signature dish", "culinary tradition", "mouth-watering"],
    )

    # 10 meals of the day
    t10 = (
        "I love all kinds of meals, but if I had to choose one, it would have to be "
        "{kind_choice_meal}. This is because it's {kind_lex_reason}. "
        "{kind_followup}"
    )
    add(
        "What kind of meals do you like most?",
        t10.format(
            kind_choice_meal=phrase_pick("kind_choice_meal", 2),
            kind_lex_reason=phrase_pick("kind_lex_reason", 1),
            kind_followup=phrase_pick("kind_followup", 4),
        ),
        "Tôi thích mọi bữa ăn, nhưng nếu phải chọn thì bữa tối sớm ở nhà vì làm từ đầu với nguyên liệu tươi. Tôi cố dùng nguyên liệu theo mùa khi có thể.",
        "I love all kinds of meals, but if I had to choose one, it would have to be an early dinner at home. This is because it's made from scratch with fresh ingredients. I try using seasonal ingredients whenever I can.",
        "/aɪ lʌv ɔːl kaɪndz əv miːlz…/",
        t10,
        notes=["try + V-ing", "from scratch"],
    )

    cards = []
    for it in items:
        alts = ""
        if it.get("alt_html"):
            alts = _pair_answer_html(
                kind="alt",
                en_html=it["alt_html"],
                vi=it["alt_vi"],
                plain=it["alt_plain"],
                ipa=it["alt_ipa"],
                q=it["q"],
                ex_en=it.get("alt_ex", ""),
            )
        cards.append(
            f"""          <article class="lr-food-ex-card">
            <p class="lr-food-ex-q">{esc(it["q"])}</p>
            <div class="lr-food-ex-pair lr-food-ex-pair--kind">
{_pair_answer_html(kind="sample", en_html=it["html"], vi=it["vi"], plain=it["plain"], ipa=it["ipa"], q=it["q"], ex_en=it["ex"])}
{alts}
            </div>
{_ex_chip_notes_html(it.get("notes"))}
          </article>"""
        )
    return f"""
        <div class="lr-food-examples" id="food-examples-l5">
          <h3 class="lr-core-subtitle">Ví dụ Food · What kind of X?</h3>
          <p class="lr-mm-hint">10 câu Part 1 (Food). Hover EN → tooltip VI. Chip dưới mỗi card = cấu trúc / từ mới trong câu đó.</p>
{chr(10).join(cards)}
        </div>"""


def food_lesson6_examples_html() -> str:
    """Lesson 6 · Do you prefer X or Y? — 10 Food Qs with prefer + contrast structures."""
    items: list[dict] = []

    def add(
        q: str,
        en_html: str,
        vi: str,
        plain: str,
        ipa: str,
        ex: str,
        *,
        alt_html: str = "",
        alt_vi: str = "",
        alt_plain: str = "",
        alt_ipa: str = "",
        alt_ex: str = "",
        notes: list[str] | None = None,
    ) -> None:
        items.append(
            {
                "q": q,
                "html": en_html,
                "vi": vi,
                "plain": plain,
                "ipa": ipa,
                "ex": ex,
                "alt_html": alt_html,
                "alt_vi": alt_vi,
                "alt_plain": alt_plain,
                "alt_ipa": alt_ipa,
                "alt_ex": alt_ex,
                "notes": notes or [],
            }
        )

    # 1 — home vs out (It takes + while)
    t1 = (
        "I prefer {prefer_pair_home} because it's much healthier and more relaxing, "
        "{prefer_contrast}. Preparing dinner myself, {prefer_it_takes}, whereas "
        "ordering takeaway only takes a few minutes — but I still choose home food."
    )
    add(
        "Do you prefer eating at home or eating out?",
        t1.format(
            prefer_pair_home=phrase_pick("prefer_pair_home", 0),
            prefer_contrast=phrase_pick("prefer_contrast", 0),
            prefer_it_takes=phrase_pick("prefer_it_takes", 0),
        ),
        "Tôi thích ăn ở nhà hơn ăn ngoài vì lành mạnh và thư giãn hơn, trong khi ăn ngoài thường tốn thời gian và đắt. Tự nấu tối mất khoảng một giờ, còn gọi mang về chỉ vài phút — nhưng tôi vẫn chọn đồ nhà.",
        "I prefer eating at home to eating out because it's much healthier and more relaxing, while eating out is often more time-consuming and expensive. Preparing dinner myself, it takes me about an hour to cook a proper meal from scratch, whereas ordering takeaway only takes a few minutes — but I still choose home food.",
        "/aɪ prɪˈfɜː ˈiːtɪŋ ət həʊm tuː ˈiːtɪŋ aʊt…/",
        t1,
        notes=["It takes + time (+ for sb) + to V", "while / whereas"],
    )

    # 2 — cook vs takeaway (love the feeling)
    t2 = (
        "I prefer {prefer_pair_home} because I love the feeling of {prefer_feeling}. "
        "Takeaway is convenient, {prefer_contrast}."
    )
    add(
        "Do you prefer cooking yourself or ordering takeaway?",
        t2.format(
            prefer_pair_home=phrase_pick("prefer_pair_home", 2),
            prefer_feeling=phrase_pick("prefer_feeling", 1),
            prefer_contrast=phrase_pick("prefer_contrast", 1),
        ),
        "Tôi thích tự nấu hơn gọi mang về vì tôi thích cảm giác nấu chậm và ngửi mùi gia vị. Mang về thì tiện, trong khi fast food có thể đe dọa sức khỏe.",
        "I prefer cooking at home to ordering takeaway because I love the feeling of cooking slowly and smelling the spices in the kitchen. Takeaway is convenient, whereas fast food can pose a threat to my health.",
        "/aɪ prɪˈfɜː ˈkʊkɪŋ ət həʊm…/",
        t2,
        notes=["love the feeling of + V-ing", "pose a threat to (my) health"],
    )

    # 3 — sweet vs savoury (sweet tooth + function)
    t3 = (
        "To be honest, I have a bit of a sweet tooth, but I still prefer "
        "{prefer_pair_sweet} most days. This is because after a savoury meal "
        "{prefer_function}."
    )
    add(
        "Do you prefer sweet food or savoury food?",
        t3.format(
            prefer_pair_sweet=phrase_pick("prefer_pair_sweet", 0),
            prefer_function=phrase_pick("prefer_function", 0),
        ),
        "Thành thật thì tôi hơi thích đồ ngọt, nhưng hầu hết ngày tôi vẫn thích món mặn hơn món ngọt. Vì sau bữa mặn cơ thể tôi hoạt động hiệu quả hơn cả ngày.",
        "To be honest, I have a bit of a sweet tooth, but I still prefer savoury dishes to sweet desserts most days. This is because after a savoury meal my body functions more effectively throughout the day.",
        "/tuː bi ˈɒnɪst… swiːt tuːθ…/",
        t3,
        notes=["have a sweet tooth", "function (v) — body / brain / nutrients"],
    )

    # 4 — family vs alone (have someone to)
    t4 = (
        "I prefer {prefer_pair_social} because it's more interesting if you "
        "{prefer_have_someone} during the meal, and it's much safer when you "
        "{prefer_have_someone} with portion sizes and new recipes."
    )
    # Fix: two have_someone picks - use different indices
    t4 = (
        "I prefer {prefer_pair_social} because it's more interesting if you "
        "{prefer_have_someone}. I also love the feeling of {prefer_feeling}."
    )
    add(
        "Do you prefer eating with your family or eating alone?",
        t4.format(
            prefer_pair_social=phrase_pick("prefer_pair_social", 0),
            prefer_have_someone=phrase_pick("prefer_have_someone", 0),
            prefer_feeling=phrase_pick("prefer_feeling", 0),
        ),
        "Tôi thích ăn với gia đình hơn ăn một mình vì thú vị hơn khi có ai đó chia sẻ bữa. Tôi cũng thích cảm giác ngồi quanh bàn với gia đình thưởng thức món mới nấu.",
        "I prefer eating with my family to eating alone because it's more interesting if you have someone to share the meal with. I also love the feeling of sitting around the table with my family and tasting freshly cooked dishes.",
        "/aɪ prɪˈfɜː ˈiːtɪŋ wɪð maɪ ˈfæməli…/",
        t4,
        notes=["have someone to + V", "love the feeling of + V-ing"],
    )

    # 5 — tea vs coffee (feeling + function)
    t5 = (
        "I prefer {prefer_pair_drink} because I love the feeling of {prefer_feeling}. "
        "With a light drink, {prefer_function}, while strong coffee sometimes makes me restless."
    )
    add(
        "Do you prefer drinking tea or coffee?",
        t5.format(
            prefer_pair_drink=phrase_pick("prefer_pair_drink", 0),
            prefer_feeling=phrase_pick("prefer_feeling", 3),
            prefer_function=phrase_pick("prefer_function", 0),
        ),
        "Tôi thích trà thảo mộc hơn cà phê vì thích cảm giác nhấp trà sau bữa nhẹ. Với đồ uống nhẹ, cơ thể hoạt động hiệu quả hơn cả ngày, trong khi cà phê đậm đôi khi làm tôi bồn chồn.",
        "I prefer herbal tea to coffee because I love the feeling of sipping tea after a light homemade meal. With a light drink, my body functions more effectively throughout the day, while strong coffee sometimes makes me restless.",
        "/aɪ prɪˈfɜː ˈhɜːbl tiː…/",
        t5,
        notes=["love the feeling of + V-ing", "function (v) — body / brain / nutrients"],
    )

    # 6 — healthy vs fast food (function + threat)
    t6 = (
        "I prefer {prefer_pair_health} because {prefer_function}, {prefer_contrast}. "
        "Fast food may help me grab a bite quickly, but it can also shorten my life expectancy "
        "if I rely on it every day."
    )
    add(
        "Do you prefer healthy food or fast food?",
        t6.format(
            prefer_pair_health=phrase_pick("prefer_pair_health", 0),
            prefer_function=phrase_pick("prefer_function", 3),
            prefer_contrast=phrase_pick("prefer_contrast", 1),
        ),
        "Tôi thích bữa nấu nhà lành mạnh hơn fast food vì tôi làm việc hiệu quả hơn sau bữa trưa lành mạnh, trong khi fast food đe dọa sức khỏe. Fast food giúp ăn vội nhưng có thể giảm tuổi thọ nếu dựa vào mỗi ngày.",
        "I prefer wholesome home-cooked meals to fast food because I function better at work after a wholesome lunch, whereas fast food can pose a threat to my health. Fast food may help me grab a bite quickly, but it can also shorten my life expectancy if I rely on it every day.",
        "/aɪ prɪˈfɜː ˈhəʊlsəm…/",
        t6,
        notes=[
            "function (v) — body / brain / nutrients",
            "grab a bite",
            "shorten one's / my life expectancy",
        ],
    )

    # 7 — spicy vs mild
    t7 = (
        "I prefer {prefer_pair_taste} because spicy food wakes up my taste buds, "
        "while mild dishes sometimes feel bland. Still, I try not to overdo chilli "
        "because too much spice can take a heavy toll on my stomach."
    )
    add(
        "Do you prefer spicy food or mild food?",
        t7.format(prefer_pair_taste=phrase_pick("prefer_pair_taste", 1)),
        "Tôi thích món cay hơn món nhạt vì món cay đánh thức vị giác, trong khi món dịu đôi khi nhạt. Vẫn cố không lạm dụng ớt vì quá cay có thể hại dạ dày.",
        "I prefer spicy food rather than bland meals because spicy food wakes up my taste buds, while mild dishes sometimes feel bland. Still, I try not to overdo chilli because too much spice can take a heavy toll on my stomach.",
        "/aɪ prɪˈfɜː ˈspaɪsi fuːd…/",
        t7,
        notes=["try not to + V", "take a heavy toll on (my) health"],
    )

    # 8 — restaurant vs street food (it takes)
    t8 = (
        "I prefer grabbing street food to sitting in a formal restaurant because "
        "{prefer_it_takes}, while a full restaurant meal is more time-consuming. "
        "I love the feeling of {prefer_feeling}."
    )
    add(
        "Do you prefer eating in a restaurant or grabbing street food?",
        t8.format(
            prefer_it_takes=phrase_pick("prefer_it_takes", 2),
            prefer_feeling=phrase_pick("prefer_feeling", 2),
        ),
        "Tôi thích ăn vặt đường phố hơn ngồi nhà hàng trang trọng vì chỉ mất vài phút để ăn vội ở quán vỉa hè, trong khi bữa nhà hàng tốn thời gian hơn. Tôi thích cảm giác ăn lẩu chung và tám chuyện.",
        "I prefer grabbing street food to sitting in a formal restaurant because it only takes a few minutes to grab a bite from a street stall, while a full restaurant meal is more time-consuming. I love the feeling of sharing a hot pot and chatting over food.",
        "/aɪ prɪˈfɜː ˈɡræbɪŋ striːt fuːd…/",
        t8,
        notes=["It takes + time (+ for sb) + to V", "love the feeling of + V-ing"],
    )

    # 9 — meal prep vs fresh daily (It takes + while)
    t9 = (
        "I prefer preparing meals in advance to cooking everything fresh every evening "
        "because {prefer_it_takes} on Sunday, while weekday cooking can be exhausting. "
        "Then I only need a few minutes to reheat and eat."
    )
    add(
        "Do you prefer preparing meals in advance or cooking fresh every day?",
        t9.format(prefer_it_takes=phrase_pick("prefer_it_takes", 1)),
        "Tôi thích chuẩn bị sẵn hơn nấu mới mỗi tối vì cuối tuần có thể mất vài giờ chuẩn bị tiệc/phần ăn, trong khi nấu ngày thường dễ mệt. Sau đó chỉ cần vài phút hâm nóng và ăn.",
        "I prefer preparing meals in advance to cooking everything fresh every evening because it can take several hours to prepare a traditional feast on Sunday, while weekday cooking can be exhausting. Then I only need a few minutes to reheat and eat.",
        "/aɪ prɪˈfɜː prɪˈpeərɪŋ miːlz…/",
        t9,
        notes=["It takes + time (+ for sb) + to V", "while / whereas"],
    )

    # 10 — send photos (send sth to sb)
    t10 = (
        "I prefer sharing food moments online to keeping them private because I can "
        "{prefer_send}. It's more fun when you {prefer_have_someone}, and they often "
        "send a recipe back to me as well."
    )
    add(
        "Do you prefer sharing food photos online or keeping them private?",
        t10.format(
            prefer_send=phrase_pick("prefer_send", 0),
            prefer_have_someone=phrase_pick("prefer_have_someone", 3),
        ),
        "Tôi thích chia sẻ khoảnh khắc đồ ăn online hơn giữ riêng vì tôi có thể gửi ảnh món tự nấu cho bạn. Vui hơn khi có ai đó để gửi gợi ý món, và họ thường gửi lại công thức cho tôi.",
        "I prefer sharing food moments online to keeping them private because I can send photos of my homemade dishes to my friends. It's more fun when you have someone to send food recommendations to, and they often send a recipe back to me as well.",
        "/aɪ prɪˈfɜː ˈʃeərɪŋ fuːd ˈməʊmənts…/",
        t10,
        alt_html=(
            "I prefer cooking with friends to cooking on my own because I "
            "{prefer_have_someone}, and we can {prefer_send} afterwards.".format(
                prefer_have_someone=phrase_pick("prefer_have_someone", 2),
                prefer_send=phrase_pick("prefer_send", 1),
            )
        ),
        alt_vi="Tôi thích nấu với bạn hơn nấu một mình vì có người giúp trong bếp, và sau đó có thể gửi công thức cho chị/em.",
        alt_plain="I prefer cooking with friends to cooking on my own because I have someone to help me in the kitchen, and we can send a recipe to my sister afterwards.",
        alt_ipa="/aɪ prɪˈfɜː ˈkʊkɪŋ wɪð frendz…/",
        alt_ex=(
            "I prefer cooking with friends to cooking on my own because I "
            "{prefer_have_someone}, and we can {prefer_send} afterwards."
        ),
        notes=["send sth to sb", "have someone to + V"],
    )

    cards = []
    for it in items:
        alts = ""
        if it.get("alt_html"):
            alts = _pair_answer_html(
                kind="alt",
                en_html=it["alt_html"],
                vi=it["alt_vi"],
                plain=it["alt_plain"],
                ipa=it["alt_ipa"],
                q=it["q"],
                ex_en=it.get("alt_ex", ""),
            )
        cards.append(
            f"""          <article class="lr-food-ex-card">
            <p class="lr-food-ex-q">{esc(it["q"])}</p>
            <div class="lr-food-ex-pair lr-food-ex-pair--prefer">
{_pair_answer_html(kind="sample", en_html=it["html"], vi=it["vi"], plain=it["plain"], ipa=it["ipa"], q=it["q"], ex_en=it["ex"])}
{alts}
            </div>
{_ex_chip_notes_html(it.get("notes"))}
          </article>"""
        )
    return f"""
        <div class="lr-food-examples" id="food-examples-l6">
          <h3 class="lr-core-subtitle">Ví dụ Food · Do you prefer X or Y?</h3>
          <p class="lr-mm-hint">10 câu Part 1 (Food). Chip dưới mỗi card = cấu trúc slide dùng trong câu đó.</p>
{chr(10).join(cards)}
        </div>"""


def food_lesson_examples_html() -> str:
    """Unified Food cards: every Q has Thích + Không thích; both sides have contextual dropdowns."""
    items = []

    # ── cooking at home (Favourite: prefer on YES · hardly ever on NO) ──
    cook_yes_tpl = (
        "Yes, definitely. I'm keen on cooking {cuisine} at home because it gives me "
        "the chance to try new recipes and {relax_phrase}. "
        "I prefer {prefer_rather_than}."
    )
    cook_no_tpl = (
        "No, I don't enjoy cooking. I hardly ever {hardly_ever_action} because it {dislike_feel} "
        "after a long day at work."
    )
    items.append({
        "q": "Do you like cooking at home?",
        "yes_html": cook_yes_tpl.format(
            cuisine=slot_select("cuisine"),
            relax_phrase=phrase_pick("relax_phrase", 1),
            prefer_rather_than=phrase_pick("prefer_rather_than", 3),
        ),
        "yes_vi": "Vâng, chắc chắn. Tôi thích nấu ăn ở nhà vì được thử công thức mới và thư giãn. Tôi thích đồ nấu nhà hơn ăn ngoài.",
        "yes_plain": "Yes, definitely. I'm keen on cooking cuisine at home because it gives me the chance to try new recipes and relax and clear their head. I prefer home-cooked food rather than eating out.",
        "yes_ipa": "/jes ˈdefɪnətli · aɪm kiːn ɒn ˈkʊkɪŋ ət həʊm…/",
        "yes_ex": cook_yes_tpl,
        "no_html": cook_no_tpl.format(
            hardly_ever_action=phrase_pick("hardly_ever_action", 0),
            dislike_feel=phrase_pick("dislike_feel", 0),
        ),
        "no_vi": "Không, tôi không thích nấu ăn. Tôi hiếm khi nấu ăn vì nó làm tôi kiệt sức sau một ngày dài làm việc.",
        "no_plain": "No, I don't enjoy cooking. I hardly ever cook because it makes me exhausted after a long day at work.",
        "no_ipa": "/nəʊ aɪ dəʊnt ɪnˈdʒɔɪ ˈkʊkɪŋ · aɪ ˈhɑːdli ˈevə kʊk…/",
        "no_ex": cook_no_tpl,
        "notes": ["I hardly ever + V", "prefer … rather than …"],
    })

    # ── fast food ──
    ff_yes_tpl = (
        "Yes, occasionally — it's convenient when I'm busy and {convenience_benefit}. "
        "Grabbing a bite with friends is also {social_benefit}."
    )
    ff_no_tpl = (
        "No, definitely not because it's not good for my health. Consuming too much "
        "{unhealthy_food} and greasy {dessert} can lead to {health_outcome}."
    )
    items.append({
        "q": "Do you like fast food?",
        "yes_html": ff_yes_tpl.format(
            convenience_benefit=phrase_pick("convenience_benefit", 0),
            social_benefit=phrase_pick("social_benefit", 0),
        ),
        "yes_vi": "Có, thỉnh thoảng — tiện khi tôi bận và giúp thư giãn sau ngày dài. Ăn vội với bạn cũng giúp thoát khỏi thực tại một lúc.",
        "yes_plain": "Yes, occasionally — it's convenient when I'm busy and it helps me unwind after a long day. Grabbing a bite with friends is also a great way to escape from reality for a while.",
        "yes_ipa": "/jes əˈkeɪʒənəli…/",
        "yes_ex": ff_yes_tpl,
        "no_html": ff_no_tpl.format(
            unhealthy_food=phrase_pick("unhealthy_food", 0),
            dessert=slot_select("dessert"),
            health_outcome=phrase_pick("health_outcome", 0),
        ),
        "no_vi": "Không, chắc chắn không rồi vì nó không tốt cho sức khỏe của tôi. Tiêu thụ quá nhiều thức ăn nhanh có thể dẫn đến các vấn đề sức khỏe khác nhau, chẳng hạn như bệnh tiểu đường, đau tim, huyết áp cao hoặc thậm chí là ung thư.",
        "no_plain": "No, definitely not because it's not good for my health. Consuming too much fast food and greasy cheesecake can lead to various health problems, such as diabetes, heart attack, high blood pressure or even cancer.",
        "no_ipa": "/nəʊ ˈdefɪnətli nɒt…/",
        "no_ex": ff_no_tpl,
        "notes": ["can lead to …", "because / because of"],
    })

    # ── vegetables ──
    veg_yes_tpl = (
        "Yes, definitely, because it's a great way to {health_phrase}. "
        "{health_followup}"
    )
    veg_no_tpl = (
        "No, not really — plain vegetables {soft_dislike} and {taste_complaint}."
    )
    items.append({
        "q": "Do you like eating vegetables?",
        "yes_html": veg_yes_tpl.format(
            health_phrase=phrase_pick("health_phrase"),
            health_followup=phrase_pick("health_followup", 0),
        ),
        "yes_vi": "Vâng — rau giúp giữ dáng, khỏe mạnh và phòng bệnh. Nó cũng giúp tăng cơ bắp.",
        "yes_plain": "Yes, definitely, because it's a great way to stay healthy and prevent various health problems. It also helps them strengthen their muscles.",
        "yes_ipa": "/jes ˈdefɪnətli…/",
        "yes_ex": veg_yes_tpl,
        "no_html": veg_no_tpl.format(
            soft_dislike=phrase_pick("soft_dislike", 0),
            taste_complaint=phrase_pick("taste_complaint", 0),
        ),
        "no_vi": "Không thực sự — rau nhạt không phải sở thích của tôi và không mang lại hương vị phong phú.",
        "no_plain": "No, not really — plain vegetables aren't my cup of tea and they don't give me richer flavours.",
        "no_ipa": "/nəʊ nɒt ˈrɪəli…/",
        "no_ex": veg_no_tpl,
    })

    # ── new cuisines ──
    cui_yes_tpl = (
        "Yes, absolutely. I'm a big fan of {cuisine} from different cultures. "
        "This is because it helps me {edu_phrase}."
    )
    cui_no_tpl = (
        "Well, not really — I'm not keen on unfamiliar food because {dislike_no_benefit}."
    )
    # dislike_no_benefit starts with "It doesn't..." — for "because It doesn't" grammar is ok
    # Better: use a because_reason slot without "It" for this sentence
    # Adjust template: "because it doesn't help me relax when I eat out" style
    # Use soft reasons that fit after "because"
    cui_no_tpl = (
        "Well, not really — unfamiliar food {soft_dislike} because "
        "eating out {dislike_feel} when I don't know the menu."
    )
    # hmm dislike_feel is "makes me exhausted" - "eating out makes me exhausted" works
    cui_no_tpl = (
        "Well, not really — unfamiliar food {soft_dislike}. "
        "{dislike_no_benefit} when I eat out."
    )
    items.append({
        "q": "Do you like trying new cuisines?",
        "yes_html": cui_yes_tpl.format(
            cuisine=slot_select("cuisine"),
            edu_phrase=phrase_pick("edu_phrase"),
        ),
        "yes_vi": "Có, chắc chắn. Tôi rất thích ẩm thực đa dạng vì giúp mở rộng kiến thức.",
        "yes_plain": "Yes, absolutely. I'm a big fan of cuisine from different cultures. This is because it helps me learn how to manage my diet better and make healthier choices.",
        "yes_ipa": "/jes ˌæbsəˈluːtli…/",
        "yes_ex": cui_yes_tpl,
        "no_html": cui_no_tpl.format(
            soft_dislike=phrase_pick("soft_dislike", 0),
            dislike_no_benefit=phrase_pick("dislike_no_benefit", 1),  # It doesn't help me relax
        ),
        "no_vi": "Không thực sự — món lạ không phải sở thích của tôi. Nó không giúp tôi thư giãn khi ăn ngoài.",
        "no_plain": "Well, not really — unfamiliar food isn't my cup of tea. It doesn't help me relax when I eat out.",
        "no_ipa": "/wel nɒt ˈrɪəli…/",
        "no_ex": cui_no_tpl,
    })

    # ── seafood ──
    sea_yes_tpl = (
        "Yes, absolutely. I enjoy eating {seafood} and {meat} because "
        "{phrase_food} with friends is a great way to unwind."
    )
    sea_no_tpl = (
        "No, not really — seafood {soft_dislike} and I'm worried it {allergy_risk}."
    )
    items.append({
        "q": "Do you like seafood?",
        "yes_html": sea_yes_tpl.format(
            seafood=slot_select("seafood"),
            meat=slot_select("meat"),
            phrase_food=phrase_pick("phrase_food"),
        ),
        "yes_vi": "Có, chắc chắn. Tôi thích hải sản — ăn cùng bạn bè là cách thư giãn tuyệt vời.",
        "yes_plain": "Yes, absolutely. I enjoy eating seafood and bacon because grab a bite with friends is a great way to unwind.",
        "yes_ipa": "/jes ˌæbsəˈluːtli…/",
        "yes_ex": sea_yes_tpl,
        "no_html": sea_no_tpl.format(
            soft_dislike=phrase_pick("soft_dislike", 0),
            allergy_risk=phrase_pick("allergy_risk", 0),
        ),
        "no_vi": "Không thực sự — hải sản không phải sở thích của tôi và tôi lo nó có thể gây dị ứng.",
        "no_plain": "No, not really — seafood isn't my cup of tea and I'm worried it can lead to allergies.",
        "no_ipa": "/nəʊ nɒt ˈrɪəli…/",
        "no_ex": sea_no_tpl,
    })

    # ── busy kitchen ──
    kit_yes_tpl = (
        "Yes, absolutely. Working in a busy kitchen {job_benefit} and "
        "I also get the opportunity to push myself every day."
    )
    kit_no_tpl = (
        "Well, not really because my job is quite boring. {dislike_no_benefit}. "
        "I {dislike_duty} and the same {kitchen_tool} every day."
    )
    # dislike_duty already has "have to deal with the same tasks every day" - "and the same blender" is redundant
    kit_no_tpl = (
        "Well, not really because my job is quite boring. {dislike_no_benefit}. "
        "I have to deal with the same tasks and the same {kitchen_tool} every day."
    )
    items.append({
        "q": "Do you like your job in a busy kitchen?",
        "yes_html": kit_yes_tpl.format(job_benefit=phrase_pick("job_benefit", 0)),
        "yes_vi": "Có, chắc chắn. Làm bếp bận rộn cho tôi cơ hội thử thách bản thân và đẩy mình mỗi ngày.",
        "yes_plain": "Yes, absolutely. Working in a busy kitchen gives me the chance to challenge myself and I also get the opportunity to push myself every day.",
        "yes_ipa": "/jes ˌæbsəˈluːtli…/",
        "yes_ex": kit_yes_tpl,
        "no_html": kit_no_tpl.format(
            dislike_no_benefit=phrase_pick("dislike_no_benefit", 0),
            kitchen_tool=slot_select("kitchen_tool"),
        ),
        "no_vi": "Không thực sự thích — công việc nhàm, lặp lại mỗi ngày với cùng một dụng cụ.",
        "no_plain": "Well, not really because my job is quite boring. It doesn't give me the chance to try anything new. I have to deal with the same tasks and the same blender every day.",
        "no_ipa": "/wel nɒt ˈrɪəli…/",
        "no_ex": kit_no_tpl,
    })

    # ── spicy food (Favourite · food lexical only — no job_benefit) ──
    spicy_yes_tpl = (
        "Yes, absolutely. I'm a big fan of spicy dishes because {food_taste_reason}. "
        "Trying new spices also {food_benefit}."
    )
    spicy_no_tpl = (
        "No, I'm not keen on spicy dishes. I hardly ever {hardly_ever_action} because they "
        "{food_health_threat}. I prefer {prefer_rather_than}."
    )
    items.append({
        "q": "Do you like spicy food?",
        "yes_html": spicy_yes_tpl.format(
            food_taste_reason=phrase_pick("food_taste_reason", 0),
            food_benefit=phrase_pick("food_benefit", 0),
        ),
        "yes_vi": "Có, chắc chắn. Tôi rất thích món cay vì chúng đánh thức vị giác. Thử gia vị mới cũng giúp khám phá hương vị mới.",
        "yes_plain": "Yes, absolutely. I'm a big fan of spicy dishes because they wake up my taste buds. Trying new spices also helps me explore new flavours.",
        "yes_ipa": "/jes ˌæbsəˈluːtli…/",
        "yes_ex": spicy_yes_tpl,
        "no_html": spicy_no_tpl.format(
            hardly_ever_action=phrase_pick("hardly_ever_action", 2),
            food_health_threat=phrase_pick("food_health_threat", 0),
            prefer_rather_than=phrase_pick("prefer_rather_than", 2),
        ),
        "no_vi": "Không, tôi không thích các món cay. Tôi hiếm khi ăn chúng vì chúng gây đe dọa đến sức khỏe. Tôi thích món dịu hơn món cay.",
        "no_plain": "No, I'm not keen on spicy dishes. I hardly ever eat spicy dishes because they pose a threat to my health. I prefer to have mild dishes rather than spicy food.",
        "no_ipa": "/nəʊ aɪm nɒt kiːn ɒn ˈspaɪsi ˈdɪʃɪz…/",
        "no_ex": spicy_no_tpl,
        "notes": [
            "I hardly ever + V",
            "pose a threat to (my) health",
            "prefer to V rather than V",
        ],
    })

    # ── eating out (Favourite · prefer … rather than …) ──
    eat_out_yes_tpl = (
        "Yes, occasionally. Dining out with friends is {social_benefit}. "
        "Still, most days I prefer {prefer_rather_than} because it's healthier."
    )
    eat_out_no_tpl = (
        "No, not really. I hardly ever {hardly_ever_action} because it's expensive "
        "and not always good for my health. I prefer {prefer_rather_than}."
    )
    items.append({
        "q": "Do you like eating out?",
        "yes_html": eat_out_yes_tpl.format(
            social_benefit=phrase_pick("social_benefit", 1),
            prefer_rather_than=phrase_pick("prefer_rather_than", 3),
        ),
        "yes_vi": "Có, thỉnh thoảng. Ăn ngoài với bạn là cách thư giãn tuyệt. Nhưng hầu hết ngày tôi vẫn thích đồ nấu nhà hơn ăn ngoài vì lành mạnh hơn.",
        "yes_plain": "Yes, occasionally. Dining out with friends is a great way to unwind with friends. Still, most days I prefer home-cooked food rather than eating out because it's healthier.",
        "yes_ipa": "/jes əˈkeɪʒənəli…/",
        "yes_ex": eat_out_yes_tpl,
        "no_html": eat_out_no_tpl.format(
            hardly_ever_action=phrase_pick("hardly_ever_action", 4),
            prefer_rather_than=phrase_pick("prefer_rather_than", 0),
        ),
        "no_vi": "Không thực sự. Tôi hiếm khi ăn ngoài vì đắt và không phải lúc nào cũng tốt cho sức khỏe. Tôi thích nấu ở nhà hơn là ăn ngoài.",
        "no_plain": "No, not really. I hardly ever eat out because it's expensive and not always good for my health. I prefer to cook at home rather than eat out.",
        "no_ipa": "/nəʊ nɒt ˈrɪəli · aɪ ˈhɑːdli ˈevə iːt aʊt…/",
        "no_ex": eat_out_no_tpl,
        "notes": ["I hardly ever + V", "prefer … rather than …"],
    })

    cards = []
    for it in items:
        cards.append(
            f"""          <article class="lr-food-ex-card">
            <p class="lr-food-ex-q">{esc(it["q"])}</p>
            <div class="lr-food-ex-pair">
{_pair_answer_html(kind="yes", en_html=it["yes_html"], vi=it["yes_vi"], plain=it["yes_plain"], ipa=it["yes_ipa"], q=it["q"], ex_en=it.get("yes_ex", ""))}
{_pair_answer_html(kind="no", en_html=it["no_html"], vi=it["no_vi"], plain=it["no_plain"], ipa=it["no_ipa"], q=it["q"], ex_en=it.get("no_ex", ""))}
            </div>
{_ex_chip_notes_html(it.get("notes"))}
          </article>"""
        )
    return f"""
        <div class="lr-food-examples" id="food-examples">
          <h3 class="lr-core-subtitle">Ví dụ Food · Thích / Không thích</h3>
          <p class="lr-mm-hint">Mỗi câu hỏi có <strong>Thích / Không thích</strong> + dropdown. Chip dưới card = cấu trúc đặc biệt trong câu (vd. <code>hardly ever</code>).</p>
{chr(10).join(cards)}
        </div>"""


def _lesson2_practice_html(*, open_attr: str = "") -> str:
    """Lesson 2 practice — Thích + Không thích đều có dropdown ngữ cảnh."""
    home_yes_tpl = (
        "I think because it's a great way to {relax_phrase} — especially when they're tired after work. "
        "{relax_followup}"
    )
    home_no_tpl = (
        "Well, some people don't enjoy home-cooked meals because cooking {dislike_feel} "
        "and they {dislike_duty}."
    )
    # dislike_feel has "makes me exhausted" and "makes them exhausted" - for "cooking makes them..." use index 3
    home_yes = home_yes_tpl.format(
        relax_phrase=phrase_pick("relax_phrase"),
        relax_followup=phrase_pick("relax_followup", 0),
    )
    home_no = home_no_tpl.format(
        dislike_feel=phrase_pick("dislike_feel", 3),
        dislike_duty=phrase_pick("dislike_duty", 0),
    )

    read_yes_tpl = (
        "Yes, because it helps me {edu_phrase}. "
        "It also gives me the chance to enrich my knowledge."
    )
    read_no_tpl = (
        "No, not really — reading about nutrition {soft_dislike} because {dislike_no_benefit}."
    )
    # "because It doesn't help me relax" - capital I is ok mid sentence if we lowercase - the forms start with It
    # Change template to avoid double subject: "because {soft reason without It}"
    # Better soft_dislike + separate: "because it doesn't help me relax" as full phrase slot
    read_no_tpl = (
        "No, not really — reading about nutrition {soft_dislike}. {dislike_no_benefit}."
    )
    read_yes = read_yes_tpl.format(edu_phrase=phrase_pick("edu_phrase"))
    read_no = read_no_tpl.format(
        soft_dislike=phrase_pick("soft_dislike", 0),
        dislike_no_benefit=phrase_pick("dislike_no_benefit", 1),
    )

    veg_yes_tpl = (
        "Yes, because it's a great way to {health_phrase}. "
        "{health_followup}"
    )
    veg_no_tpl = (
        "No, not really — plain vegetables {soft_dislike} and {taste_complaint}."
    )
    veg_yes = veg_yes_tpl.format(
        health_phrase=phrase_pick("health_phrase"),
        health_followup=phrase_pick("health_followup", 0),
    )
    veg_no = veg_no_tpl.format(
        soft_dislike=phrase_pick("soft_dislike", 0),
        taste_complaint=phrase_pick("taste_complaint", 2),
    )

    cards = f"""
            <div class="lr-practice-source" id="lesson2-practice">
              <article class="lr-food-ex-card">
                <p class="lr-food-ex-q">Why do people like home-cooked meals?</p>
                <div class="lr-food-ex-pair">
{_pair_answer_html(kind="yes", en_html=home_yes, vi="Tôi nghĩ vì đó là cách tuyệt vời để thư giãn — nhất là khi mệt sau giờ làm. Ở trong bếp cũng giúp tạm quên áp lực công việc.", plain="I think because it's a great way to unwind and recharge their batteries — especially when they're tired after work. Being in the kitchen also helps them temporarily forget all the pressures from their work.", ipa="/aɪ θɪŋk bɪˈkɒz ɪts ə ɡreɪt weɪ tuː…/", q="Why do people like home-cooked meals?", ex_en=home_yes_tpl)}
{_pair_answer_html(kind="no", en_html=home_no, vi="Một số người không thích nấu ở nhà vì việc nấu khiến họ kiệt sức và phải làm những việc lặp lại mỗi ngày.", plain="Well, some people don't enjoy home-cooked meals because cooking makes them exhausted and they have to deal with the same tasks every day.", ipa="/wel səm ˈpiːpl…/", q="Why do people like home-cooked meals?", ex_en=home_no_tpl)}
                </div>
              </article>
              <article class="lr-food-ex-card">
                <p class="lr-food-ex-q">Do you like reading about food &amp; nutrition?</p>
                <div class="lr-food-ex-pair">
{_pair_answer_html(kind="yes", en_html=read_yes, vi="Có, vì nó giúp tôi học cách quản lý chế độ ăn tốt hơn. Cũng cho tôi cơ hội làm giàu kiến thức.", plain="Yes, because it helps me learn how to manage my diet better and make healthier choices. It also gives me the chance to enrich my knowledge.", ipa="/jes bɪˈkɒz ɪt helps miː…/", q="Do you like reading about food & nutrition?", ex_en=read_yes_tpl)}
{_pair_answer_html(kind="no", en_html=read_no, vi="Không thực sự — đọc về dinh dưỡng không phải sở thích của tôi vì nó không giúp tôi thư giãn.", plain="No, not really — reading about nutrition isn't my cup of tea. It doesn't help me relax.", ipa="/nəʊ nɒt ˈrɪəli…/", q="Do you like reading about food & nutrition?", ex_en=read_no_tpl)}
                </div>
              </article>
              <article class="lr-food-ex-card">
                <p class="lr-food-ex-q">Do you like eating vegetables?</p>
                <div class="lr-food-ex-pair">
{_pair_answer_html(kind="yes", en_html=veg_yes, vi="Có, vì đó là cách tuyệt vời để giữ khỏe và phòng bệnh. Nó cũng giúp tăng cơ bắp.", plain="Yes, because it's a great way to stay healthy and prevent various health problems. It also helps them strengthen their muscles.", ipa="/jes bɪˈkɒz ɪts ə ɡreɪt weɪ tuː…/", q="Do you like eating vegetables?", ex_en=veg_yes_tpl)}
{_pair_answer_html(kind="no", en_html=veg_no, vi="Không thực sự — rau nhạt không phải sở thích của tôi và không giúp tôi thưởng thức bữa ăn.", plain="No, not really — plain vegetables aren't my cup of tea and they don't help me enjoy my meals.", ipa="/nəʊ nɒt ˈrɪəli…/", q="Do you like eating vegetables?", ex_en=veg_no_tpl)}
                </div>
              </article>
            </div>"""
    return f"""
          <details class="lr-formula-details"{open_attr}>
            <summary>Thực hành · Giải trí / Giáo dục / Sức khỏe</summary>
            <p class="lr-mm-hint">Cùng format hình 1: <strong>Thích</strong> và <strong>Không thích</strong> đều có dropdown (đổi cụm lý do Lesson 2). Hover cả đoạn → 1 tooltip VI.</p>
{cards}
          </details>
{lesson_scroll_read_html("lesson2", title="Lesson 2", source_sel="#lesson2-practice")}"""


def _g_mark(text: str) -> str:
    """Pill highlight for a grammar chunk (Hình 2)."""
    return f"<mark>{esc(text)}</mark>"


def _g_alts(*options: str) -> str:
    """Vertical choice stack — Hình 3 (would have to be / go for / opt for)."""
    items = "".join(f"<span>{esc(o)}</span>" for o in options)
    return f'<span class="lr-g-alts" aria-label="choose one">{items}</span>'


def lesson_grammar_notes_html(title: str, skeleton_lines: list[str]) -> str:
    """Grammar notes after mind map — general patterns only."""
    body = "\n".join(f'            <p class="lr-g-skel-line">{line}</p>' for line in skeleton_lines)
    return f"""
          <div class="lr-grammar-notes">
            <h4 class="lr-grammar-notes-title">Grammar notes · {esc(title)}</h4>
            <div class="lr-g-skel">
{body}
            </div>
          </div>"""


def lesson_highlights_html(
    *,
    map_suffix: str = "",
    include_food_examples: bool = False,
    open_practice: bool = False,
) -> str:
    """Lesson 2 + 3 + 5 + 6 mind maps and practice (Lesson 4 skipped).

    map_suffix: unique id suffix when the same maps appear on Review Exercise 2.
    include_food_examples: annotated Food cards (Review Exercise 2).
    open_practice: expand Lesson 2 dropdown practice by default.
    """
    m2 = f"lesson2Mindmap{map_suffix}"
    m3 = f"lesson3Mindmap{map_suffix}"
    m5 = f"lesson5Mindmap{map_suffix}"
    m6 = f"lesson6Mindmap{map_suffix}"
    open_attr = " open" if open_practice else ""
    examples_block = food_lesson_examples_html() if include_food_examples else ""
    examples_l5 = food_lesson5_examples_html() if include_food_examples else ""
    examples_l6 = food_lesson6_examples_html() if include_food_examples else ""
    lesson3_scroll = ""
    lesson5_scroll = ""
    lesson6_scroll = ""
    if include_food_examples:
        lesson3_scroll = lesson_scroll_read_html(
            "lesson3", title="Lesson 3", source_sel="#lesson3-scroll-source"
        )
        lesson5_scroll = lesson_scroll_read_html(
            "lesson5", title="Lesson 5", source_sel="#lesson5-scroll-source"
        )
        lesson6_scroll = lesson_scroll_read_html(
            "lesson6", title="Lesson 6", source_sel="#lesson6-scroll-source"
        )

    g2 = lesson_grammar_notes_html(
        "Lesson 2",
        [
            f'{_g_mark("I love / enjoy")} + V-ing {_g_mark("because")} it\'s + adj.',
            f'{_g_alts("It helps me + V", "It\'s a great way to + V", "It gives me the chance to + V", "I also get the opportunity to + V")}',
            f'NO: {_g_mark("I don\'t like")} + V-ing '
            f'{_g_alts("because + S + V", "because of + NP")}. '
            f'{_g_mark("can lead to")} …',
        ],
    )
    g3 = lesson_grammar_notes_html(
        "Lesson 3",
        [
            f'{_g_alts("Yes, definitely", "Yes, absolutely")}. '
            f'{_g_alts("I like / love / enjoy + V-ing", "I\'m keen on …", "I\'m a big fan of …")}',
            f'{_g_alts("This is because + S + V", "because of + NP")}',
            f'{_g_alts("No, definitely not", "No, not really")}. '
            f'{_g_alts("I don\'t enjoy + V-ing", "I\'m not keen on …")}',
        ],
    )
    g5 = lesson_grammar_notes_html(
        "Lesson 5",
        [
            f'Well, I love all kinds of + sth, but if I had to choose one, it '
            f'{_g_alts("would have to be", "would go for", "I would opt for")} …',
            f'{_g_alts("This is because + S + V", "because of + NP")}',
        ],
    )
    g6 = lesson_grammar_notes_html(
        "Lesson 6",
        [
            f'{_g_alts("I prefer X", "I prefer X to Y", "I prefer X rather than Y")} '
            f'{_g_mark("because")} + ưu điểm của X.',
            f'{_g_alts("while + nhược điểm của Y", "whereas + nhược điểm của Y")}',
        ],
    )

    return f"""
      <div class="lr-core-lessons">

        <article class="lr-core-lesson" id="lesson2-formulas">
          <header class="lr-core-lesson-head">
            <h3>Lesson 2 · Reasons like / dislike</h3>
          </header>

{mind_map_html(
            m2,
            "Lesson 2 · Reasons like / dislike",
            "Reasons",
            "Dislike ↔ Like",
            LESSON2_MINDMAP_LEFT,
            LESSON2_MINDMAP_RIGHT,
            note="Trái = <strong>KHÔNG THÍCH</strong> · Phải = <strong>THÍCH</strong>.",
            extra_class=" lr-mmap--lesson2",
            min_width="1280px",
        )}
{g2}
{_lesson2_practice_html(open_attr=open_attr)}
        </article>

        <article class="lr-core-lesson" id="lesson3-formulas">
          <header class="lr-core-lesson-head">
            <h3>Lesson 3 · Do you like X?</h3>
          </header>

{mind_map_html(
            m3,
            "Lesson 3 · Do you like X?",
            "Do you like X?",
            "No ↔ Yes + Reasons",
            LESSON3_MINDMAP_LEFT,
            LESSON3_MINDMAP_RIGHT,
            note="Trái = <strong>NO</strong> · Phải = <strong>YES</strong> + Reasons.",
            extra_class=" lr-mmap--lesson3",
            min_width="1200px",
        )}
{g3}
          <div id="lesson3-scroll-source">
{examples_block}
          </div>

{lesson3_scroll}
        </article>

        <article class="lr-core-lesson" id="lesson5-formulas">
          <header class="lr-core-lesson-head">
            <h3>Lesson 5 · What kind of X do you like most?</h3>
          </header>

{mind_map_html(
            m5,
            "Lesson 5 · What kind of X do you like most?",
            "What kind of X?",
            "Loại gì? ↔ Lý do",
            LESSON5_MINDMAP_LEFT,
            LESSON5_MINDMAP_RIGHT,
            note="Trái = <strong>Loại gì?</strong> · Phải = <strong>Lý do</strong> + Lexical Food.",
            extra_class=" lr-mmap--lesson5",
            min_width="1200px",
        )}
{g5}
          <div id="lesson5-scroll-source">
{examples_l5}
          </div>

{lesson5_scroll}
        </article>

        <article class="lr-core-lesson" id="lesson6-formulas">
          <header class="lr-core-lesson-head">
            <h3>Lesson 6 · Do you prefer X or Y?</h3>
          </header>

{mind_map_html(
            m6,
            "Lesson 6 · Do you prefer X or Y?",
            "Do you prefer X or Y?",
            "Chọn ↔ Lý do",
            LESSON6_MINDMAP_LEFT,
            LESSON6_MINDMAP_RIGHT,
            note="Trái = <strong>prefer X / X to Y / rather than</strong> · Phải = lý do + cấu trúc slide.",
            extra_class=" lr-mmap--lesson6",
            min_width="1200px",
        )}
{g6}
          <div id="lesson6-scroll-source">
{examples_l6}
          </div>

{lesson6_scroll}
        </article>

      </div>"""


FOOD_LANG_GROUPS = [
    (
        "Idioms",
        "Thành ngữ cố định — tăng Lexical Resource nếu dùng đúng ngữ cảnh",
        [
            "idiom_taste",
            "idiom_ease",
            "idiom_enjoy",
            "idiom_social",
            "idiom_health",
        ],
    ),
    (
        "Phrases",
        "Cụm từ thông dụng — tự nhiên hơn idiom, vẫn ghi điểm vocabulary",
        ["phrase_food"],
    ),
    (
        "Slang & informal",
        "Thân mật — dùng 1–2 lần trong Part 1 cho tự nhiên, tránh lạm dụng",
        ["slang_food"],
    ),
]

def food_lang_html() -> str:
    cards = []
    for title, hint, slot_ids in FOOD_LANG_GROUPS:
        items = []
        for sid in slot_ids:
            for o in WORD_SLOTS[sid]:
                items.append(
                    f'<li><mark class="lr-idiom-mark">{esc(o["form"])}</mark>'
                    f' <span class="lr-idiom-vi">— {esc(o["vi"])}</span></li>'
                )
        extra = ""
        if title == "Phrases":
            extra = ' lr-idiom-card--phrases'
        cards.append(
            f"""        <article class="lr-idiom-card{extra}">
          <h3>{esc(title)}</h3>
          <p class="lr-idiom-hint">{esc(hint)}</p>
          <ul class="lr-idiom-list">{"".join(items)}</ul>
        </article>"""
        )

    # practice sentence with dropdowns
    practice = (
        f'When friends ask about my diet, I admit I\'m {idiom_pick("idiom_taste", 1)} — '
        f'but cooking at home is {idiom_pick("idiom_ease", 0)} once you practise. '
        f'On Friday I might {idiom_pick("slang_food")} or {idiom_pick("phrase_food", 1)} with colleagues. '
        f'Good {idiom_pick("phrase_food", 3)} should {idiom_pick("idiom_enjoy", 0)}; '
        f'that\'s {idiom_pick("idiom_enjoy", 3)} when you travel.'
    )

    phrase_drills = food_phrase_drills_html()

    return (
        "\n".join(cards)
        + phrase_drills
        + f"""
        <div class="lr-idiom-practice">
          <p class="lr-chain-ex-label">Try combining (dropdown)</p>
          <p class="lr-idiom-practice-text">{practice}</p>
          <p class="lr-ref">Nguồn: <a href="https://langgo.edu.vn/food-idioms-thanh-ngu-ve-do-an-tieng-anh" target="_blank" rel="noopener noreferrer">LangGo — 70+ Food idioms</a> · Ôn ở đây trước — áp dụng vào mock test khi đã quen.</p>
        </div>"""
    )


def food_phrase_drills_html() -> str:
    """Example chunks for each Phrases item × Lesson-3 speaking frames."""
    drills = [
        {
            "form": "grab a bite",
            "vi": "ăn vội một miếng",
            "frame": "Whenever I have free time, I really love to + V · because it helps me unwind",
            "tense": "Present Simple · habit",
            "en": (
                "Whenever I have free time, I really love to "
                "<mark class=\"vocab\">grab a bite</mark> with friends because it helps me unwind."
            ),
            "vi_ex": "Mỗi khi rảnh, tôi rất thích ăn vội với bạn vì nó giúp tôi thư giãn.",
        },
        {
            "form": "grab a bite",
            "vi": "ăn vội một miếng",
            "frame": "It gives me the chance to + V",
            "tense": "Present Simple",
            "en": (
                "A short lunch break gives me the chance to "
                "<mark class=\"vocab\">grab a bite</mark> near the office without wasting time."
            ),
            "vi_ex": "Giờ nghỉ trưa ngắn cho tôi cơ hội ăn vội gần công ty mà không mất nhiều thời gian.",
        },
        {
            "form": "dine out",
            "vi": "ăn ngoài",
            "frame": "I'm a big fan of + V-ing · It gives me the chance to + V",
            "tense": "Present Simple · opinion",
            "en": (
                "To be honest, I'm a big fan of <mark class=\"vocab\">dining out</mark> on Friday nights "
                "because it gives me the chance to try new restaurants."
            ),
            "vi_ex": "Thành thật thì tôi rất thích ăn ngoài tối Thứ Sáu vì có cơ hội thử quán mới.",
        },
        {
            "form": "dine out",
            "vi": "ăn ngoài",
            "frame": "I don't think … · soft no",
            "tense": "Present Simple · soft no",
            "en": (
                "I don't think we should <mark class=\"vocab\">dine out</mark> every night — "
                "it's not practical for my budget."
            ),
            "vi_ex": "Tôi không nghĩ nên ăn ngoài mỗi tối — không thực tế với túi tiền của tôi.",
        },
        {
            "form": "treat yourself",
            "vi": "tự thưởng cho bản thân",
            "frame": "To be honest · I love to + V · It's + relaxing",
            "tense": "Present Simple · opinion",
            "en": (
                "To be honest, I love to <mark class=\"vocab\">treat myself</mark> to dessert "
                "after a tough week — it's so relaxing."
            ),
            "vi_ex": "Thành thật thì tôi thích tự thưởng dessert sau tuần mệt — rất thư giãn.",
        },
        {
            "form": "treat yourself",
            "vi": "tự thưởng cho bản thân",
            "frame": "It helps me + V",
            "tense": "Present Simple",
            "en": (
                "Knowing I can <mark class=\"vocab\">treat myself</mark> once in a while "
                "helps me stay motivated on a healthy diet."
            ),
            "vi_ex": "Biết mình thỉnh thoảng được tự thưởng giúp tôi giữ động lực khi ăn uống lành mạnh.",
        },
        {
            "form": "comfort food",
            "vi": "đồ ăn an ủi",
            "frame": "I think … · It's + relaxing · It helps me + V",
            "tense": "Present Simple · opinion",
            "en": (
                "I think a bowl of <mark class=\"vocab\">comfort food</mark> after a long day "
                "is so relaxing — it helps me forget work stress for a while."
            ),
            "vi_ex": "Tôi nghĩ một tô comfort food sau ngày dài rất thư giãn — giúp tôi tạm quên stress công việc.",
        },
        {
            "form": "comfort food",
            "vi": "đồ ăn an ủi",
            "frame": "I'm keen on + N",
            "tense": "Present Simple · habit",
            "en": (
                "I'm keen on simple <mark class=\"vocab\">comfort food</mark> like rice and soup "
                "when the weather turns cold."
            ),
            "vi_ex": "Tôi thích comfort food đơn giản như cơm với canh khi trời trở lạnh.",
        },
        {
            "form": "guilty pleasure",
            "vi": "thú thích tội lỗi",
            "frame": "To be honest · I don't think … · soft admission",
            "tense": "Present Simple · opinion",
            "en": (
                "To be honest, late-night snacks are my <mark class=\"vocab\">guilty pleasure</mark> — "
                "I don't think it's perfect, but I enjoy it sometimes."
            ),
            "vi_ex": "Thành thật thì snack khuya là guilty pleasure của tôi — không hoàn hảo, nhưng thỉnh thoảng vẫn thích.",
        },
        {
            "form": "guilty pleasure",
            "vi": "thú thích tội lỗi",
            "frame": "It's not my cup of tea · contrast",
            "tense": "Present Simple · contrast",
            "en": (
                "Fancy desserts are not my cup of tea, but ice cream is still a "
                "<mark class=\"vocab\">guilty pleasure</mark> I can't stand giving up."
            ),
            "vi_ex": "Bánh ngọt sang chảnh không hợp gu tôi, nhưng kem vẫn là guilty pleasure tôi không bỏ được.",
        },
        {
            "form": "home-cooked meal",
            "vi": "bữa ăn nấu ở nhà",
            "frame": "I'm keen on + N · It helps me + V · I also get the opportunity to + V",
            "tense": "Present Simple · habit",
            "en": (
                "I'm keen on a <mark class=\"vocab\">home-cooked meal</mark> most evenings "
                "because it helps me eat healthier, and I also get the opportunity to practise cooking."
            ),
            "vi_ex": "Tôi thích bữa ăn nấu ở nhà hầu hết các tối vì giúp ăn lành hơn, và cũng có cơ hội luyện nấu ăn.",
        },
        {
            "form": "home-cooked meal",
            "vi": "bữa ăn nấu ở nhà",
            "frame": "What I like most about … is that … · It's + interesting",
            "tense": "Present Simple · opinion",
            "en": (
                "What I like most about a <mark class=\"vocab\">home-cooked meal</mark> "
                "is that it always gives me a warm, interesting experience with family."
            ),
            "vi_ex": "Điều tôi thích nhất ở bữa ăn nấu ở nhà là nó luôn mang lại trải nghiệm ấm áp, thú vị với gia đình.",
        },
    ]

    def _role_of(frame: str) -> str:
        f = frame.lower()
        if "avoid" in f:
            return "ket"
        if any(
            x in f
            for x in (
                "helps me",
                "chance to",
                "opportunity",
                "can lead",
                "it's +",
                "relaxing",
                "interesting",
                "entertaining",
                "what i like",
            )
        ):
            return "than"
        if any(
            x in f
            for x in (
                "keen on",
                "big fan",
                "i love",
                "i think",
                "don't think",
                "don't like",
                "can't stand",
                "cup of tea",
                "to be honest",
            )
        ):
            return "mo"
        return "than"

    cards = []
    for d in drills:
        role = d.get("role") or _role_of(d["frame"])
        role_label = {"mo": "Mở", "than": "Thân", "ket": "Kết"}.get(role, "Thân")
        role_cls = {"mo": "open", "than": "body", "ket": "close"}.get(role, "body")
        cards.append(
            f"""          <article class="lr-phrase-card lr-idiom-ex-card lr-phrase-card--{role_cls}">
            <div class="lr-phrase-meta">
              <span class="lr-role-tag lr-role-tag--{role_cls}">{role_label}</span>
              <mark class="vocab">{esc(d["form"])}</mark>
              <span class="lr-phrase-vi-word">{esc(d["vi"])}</span>
              <span class="lr-tense-tag">{esc(d["tense"])}</span>
            </div>
            <p class="lr-phrase-frame"><code>{esc(d["frame"])}</code></p>
            <p class="lr-phrase-en">{d["en"]}</p>
            <p class="lr-phrase-vi">{esc(d["vi_ex"])}</p>
          </article>"""
        )

    return f"""
        <div class="lr-idiom-ex-block">
          <h3 class="lr-idiom-ex-title">Phrases · ví dụ theo khung câu</h3>
          <p class="lr-idiom-ex-hint">Mỗi cụm gắn vào <strong>1–2 khung Lesson 3</strong> — học thuộc cả câu, không học lemma đơn. Bật <strong>Vietnamese</strong> để xem bản dịch.</p>
          <div class="lr-phrase-grid">
{chr(10).join(cards)}
          </div>
        </div>"""


def food_phrase_mindmap_html() -> str:
    """Food-specific reasons mind map for §6 — structures + idea lists."""
    return f"""
        <div class="lr-food-phrase-map" id="food-phrase-map">
          <h3>Sơ đồ tư duy · Food — cấu trúc + cụm ý</h3>
          <p class="lr-section-hint">Nhìn tổng thể trước khi học thẻ: <strong>① Mở</strong> (thái độ) → <strong>because</strong> → <strong>② Thân</strong> (1–2 nhánh) → <strong>③ Kết</strong> (optional). Trái = không thích · Phải = thích. Các từ <mark class="vocab">vàng</mark> trùng với Phrase drills bên dưới.</p>
{mind_map_html(
            "foodPhraseMindmap",
            "Food · Reasons like / dislike",
            "Food",
            "Dislike ↔ Like",
            FOOD_PHRASE_MINDMAP_LEFT,
            FOOD_PHRASE_MINDMAP_RIGHT,
            note=(
                "Luồng: <strong>🕐 MỞ</strong> → <strong>because</strong> → <strong>Nhánh 1</strong> (It's + adj) "
                "hoặc <strong>Nhánh 2</strong> (helps / chance / can lead to). "
                "Chọn <strong>1 nhánh LIKE</strong> hoặc <strong>1 nhánh DISLIKE</strong> — không nhồi hết."
            ),
            extra_class=" lr-mmap--lesson2 lr-mmap--food-phrase",
            min_width="1320px",
        )}
          <div class="lr-mm-assemble">
            <p class="lr-mm-label">Ví dụ ráp nhanh (từ sơ đồ → đoạn)</p>
            <div class="lr-mm-assemble-grid">
              <p><span class="lr-mm-tag-yes">LIKE</span> Healthy: <em>To be honest, I'm keen on eating healthy food. Drinking a smoothie every morning helps me stay full — that's why I avoid sugary soft drinks.</em></p>
              <p><span class="lr-mm-tag-yes">LIKE</span> Enjoy: <em>Whenever I have free time, I love to grab a bite with friends because it helps me unwind. A home-cooked meal also gives me the chance to practise cooking.</em></p>
              <p><span class="lr-mm-tag-no">DISLIKE</span> Fast food: <em>Well, not really — greasy take-away every night is not my cup of tea. Consuming too much bacon can lead to a high salt intake, so I avoid it on weekdays.</em></p>
            </div>
          </div>
        </div>"""


def gold_phrase_drills_html() -> str:
    """Lesson-3 frames × Pareto 'Phải học' words — memorise whole chunks, not bare lemmas."""
    # form | vi | ipa | frame | tense | en | vi_ex
    drills: list[dict] = [
        # ── Positive reasons: helps / chance / opportunity ──
        {
            "form": "smoothie",
            "vi": "sinh tố",
            "ipa": "/ˈsmuːði/",
            "frame": "It helps me + V",
            "group": "yes",
            "role": "than",
            "tense": "Present Simple · habit",
            "en": "Drinking a <mark class=\"vocab\">smoothie</mark> every morning helps me stay full until lunch.",
            "vi_ex": "Uống một ly smoothie mỗi sáng giúp tôi no đến tận giờ trưa.",
        },
        {
            "form": "fruit salad",
            "vi": "salad trái cây",
            "ipa": "/fruːt ˈsæləd/",
            "frame": "It gives me the chance to + V",
            "group": "yes",
            "role": "than",
            "tense": "Present Simple",
            "en": "Making a <mark class=\"vocab\">fruit salad</mark> gives me the chance to add more vitamins to my diet.",
            "vi_ex": "Làm salad trái cây cho tôi cơ hội bổ sung thêm vitamin vào chế độ ăn.",
        },
        {
            "form": "plant-based",
            "vi": "thuần chay",
            "ipa": "/ˈplæntˌbeɪst/",
            "frame": "I also get the opportunity to + V",
            "group": "yes",
            "role": "than",
            "tense": "Present Continuous",
            "en": "These days I'm following a <mark class=\"vocab\">plant-based</mark> diet, so I also get the opportunity to try new recipes every week.",
            "vi_ex": "Dạo này tôi đang theo chế độ plant-based, nên cũng có cơ hội thử công thức mới mỗi tuần.",
        },
        {
            "form": "nutrition",
            "vi": "dinh dưỡng",
            "ipa": "/nuˈtrɪʃən/",
            "frame": "It helps me + V",
            "group": "yes",
            "role": "than",
            "tense": "Present Perfect Continuous",
            "en": "I've been paying more attention to <mark class=\"vocab\">nutrition</mark> lately because it helps me feel more energetic at work.",
            "vi_ex": "Gần đây tôi chú ý hơn đến dinh dưỡng vì nó giúp tôi thấy nhiều năng lượng hơn khi làm việc.",
        },
        {
            "form": "garlic",
            "vi": "tỏi",
            "ipa": "/ˈɡɑrlɪk/",
            "frame": "It helps me + V",
            "group": "yes",
            "role": "than",
            "tense": "Present Simple",
            "en": "Cooking with <mark class=\"vocab\">garlic</mark> helps me add flavour without using too much salt.",
            "vi_ex": "Nấu với tỏi giúp tôi tăng hương vị mà không cần nhiều muối.",
        },
        {
            "form": "mineral water",
            "vi": "nước khoáng",
            "ipa": "/ˈmɪnərəl ˌwɔtɚ/",
            "frame": "It helps me + V",
            "group": "yes",
            "role": "than",
            "tense": "Present Simple · habit",
            "en": "Keeping a bottle of <mark class=\"vocab\">mineral water</mark> on my desk helps me drink more water throughout the day.",
            "vi_ex": "Để sẵn một chai nước khoáng trên bàn giúp tôi uống nhiều nước hơn trong ngày.",
        },
        # ── It's + adj ──
        {
            "form": "pancake",
            "vi": "bánh kếp",
            "ipa": "/pænkeɪk/",
            "frame": "It's + interesting / relaxing …",
            "group": "adj",
            "role": "than",
            "tense": "Present Simple",
            "en": "Making homemade <mark class=\"vocab\">pancake</mark>s with fresh berries on Sunday is always interesting for me.",
            "vi_ex": "Làm bánh kếp homemade với quả mọng tươi vào Chủ nhật luôn thú vị với tôi.",
        },
        {
            "form": "cheesecake",
            "vi": "bánh phô mai",
            "ipa": "/ˈtʃiːzˌkeɪk/",
            "frame": "It's + relaxing",
            "group": "adj",
            "role": "than",
            "tense": "Present Simple",
            "en": "Having a small slice of <mark class=\"vocab\">cheesecake</mark> after a long day is so relaxing.",
            "vi_ex": "Ăn một miếng cheesecake nhỏ sau ngày dài thật sự rất thư giãn.",
        },
        {
            "form": "oyster",
            "vi": "hàu",
            "ipa": "/ˈɔɪstɚ/",
            "frame": "It's + exciting / thrilling",
            "group": "adj",
            "role": "than",
            "tense": "Past Simple",
            "en": "Trying <mark class=\"vocab\">oyster</mark> for the first time was exciting, though I was a bit nervous.",
            "vi_ex": "Lần đầu thử hàu khá hồi hộp, dù lúc đó tôi hơi lo.",
        },
        {
            "form": "cocktail",
            "vi": "cocktail",
            "ipa": "/ˈkɑkˌteɪl/",
            "frame": "It's + entertaining",
            "group": "adj",
            "role": "than",
            "tense": "Present Simple · can",
            "en": "Mixing a <mark class=\"vocab\">nonalcoholic</mark> <mark class=\"vocab\">cocktail</mark> at home can be quite entertaining with friends.",
            "vi_ex": "Pha cocktail không cồn ở nhà với bạn bè có thể khá vui.",
        },
        {
            "form": "nonalcoholic",
            "vi": "không cồn",
            "ipa": "/ˌnɑnˌælkəˈhɑlɪk/",
            "frame": "It's + interesting",
            "group": "adj",
            "role": "than",
            "tense": "Present Perfect",
            "en": "I've tried a few <mark class=\"vocab\">nonalcoholic</mark> options lately, and it's more interesting than I expected.",
            "vi_ex": "Gần đây tôi đã thử vài lựa chọn không cồn, thú vị hơn tôi nghĩ.",
        },
        # ── Like / keen on / I think / I love ──
        {
            "form": "citrus",
            "vi": "trái cây có múi",
            "ipa": "/ˈsɪtrəs/",
            "frame": "I'm keen on + N / V-ing",
            "group": "like",
            "role": "mo",
            "tense": "Present Simple · opinion",
            "en": "To be honest, I'm keen on eating healthy food, so <mark class=\"vocab\">citrus</mark> fruit is always my top choice for breakfast.",
            "vi_ex": "Thành thật mà nói, tôi khá thích ăn lành mạnh, nên trái cây có múi luôn là lựa chọn hàng đầu cho bữa sáng.",
        },
        {
            "form": "bacon",
            "vi": "thịt xông khói",
            "ipa": "/ˈbeɪkən/",
            "frame": "I love this · I love + N",
            "group": "like",
            "role": "mo",
            "tense": "Present Simple · habit",
            "en": "I love crispy <mark class=\"vocab\">bacon</mark> with eggs on Sunday mornings.",
            "vi_ex": "Tôi thích bacon giòn kèm trứng vào sáng Chủ nhật.",
        },
        {
            "form": "cheeseburger",
            "vi": "bánh mì kẹp thịt phô mai",
            "ipa": "/ˈtʃiːzˌbɝːɡɚ/",
            "frame": "I think …",
            "group": "like",
            "role": "mo",
            "tense": "Present Simple · opinion",
            "en": "I think a classic <mark class=\"vocab\">cheeseburger</mark> tastes better when the meat is juicy and the bun is soft.",
            "vi_ex": "Tôi nghĩ một chiếc cheeseburger cổ điển ngon hơn khi thịt mọng nước và bánh mềm.",
        },
        {
            "form": "macadamia nut",
            "vi": "hạt mắc ca",
            "ipa": "/ˌmækəˈdeɪmiə ˈnʌt/",
            "frame": "I'm keen on + V-ing",
            "group": "like",
            "role": "mo",
            "tense": "Present Simple",
            "en": "I'm keen on snacking on <mark class=\"vocab\">macadamia nut</mark>s instead of chips.",
            "vi_ex": "Tôi thích ăn vặt hạt mắc ca thay vì snack.",
        },
        {
            "form": "tangerine",
            "vi": "quýt",
            "ipa": "/ˌtændʒəˈrin/",
            "frame": "I love + V-ing",
            "group": "like",
            "role": "mo",
            "tense": "Present Simple · habit",
            "en": "I love peeling a sweet <mark class=\"vocab\">tangerine</mark> after lunch — it's my little reset.",
            "vi_ex": "Tôi thích bóc một quả quýt ngọt sau bữa trưa — kiểu reset nhỏ của mình.",
        },
        {
            "form": "ripe",
            "vi": "chín",
            "ipa": "/raɪp/",
            "frame": "I think …",
            "group": "like",
            "role": "mo",
            "tense": "Present Simple · opinion",
            "en": "I think choosing <mark class=\"vocab\">ripe</mark> fruit makes every salad taste better.",
            "vi_ex": "Tôi nghĩ chọn trái cây chín làm mọi món salad ngon hơn rõ.",
        },
        {
            "form": "loaf",
            "vi": "ổ bánh mì",
            "ipa": "/loʊf/",
            "frame": "I'm keen on + V-ing",
            "group": "like",
            "role": "mo",
            "tense": "Present Continuous · these days",
            "en": "These days I'm keen on baking a fresh <mark class=\"vocab\">loaf</mark> at home at the weekend.",
            "vi_ex": "Dạo này tôi thích tự nướng một ổ bánh mì ở nhà vào cuối tuần.",
        },
        {
            "form": "bread roll",
            "vi": "ổ bánh mì tròn",
            "ipa": "/brɛd roʊl/",
            "frame": "I love this",
            "group": "like",
            "role": "mo",
            "tense": "Present Simple",
            "en": "I love a warm <mark class=\"vocab\">bread roll</mark> with soup on rainy days.",
            "vi_ex": "Tôi thích một ổ bánh mì tròn nóng kèm súp vào ngày mưa.",
        },
        {
            "form": "berry",
            "vi": "quả mọng",
            "ipa": "/ˈbɛri/",
            "frame": "I'm a big fan of + N",
            "group": "like",
            "role": "mo",
            "tense": "Present Simple",
            "en": "I'm a big fan of fresh <mark class=\"vocab\">berry</mark> toppings on yoghurt.",
            "vi_ex": "Tôi là fan lớn của topping quả mọng tươi trên sữa chua.",
        },
        {
            "form": "pomegranate",
            "vi": "lựu",
            "ipa": "/ˈpɑməˌɡrænɪt/",
            "frame": "I'm keen on + N",
            "group": "like",
            "role": "mo",
            "tense": "Present Perfect",
            "en": "I've become keen on <mark class=\"vocab\">pomegranate</mark> seeds in salads — they add a nice crunch.",
            "vi_ex": "Tôi đã bắt đầu thích hạt lựu trong salad — chúng thêm độ giòn dễ chịu.",
        },
        {
            "form": "cantaloupe",
            "vi": "dưa lưới",
            "ipa": "/ˈkæntəˌloʊp/",
            "frame": "I love + N",
            "group": "like",
            "role": "mo",
            "tense": "Present Simple · habit",
            "en": "In summer I love chilled <mark class=\"vocab\">cantaloupe</mark> as a light dessert.",
            "vi_ex": "Mùa hè tôi thích dưa lưới mát lạnh làm món tráng miệng nhẹ.",
        },
        {
            "form": "lime",
            "vi": "chanh xanh",
            "ipa": "/laɪm/",
            "frame": "I think … · It helps me",
            "group": "like",
            "role": "mo",
            "tense": "Present Simple",
            "en": "I think a squeeze of <mark class=\"vocab\">lime</mark> helps me brighten up almost any seafood dish.",
            "vi_ex": "Tôi nghĩ một chút chanh xanh giúp tôi làm dậy vị hầu như mọi món hải sản.",
        },
        {
            "form": "low-carb diet",
            "vi": "chế độ ăn kiêng low-carb",
            "ipa": "/ˈloʊ ˈkɑrb ˈdaɪət/",
            "frame": "I'm keen on + N",
            "group": "like",
            "role": "mo",
            "tense": "Present Continuous",
            "en": "Right now I'm keen on a simple <mark class=\"vocab\">low-carb diet</mark> during the week.",
            "vi_ex": "Hiện tại tôi đang theo một chế độ low-carb đơn giản trong tuần.",
        },
        # ── Soft dislike ──
        {
            "form": "soda",
            "vi": "soda",
            "ipa": "/ˈsoʊdə/",
            "frame": "I can't stand …",
            "group": "soft",
            "role": "mo",
            "tense": "Present Simple · dislike",
            "en": "I can't stand drinking too much <mark class=\"vocab\">soda</mark> because it's way too sweet.",
            "vi_ex": "Tôi không chịu nổi việc uống quá nhiều soda vì nó ngọt gắt.",
        },
        {
            "form": "energy drink",
            "vi": "nước tăng lực",
            "ipa": "/ˈɛnɚdʒi ˌdrɪŋk/",
            "frame": "I don't like this · I avoid …",
            "group": "soft",
            "role": "ket",
            "tense": "Present Simple",
            "en": "I don't like drinking an <mark class=\"vocab\">energy drink</mark> late at night, so I avoid it after 6 p.m.",
            "vi_ex": "Tôi không thích uống nước tăng lực muộn, nên tránh sau 6 giờ tối.",
        },
        {
            "form": "take-away",
            "vi": "mang đi",
            "ipa": "/ˈteɪk əˌweɪ/",
            "frame": "It's not my cup of tea",
            "group": "soft",
            "role": "mo",
            "tense": "Present Simple · soft no",
            "en": "Ordering greasy <mark class=\"vocab\">take-away</mark> every night is not my cup of tea.",
            "vi_ex": "Gọi đồ take-away dầu mỡ mỗi tối không phải gu của tôi.",
        },
        {
            "form": "veal",
            "vi": "thịt bê",
            "ipa": "/viːl/",
            "frame": "It's not my cup of tea",
            "group": "soft",
            "role": "mo",
            "tense": "Present Simple · opinion",
            "en": "To be honest, <mark class=\"vocab\">veal</mark> is not really my cup of tea.",
            "vi_ex": "Thành thật thì thịt bê không thật sự hợp gu tôi.",
        },
        {
            "form": "Jell-O",
            "vi": "thạch",
            "ipa": "/ˈʤɛloʊ/",
            "frame": "I don't like this",
            "group": "soft",
            "role": "mo",
            "tense": "Present Simple",
            "en": "I don't like <mark class=\"vocab\">Jell-O</mark> desserts — the texture feels strange to me.",
            "vi_ex": "Tôi không thích món thạch Jell-O — cảm giác kết cấu hơi lạ.",
        },
        {
            "form": "soft drink",
            "vi": "nước ngọt có ga",
            "ipa": "/ˈsɔft ˌdrɪŋk/",
            "frame": "To be honest, I don't enjoy …",
            "group": "soft",
            "role": "mo",
            "tense": "Present Simple · soft no",
            "en": "To be honest, I don't enjoy sugary <mark class=\"vocab\">soft drink</mark>s with meals.",
            "vi_ex": "Thành thật thì tôi không thích uống nước ngọt có ga kèm bữa ăn.",
        },
        {
            "form": "alcoholic",
            "vi": "có cồn",
            "ipa": "/ˌælkəˈhɑlɪk/",
            "frame": "I don't think …",
            "group": "soft",
            "role": "mo",
            "tense": "Present Simple · opinion",
            "en": "I don't think <mark class=\"vocab\">alcoholic</mark> drinks are necessary at every dinner.",
            "vi_ex": "Tôi không nghĩ đồ uống có cồn là bắt buộc ở mọi bữa tối.",
        },
        # ── It's not + adj / doesn't … ──
        {
            "form": "low-fat diet",
            "vi": "chế độ ăn ít chất béo",
            "ipa": "/ˈloʊ ˈfæt ˈdaɪət/",
            "frame": "It's + not + practical / useful",
            "group": "neg",
            "role": "than",
            "tense": "Present Simple · opinion",
            "en": "Following a strict <mark class=\"vocab\">low-fat diet</mark> is not always practical when I eat out.",
            "vi_ex": "Theo một chế độ low-fat quá chặt không phải lúc nào cũng thực tế khi ăn ngoài.",
        },
        {
            "form": "sugar-free",
            "vi": "không đường",
            "ipa": "/ˈʃʊɡɚˌfriː/",
            "frame": "It's + not + useful",
            "group": "neg",
            "role": "than",
            "tense": "Present Simple · opinion",
            "en": "Choosing only <mark class=\"vocab\">sugar-free</mark> snacks is not always useful if the ingredients are still heavily processed.",
            "vi_ex": "Chỉ chọn snack sugar-free không phải lúc nào cũng hữu ích nếu nguyên liệu vẫn chế biến sẵn nặng.",
        },
        {
            "form": "white meat",
            "vi": "thịt trắng",
            "ipa": "/ˌwaɪt ˈmiːt/",
            "frame": "doesn't + V nguyên mẫu",
            "group": "neg",
            "role": "than",
            "tense": "Present Simple",
            "en": "Eating only <mark class=\"vocab\">white meat</mark> doesn't automatically make a meal healthy.",
            "vi_ex": "Chỉ ăn thịt trắng không tự động làm bữa ăn trở nên lành mạnh.",
        },
        {
            "form": "breast",
            "vi": "ức",
            "ipa": "/brɛst/",
            "frame": "It doesn't give me the chance to …",
            "group": "neg",
            "role": "than",
            "tense": "Present Simple · contrast",
            "en": "Plain grilled chicken <mark class=\"vocab\">breast</mark> doesn't give me the chance to enjoy richer flavours like ribs.",
            "vi_ex": "Ức gà nướng trơn không cho tôi cơ hội thưởng thức vị đậm hơn như sườn.",
        },
        {
            "form": "yolk",
            "vi": "lòng đỏ trứng",
            "ipa": "/joʊk/",
            "frame": "It doesn't help me …",
            "group": "neg",
            "role": "than",
            "tense": "Present Simple",
            "en": "Skipping the <mark class=\"vocab\">yolk</mark> doesn't help me feel satisfied after breakfast.",
            "vi_ex": "Bỏ lòng đỏ trứng không giúp tôi cảm thấy no đủ sau bữa sáng.",
        },
        {
            "form": "calorie",
            "vi": "calo",
            "ipa": "/ˈkælɚi/",
            "frame": "I don't think … · It doesn't help me",
            "group": "neg",
            "role": "than",
            "tense": "Present Simple · opinion",
            "en": "I don't think counting every <mark class=\"vocab\">calorie</mark> helps me build a healthier relationship with food.",
            "vi_ex": "Tôi không nghĩ đếm từng calo giúp tôi xây quan hệ lành mạnh hơn với đồ ăn.",
        },
        # ── Strong no / avoid / can lead to ──
        {
            "form": "rib",
            "vi": "sườn",
            "ipa": "/rɪb/",
            "frame": "I avoid …",
            "group": "avoid",
            "role": "ket",
            "tense": "Present Simple · habit",
            "en": "I avoid ordering huge <mark class=\"vocab\">rib</mark> portions on weekdays because I feel too heavy afterwards.",
            "vi_ex": "Tôi tránh gọi phần sườn quá lớn vào ngày thường vì sau đó thấy nặng bụng.",
        },
        {
            "form": "shellfish",
            "vi": "hải sản có vỏ",
            "ipa": "/ˈʃɛlˌfɪʃ/",
            "frame": "No, definitely not because … · I avoid …",
            "group": "avoid",
            "role": "mo",
            "tense": "Present Simple · strong no",
            "en": "No, definitely not — I avoid raw <mark class=\"vocab\">shellfish</mark> when I'm unsure about freshness.",
            "vi_ex": "Không, chắc chắn không — tôi tránh hải sản có vỏ sống khi không chắc độ tươi.",
        },
        {
            "form": "meatball",
            "vi": "viên thịt",
            "ipa": "/ˈmiːtˌbɔl/",
            "frame": "Consuming too much … can lead to …",
            "group": "avoid",
            "role": "than",
            "tense": "Present Simple · cause → effect",
            "en": "Consuming too many fried <mark class=\"vocab\">meatball</mark>s can lead to feeling heavy after meals.",
            "vi_ex": "Ăn quá nhiều thịt viên chiên có thể khiến bạn thấy nặng bụng sau bữa ăn.",
        },
        {
            "form": "soda+",
            "vi": "soda / soft drink",
            "ipa": "",
            "frame": "Consuming too much … can lead to …",
            "group": "avoid",
            "role": "than",
            "tense": "Present Simple · warning",
            "en": "Consuming too much <mark class=\"vocab\">soda</mark> or other sugary <mark class=\"vocab\">soft drink</mark>s can lead to various health problems.",
            "vi_ex": "Uống quá nhiều soda hay nước ngọt có ga có thể dẫn đến nhiều vấn đề sức khỏe.",
            "skip_bank": True,
        },
        {
            "form": "bacon+",
            "vi": "bacon",
            "ipa": "",
            "frame": "Consuming too much … can lead to …",
            "group": "avoid",
            "role": "than",
            "tense": "Present Simple · cause → effect",
            "en": "Consuming too much <mark class=\"vocab\">bacon</mark> can lead to a high salt intake over time.",
            "vi_ex": "Ăn quá nhiều bacon lâu dần có thể dẫn đến lượng muối cao.",
            "skip_bank": True,
        },
        {
            "form": "pancake+",
            "vi": "pancake",
            "ipa": "",
            "frame": "Consuming too much … can lead to …",
            "group": "avoid",
            "role": "than",
            "tense": "Present Simple · cause → effect",
            "en": "Consuming too many <mark class=\"vocab\">pancake</mark>s with syrup can lead to a sugar crash later.",
            "vi_ex": "Ăn quá nhiều bánh kếp với siro có thể khiến bạn tụt đường huyết sau đó.",
            "skip_bank": True,
        },
    ]

    group_meta = [
        (
            "yes",
            "Yes · lý do tích cực",
            "It helps me + V · It gives me the chance to + V · I also get the opportunity to + V",
        ),
        (
            "adj",
            "Cảm xúc · It's + adj",
            "It's + relaxing / exciting / thrilling / entertaining / interesting …",
        ),
        (
            "like",
            "Thích · love / keen on / I think",
            "I love this · I think … · I'm keen on … · I'm a big fan of …",
        ),
        (
            "soft",
            "Không thích · soft no",
            "I don't like this · I can't stand … · It's not my cup of tea · I don't think … · To be honest, I don't enjoy …",
        ),
        (
            "neg",
            "Phủ định cấu trúc · not / doesn't",
            "It's + not + useful / practical · doesn't + V · It doesn't give me the chance to … · It doesn't help me …",
        ),
        (
            "avoid",
            "Tránh / hệ quả",
            "No, definitely not because … · I avoid … · Consuming too much … can lead to …",
        ),
    ]

    parts: list[str] = []
    for gid, title, formula in group_meta:
        uniq = [d for d in drills if d["group"] == gid]
        if not uniq:
            continue
        card_html = []
        for d in uniq:
            ipa = f'<span class="ipa">{esc(d["ipa"])}</span>' if d.get("ipa") else ""
            role = d.get("role", "than")
            role_label = {"mo": "Mở", "than": "Thân", "ket": "Kết"}.get(role, "Thân")
            role_cls = {"mo": "open", "than": "body", "ket": "close"}.get(role, "body")
            card_html.append(
                f"""          <article class="lr-phrase-card lr-phrase-card--{role_cls}">
            <div class="lr-phrase-meta">
              <span class="lr-role-tag lr-role-tag--{role_cls}">{role_label}</span>
              <mark class="vocab">{esc(d["form"].rstrip("+"))}</mark>
              {ipa}
              <span class="lr-phrase-vi-word">{esc(d["vi"])}</span>
              <span class="lr-tense-tag">{esc(d["tense"])}</span>
            </div>
            <p class="lr-phrase-frame"><code>{esc(d["frame"])}</code></p>
            <p class="lr-phrase-en">{d["en"]}</p>
            <p class="lr-phrase-vi">{esc(d["vi_ex"])}</p>
          </article>"""
            )
        parts.append(
            f"""        <div class="lr-phrase-group">
          <h3>{esc(title)}</h3>
          <p class="lr-phrase-formula">{esc(formula)}</p>
          <div class="lr-phrase-grid">
{chr(10).join(card_html)}
          </div>
        </div>"""
        )

    bank_items = []
    bank_seen: set[str] = set()
    for d in drills:
        if d.get("skip_bank"):
            continue
        form = d["form"]
        if form in bank_seen:
            continue
        bank_seen.add(form)
        ipa = f' <span class="ipa">{esc(d["ipa"])}</span>' if d.get("ipa") else ""
        bank_items.append(
            f'<li><mark class="vocab">{esc(form)}</mark>{ipa} — {esc(d["vi"])}</li>'
        )

    return (
        '<p class="lr-role-legend">Mỗi thẻ có tag vai trò khi ghép đoạn: '
        '<span class="lr-role-tag lr-role-tag--open">Mở</span> '
        '<span class="lr-role-tag lr-role-tag--body">Thân</span> '
        '<span class="lr-role-tag lr-role-tag--close">Kết</span> '
        "— nhớ tag này khi làm Bước 2.</p>\n"
        + "\n".join(parts)
        + f"""
        <details class="lr-vocab-bank">
          <summary>Phải học bank ({len(bank_items)} từ · Pareto gold)</summary>
          <ul class="ex-vocab-list">{"".join(bank_items)}</ul>
        </details>"""
    )




def phrase_assemble_html() -> str:
    """Step 2 after memorising single frames: label roles → assemble a short paragraph."""
    return """
        <div class="lr-assemble" id="phrase-assemble">
          <h3>Bước 2 · Ghép câu đơn thành đoạn (hiểu vai trò — không học vẹt đoạn)</h3>
          <p class="lr-assemble-lead">Bước 1 chỉ giúp bạn <strong>thuộc câu đơn + hiểu nghĩa</strong>. Bước 2 không phải thuộc một đoạn mẫu dài, mà là biết mỗi câu đang đóng vai gì rồi <strong>xếp đúng chỗ</strong>.</p>

          <div class="lr-assemble-roles">
            <article class="lr-assemble-role lr-assemble-role--open">
              <span class="lr-assemble-badge">Mở</span>
              <h4>Trả lời trực tiếp</h4>
              <p>Thái độ Yes / No / soft no. Dùng khung: <code>I'm keen on…</code> · <code>I love…</code> · <code>To be honest…</code> · <code>No, definitely not…</code> · <code>It's not my cup of tea</code></p>
            </article>
            <article class="lr-assemble-role lr-assemble-role--body">
              <span class="lr-assemble-badge">Thân</span>
              <h4>Lý do + ví dụ</h4>
              <p>Giải thích vì sao. Dùng khung: <code>It helps me…</code> · <code>It gives me the chance to…</code> · <code>Whenever I…</code> · <code>I think…</code> · <code>Consuming too much… can lead to…</code></p>
            </article>
            <article class="lr-assemble-role lr-assemble-role--close">
              <span class="lr-assemble-badge">Kết</span>
              <h4>Chốt / giới hạn</h4>
              <p>Nhấn lại ý hoặc đối chiếu nhẹ. Dùng: <code>so / that's why</code> · <code>but I still…</code> · <code>I avoid…</code> · <code>I don't think…</code></p>
            </article>
          </div>

          <div class="lr-assemble-flow">
            <p class="lr-assemble-flow-label">Công thức ráp đoạn Part 1</p>
            <p class="lr-assemble-flow-line"><strong>1 Mở</strong> → <strong>1–2 Thân</strong> → <strong>(optional) 1 Kết</strong></p>
            <p class="lr-assemble-glue">Keo nối ngắn: <code>because</code> · <code>This is because</code> · <code>so</code> · <code>but</code> · <code>that's why</code> · <code>and</code></p>
          </div>

          <ol class="lr-assemble-howto">
            <li><strong>Hiểu từng câu đơn</strong> — biết câu đó nói thái độ, lý do, hay giới hạn.</li>
            <li><strong>Gắn nhãn vai</strong> — Mở / Thân / Kết (một câu chỉ một việc).</li>
            <li><strong>Chọn theo câu hỏi</strong> — lấy 1 Mở + 1–2 Thân (+ 1 Kết nếu cần), <em>không</em> nhồi hết 40 câu.</li>
            <li><strong>Nối bằng keo ngắn</strong> — because / so / but / that's why. Đọc to 2–3 lần để nghe nhịp đoạn.</li>
          </ol>
          <p class="lr-note-tip">Mục tiêu: hiểu mối quan hệ giữa câu → tự ghép. Đừng thuộc nguyên một đoạn rồi “xả” mỗi lần thi.</p>

          <h4 class="lr-assemble-samples-title">Đoạn mẫu · thấy rõ Mở → Thân → Kết</h4>
          <p class="lr-assemble-samples-hint">Mỗi dòng màu = một câu đơn đã học ở trên. Đọc từng dòng trước, rồi đọc cả đoạn.</p>

          <article class="lr-assemble-sample">
            <p class="lr-assemble-q">Q: Do you eat healthy food?</p>
            <div class="lr-assemble-lines">
              <p class="lr-line lr-line--open"><span class="lr-line-tag">Mở</span> To be honest, I'm keen on eating healthy food, so <mark class="vocab">citrus</mark> fruit is always my top choice for breakfast.</p>
              <p class="lr-line lr-line--body"><span class="lr-line-tag">Thân</span> Drinking a <mark class="vocab">smoothie</mark> every morning helps me stay full until lunch.</p>
              <p class="lr-line lr-line--body"><span class="lr-line-tag">Thân</span> Making a <mark class="vocab">fruit salad</mark> also gives me the chance to add more vitamins to my diet.</p>
              <p class="lr-line lr-line--close"><span class="lr-line-tag">Kết</span> That's why I avoid sugary <mark class="vocab">soft drink</mark>s with meals.</p>
            </div>
            <p class="lr-assemble-joined"><strong>Đọc liền:</strong> To be honest, I'm keen on eating healthy food, so citrus fruit is always my top choice for breakfast. Drinking a smoothie every morning helps me stay full until lunch, and making a fruit salad also gives me the chance to add more vitamins to my diet — that's why I avoid sugary soft drinks with meals.</p>
            <p class="lr-phrase-vi">Thành thật thì tôi thích ăn lành, nên trái cây có múi luôn là lựa chọn sáng. Uống smoothie mỗi sáng giúp no đến trưa, và làm salad trái cây cũng cho cơ hội thêm vitamin — vì vậy tôi tránh nước ngọt có ga kèm bữa.</p>
          </article>

          <article class="lr-assemble-sample">
            <p class="lr-assemble-q">Q: Do you like eating out / fast food?</p>
            <div class="lr-assemble-lines">
              <p class="lr-line lr-line--open"><span class="lr-line-tag">Mở</span> Well, not really — ordering greasy <mark class="vocab">take-away</mark> every night is not my cup of tea.</p>
              <p class="lr-line lr-line--body"><span class="lr-line-tag">Thân</span> I think a classic <mark class="vocab">cheeseburger</mark> tastes better sometimes, but consuming too much <mark class="vocab">bacon</mark> can lead to a high salt intake.</p>
              <p class="lr-line lr-line--body"><span class="lr-line-tag">Thân</span> I'm still keen on a <mark class="vocab">home-cooked meal</mark> most evenings because it helps me eat healthier.</p>
              <p class="lr-line lr-line--close"><span class="lr-line-tag">Kết</span> So I might <mark class="vocab">grab a bite</mark> with friends at the weekend, but I don't dine out every night.</p>
            </div>
            <p class="lr-assemble-joined"><strong>Đọc liền:</strong> Well, not really — ordering greasy take-away every night is not my cup of tea. I think a classic cheeseburger tastes better sometimes, but consuming too much bacon can lead to a high salt intake. I'm still keen on a home-cooked meal most evenings because it helps me eat healthier. So I might grab a bite with friends at the weekend, but I don't dine out every night.</p>
            <p class="lr-phrase-vi">À không hẳn — gọi take-away dầu mỡ mỗi tối không hợp tôi. Đôi khi cheeseburger ngon, nhưng ăn quá nhiều bacon dễ tăng muối. Tôi vẫn thích bữa nấu ở nhà hầu hết các tối vì ăn lành hơn. Cuối tuần có thể ăn vội với bạn, nhưng không ăn ngoài mỗi tối.</p>
          </article>

          <article class="lr-assemble-sample">
            <p class="lr-assemble-q">Q: What's your favourite drink?</p>
            <div class="lr-assemble-lines">
              <p class="lr-line lr-line--open"><span class="lr-line-tag">Mở</span> I'm a big fan of fresh <mark class="vocab">berry</mark> toppings in a yoghurt drink, and I love chilled <mark class="vocab">cantaloupe</mark> in summer.</p>
              <p class="lr-line lr-line--body"><span class="lr-line-tag">Thân</span> Keeping <mark class="vocab">mineral water</mark> on my desk helps me drink more water throughout the day.</p>
              <p class="lr-line lr-line--body"><span class="lr-line-tag">Thân</span> I've tried a few <mark class="vocab">nonalcoholic</mark> <mark class="vocab">cocktail</mark>s lately — mixing them at home can be quite entertaining with friends.</p>
              <p class="lr-line lr-line--close"><span class="lr-line-tag">Kết</span> But I don't like an <mark class="vocab">energy drink</mark> late at night, so I avoid it after 6 p.m.</p>
            </div>
            <p class="lr-assemble-joined"><strong>Đọc liền:</strong> I'm a big fan of fresh berry toppings in a yoghurt drink, and I love chilled cantaloupe in summer. Keeping mineral water on my desk helps me drink more water throughout the day. I've tried a few nonalcoholic cocktails lately — mixing them at home can be quite entertaining with friends. But I don't like an energy drink late at night, so I avoid it after 6 p.m.</p>
            <p class="lr-phrase-vi">Tôi thích topping quả mọng trong sữa chua uống, và mùa hè thích dưa lưới mát. Để nước khoáng trên bàn giúp uống nhiều nước hơn. Gần đây thử vài cocktail không cồn — pha ở nhà với bạn khá vui. Nhưng không thích nước tăng lực muộn tối, nên tránh sau 6 giờ.</p>
          </article>
        </div>"""



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
        (
            "What kind of drinks do you like?",
            "Bạn thích loại đồ uống nào?",
            (
                'I\'m quite flexible. In the morning I go for '
                f'{slot_select("morning_drink", 1)}, but in the evening I might sip '
                f'{slot_select("b2_drink", 2)} or just stick to {slot_select("soft_drink")}. '
                '<span class="lr-tense-tag">Present Simple · habit</span>'
            ),
        ),
        (
            "Do you like trying new cuisines?",
            "Bạn có thích thử ẩm thực mới không?",
            (
                'Yes, absolutely. <strong>What I enjoy most</strong> is exploring '
                f'different {slot_select("cuisine")} styles — last month I tried '
                f'{slot_select("meat", 4)} with {slot_select("sauce", 0)}. '
                '<span class="lr-tense-tag">Present Perfect · emphasis</span>'
            ),
        ),
        (
            "Did you cook when you were younger?",
            "Khi còn nhỏ bạn có nấu ăn không?",
            (
                'Not really. <strong>When I was a child</strong>, my parents did all the cooking. '
                f'I <strong>would</strong> only help {slot_select("cook_verb", 3)} vegetables sometimes. '
                '<span class="lr-tense-tag">Past Simple · would</span>'
            ),
        ),
        (
            "Are you trying to eat more healthily these days?",
            "Dạo này bạn có cố ăn uống lành mạnh hơn không?",
            (
                'Yes, definitely. I\'m <strong>paying more attention to</strong> '
                f'{slot_select("diet_term", 1)} and {slot_select("diet_term", 0)}. '
                f'I\'ve been eating more {slot_select("fruit", 0)} and less '
                f'{slot_select("dislike_food", 2)}. '
                '<span class="lr-tense-tag">Present Perfect Continuous</span>'
            ),
        ),
    ]

    p2_natural = (
        '<blockquote class="lr-vlog lr-vlog--part2" cite="food-date-part2">'
        '<p class="lr-vlog-text"><mark class="lr-filler">Okay</mark> <mark class="lr-filler">so</mark> um I\'m supposed to talk about a meal I enjoyed, right? '
        "This was last Saturday evening — our first proper dinner date, and honestly I was "
        '<mark class="lr-filler">kind of</mark> nervous the whole way there.</p>'
        '<p class="lr-vlog-text">I went with someone I\'d been texting for maybe two weeks — we picked a small restaurant near the river, '
        "nothing fancy, just warm lights and, <mark class=\"lr-filler\">you know</mark>, that nice smell when you walk in.</p>"
        '<p class="lr-vlog-text">We shared fried rice and grilled chicken, and a small fruit cake at the end — '
        '<mark class="lr-filler">I mean</mark> the food was really good, but what stuck with me is we kept laughing because I '
        'could not use the chopsticks properly and she had to show me, which was embarrassing but '
        '<mark class="lr-filler">like</mark>… cute, <mark class="lr-filler">I guess</mark>.</p>'
        '<p class="lr-vlog-text"><mark class="lr-filler">And</mark> <mark class="lr-filler">yeah</mark> why I enjoyed it — it wasn\'t because the food was '
        "super expensive or anything. For the first time that week I wasn't checking my phone or thinking about work. "
        'It just felt easy — <mark class="lr-filler">like</mark> eating with someone you actually want to see again. '
        "<mark class=\"lr-filler\">That's</mark> the meal I still think about.</p>"
        '<details class="lr-vlog-vi-details">'
        '<summary>Bản dịch tiếng Việt</summary>'
        '<div class="lr-vlog-vi-body">'
        '<p>Mình kể về một bữa ăn thật sự thích nhé — tối thứ Bảy tuần trước, buổi hẹn ăn tối đầu tiên, đi đến quán mà hơi hồi hộp cả đường.</p>'
        '<p>Đi với người mình nhắn tin khoảng hai tuần — chọn quán nhỏ gần sông, không sang, chỉ đèn ấm và mùi thơm dễ chịu khi bước vào.</p>'
        '<p>Gọi cơm chiên và gà nướng ăn chung, cuối buổi thêm bánh tráng miệng nhỏ — đồ ăn ngon thật, nhưng nhớ nhất là hai đứa cười vì mình cầm đũa vụng quá, cô ấy phải chỉ, hơi ngại mà cũng dễ thương.</p>'
        '<p>Thích vì không phải đồ ăn đắt đỏ — mà vì lần đầu cả tuần mình không cắm điện thoại hay nghĩ việc. Cảm giác nhẹ nhàng, kiểu muốn gặp lại người đó. Bữa đó mình vẫn nhớ.</p>'
        '</div></details>'
        "</blockquote>"
    )

    p2_en = (
        "I'm going to describe a meal I really enjoyed. "
        f"It was last month when my family cooked together. "
        f"First, we decided to {slot_select('cook_verb', 2)} "
        f"{slot_select('meat', 2)} and prepare "
        f"{slot_select('healthy_item', 1)} on the side. "
        f"I was {slot_select('cook_verb', 4)} sauce with {slot_select('sauce', 3)} "
        f"while my mom chopped vegetables — "
        "<strong>Past Continuous</strong> for background. "
        f"Before that day, I <strong>had never tried</strong> that recipe with "
        f"{slot_select('cheese', 0)}, so everything felt new. "
        f"We used our {slot_select('kitchen_tool', 3)} and finished with "
        f"{slot_select('dessert', 0)} and shared "
        f"{slot_select('alcohol', 0)} for a toast. "
        "<strong>What I enjoyed most</strong> was spending time together — not just the food. "
        "Looking back now, it makes a good story!"
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
        (
            "What role does food play in your culture?",
            "Thức ăn đóng vai trò gì trong văn hóa của bạn?",
            (
                'Food is <strong>extremely important</strong>. Sharing a meal brings families together, '
                f'and traditional {slot_select("cuisine", 2)} is passed down through generations. '
                f'On special occasions we prepare {slot_select("seafood", 0)} or '
                f'{slot_select("meat", 0)} — it\'s a great way to unwind and reconnect. '
                '<span class="lr-tense-tag">Present Simple · general truth</span>'
            ),
        ),
        (
            "Why do some people prefer cooking at home?",
            "Tại sao một số người thích nấu ăn ở nhà?",
            (
                'I think <strong>because</strong> it helps them control '
                f'{slot_select("diet_term", 1)} and save money. '
                f'It\'s also a great way to experiment with {slot_select("ingredient", 0)} '
                f'and {slot_select("sauce", 1)}. '
                '<span class="lr-tense-tag">Because + S + V</span>'
            ),
        ),
        (
            "How important is it to know where your food comes from?",
            "Biết nguồn gốc thức ăn quan trọng thế nào?",
            (
                'I think it\'s <strong>absolutely essential</strong>. '
                f'If you care about {slot_select("diet_term", 2)} eating, you need to check '
                'whether ingredients are fresh and sustainably sourced. '
                f'<strong>More people have been paying attention to</strong> this lately. '
                '<span class="lr-tense-tag">Present Perfect Continuous</span>'
            ),
        ),
        (
            "Do you think children should learn to cook?",
            "Bạn có nghĩ trẻ em nên học nấu ăn không?",
            (
                'Yes, definitely. <strong>It gives them the chance to</strong> learn practical skills '
                f'and understand {slot_select("diet_term", 1)}. '
                f'If they start early, they <strong>will have developed</strong> healthy habits '
                'by the time they leave home. '
                '<span class="lr-tense-tag">Future Perfect · reasons</span>'
            ),
        ),
    ]

    p2_idx = len(p1) + 1
    p2_natural_idx = p2_idx + 1
    p3_start = p2_natural_idx + 1

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
    lines.append(f'            <p class="ex-sent lr-answer" data-sent="{p2_idx}">')
    lines.append('              <span class="ex-a-label">You</span>')
    lines.append('              <span class="ex-a-label-hint">Structured · grammar + vocab</span>')
    lines.append(f'              <span class="ex-en lr-answer-text">{p2_en}</span>')
    lines.append("            </p></div>")
    lines.append('          <div class="ex-qa lr-mock-natural">')
    lines.append('            <p class="lr-chain-ex-label">Real talk · dinner date (natural voice)</p>')
    lines.append('            <p class="lr-idiom-hint">Tự sự buổi hẹn ăn — filler tự nhiên · when / who / what / why · bấm <strong>Bản dịch tiếng Việt</strong> để mở/đóng.</p>')
    lines.append(f'            <div class="ex-sent lr-answer lr-answer--natural" data-sent="{p2_natural_idx}">')
    lines.append('              <span class="ex-a-label">You</span>')
    lines.append('              <span class="ex-a-label-hint">Date story</span>')
    lines.append(f'              {p2_natural}')
    lines.append("            </div></div></div>")

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
            <a class="lr-ref-card" href="https://www.dolenglish.vn/blog/ielts-speaking-food" target="_blank" rel="noopener noreferrer">
              <strong>DOL — IELTS Speaking Food</strong>
              <span>Chủ đề Food thực tế, câu hỏi Part 1/2/3 và gợi ý trả lời</span>
              <span class="lr-card-cta">Xem chủ đề Food ↗</span>
            </a>
            <a class="lr-ref-card" href="https://langgo.edu.vn/food-idioms-thanh-ngu-ve-do-an-tieng-anh" target="_blank" rel="noopener noreferrer">
              <strong>LangGo — 70+ Food idioms</strong>
              <span>Thành ngữ đồ ăn — nguồn idiom &amp; phrase trong mục 5</span>
              <span class="lr-card-cta">Xem idioms ↗</span>
            </a>
          </div>
          <h4 class="lr-ref-subtitle">Giọng tự nhiên · kể chuyện Food (Part 2)</h4>
          <p class="lr-ref-subhint">Tổng hợp hướng dẫn nói <strong>như kể chuyện thật</strong> — dùng giác quan (sight, smell, taste…), beginning–middle–end. Phù hợp luyện <strong>Real talk</strong> &amp; Date story bên dưới; tránh nhồi từ khó.</p>
          <div class="lr-ref-grid lr-ref-grid--natural">
            <a class="lr-ref-card lr-ref-card--featured" href="https://www.ieltsjacky.com/ielts-speaking-test-sample.html" target="_blank" rel="noopener noreferrer">
              <strong>IELTS Jacky — Tell a story · Food</strong>
              <span>Method 3: <em>Using the Senses</em> · mẫu Part 2 “food you disliked but now enjoy” (figs — Christmas → Spain) · beginning / middle / end</span>
              <span class="lr-card-cta">Đọc bài mẫu ↗</span>
            </a>
            <a class="lr-ref-card" href="https://www.ieltsjacky.com/ielts-speaking-part-2.html" target="_blank" rel="noopener noreferrer">
              <strong>IELTS Jacky — Part 2 format &amp; cue cards</strong>
              <span>1 phút chuẩn bị, cách tránh lỗi thường gặp, thêm cue card Food &amp; topic vocabulary</span>
              <span class="lr-card-cta">Xem Part 2 ↗</span>
            </a>
            <a class="lr-ref-card" href="https://ielts.idp.com/prepare/article-how-to-talk-naturally-about-food-in-ielts-speaking" target="_blank" rel="noopener noreferrer">
              <strong>IDP — Talk naturally about food</strong>
              <span>Nói như hội thoại thật · collocation (home-cooked, eat out) · phrasal verb · không cố nghe “band cao”</span>
              <span class="lr-card-cta">Đọc IDP ↗</span>
            </a>
            <a class="lr-ref-card" href="https://engage.mosaicbc.org/blog/ielts-tips-speaking-part-2-practice" target="_blank" rel="noopener noreferrer">
              <strong>MOSAIC — Meal at a restaurant</strong>
              <span>Mẫu Part 2 ~2 phút: sinh nhật bạn, quán vegan, bowl &amp; rice — giọng đơn giản, kết bằng “enjoyed the company”</span>
              <span class="lr-card-cta">Xem mẫu ↗</span>
            </a>
            <a class="lr-ref-card" href="https://careerwiseenglish.com.au/ielts-speaking-part-2-food-and-cooking-cue-card-sample/" target="_blank" rel="noopener noreferrer">
              <strong>CareerWise — Homemade chicken curry</strong>
              <span>Kể một trải nghiệm nấu ăn với chị · mùi trong bếp · “organised and real”, không cố nghe band 9</span>
              <span class="lr-card-cta">Đọc mẫu ↗</span>
            </a>
            <a class="lr-ref-card" href="https://www.ieltsjacky.com/ielts-speaking-samples.html" target="_blank" rel="noopener noreferrer">
              <strong>IELTS Jacky — Sample 1 · Question prompts</strong>
              <span>Method 1: ghi chú theo bullet points trên cue card — mẫu “healthy activity” (circuit training)</span>
              <span class="lr-card-cta">Sample 1 ↗</span>
            </a>
            <a class="lr-ref-card" href="https://www.ieltsjacky.com/ielts-speaking-sample.html" target="_blank" rel="noopener noreferrer">
              <strong>IELTS Jacky — Sample 2 · Brainstorming</strong>
              <span>Method 2: liệt kê ý tự do rồi xếp thành story — mẫu “place near water”</span>
              <span class="lr-card-cta">Sample 2 ↗</span>
            </a>
          </div>
        </aside>"""


def core_steps_html() -> str:
    """Method notes before vocab drill + review — Pareto → anchor → safe frames."""
    return """      <section class="lr-section lr-core-steps" id="core-steps">
        <h2>Core · 3 bước trước khi học từ mới</h2>
        <p class="lr-section-hint">Đọc xong 3 bước này rồi mới sang Flashcards A1–B2 / Review. Mục tiêu: rút còn <strong>20–30 từ vàng</strong>, neo vào 1 câu mẫu, rồi lắp vào khung câu an toàn — không ôm đồm 100 từ.</p>

        <article class="lr-core-step">
          <header class="lr-core-step-head">
            <span class="lr-core-step-num">1</span>
            <div>
              <h3>Sàng lọc tàn nhẫn (Pareto 80/20)</h3>
              <p class="lr-core-step-sub">Chỉ giữ lại 20–30 từ “vàng”</p>
            </div>
          </header>
          <p>Đừng ôm đồm học cả 100 từ. Chia đống từ thành <strong>3 nhóm</strong> (Flashcards đã có nút phân loại + tải <code>.txt</code>):</p>
          <ul class="lr-core-groups">
            <li class="lr-core-group lr-core-group--trash">
              <strong>Nhóm 1 · Rác / Quá khó</strong>
              <span>Từ hàn lâm, hiếm dùng trong văn nói hàng ngày (vd. <em>gastronomy</em>, <em>culinary spectrum</em>). Gạt bỏ ngay.</span>
            </li>
            <li class="lr-core-group lr-core-group--gold">
              <strong>Nhóm 2 · Dễ dùng, Đa năng</strong>
              <span>Áp dụng được nhiều chủ đề (vd. <em>delve into</em>, <em>hit the spot</em>, <em>grab a bite</em>, <em>mouth-watering</em>). Giữ lại và tập trung toàn lực.</span>
            </li>
            <li class="lr-core-group lr-core-group--known">
              <strong>Nhóm 3 · Đã biết</strong>
              <span>Từ đã quen — bỏ qua, đừng lãng phí slot nhớ.</span>
            </li>
          </ul>
          <p class="lr-core-result"><strong>Kết quả:</strong> ~100 từ → còn khoảng <strong>20–30 từ</strong> thực sự chất lượng.</p>
        </article>

        <article class="lr-core-step">
          <header class="lr-core-step-head">
            <span class="lr-core-step-num">2</span>
            <div>
              <h3>Neo ngữ cảnh (Contextual Anchoring)</h3>
              <p class="lr-core-step-sub">Học cụm trong 1 câu mẫu — không học từ đơn</p>
            </div>
          </header>
          <p>Học từ độc lập là cách nhanh nhất để quên. Với chủ đề Food, đừng học <em>mouth-watering</em> rồi để đấy — gắn chết dính vào <strong>một câu trả lời mẫu</strong> thuận miệng nhất:</p>
          <div class="lr-core-compare">
            <p class="lr-core-wrong"><span>Sai</span> Học từ <em>mouth-watering</em> = ngon chảy nước miếng.</p>
            <p class="lr-core-right"><span>Đúng</span> Nhớ luôn câu: <em>“The street food in Vietnam is just mouth-watering.”</em></p>
          </div>
          <p class="lr-note-tip">Lặp câu này 5–10 lần — não ghi nhớ cụm ngữ pháp, ngữ điệu và phản xạ; không đứng hình đi ghép từ.</p>
        </article>

        <article class="lr-core-step">
          <header class="lr-core-step-head">
            <span class="lr-core-step-num">3</span>
            <div>
              <h3>Khung câu an toàn — chữa “sợ sai ngữ pháp”</h3>
              <p class="lr-core-step-sub">1–2 công thức bất bại · chỉ lắp từ mới vào chỗ trống</p>
            </div>
          </header>
          <p>Ú á vì vừa nghĩ từ khó vừa lo cấu trúc phức tạp. Dùng khung đệm an toàn để <strong>bọc</strong> từ mới — đóng khung cả ý trả lời vào đúng 1–2 công thức ngắn:</p>
          <ol class="lr-core-frames">
            <li>
              <code>To be honest, I'm a big fan of + [từ mới / cụm chủ đề].</code>
              <span class="lr-core-ex">“To be honest, I'm a big fan of ginger ale because it's so refreshing.”</span>
            </li>
            <li>
              <code>Whenever I have free time, I really love to + [từ mới] because it helps me unwind.</code>
              <span class="lr-core-ex">“Whenever I have free time, I really love to grab a bite with friends because it helps me unwind.”</span>
            </li>
            <li>
              <code>What I like most about [Food] is that it always gives me a + [từ mới] experience.</code>
              <span class="lr-core-ex">“What I like most about Vietnamese street food is that it always gives me a mouth-watering experience.”</span>
            </li>
          </ol>
          <p class="lr-note-tip">Bonus khung đồ vật / hành động: <code>To be honest, I always use a [từ mới] when I…</code> → “I always use a frying pan when I cook dinner.”</p>
        </article>
      </section>
"""


def core_steps_teaser_html() -> str:
    """Compact block for topic index under Review card."""
    return """
        <div class="vocab-core-steps">
          <h3 class="vocab-core-steps-title">Core steps · trước khi học &amp; ôn</h3>
          <p class="vocab-core-steps-lead">Đừng ôm 100 từ. Làm 3 bước này trước Flashcards / Review Exercise:</p>
          <ol class="vocab-core-steps-list">
            <li><strong>Pareto 80/20</strong> — chia 3 nhóm: Không thông dụng · Phải học · Đã biết. Chỉ giữ ~20–30 từ vàng (Flashcards có nút phân loại + tải <code>.txt</code>).</li>
            <li><strong>Neo ngữ cảnh</strong> — gắn mỗi từ vào 1 câu mẫu duy nhất (vd. “The street food in Vietnam is just <em>mouth-watering</em>.”), lặp 5–10 lần.</li>
            <li><strong>Khung câu an toàn</strong> — lắp từ vào: <em>I'm a big fan of…</em> · <em>Whenever I have free time, I really love to…</em> · <em>What I like most about…</em></li>
          </ol>
          <p class="vocab-core-steps-more"><a href="review-exercise/#core-steps">Xem hướng dẫn đầy đủ trong Review Exercise 1 →</a></p>
        </div>
"""


def natural_vlog_html() -> str:
    return """      <section class="lr-section lr-vlog-section" id="natural-vlog">
        <h2>0 · Real talk — Food vlogger vlog</h2>
        <p class="lr-section-hint">Văn nói tự sự kiểu vlog — không phải IELTS script. Nghe nhịp tự nhiên: filler (<mark class="lr-filler">yeah</mark>, <mark class="lr-filler">like</mark>, <mark class="lr-filler">kind of</mark>, <mark class="lr-filler">I mean</mark>…), câu chạy dài, hạ giọng cuối câu. Bật <strong>Vietnamese</strong> ở trên để xem bản dịch.</p>
        <blockquote class="lr-vlog" cite="food-vlogger-vlog">
          <p class="lr-vlog-text"><mark class="lr-filler">Yeah</mark> <mark class="lr-filler">so</mark> um I've been <mark class="lr-filler">like</mark> doing this food vlog thing for maybe two years now, and honestly it's been pretty wild — <mark class="lr-filler">like</mark> I never thought people would actually watch me eat street food at midnight, <mark class="lr-filler">you know</mark>, but here we are.</p>
          <p class="lr-vlog-text"><mark class="lr-filler">So</mark> basically my whole thing is I just walk around the city, find <mark class="lr-filler">like</mark> a random little spot, order whatever looks good, and I <mark class="lr-filler">kind of</mark> talk to the camera while I'm eating — <mark class="lr-filler">I mean</mark> I'm not trying to be super fancy, it's more <mark class="lr-filler">like</mark> hanging out with a friend, <mark class="lr-filler">I guess</mark>.</p>
          <p class="lr-vlog-text">The tricky part is when the food's really hot and I'm <mark class="lr-filler">like</mark> still filming — you have to keep talking even when your mouth is <mark class="lr-filler">kind of</mark> on fire — but that's <mark class="lr-filler">kind of</mark> the fun part too, <mark class="lr-filler">you know</mark>?</p>
          <p class="lr-vlog-text">And <mark class="lr-filler">yeah</mark> I get comments <mark class="lr-filler">like</mark> oh you should review more desserts or whatever, and I'm <mark class="lr-filler">like</mark> okay maybe next week, because I do want to mix it up — sometimes noodles, sometimes coffee, sometimes just <mark class="lr-filler">like</mark> a really good bánh mì on the corner.</p>
          <p class="lr-vlog-text"><mark class="lr-filler">I mean</mark> at the end of the day it's not really about getting everything perfect on camera — it's more about sharing what actually tastes good and <mark class="lr-filler">kind of</mark> showing people the places I'd go with my friends anyway.</p>
          <p class="ex-vi lr-vlog-vi">Ừ thì mình làm food vlog được khoảng hai năm rồi, thật sự cũng hơi “điên” — kiểu không ngờ có người xem mình ăn đồ ăn đường phố lúc nửa đêm, nhưng mà giờ thì cứ thế. Cơ bản là đi loanh quanh thành phố, tìm quán nhỏ bất kỳ, gọi món trông ngon là quay và nói chuyện với camera — không cần sang, giống đi ăn với bạn thôi. Khó nhất là món còn nóng mà vẫn phải nói, miệng “cháy” mà vẫn quay — nhưng đó cũng là phần vui. Viewer bảo nên review thêm dessert, mình bảo tuần sau đi, vì muốn đổi gu: mì, cà phê, hay bánh mì góc phố. Cuối cùng không phải quay cho hoàn hảo, mà chia sẻ chỗ ngon và nơi mình sẽ rủ bạn bè đi.</p>
        </blockquote>
        <p class="lr-note-tip">Tip: Đọc to với tốc độ hơi nhanh, nuốt âm nhẹ ở <em>kind of</em> → <em>kinda</em>, <em>going to</em> → <em>gonna</em> nếu muốn giống native casual hơn.</p>
      </section>"""


def build_page() -> str:
    home = "../../../../"  # review-exercise/ → public/
    slots_json = json.dumps(WORD_SLOTS, ensure_ascii=False)

    body = f"""    <aside class="docs-sidebar" id="docsSidebar" data-nav="english" data-docs-root="../../" data-active="food-drink">
      <div class="docs-nav-label">English</div>
      <ul class="docs-nav" id="docsNav">
        <li><a href="../../">All topics</a></li>
        <li><a href="../">Food &amp; Drink</a></li>
        <li><a class="active" href="./">Review Exercise 1</a></li>
        <li><a href="../review-exercise-2/">Review Exercise 2</a></li>
      </ul>
    </aside>
    <article class="docs-main lr-page">
      <div class="docs-breadcrumb">
        <a href="{home}">Home</a><span>›</span>
        <a href="{home}#blogs">Blogs</a><span>›</span>
        <a href="../../">English</a><span>›</span>
        <a href="../">Food &amp; Drink</a><span>›</span>
        <span>Review Exercise 1</span>
      </div>

      <header class="lr-hero">
        <p class="lr-hero-badge">Linear Thinking · Capstone</p>
        <h1>Food &amp; Drink — Review Exercise 1</h1>
        <p class="lede">Sau khi hoàn thành B2, ôn tập theo <a href="https://www.dolenglish.vn/blog/linearthinking-trong-speaking" target="_blank" rel="noopener noreferrer">Linear Thinking</a>: ngữ pháp (6 thì) → mental model → cấu trúc Speaking → từ vựng B1/B2 → mock IELTS Part 1/2/3 với dropdown từ thay thế. Chỉ muốn Lesson 2–6 (skip 4)? Xem <a href="../review-exercise-2/">Review Exercise 2</a>.</p>
        <nav class="lr-toc" aria-label="On this page">
          <a href="#core-steps">Core · 3 bước</a>
          <a href="#natural-vlog">0 · Real talk</a>
          <a href="#grammar">1 · Grammar</a>
          <a href="#mental-model">2 · Mental model</a>
          <a href="#ed-ending">2b · -ed</a>
          <a href="#structures">3 · Structures</a>
          <a href="#lessons">4 · Lessons 2 · 3 · 5 · 6</a>
          <a href="#food-lang">5 · Idioms &amp; phrases</a>
          <a href="#phrase-drills">6 · Phrase drills</a>
          <a href="#food-phrase-map">6 · Mind map</a>
          <a href="#phrase-assemble">6b · Ghép đoạn</a>
          <a href="#mock-test">7 · Mock test</a>
        </nav>
        <div class="ex-toolbar lr-toolbar lr-toolbar--hero">
          <label class="ex-toggle"><input type="checkbox" id="togVi" /> Vietnamese</label>
        </div>
      </header>

{core_steps_html()}

{natural_vlog_html()}

      <section class="lr-section" id="grammar">
        <h2>1 · Grammar foundations</h2>
        <p class="lr-section-hint">Click từng card để mở bài đọc trên IELTS Fighter. Mỗi thì gắn với ngữ cảnh Food &amp; Drink.</p>
        <div class="lr-grammar-list">
{grammar_section()}
        </div>
        <p class="lr-ref">Tham khảo thêm: <a href="https://www.dolenglish.vn/blog/linearthinking-trong-hoc-ngu-phap-grammar" target="_blank" rel="noopener noreferrer">Linear Thinking trong Grammar</a> · <a href="https://www.dolenglish.vn/blog/ielts-speaking-food" target="_blank" rel="noopener noreferrer">DOL — IELTS Speaking Food</a></p>
      </section>

      <section class="lr-section" id="mental-model">
        <h2>2 · Mental model — Tenses for Food speaking</h2>
        <p class="lr-section-hint">Ba lớp: <strong>sơ đồ ngữ pháp</strong> (công thức + dấu hiệu, badge <strong>1–12</strong>) · <strong>cách đọc -ed</strong> (Past Simple / V₃) · <strong>timeline use case</strong> + <strong>hội thoại Food</strong>. <span class="lr-mmap-star">★</span> = Section 3.</p>
{mental_model_html()}
      </section>

      <section class="lr-section" id="structures">
        <h2>3 · Speaking structures (food + tenses)</h2>
        <p class="lr-section-hint">Xem video gốc trước, sau đó mở <strong>Video catch-up</strong>. Sau mỗi slide grammar có <strong>Food practice</strong> — hội thoại + ví dụ cùng cấu trúc, chủ đề ẩm thực.</p>
        <ul class="lr-lesson-list">
{speaking_lessons_html()}
        </ul>
      </section>

      <section class="lr-section" id="lessons">
        <h2>4 · Core formulas — Lesson 2, 3, 5 &amp; 6</h2>
        <p class="lr-section-hint">Công thức <strong>IELTS Nguyễn Huyền</strong> — L2 Reasons → L3 Do you like X? → L5 What kind? → L6 Prefer X or Y · <em>skip Lesson 4</em>. Chọn <strong>1–2 nhánh</strong>.</p>
{lesson_highlights_html()}
      </section>

      <section class="lr-section" id="food-lang">
        <h2>5 · Food lang · idioms &amp; phrases</h2>
        <p class="lr-section-hint">IELTS đánh giá <strong>Lexical Resource</strong> — không chỉ từ đúng nghĩa mà còn idiom, phrase, collocation tự nhiên. Phần <strong>Phrases</strong> có ví dụ gắn khung Lesson 3–5 — học thuộc cả cụm. Chọn 1–2 cái phù hợp ngữ cảnh (không nhồi).</p>
        <div class="lr-idiom-grid">
{food_lang_html()}
        </div>
      </section>

      <section class="lr-section" id="phrase-drills">
        <h2>6 · Phrase drills · khung câu + từ “Phải học”</h2>
        <p class="lr-section-hint"><strong>Bước 1:</strong> xem <a href="#food-phrase-map">sơ đồ tư duy Food</a> → thuộc từng câu đơn (khung + từ vàng). <strong>Bước 2:</strong> gắn vai <em>Mở / Thân / Kết</em> rồi ghép 3–4 câu thành đoạn — không học vẹt cả đoạn. Xem <a href="#phrase-assemble">6b · Ghép đoạn</a>.</p>
{food_phrase_mindmap_html()}
{gold_phrase_drills_html()}
{phrase_assemble_html()}
      </section>

      <section class="lr-section lr-mock" id="mock-test">
        <h2>7 · IELTS Speaking mock — Food</h2>
        <p class="lr-section-hint">Part 1 / 2 / 3 thực chiến. Dùng dropdown để đổi từ (vd. <em>booze</em> → <em>cider</em> → <em>gin</em>) — không cần nhồi hết từ vào một câu.</p>
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
  <title>Review Exercise 1 · Food &amp; Drink — The Quiet Corner</title>
  <meta name="description" content="Linear Thinking review: grammar, mental models, and IELTS Speaking mock for Food &amp; Drink (B1/B2 focus).">
  <link rel="icon" href="{home}favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{home}css/docs.css?v=lr38">
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
  <script src="{home}js/docs.js?v=lr22"></script>
  <script src="{home}js/linear-review.js?v=lr25"></script>
</body>
</html>"""


def build_page_review2() -> str:
    """Focused page: Lesson 2 & 3 mind maps + Food examples + dropdown practice only."""
    home = "../../../../"  # review-exercise-2/ → public/
    slots_json = json.dumps(WORD_SLOTS, ensure_ascii=False)

    body = f"""    <aside class="docs-sidebar" id="docsSidebar" data-nav="english" data-docs-root="../../" data-active="food-drink">
      <div class="docs-nav-label">English</div>
      <ul class="docs-nav" id="docsNav">
        <li><a href="../../">All topics</a></li>
        <li><a href="../">Food &amp; Drink</a></li>
        <li><a href="../review-exercise/">Review Exercise 1</a></li>
        <li><a class="active" href="./">Review Exercise 2</a></li>
      </ul>
    </aside>
    <article class="docs-main lr-page">
      <div class="docs-breadcrumb">
        <a href="{home}">Home</a><span>›</span>
        <a href="{home}#blogs">Blogs</a><span>›</span>
        <a href="../../">English</a><span>›</span>
        <a href="../">Food &amp; Drink</a><span>›</span>
        <span>Review Exercise 2</span>
      </div>

      <header class="lr-hero">
        <p class="lr-hero-badge">Linear Thinking · Lesson 2, 3, 5 &amp; 6</p>
        <h1>Food &amp; Drink — Review Exercise 2</h1>
        <p class="lede">Lesson 2 + 3 + 5 + 6 (Prefer X or Y) · skip Lesson 4. Sơ đồ tư duy → ví dụ Food → Scroll read. Full capstone: <a href="../review-exercise/">Review Exercise 1</a>.</p>
        <nav class="lr-toc" aria-label="On this page">
          <a href="#lesson2-formulas">Lesson 2 · Reasons</a>
          <a href="#scroll-lesson2">Scroll · L2</a>
          <a href="#lesson3-formulas">Lesson 3 · Do you like X?</a>
          <a href="#food-examples">Ví dụ L3</a>
          <a href="#scroll-lesson3">Scroll · L3</a>
          <a href="#lesson5-formulas">Lesson 5 · What kind?</a>
          <a href="#food-examples-l5">Ví dụ L5</a>
          <a href="#scroll-lesson5">Scroll · L5</a>
          <a href="#lesson6-formulas">Lesson 6 · Prefer X or Y?</a>
          <a href="#food-examples-l6">Ví dụ L6</a>
          <a href="#scroll-lesson6">Scroll · L6</a>
        </nav>
        <div class="ex-toolbar lr-toolbar lr-toolbar--hero">
          <label class="ex-toggle"><input type="checkbox" id="togVi" /> Vietnamese</label>
        </div>
      </header>

      <section class="lr-section" id="lessons">
        <h2>Core formulas — Lesson 2, 3, 5 &amp; 6</h2>
        <p class="lr-section-hint">Công thức <strong>IELTS Nguyễn Huyền</strong> — chọn <strong>1–2 nhánh</strong>, không nhồi hết. Dropdown bên dưới để thay từ B1/B2.</p>
{lesson_highlights_html(map_suffix="R2", include_food_examples=True, open_practice=True)}
      </section>

      <script type="application/json" id="lrWordSlots">{slots_json}</script>
    </article>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Review Exercise 2 · Food &amp; Drink — The Quiet Corner</title>
  <meta name="description" content="Lesson 2, 3, 5 &amp; 6: Reasons, Do you like X?, What kind?, Prefer X or Y — Food mind maps and practice.">
  <link rel="icon" href="{home}favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{home}css/docs.css?v=lr38">
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
  <script src="{home}js/docs.js?v=lr22"></script>
  <script src="{home}js/linear-review.js?v=lr25"></script>
</body>
</html>"""


def patch_topic_index() -> None:
    path = ROOT / "public" / "blog" / "english" / "food-drink" / "index.html"
    text = path.read_text(encoding="utf-8")
    review_icon = (
        "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 72 72' fill='none'%3E"
        "%3Crect width='72' height='72' rx='14' fill='%231a1033'/%3E"
        "%3Ccircle cx='36' cy='36' r='22' stroke='%23a78bfa' stroke-width='2.5'/%3E"
        "%3Cpath d='M36 20v16l10 8' stroke='%2322d3ee' stroke-width='2.5' stroke-linecap='round'/%3E"
        "%3Cpath d='M22 48h28' stroke='%23e4e4e7' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E"
    )
    review2_icon = (
        "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 72 72' fill='none'%3E"
        "%3Crect width='72' height='72' rx='14' fill='%23101828'/%3E"
        "%3Ccircle cx='36' cy='36' r='18' stroke='%2334d399' stroke-width='2.5'/%3E"
        "%3Cpath d='M24 36h24M36 24v24' stroke='%2367e8f9' stroke-width='2.5' stroke-linecap='round'/%3E"
        "%3C/svg%3E"
    )
    review_section = f"""
      <section class="vocab-level vocab-level--review" id="review">
        <div class="vocab-level__head">
          <span class="vocab-level__badge vocab-level__badge--review">Review</span>
          <h2>Linear Thinking · Capstone exercise</h2>
        </div>
        <p class="vocab-level__desc"><strong>Review 1</strong> — full capstone: ngữ pháp (6 thì), mental model, cấu trúc Speaking, mock IELTS Part 1/2/3. <strong>Review 2</strong> — Lesson 2, 3, 5 &amp; 6 (mind map + ví dụ Food + dropdown; skip Lesson 4). Trước khi học: Pareto 80/20 → neo ngữ cảnh → khung câu an toàn.</p>
        <div class="vocab-lesson-grid">
          <a class="vocab-lesson-card vocab-lesson-card--review" href="review-exercise/">
            <img src="{review_icon}" alt="" width="72" height="72" loading="lazy">
            <span>Review Exercise 1</span>
          </a>
          <a class="vocab-lesson-card vocab-lesson-card--review" href="review-exercise-2/">
            <img src="{review2_icon}" alt="" width="72" height="72" loading="lazy">
            <span>Review Exercise 2</span>
          </a>
        </div>
{core_steps_teaser_html()}
      </section>
"""
    import re

    if 'id="review"' in text:
        text, n = re.subn(
            r'\s*<section class="vocab-level vocab-level--review" id="review">.*?</section>',
            "\n" + review_section.rstrip() + "\n",
            text,
            count=1,
            flags=re.S,
        )
        if n:
            path.write_text(text, encoding="utf-8")
        return
    marker = '      <section class="vocab-level" id="b2">'
    if marker not in text:
        text = text.replace("    </article>", review_section + "\n    </article>")
    else:
        b2_end = text.find("</section>", text.find('id="b2"'))
        if b2_end > 0:
            insert_at = b2_end + len("</section>")
            text = text[:insert_at] + "\n" + review_section + text[insert_at:]
    path.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    OUT2.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(build_page(), encoding="utf-8")
    (OUT2 / "index.html").write_text(build_page_review2(), encoding="utf-8")
    patch_topic_index()
    print("Wrote", OUT / "index.html")
    print("Wrote", OUT2 / "index.html")
    print("Patched food-drink/index.html with Review section")


if __name__ == "__main__":
    main()
